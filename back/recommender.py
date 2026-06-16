"""Score-based cover song recommendation engine."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

GENDER_MAP = {
    "남자": "male",
    "여자": "female",
    "혼성": "mixed",
    "상관없음": "any",
}

RANGE_MAP = {
    "낮은 음역": "low",
    "중저음": "mid_low",
    "중고음": "mid_high",
    "높은 음역": "high",
}

SESSION_COUNT_MAP = {
    "1명": 1,
    "2명": 2,
    "3명": 3,
    "4명": 4,
    "5명 이상": 5,
    "풀세션": 8,
}

INSTRUMENT_MAP = {
    "기타": "guitar",
    "베이스": "bass",
    "드럼": "drum",
    "카혼": "cajon",
    "키보드": "keyboard",
    "신디": "synth",
    "스트링": "string",
    "코러스": "chorus",
}

DIFFICULTY_KO = {"easy": "쉬움", "normal": "보통", "hard": "어려움"}
RANGE_KO = {"low": "낮은 음역", "mid_low": "중저음", "mid_high": "중고음", "high": "높은 음역"}
GENDER_KO = {"male": "남성 보컬", "female": "여성 보컬", "mixed": "혼성 보컬", "any": "성별 무관"}

IMMEDIATE_ADJACENT: dict[str, list[str]] = {
    "low": ["mid_low"],
    "mid_low": ["low", "mid_high"],
    "mid_high": ["mid_low", "high"],
    "high": ["mid_high"],
}


@dataclass
class ScoredSong:
    song: dict[str, Any]
    score: float
    reasons: list[str]
    simplified_possible: bool
    missing_instruments: list[str]
    exact_range_match: bool


def _user_session_count(session_label: str) -> int:
    return SESSION_COUNT_MAP[session_label]


def _count_available_instruments(available: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {"vocal": 1}
    for item in available:
        key = INSTRUMENT_MAP[item]
        counts[key] = counts.get(key, 0) + 1
    return counts


def _can_cover_sessions(required: list[str], available_counts: dict[str, int]) -> tuple[bool, list[str]]:
    needed: dict[str, int] = {}
    for session in required:
        needed[session] = needed.get(session, 0) + 1

    missing: list[str] = []
    for session, count in needed.items():
        have = available_counts.get(session, 0)
        if have < count:
            missing.extend([session] * (count - have))

    return len(missing) == 0, missing


def _score_gender(user_gender: str, song_gender: str) -> tuple[float, str | None]:
    mapped = GENDER_MAP[user_gender]
    if mapped == "any" or song_gender == "any":
        return 8.0, None
    if mapped == song_gender:
        return 20.0, f"보컬 성별({user_gender}) 일치"
    if song_gender == "mixed":
        return 12.0, "혼성 보컬 곡으로 편곡 유연"
    return 0.0, None


def _score_range(user_range: str, song_range: str) -> tuple[float, str | None, bool]:
    mapped = RANGE_MAP[user_range]
    if mapped == song_range:
        return 50.0, f"음역대({user_range}) 정확히 일치", True
    if song_range in IMMEDIATE_ADJACENT.get(mapped, []):
        return 2.0, f"음역대 인접 후보", False
    return -50.0, None, False


def _score_mood(user_mood: str, song_moods: list[str]) -> tuple[float, str | None]:
    if user_mood in song_moods:
        return 18.0, f"분위기 '{user_mood}' 일치"
    return 0.0, None


def _score_session(user_count: int, song: dict[str, Any]) -> tuple[float, bool, str | None]:
    required = song["session_count"]
    simplified = song.get("simplified_arrangement", False)

    if user_count >= required:
        bonus = min(15.0, (user_count - required + 1) * 3)
        return 15.0 + bonus, False, f"세션 {user_count}명으로 구성 가능"

    if simplified and user_count >= max(2, required - 2):
        return 8.0, True, f"세션 {user_count}명 → 간소화 편곡 가능"
    if simplified:
        return 4.0, True, f"세션 부족 → 간소화 편곡 검토 필요"
    return -5.0, False, None


def _score_instruments(required: list[str], available_counts: dict[str, int]) -> tuple[float, list[str], str | None]:
    if not required:
        return 0.0, [], None

    ok, missing = _can_cover_sessions(required, available_counts)
    unique_required = set(required) - {"vocal"}
    matched = sum(1 for inst in unique_required if available_counts.get(inst, 0) > 0)
    total = len(unique_required) or 1
    ratio = matched / total
    points = ratio * 20.0

    if ok:
        return points + 5.0, missing, f"보유 악기로 세션 {int(ratio * 100)}% 커버"
    return points - len(missing) * 2, missing, None


def score_song(
    song: dict[str, Any],
    *,
    vocal_gender: str,
    vocal_range: str,
    session_count_label: str,
    available_instruments: list[str],
    mood: str,
) -> ScoredSong:
    reasons: list[str] = []
    score = 0.0

    g_pts, g_reason = _score_gender(vocal_gender, song["vocal_gender"])
    score += g_pts
    if g_reason:
        reasons.append(g_reason)

    r_pts, r_reason, exact_range = _score_range(vocal_range, song["vocal_range"])
    score += r_pts
    if r_reason:
        reasons.append(r_reason)

    m_pts, m_reason = _score_mood(mood, song["mood"])
    score += m_pts
    if m_reason:
        reasons.append(m_reason)

    user_count = _user_session_count(session_count_label)
    s_pts, simplified, s_reason = _score_session(user_count, song)
    score += s_pts
    if s_reason:
        reasons.append(s_reason)

    available_counts = _count_available_instruments(available_instruments)
    i_pts, missing, i_reason = _score_instruments(song["required_sessions"], available_counts)
    score += i_pts
    if i_reason:
        reasons.append(i_reason)

    simplified_possible = simplified or (bool(missing) and song.get("simplified_arrangement", False))

    # Difficulty soft bonus for smaller sessions
    if user_count <= 3 and song["difficulty"] == "easy":
        score += 5.0
        reasons.append("소규모 세션에 적합한 난이도")

    return ScoredSong(
        song=song,
        score=round(max(score, 0.0), 1),
        reasons=reasons,
        simplified_possible=simplified_possible,
        missing_instruments=missing,
        exact_range_match=exact_range,
    )


def build_mixing_direction(song: dict[str, Any]) -> dict[str, str]:
    tip = song.get("mixing_tip", {})
    return {
        "vocal_eq": tip.get("vocal", "보컬 2~5kHz presence 조정"),
        "instrument_balance": tip.get("instrument", "악기 mid-range 정리"),
        "reverb_delay": tip.get("space", "곡 분위기에 맞는 reverb/delay"),
        "compressor_limiter": tip.get("compressor_limiter", "보컬 comp 3:1, light bus comp"),
        "mastering_tip": tip.get("master", "자연스러운 다이내믹 유지, ceiling -1.0 dBTP"),
    }


def build_recommendation_item(scored: ScoredSong) -> dict[str, Any]:
    song = scored.song
    reason = " · ".join(scored.reasons[:4]) if scored.reasons else "조건에 부합하는 곡"
    if scored.simplified_possible:
        reason += " · 간소화 편곡 가능"

    return {
        "title": song["title"],
        "artist": song["artist"],
        "score": scored.score,
        "reason": reason,
        "difficulty": DIFFICULTY_KO.get(song["difficulty"], song["difficulty"]),
        "vocal_range": RANGE_KO.get(song["vocal_range"], song["vocal_range"]),
        "session_description": song["session_description"],
        "required_sessions": song["required_sessions"],
        "simplified_arrangement_possible": scored.simplified_possible,
        "arrangement_tip": song["arrangement_tip"],
        "mixing_direction": build_mixing_direction(song),
    }


def _select_top_songs(scored_list: list[ScoredSong], vocal_range: str, top_n: int) -> list[ScoredSong]:
    """음역대 정확 일치 곡을 우선 추천하고, 부족할 때만 인접 음역으로 보충."""
    mapped = RANGE_MAP[vocal_range]
    adjacent_ranges = set(IMMEDIATE_ADJACENT.get(mapped, []))

    exact = sorted(
        [s for s in scored_list if s.exact_range_match],
        key=lambda x: x.score,
        reverse=True,
    )
    if len(exact) >= top_n:
        return exact[:top_n]

    adjacent = sorted(
        [
            s for s in scored_list
            if not s.exact_range_match and s.song["vocal_range"] in adjacent_ranges
        ],
        key=lambda x: x.score,
        reverse=True,
    )
    combined = exact + [s for s in adjacent if s.song["title"] not in {e.song["title"] for e in exact}]
    return combined[:top_n]


def recommend_songs(
    songs: list[dict[str, Any]],
    *,
    vocal_gender: str,
    vocal_range: str,
    session_count: str,
    available_instruments: list[str],
    mood: str,
    top_n: int = 5,
) -> list[dict[str, Any]]:
    scored_list = [
        score_song(
            song,
            vocal_gender=vocal_gender,
            vocal_range=vocal_range,
            session_count_label=session_count,
            available_instruments=available_instruments,
            mood=mood,
        )
        for song in songs
    ]
    selected = _select_top_songs(scored_list, vocal_range, top_n)
    return [build_recommendation_item(s) for s in selected]
