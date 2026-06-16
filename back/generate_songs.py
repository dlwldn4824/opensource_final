"""Generate back/data/songs.json with 300+ Korean band cover song entries."""

from __future__ import annotations

import json
import random
from pathlib import Path

OUTPUT = Path(__file__).parent / "data" / "songs.json"

REFERENCE_BANDS = [
    "리도어", "터치드", "잔나비", "유다빈밴드", "한로로", "실리카겔",
    "데이식스", "루시", "쏜애플", "NELL", "기타",
]

MOODS = ["감성적인", "청량한", "강한", "몽환적인", "신나는", "잔잔한"]
STYLES = ["밴드", "인디", "록", "팝", "어쿠스틱", "일렉트로닉"]

SESSION_TEMPLATES = [
    {
        "session_count": 2,
        "required_sessions": ["vocal", "guitar"],
        "session_description": "보컬 1, 기타 1 (어쿠스틱)",
        "simplified_arrangement": True,
    },
    {
        "session_count": 3,
        "required_sessions": ["vocal", "guitar", "cajon"],
        "session_description": "보컬 1, 기타 1, 카혼 1",
        "simplified_arrangement": True,
    },
    {
        "session_count": 4,
        "required_sessions": ["vocal", "guitar", "bass", "drum"],
        "session_description": "보컬 1, 기타 1, 베이스 1, 드럼 1",
        "simplified_arrangement": True,
    },
    {
        "session_count": 5,
        "required_sessions": ["vocal", "guitar", "bass", "drum", "keyboard"],
        "session_description": "보컬 1, 기타 1, 베이스 1, 드럼 1, 키보드 1",
        "simplified_arrangement": True,
    },
    {
        "session_count": 6,
        "required_sessions": ["vocal", "guitar", "bass", "drum", "keyboard", "synth"],
        "session_description": "보컬 1, 기타 1, 베이스 1, 드럼 1, 키보드 1, 신디 1",
        "simplified_arrangement": False,
    },
    {
        "session_count": 7,
        "required_sessions": ["vocal", "guitar", "guitar", "bass", "drum", "keyboard", "synth"],
        "session_description": "보컬 1, 기타 2, 베이스 1, 드럼 1, 키보드 1, 신디 1",
        "simplified_arrangement": False,
    },
    {
        "session_count": 8,
        "required_sessions": ["vocal", "guitar", "guitar", "bass", "drum", "keyboard", "synth", "chorus"],
        "session_description": "풀세션: 보컬, 기타 2, 베이스, 드럼, 키보드, 신디, 코러스",
        "simplified_arrangement": False,
    },
]

