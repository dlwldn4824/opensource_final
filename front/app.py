import html
import os
import socket

import requests
import streamlit as st


def _default_api_url() -> str:
    if url := os.getenv("API_URL"):
        return url
    # Docker Compose 내부
    try:
        socket.gethostbyname("back")
        return "http://back:8000/recommend"
    except OSError:
        pass
    # 로컬: 8000은 IDE(Cursor)가 점유하는 경우가 많아 8001 우선
    for port in (8001, 8000, 8002):
        try:
            res = requests.get(f"http://127.0.0.1:{port}/health", timeout=1)
            if res.ok and "songs_loaded" in res.json():
                return f"http://127.0.0.1:{port}/recommend"
        except requests.RequestException:
            continue
    return "http://127.0.0.1:8001/recommend"


API_URL = _default_api_url()
API_BASE = API_URL.rsplit("/", 1)[0]


def _check_api_ready() -> tuple[bool, str]:
    try:
        res = requests.get(f"{API_BASE}/health", timeout=5)
        res.raise_for_status()
        data = res.json()
        if "songs_loaded" not in data:
            return False, "구버전 API가 실행 중입니다. 백엔드를 재시작하거나 Docker 이미지를 다시 빌드해 주세요."
        return True, f"API 연결됨 · {data['songs_loaded']}곡 로드"
    except requests.exceptions.ConnectionError:
        return False, (
            f"FastAPI({API_BASE})에 연결할 수 없습니다. "
            "로컬 실행: `cd back && uvicorn main:app --port 8001` 후 페이지를 새로고침하세요. "
            "Docker: `docker compose up --build`"
        )
    except requests.exceptions.RequestException as exc:
        return False, f"API 상태 확인 실패: {exc}"

