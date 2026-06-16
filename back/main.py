import json
from pathlib import Path
from typing import Literal

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from recommender import recommend_songs

app = FastAPI(
    title="Band Setlist Recommender API",
    description="밴드 커버곡 추천 + 믹싱 방향 추천 API",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATA_PATH = Path(__file__).parent / "data" / "songs.json"


def load_songs() -> list[dict]:
    with DATA_PATH.open(encoding="utf-8") as f:
        payload = json.load(f)
    return payload["songs"]


SONGS = load_songs()

VocalGender = Literal["남자", "여자", "혼성", "상관없음"]
VocalRange = Literal["낮은 음역", "중저음", "중고음", "높은 음역"]
SessionCount = Literal["1명", "2명", "3명", "4명", "5명 이상", "풀세션"]
Mood = Literal["감성적인", "청량한", "강한", "몽환적인", "신나는", "잔잔한"]


class RecommendRequest(BaseModel):
    vocal_gender: VocalGender = Field(..., description="보컬 성별")
    vocal_range: VocalRange = Field(..., description="보컬 음역대")
    session_count: SessionCount = Field(..., description="세션 수")
    available_instruments: list[str] = Field(..., min_length=1, description="가능한 악기")
    mood: Mood = Field(..., description="곡 분위기")


class MixingDirection(BaseModel):
    vocal_eq: str
    instrument_balance: str
    reverb_delay: str
    compressor_limiter: str
    mastering_tip: str


class SongRecommendation(BaseModel):
    title: str
    artist: str
    score: float
    reason: str
    difficulty: str
    vocal_range: str
    session_description: str
    required_sessions: list[str]
    simplified_arrangement_possible: bool
    arrangement_tip: str
    mixing_direction: MixingDirection


class RecommendResponse(BaseModel):
    title: str
    summary: str
    recommendations: list[SongRecommendation]
    caution: list[str]


def _build_summary(payload: RecommendRequest) -> str:
    instruments = ", ".join(payload.available_instruments)
    return (
        f"{payload.vocal_gender} · {payload.vocal_range} · "
        f"세션 {payload.session_count} · {instruments} · "
        f"'{payload.mood}' 기준 Top 5 추천"
    )


def _build_cautions(items: list[dict]) -> list[str]:
    cautions = [
        "추천 점수는 입력 조건과의 일치도이며, 실제 연주 난이도는 멤버 숙련도에 따라 달라집니다.",
        "간소화 편곡 가능 곡도 원곡 템포·키를 맞추면 더 자연스럽게 들립니다.",
    ]
    if any(item["simplified_arrangement_possible"] for item in items):
        cautions.append("세션 수가 부족한 곡은 카혼·loop station·어쿠스틱 편곡으로 대체해 보세요.")
    if any(item["difficulty"] == "어려움" for item in items):
        cautions.append("난이도 '어려움' 곡은 리허설 일정을 넉넉히 잡는 것을 권장합니다.")
    return cautions


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok", "songs_loaded": len(SONGS)}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(payload: RecommendRequest) -> RecommendResponse:
    results = recommend_songs(
        SONGS,
        vocal_gender=payload.vocal_gender,
        vocal_range=payload.vocal_range,
        session_count=payload.session_count,
        available_instruments=payload.available_instruments,
        mood=payload.mood,
        top_n=5,
    )

    return RecommendResponse(
        title="Band Setlist 추천 결과",
        summary=_build_summary(payload),
        recommendations=results,
        caution=_build_cautions(results),
    )