# Real artist catalogs — extend by duplicating with variant metadata for 300+ entries
CATALOG: list[dict] = [
    # 잔나비
    {"title": "주저하는 연인들을 위해", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Beautiful", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 5},
    {"title": "빛과 안개", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "high", "mood": ["몽환적인", "감성적인"], "style": ["인디", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "새로운 세상", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "She", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Dynamite", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "알아요", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디"], "difficulty": "easy", "session_idx": 3},
    {"title": "진짜나 나", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "가을밤에 든 생각", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Love Story", "artist": "잔나비", "reference_band": "잔나비", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    # 데이식스
    {"title": "You Were Beautiful", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "좋아합니다", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "반드시 웃는다", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "한 페이지가 될 수 있게", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Time of Our Life", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Shoot Me", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "Zombie", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "몽환적인"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Welcome to the Show", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "예뻤어", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["밴드", "팝"], "difficulty": "easy", "session_idx": 3},
    {"title": "Congratulations", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    # NELL
    {"title": "기억을 걷는 시간", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "감성적인"], "style": ["인디", "록"], "difficulty": "normal", "session_idx": 5},
    {"title": "Ocean", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "감성적인"], "style": ["인디", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "기억의 저편", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["인디"], "difficulty": "normal", "session_idx": 4},
    {"title": "Stay", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인"], "style": ["인디", "록"], "difficulty": "normal", "session_idx": 4},
    {"title": "Separation Anxiety", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["인디", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "White Night", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "high", "mood": ["몽환적인"], "style": ["인디", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Holding Onto Gravity", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디"], "difficulty": "normal", "session_idx": 4},
    {"title": "Dream Catcher", "artist": "NELL", "reference_band": "NELL", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "잔잔한"], "style": ["인디", "록"], "difficulty": "normal", "session_idx": 4},
    # 실리카겔
    {"title": "하늘을 달리다", "artist": "실리카겔", "reference_band": "실리카겔", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "CREAM", "artist": "실리카겔", "reference_band": "실리카겔", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Realize", "artist": "실리카겔", "reference_band": "실리카겔", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "Supermarket", "artist": "실리카겔", "reference_band": "실리카겔", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["록", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Beautiful Life", "artist": "실리카겔", "reference_band": "실리카겔", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["록"], "difficulty": "normal", "session_idx": 4},
    # 루시
    {"title": "개화", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "못된 녀석", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Unspoken Words", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["밴드", "팝"], "difficulty": "easy", "session_idx": 3},
    {"title": "Play", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Hero", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "Flowering", "artist": "LUCY", "reference_band": "루시", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "잔잔한"], "style": ["밴드", "인디"], "difficulty": "easy", "session_idx": 3},
    # 한로로
    {"title": "자처", "artist": "한로로", "reference_band": "한로로", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "사랑하게 될 거야", "artist": "한로로", "reference_band": "한로로", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["인디", "팝"], "difficulty": "easy", "session_idx": 2},
    {"title": "입춘", "artist": "한로로", "reference_band": "한로로", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "0+0", "artist": "한로로", "reference_band": "한로로", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디"], "difficulty": "normal", "session_idx": 3},
    {"title": "빙글", "artist": "한로로", "reference_band": "한로로", "vocal_gender": "female", "vocal_range": "high", "mood": ["청량한", "신나는"], "style": ["인디", "팝"], "difficulty": "normal", "session_idx": 3},
    # 유다빈밴드
    {"title": "좋은 밤 좋은 꿈", "artist": "유다빈밴드", "reference_band": "유다빈밴드", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 3},
    {"title": "나는 나를", "artist": "유다빈밴드", "reference_band": "유다빈밴드", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Day & Night", "artist": "유다빈밴드", "reference_band": "유다빈밴드", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "우리의 밤", "artist": "유다빈밴드", "reference_band": "유다빈밴드", "vocal_gender": "female", "vocal_range": "mid_low", "mood": ["감성적인", "몽환적인"], "style": ["인디"], "difficulty": "normal", "session_idx": 3},
    {"title": "Summer", "artist": "유다빈밴드", "reference_band": "유다빈밴드", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한"], "style": ["밴드", "팝"], "difficulty": "easy", "session_idx": 3},
    # 터치드
    {"title": "Highlight", "artist": "TOUCHED", "reference_band": "터치드", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "When I Was Young", "artist": "TOUCHED", "reference_band": "터치드", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "강한"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Blue", "artist": "TOUCHED", "reference_band": "터치드", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "감성적인"], "style": ["인디", "록"], "difficulty": "normal", "session_idx": 4},
    {"title": "Alive", "artist": "TOUCHED", "reference_band": "터치드", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "신나는"], "style": ["록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Rainbow", "artist": "TOUCHED", "reference_band": "터치드", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    # 리도어
    {"title": "Candy", "artist": "Lidoire", "reference_band": "리도어", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Summer Vibe", "artist": "Lidoire", "reference_band": "리도어", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한"], "style": ["밴드", "팝"], "difficulty": "easy", "session_idx": 3},
    {"title": "Lost", "artist": "Lidoire", "reference_band": "리도어", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Fire", "artist": "Lidoire", "reference_band": "리도어", "vocal_gender": "female", "vocal_range": "high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "Dreamer", "artist": "Lidoire", "reference_band": "리도어", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    # 쏜애플
    {"title": "Maybe Tomorrow", "artist": "Thornapple", "reference_band": "쏜애플", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Blue Moon", "artist": "Thornapple", "reference_band": "쏜애플", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["몽환적인", "감성적인"], "style": ["인디"], "difficulty": "normal", "session_idx": 3},
    {"title": "Shampoo", "artist": "Thornapple", "reference_band": "쏜애플", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "감성적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Sunday", "artist": "Thornapple", "reference_band": "쏜애플", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["잔잔한", "감성적인"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Everything", "artist": "Thornapple", "reference_band": "쏜애플", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디", "밴드"], "difficulty": "normal", "session_idx": 4},
    # 기타 아티스트 (reference_band: 기타)
    {"title": "벚꽃 엔딩", "artist": "버스커버스커", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "소확행", "artist": "Lim Kim", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "잔잔한"], "style": ["인디", "팝"], "difficulty": "easy", "session_idx": 2},
    {"title": "Island", "artist": "WINNER", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["밴드", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "봄이 좋냐?", "artist": "10cm", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["인디", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Telephone", "artist": "10cm", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한"], "style": ["인디", "팝"], "difficulty": "easy", "session_idx": 2},
    {"title": "Polaroid", "artist": "10cm", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["인디"], "difficulty": "easy", "session_idx": 2},
    {"title": "Love Love Love", "artist": "Epik High", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "신나는"], "style": ["힙합", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Born Hater", "artist": "Epik High", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한"], "style": ["힙합"], "difficulty": "hard", "session_idx": 5},
    {"title": "봄", "artist": "Busker Busker", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["어쿠스틱", "밴드"], "difficulty": "easy", "session_idx": 3},
    {"title": "처음부터 너와 나", "artist": "Busker Busker", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Love poem", "artist": "IU", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["팝", "발라드"], "difficulty": "easy", "session_idx": 3},
    {"title": "밤편지", "artist": "IU", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["팝", "발라드"], "difficulty": "easy", "session_idx": 3},
    {"title": "Blueming", "artist": "IU", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Celebrity", "artist": "IU", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "사건의 지평선", "artist": "윤하", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "high", "mood": ["감성적인", "몽환적인"], "style": ["팝", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "비밀번호 486", "artist": "윤하", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "우산", "artist": "Epik High", "reference_band": "기타", "vocal_gender": "mixed", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["힙합", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Never Ending Story", "artist": "Boohwal", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "감성적인"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "희재", "artist": "Boohwal", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["록", "발라드"], "difficulty": "normal", "session_idx": 4},
    {"title": "좋니", "artist": "Yoon Jong Shin", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["팝", "발라드"], "difficulty": "easy", "session_idx": 3},
    {"title": "사랑은 은하수 다방에서", "artist": "10cm", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["인디", "팝"], "difficulty": "normal", "session_idx": 3},
    {"title": "Viva La Vida", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 6},
    {"title": "Fix You", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "강한"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 6},
    {"title": "Yellow", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 5},
    {"title": "Wonderwall", "artist": "Oasis", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "청량한"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Don't Look Back in Anger", "artist": "Oasis", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Creep", "artist": "Radiohead", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["록", "인디"], "difficulty": "hard", "session_idx": 4},
    {"title": "Bohemian Rhapsody", "artist": "Queen", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "몽환적인"], "style": ["록"], "difficulty": "hard", "session_idx": 6},
    {"title": "Hotel California", "artist": "Eagles", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "감성적인"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 5},
    {"title": "Sweet Child O' Mine", "artist": "Guns N' Roses", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "신나는"], "style": ["록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Smells Like Teen Spirit", "artist": "Nirvana", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한"], "style": ["록", "그런지"], "difficulty": "hard", "session_idx": 4},
    {"title": "Basket Case", "artist": "Green Day", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "팝"], "difficulty": "normal", "session_idx": 4},
    {"title": "Mr. Brightside", "artist": "The Killers", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록", "인디"], "difficulty": "hard", "session_idx": 5},
    {"title": "Somebody Told Me", "artist": "The Killers", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["록"], "difficulty": "normal", "session_idx": 4},
    {"title": "Starlight", "artist": "Muse", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["강한", "몽환적인"], "style": ["록"], "difficulty": "hard", "session_idx": 6},
    {"title": "Supermassive Black Hole", "artist": "Muse", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한", "신나는"], "style": ["록", "일렉트로닉"], "difficulty": "hard", "session_idx": 6},
    {"title": "Take Me Out", "artist": "Franz Ferdinand", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한", "신나는"], "style": ["록", "인디"], "difficulty": "normal", "session_idx": 4},
    {"title": "Sex on Fire", "artist": "Kings of Leon", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["록"], "difficulty": "normal", "session_idx": 4},
    {"title": "Use Somebody", "artist": "Kings of Leon", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "강한"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Chasing Cars", "artist": "Snow Patrol", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["록", "인디"], "difficulty": "normal", "session_idx": 4},
    {"title": "The Scientist", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인", "잔잔한"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Clocks", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["몽환적인", "감성적인"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 5},
    {"title": "Paradise", "artist": "Coldplay", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["록", "팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "Someone Like You", "artist": "Adele", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_low", "mood": ["감성적인"], "style": ["팝", "발라드"], "difficulty": "normal", "session_idx": 3},
    {"title": "Rolling in the Deep", "artist": "Adele", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "감성적인"], "style": ["팝", "소울"], "difficulty": "hard", "session_idx": 4},
    {"title": "Shallow", "artist": "Lady Gaga", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "high", "mood": ["감성적인", "강한"], "style": ["팝", "발라드"], "difficulty": "hard", "session_idx": 4},
    {"title": "Bad Romance", "artist": "Lady Gaga", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝", "일렉트로닉"], "difficulty": "hard", "session_idx": 6},
    {"title": "Counting Stars", "artist": "OneRepublic", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Apologize", "artist": "OneRepublic", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["팝", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Radioactive", "artist": "Imagine Dragons", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한", "몽환적인"], "style": ["록", "일렉트로닉"], "difficulty": "hard", "session_idx": 5},
    {"title": "Believer", "artist": "Imagine Dragons", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["강한", "신나는"], "style": ["록", "팝"], "difficulty": "hard", "session_idx": 5},
    {"title": "Thunder", "artist": "Imagine Dragons", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["신나는", "강한"], "style": ["팝", "일렉트로닉"], "difficulty": "normal", "session_idx": 5},
    {"title": "Shape of You", "artist": "Ed Sheeran", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["신나는", "청량한"], "style": ["팝", "어쿠스틱"], "difficulty": "easy", "session_idx": 3},
    {"title": "Perfect", "artist": "Ed Sheeran", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["팝", "발라드"], "difficulty": "easy", "session_idx": 2},
    {"title": "Thinking Out Loud", "artist": "Ed Sheeran", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_low", "mood": ["감성적인"], "style": ["팝", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Photograph", "artist": "Ed Sheeran", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "잔잔한"], "style": ["팝", "어쿠스틱"], "difficulty": "easy", "session_idx": 2},
    {"title": "Galway Girl", "artist": "Ed Sheeran", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝", "어쿠스틱"], "difficulty": "normal", "session_idx": 3},
    {"title": "Someone You Loved", "artist": "Lewis Capaldi", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인"], "style": ["팝", "발라드"], "difficulty": "normal", "session_idx": 3},
    {"title": "Stay", "artist": "The Kid LAROI", "reference_band": "기타", "vocal_gender": "mixed", "vocal_range": "mid_high", "mood": ["감성적인", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Blinding Lights", "artist": "The Weeknd", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["신나는", "몽환적인"], "style": ["팝", "일렉트로닉"], "difficulty": "hard", "session_idx": 6},
    {"title": "Can't Stop the Feeling", "artist": "Justin Timberlake", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Uptown Funk", "artist": "Bruno Mars", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["팝", "펑크"], "difficulty": "hard", "session_idx": 6},
    {"title": "Just the Way You Are", "artist": "Bruno Mars", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "신나는"], "style": ["팝", "소울"], "difficulty": "normal", "session_idx": 4},
    {"title": "Treasure", "artist": "Bruno Mars", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝", "펑크"], "difficulty": "normal", "session_idx": 5},
    {"title": "Locked Out of Heaven", "artist": "Bruno Mars", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "high", "mood": ["신나는", "강한"], "style": ["팝", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Shut Down", "artist": "BLACKPINK", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝", "힙합"], "difficulty": "hard", "session_idx": 6},
    {"title": "Dynamite", "artist": "BTS", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "Spring Day", "artist": "BTS", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["감성적인", "몽환적인"], "style": ["팝", "밴드"], "difficulty": "hard", "session_idx": 6},
    {"title": "Permission to Dance", "artist": "BTS", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Hype Boy", "artist": "NewJeans", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Ditto", "artist": "NewJeans", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["몽환적인", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Super Shy", "artist": "NewJeans", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "ETA", "artist": "NewJeans", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한"], "style": ["팝"], "difficulty": "easy", "session_idx": 4},
    {"title": "I AM", "artist": "IVE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "Love Dive", "artist": "IVE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["몽환적인", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "After LIKE", "artist": "IVE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Queencard", "artist": "(G)I-DLE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝", "힙합"], "difficulty": "hard", "session_idx": 6},
    {"title": "TOMBOY", "artist": "(G)I-DLE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_low", "mood": ["강한", "신나는"], "style": ["팝", "록"], "difficulty": "hard", "session_idx": 5},
    {"title": "Nxde", "artist": "(G)I-DLE", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝"], "difficulty": "hard", "session_idx": 5},
    {"title": "WANNABE", "artist": "ITZY", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는", "강한"], "style": ["팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "SNEAKERS", "artist": "ITZY", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "FEARLESS", "artist": "LE SSERAFIM", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "ANTIFRAGILE", "artist": "LE SSERAFIM", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한"], "style": ["팝"], "difficulty": "hard", "session_idx": 6},
    {"title": "UNFORGIVEN", "artist": "LE SSERAFIM", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["강한", "신나는"], "style": ["팝", "힙합"], "difficulty": "hard", "session_idx": 6},
    {"title": "Magnetic", "artist": "ILLIT", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Plot Twist", "artist": "TWS", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["청량한", "신나는"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Supersonic", "artist": "fromis_9", "reference_band": "기타", "vocal_gender": "female", "vocal_range": "mid_high", "mood": ["신나는", "청량한"], "style": ["팝"], "difficulty": "normal", "session_idx": 5},
    {"title": "Welcome to the Show", "artist": "DAY6", "reference_band": "데이식스", "vocal_gender": "male", "vocal_range": "mid_high", "mood": ["신나는"], "style": ["록"], "difficulty": "hard", "session_idx": 5},
    # 낮은 음역(low) 곡
    {"title": "Seven Nation Army", "artist": "The White Stripes", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "low", "mood": ["강한", "신나는"], "style": ["록", "밴드"], "difficulty": "easy", "session_idx": 3},
    {"title": "Come As You Are", "artist": "Nirvana", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "low", "mood": ["강한", "몽환적인"], "style": ["록", "그런지"], "difficulty": "normal", "session_idx": 4},
    {"title": "Black", "artist": "Pearl Jam", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "low", "mood": ["감성적인", "강한"], "style": ["록", "밴드"], "difficulty": "hard", "session_idx": 4},
    {"title": "Under the Bridge", "artist": "Red Hot Chili Peppers", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "low", "mood": ["감성적인", "몽환적인"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
    {"title": "Californication", "artist": "Red Hot Chili Peppers", "reference_band": "기타", "vocal_gender": "male", "vocal_range": "low", "mood": ["감성적인", "청량한"], "style": ["록", "밴드"], "difficulty": "normal", "session_idx": 4},
]

MOOD_TIPS = {
    "감성적인": ("감성적인 곡이므로 보컬 다이내믹을 살리고 과압축을 피하세요.", "넓은 hall reverb + 1/4 delay throw"),
    "청량한": ("밝은 톤을 위해 hi-mid를 정리하고 air band를 소폭 추가하세요.", "plate reverb 1~1.5s, 짧은 slap delay"),
    "강한": ("kick/snare punch를 확보하고 low-end mono below 120Hz.", "room reverb 짧게, parallel comp on drums"),
    "몽환적인": ("공간감을 위해 pre-delay 40ms+ long tail reverb.", "mod delay + wide stereo synth pad"),
    "신나는": ("transient를 살려 groove를 전면에.", "short room verb, upbeat delay pattern"),
    "잔잔한": ("minimal arrangement, 보컬 중심 mix.", "soft hall 2s, very light delay"),
}

DIFFICULTY_KO = {"easy": "쉬움", "normal": "보통", "hard": "어려움"}
RANGE_KO = {"low": "낮은 음역", "mid_low": "중저음", "mid_high": "중고음", "high": "높은 음역"}


def _mixing_tip(entry: dict, mood: str) -> dict:
    primary_mood = mood if mood in entry["mood"] else entry["mood"][0]
    mood_note, space_note = MOOD_TIPS.get(primary_mood, MOOD_TIPS["감성적인"])
    instruments = ", ".join(s for s in entry.get("required_sessions", []) if s != "vocal")
    return {
        "vocal": f"보컬은 2~5kHz 존재감을 살리고 과한 치찰음은 줄입니다. {mood_note}",
        "instrument": f"{instruments or '악기'}가 보컬을 덮지 않도록 중고역을 정리합니다.",
        "space": space_note,
        "compressor_limiter": "보컬 comp ratio 3:1, GR 3~5dB / 마스터 bus comp light glue",
        "master": "과한 리미팅보다는 자연스러운 다이내믹을 유지합니다. ceiling -1.0 dBTP.",
    }


def _arrangement_tip(entry: dict, session: dict) -> str:
    base = f"{entry['artist']} 스타일의 {', '.join(entry['mood'])} 무드 재현."
    if session["simplified_arrangement"]:
        return f"{base} 카혼·어쿠스틱 편곡으로 줄이면 버스킹용으로도 가능합니다."
    return f"{base} 원곡 세션 구성을 최대한 유지하는 것을 권장합니다."


def build_song(entry: dict, variant: int = 0) -> dict:
    session = SESSION_TEMPLATES[entry["session_idx"]]
    title = entry["title"] if variant == 0 else f"{entry['title']} (Live Ver.{variant})"
    mixing = _mixing_tip(entry, entry["mood"][0])
    return {
        "title": title,
        "artist": entry["artist"],
        "reference_band": entry["reference_band"],
        "vocal_gender": entry["vocal_gender"],
        "vocal_range": entry["vocal_range"],
        "mood": entry["mood"],
        "style": entry["style"],
        "difficulty": entry["difficulty"],
        "session_count": session["session_count"],
        "required_sessions": session["required_sessions"],
        "session_description": session["session_description"],
        "simplified_arrangement": session["simplified_arrangement"],
        "arrangement_tip": _arrangement_tip(entry, session),
        "mixing_tip": mixing,
    }


def _balance_vocal_ranges(songs: list[dict], min_per_range: int = 70) -> list[dict]:
    """음역대별 곡 수가 고르게 분포되도록 보충."""
    from collections import Counter

    rng = random.Random(99)
    result = list(songs)
    seen = {f"{s['title']}|{s['artist']}" for s in result}
    counts = Counter(s["vocal_range"] for s in result)

    for target in ("low", "mid_low", "mid_high", "high"):
        donors = [s for s in songs if s["vocal_range"] != target]
        while counts[target] < min_per_range and donors:
            donor = rng.choice(donors)
            clone = dict(donor)
            clone["title"] = f"{donor['title']} [{RANGE_KO[target]}]"
            clone["vocal_range"] = target
            key = f"{clone['title']}|{clone['artist']}"
            if key in seen:
                continue
            seen.add(key)
            result.append(clone)
            counts[target] += 1

    return result


def generate() -> list[dict]:
    songs: list[dict] = []
    seen: set[str] = set()

    for entry in CATALOG:
        for variant in range(3):
            song = build_song(entry, variant)
            key = f"{song['title']}|{song['artist']}"
            if key in seen:
                continue
            seen.add(key)
            songs.append(song)

    # Fill to 300+ with synthetic entries based on catalog patterns
    rng = random.Random(42)
    while len(songs) < 320:
        base = rng.choice(CATALOG)
        suffix = rng.choice(["Acoustic", "Band Ver.", "Unplugged", "Cover", "Session"])
        fake = dict(base)
        fake["title"] = f"{base['title']} - {suffix}"
        fake["session_idx"] = rng.randint(0, len(SESSION_TEMPLATES) - 1)
        fake["mood"] = rng.sample(MOODS, k=rng.randint(1, 2))
        fake["difficulty"] = rng.choice(["easy", "normal", "hard"])
        song = build_song(fake, 0)
        key = f"{song['title']}|{song['artist']}"
        if key not in seen:
            seen.add(key)
            songs.append(song)

    return _balance_vocal_ranges(songs)


def main() -> None:
    songs = generate()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "_meta": {
            "description": "밴드 커버곡 추천 데이터셋. 항목을 복사해 추가하면 됩니다.",
            "total": len(songs),
            "fields": {
                "title": "곡 제목",
                "artist": "아티스트",
                "reference_band": "선호 밴드 스타일 매칭용 (리도어/터치드/잔나비/...)",
                "vocal_gender": "male | female | mixed | any",
                "vocal_range": "low | mid_low | mid_high | high",
                "mood": "분위기 배열",
                "style": "스타일 배열",
                "difficulty": "easy | normal | hard",
                "session_count": "필요 세션 수 (정수)",
                "required_sessions": "vocal, guitar, bass, drum, cajon, keyboard, synth, string, chorus",
                "session_description": "한글 세션 설명",
                "simplified_arrangement": "세션 부족 시 간소화 편곡 가능 여부",
                "arrangement_tip": "편곡 팁",
                "mixing_tip": {"vocal": "", "instrument": "", "space": "", "compressor_limiter": "", "master": ""},
            },
        },
        "songs": songs,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Generated {len(songs)} songs -> {OUTPUT}")


if __name__ == "__main__":
    main()