st.set_page_config(
    page_title="Band Setlist Recommender",
    page_icon="🎸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

INSTRUMENTS = ["기타", "베이스", "드럼", "카혼", "키보드", "신디", "스트링", "코러스"]

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Noto+Sans+KR:wght@400;500;700;900&family=Oswald:wght@500;700&family=Special+Elite&display=swap');

    .stApp {
        background-color: #ECECEC;
        background-image:
            radial-gradient(circle, #0A0A0A 0.6px, transparent 0.6px);
        background-size: 5px 5px;
    }

    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
        background: transparent !important;
    }

    .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
    }

    [data-testid="stForm"] {
        background: #F5F5F5;
        border: 4px solid #0A0A0A;
        border-radius: 4px;
        padding: 1.25rem 1.5rem 1.5rem;
        box-shadow: 6px 6px 0 #0A0A0A;
    }

    [data-testid="stForm"] label,
    [data-testid="stForm"] .stSelectbox label,
    [data-testid="stForm"] .stMultiSelect label {
        font-family: 'Oswald', 'Noto Sans KR', sans-serif !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #0A0A0A !important;
        font-weight: 700 !important;
    }

    /* ── Hero ── */
    .poster-hero {
        background: #F0F0F0;
        border: 4px solid #0A0A0A;
        border-radius: 0;
        padding: 2rem 1.5rem 1.75rem;
        margin-bottom: 1.25rem;
        box-shadow: 8px 8px 0 #0A0A0A;
        text-align: center;
        position: relative;
        overflow: hidden;
    }

    .poster-hero::before {
        content: "";
        position: absolute;
        inset: 0;
        background-image: radial-gradient(circle, #0A0A0A 0.5px, transparent 0.5px);
        background-size: 4px 4px;
        opacity: 0.12;
        pointer-events: none;
    }

    .brush-stroke {
        position: absolute;
        bottom: 0;
        left: -5%;
        width: 110%;
        height: 14px;
        background: #E85D04;
        transform: rotate(-1.5deg);
        opacity: 0.9;
        z-index: 1;
    }

    .poster-title {
        font-family: 'Bebas Neue', 'Oswald', sans-serif;
        font-size: clamp(2.4rem, 6vw, 4rem);
        font-weight: 900;
        letter-spacing: 0.1em;
        margin: 0;
        line-height: 1;
        position: relative;
        z-index: 2;
    }

    .title-band { color: #0A0A0A; text-shadow: 3px 3px 0 rgba(0,0,0,0.15); }
    .title-setlist { color: #E85D04; text-shadow: 3px 3px 0 #0A0A0A; }
    .title-rec { color: #0A0A0A; text-shadow: 2px 2px 0 #E85D04; font-size: 0.55em; display: block; margin-top: 0.3rem; letter-spacing: 0.2em; }

    .poster-subtitle {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.95rem;
        color: #1A1A1A;
        margin-top: 1rem;
        font-weight: 500;
        position: relative;
        z-index: 2;
        border-top: 3px solid #0A0A0A;
        padding-top: 0.75rem;
    }

    /* ── Input header ── */
    .input-card {
        background: #0A0A0A;
        border: none;
        border-radius: 0;
        padding: 0.6rem 1.25rem;
        margin-bottom: 0.75rem;
        box-shadow: 4px 4px 0 #E85D04;
    }

    .input-card-title {
        font-family: 'Oswald', 'Bebas Neue', sans-serif;
        font-size: 1.35rem;
        color: #FFFFFF;
        letter-spacing: 0.15em;
        margin: 0;
        text-transform: uppercase;
    }

    /* ── Song cards ── */
    .song-card {
        background: #F5F5F5;
        border: 4px solid #0A0A0A;
        border-radius: 4px;
        padding: 1.5rem 1.25rem 1.25rem;
        margin-bottom: 1.5rem;
        box-shadow: 7px 7px 0 #0A0A0A;
        position: relative;
    }

    .song-card::after {
        content: "";
        position: absolute;
        top: 0; right: 0;
        width: 40%;
        height: 100%;
        background-image: radial-gradient(circle, #0A0A0A 0.4px, transparent 0.4px);
        background-size: 3px 3px;
        opacity: 0.06;
        pointer-events: none;
    }

    .song-rank {
        position: absolute;
        top: -16px;
        left: 16px;
        background: #E85D04;
        color: #0A0A0A;
        font-family: 'Bebas Neue', 'Oswald', sans-serif;
        font-size: 1.5rem;
        padding: 0.15rem 0.75rem;
        border-radius: 0;
        border: 3px solid #0A0A0A;
        letter-spacing: 0.05em;
        z-index: 2;
    }

    .song-title {
        font-family: 'Bebas Neue', 'Oswald', 'Noto Sans KR', sans-serif;
        font-size: clamp(1.6rem, 4vw, 2.2rem);
        color: #0A0A0A;
        margin: 0.75rem 0 0.1rem;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        line-height: 1.1;
    }

    .song-artist {
        font-family: 'Oswald', 'Noto Sans KR', sans-serif;
        font-size: 1rem;
        color: #E85D04;
        font-weight: 700;
        margin-bottom: 0.65rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
    }

    .score-badge {
        display: inline-block;
        background: #0A0A0A;
        color: #FFFFFF;
        padding: 0.25rem 0.75rem;
        border-radius: 0;
        font-family: 'Special Elite', 'Courier New', monospace;
        font-size: 0.8rem;
        letter-spacing: 0.05em;
        margin-bottom: 0.65rem;
        border: 2px solid #0A0A0A;
    }

    .tag-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.35rem;
        margin-bottom: 0.65rem;
    }

    .tag {
        background: transparent;
        color: #0A0A0A;
        border: 2px solid #E85D04;
        border-radius: 0;
        padding: 0.1rem 0.55rem;
        font-family: 'Special Elite', monospace;
        font-size: 0.72rem;
        font-weight: 400;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    .section-label {
        font-family: 'Oswald', sans-serif;
        font-size: 0.72rem;
        font-weight: 700;
        color: #0A0A0A;
        text-transform: uppercase;
        letter-spacing: 0.14em;
        margin: 0.85rem 0 0.2rem;
        border-bottom: 2px solid #E85D04;
        display: inline-block;
        padding-bottom: 0.1rem;
    }

    .section-text {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.9rem;
        color: #1A1A1A;
        line-height: 1.6;
        margin: 0;
    }

    .mix-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 0.45rem;
        margin-top: 0.45rem;
    }

    @media (max-width: 640px) {
        .mix-grid { grid-template-columns: 1fr; }
    }

    .mix-item {
        background: #E8E8E8;
        border-left: 4px solid #0A0A0A;
        border-radius: 0;
        padding: 0.45rem 0.65rem;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.8rem;
        color: #1A1A1A;
    }

    .mix-item strong {
        font-family: 'Oswald', sans-serif;
        color: #E85D04;
        display: block;
        font-size: 0.68rem;
        margin-bottom: 0.15rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    .caution-card {
        background: #F5F5F5;
        border: 3px dashed #0A0A0A;
        border-radius: 0;
        padding: 1rem 1.25rem;
        margin-top: 1rem;
        box-shadow: 5px 5px 0 #E85D04;
    }

    .caution-card .section-text::before {
        content: "! ";
        color: #E85D04;
        font-family: 'Bebas Neue', sans-serif;
        font-size: 1.1rem;
    }

    .summary-bar {
        background: #0A0A0A;
        color: #FFFFFF;
        border-radius: 0;
        border: 3px solid #0A0A0A;
        padding: 1rem 1.25rem;
        margin-bottom: 1.25rem;
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 0.92rem;
        line-height: 1.55;
        box-shadow: 5px 5px 0 #E85D04;
    }

    .summary-bar strong {
        font-family: 'Oswald', 'Bebas Neue', sans-serif;
        font-size: 1.15rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: #E85D04;
    }

    div[data-testid="stFormSubmitButton"] button {
        background: #E85D04 !important;
        color: #0A0A0A !important;
        border: 4px solid #0A0A0A !important;
        border-radius: 0 !important;
        font-family: 'Oswald', 'Noto Sans KR', sans-serif !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.12em !important;
        text-transform: uppercase !important;
        padding: 0.7rem 2rem !important;
        box-shadow: 5px 5px 0 #0A0A0A !important;
        transition: transform 0.1s, box-shadow 0.1s !important;
    }

    div[data-testid="stFormSubmitButton"] button:hover {
        transform: translate(-2px, -2px) !important;
        box-shadow: 7px 7px 0 #0A0A0A !important;
        background: #FF4500 !important;
    }

    .stMultiSelect, .stSelectbox { margin-bottom: 0.25rem; }

    [data-testid="stExpander"] {
        border: 2px solid #0A0A0A !important;
        border-radius: 0 !important;
        background: #F0F0F0 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="poster-hero">
        <div class="poster-title">
            <span class="title-band">BAND </span><span class="title-setlist">SETLIST</span>
            <span class="title-rec">RECOMMENDER</span>
        </div>
        <div class="poster-subtitle">보컬 음역대와 세션 구성에 맞는 커버곡 추천</div>
        <div class="brush-stroke"></div>
    </div>
    """,
    unsafe_allow_html=True,
)

api_ok, api_msg = _check_api_ready()
if not api_ok:
    st.warning(api_msg)

st.markdown(
    """
    <div class="input-card">
        <div class="input-card-title">YOUR BAND PROFILE</div>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("setlist_form"):
    col1, col2 = st.columns(2)

    with col1:
        vocal_gender = st.selectbox("보컬 성별", ["남자", "여자", "혼성", "상관없음"])
        vocal_range = st.selectbox("보컬 음역대", ["낮은 음역", "중저음", "중고음", "높은 음역"])
        session_count = st.selectbox("세션 수", ["1명", "2명", "3명", "4명", "5명 이상", "풀세션"])
        mood = st.selectbox("곡 분위기", ["감성적인", "청량한", "강한", "몽환적인", "신나는", "잔잔한"])

    with col2:
        available_instruments = st.multiselect(
            "가능한 악기",
            INSTRUMENTS,
            default=["기타", "베이스", "드럼"],
            help="보유·연주 가능한 악기를 모두 선택하세요.",
        )

    submitted = st.form_submit_button("커버곡 & 믹싱 추천 받기", use_container_width=True)

if submitted:
    if not available_instruments:
        st.error("가능한 악기를 최소 1개 이상 선택해 주세요.")
        st.stop()

    payload = {
        "vocal_gender": vocal_gender,
        "vocal_range": vocal_range,
        "session_count": session_count,
        "available_instruments": available_instruments,
        "mood": mood,
    }

    with st.spinner("세트리스트를 구성하는 중..."):
        try:
            response = requests.post(API_URL, json=payload, timeout=20)
            response.raise_for_status()
            data = response.json()
        except requests.exceptions.ConnectionError:
            st.error(
                f"FastAPI 서버({API_BASE})에 연결할 수 없습니다.\n\n"
                "**로컬 실행:**\n"
                "```bash\n"
                "cd back && source .venv/bin/activate\n"
                "uvicorn main:app --host 0.0.0.0 --port 8001\n"
                "```\n\n"
                "**Docker 실행:**\n"
                "```bash\n"
                "docker compose up --build\n"
                "```"
            )
            st.stop()
        except requests.exceptions.HTTPError:
            st.error(f"API 요청 실패: HTTP {response.status_code}")
            if response.status_code == 422:
                st.error(
                    "요청 형식이 API와 맞지 않습니다. **구버전 백엔드**가 실행 중일 수 있습니다.\n\n"
                    "해결: `docker compose down && docker compose up --build` 또는 "
                    "로컬 실행 시 back 폴더에서 uvicorn을 재시작하세요."
                )
            try:
                detail = response.json()
                st.json(detail)
            except ValueError:
                st.code(response.text)
            st.stop()
        except requests.exceptions.RequestException as exc:
            st.error(f"요청 중 오류: {exc}")
            st.stop()

    summary = html.escape(data.get("summary", ""))
    st.markdown(f'<div class="summary-bar"><strong>{html.escape(data.get("title", ""))}</strong><br>{summary}</div>', unsafe_allow_html=True)

    for idx, song in enumerate(data.get("recommendations", []), start=1):
        mixing = song.get("mixing_direction", {})
        simplified = song.get("simplified_arrangement_possible", False)
        simplified_tag = '<span class="tag">간소화 편곡 가능</span>' if simplified else ""

        mix_items = ""
        mix_labels = {
            "vocal_eq": "보컬 EQ",
            "instrument_balance": "악기 밸런스",
            "reverb_delay": "리버브/딜레이",
            "compressor_limiter": "컴프/리미터",
            "mastering_tip": "마스터링",
        }
        for key, label in mix_labels.items():
            val = html.escape(mixing.get(key, ""))
            mix_items += f'<div class="mix-item"><strong>{label}</strong>{val}</div>'

        card_html = f"""
        <div class="song-card">
            <div class="song-rank">#{idx}</div>
            <div class="song-title">{html.escape(song.get("title", ""))}</div>
            <div class="song-artist">{html.escape(song.get("artist", ""))}</div>
            <div class="score-badge">MATCH SCORE {song.get("score", 0)}</div>
            <div class="tag-row">
                <span class="tag">난이도 {html.escape(song.get("difficulty", ""))}</span>
                <span class="tag">{html.escape(song.get("vocal_range", ""))}</span>
                {simplified_tag}
            </div>
            <div class="section-label">Session</div>
            <p class="section-text">{html.escape(song.get("session_description", ""))}</p>
            <div class="section-label">Why This Song?</div>
            <p class="section-text">{html.escape(song.get("reason", ""))}</p>
            <div class="section-label">Arrangement Tip</div>
            <p class="section-text">{html.escape(song.get("arrangement_tip", ""))}</p>
            <div class="section-label">Mixing Direction</div>
            <div class="mix-grid">{mix_items}</div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    cautions = data.get("caution", [])
    if cautions:
        caution_html = "".join(f"<p class='section-text'>{html.escape(c)}</p>" for c in cautions)
        st.markdown(f'<div class="caution-card">{caution_html}</div>', unsafe_allow_html=True)

with st.expander("사용 방법"):
    st.markdown(
        """
        1. 밴드 프로필(보컬, 세션, 악기, 분위기)을 입력합니다.
        2. **커버곡 & 믹싱 추천 받기**를 누르면 FastAPI가 조건 점수 기반 Top 5를 반환합니다.
        3. 각 곡 카드에서 세션 구성, 편곡 팁, 믹싱 방향을 확인하세요.
        4. `back/data/songs.json`에 곡을 추가하면 추천 풀을 확장할 수 있습니다.
        """
    )
