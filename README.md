# Band Setlist Recommender

Streamlit + FastAPI + Docker Compose 기반 **밴드 커버곡 추천 + 믹싱 방향 추천** 웹 애플리케이션입니다.

보컬 성별·음역대·세션 구성·보유 악기·분위기를 입력하면, 조건 점수 기반으로 Top 5 커버곡과 각 곡에 맞는 편곡·믹싱 팁을 제공합니다.

## 주요 기능

### 1. 밴드 커버곡 추천
- `back/data/songs.json` (453곡+) 데이터셋 기반
- 보컬 성별, 음역대, 세션 수, 분위기, 스타일, 보유 악기 조건 **점수 매칭**
- Top 5 곡 추천 (제목, 아티스트, 점수, 난이도, 세션 구성, 추천 이유)
- 세션 부족 시 **간소화 편곡 가능** 여부 표시

### 2. 믹싱 방향 추천
- 추천된 각 곡별 믹싱 가이드
  - 보컬 EQ
  - 악기 밸런스
  - 리버브/딜레이
  - 컴프레서/리미터
  - 마스터링 팁

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | Streamlit (Band Poster Flat UI) |
| Backend | FastAPI |
| Data | JSON (`songs.json`) |
| Container | Docker, Docker Compose |
| 추천 로직 | Rule-based 점수 매칭 (if-else + weighted scoring) |

## 폴더 구조

```
recommend-mix-app/
├── front/
│   ├── app.py              # Streamlit UI
│   ├── Dockerfile
│   └── requirements.txt
├── back/
│   ├── main.py             # FastAPI 엔드포인트
│   ├── recommender.py      # 점수 기반 추천 엔진
│   ├── generate_songs.py   # songs.json 생성 스크립트
│   ├── data/
│   │   └── songs.json      # 곡 데이터 (453곡+)
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

## 곡 데이터 추가 방법

`back/data/songs.json`의 `songs` 배열에 아래 형식으로 항목을 추가합니다.

```json
{
  "title": "곡 제목",
  "artist": "아티스트",
  "reference_band": "잔나비",
  "vocal_gender": "male",
  "vocal_range": "mid_high",
  "mood": ["감성적인", "잔잔한"],
  "style": ["인디", "밴드"],
  "difficulty": "normal",
  "session_count": 4,
  "required_sessions": ["vocal", "guitar", "bass", "drum"],
  "session_description": "보컬 1, 기타 1, 베이스 1, 드럼 1",
  "simplified_arrangement": true,
  "arrangement_tip": "카혼 편곡으로 줄이면 버스킹용으로도 가능",
  "mixing_tip": {
    "vocal": "보컬 2~5kHz presence",
    "instrument": "기타 mid 정리",
    "space": "hall reverb 2s",
    "compressor_limiter": "comp 3:1",
    "master": "LUFS -14"
  }
}
```

대량 생성:

```bash
cd back && python generate_songs.py
```

---

## 로컬 실행 방법

### 사전 요구사항
- Python 3.11+

### 1) FastAPI 백엔드

```bash
cd back
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

> **Note:** Cursor 등 IDE가 8000 포트를 사용하는 경우가 있어 로컬에서는 **8001** 포트를 권장합니다. Streamlit은 실행 중인 API 포트를 자동 감지합니다.

- API 문서: http://localhost:8000/docs
- 헬스체크: http://localhost:8000/health

### 2) Streamlit 프론트 (새 터미널)

```bash
cd front
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

- 웹 UI: http://localhost:8501 (API URL은 자동 감지)

---

## Docker 실행 방법

프로젝트 루트에서:

```bash
docker compose up --build
```

| 서비스 | 포트 | 설명 |
|--------|------|------|
| front | 8501 | Streamlit UI |
| back | 8000 | FastAPI API |

Streamlit 컨테이너는 `http://back:8000/recommend` 로 API를 호출합니다.

```bash
# 백그라운드
docker compose up -d --build

# 종료
docker compose down
```

---

## EC2 실행 방법

### 1. 인스턴스 & 보안 그룹
- Ubuntu 22.04 / Amazon Linux 2023
- 인바운드: **8501** (Streamlit), **8000** (FastAPI, 선택), **22** (SSH)

### 2. Docker 설치 (Ubuntu)

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER
newgrp docker
```

### 3. 배포

```bash
git clone <your-repo-url>
cd recommend-mix-app
docker compose up -d --build
```

### 4. 접속

- Streamlit: `http://<EC2_PUBLIC_IP>:8501`
- FastAPI Docs: `http://<EC2_PUBLIC_IP>:8000/docs`

---

## 데모 영상 체크리스트

1. **프로젝트 소개** — Band Setlist Recommender, 2대 기능(커버곡 + 믹싱) 설명
2. **실행 환경** — `docker compose up --build` 또는 EC2 URL
3. **UI 소개** — Band Poster 스타일, 입력 폼 7항목
4. **입력 시연** — 보컬 성별/음역대/세션/악기/분위기 선택
5. **추천 요청** — "커버곡 & 믹싱 추천 받기" 버튼 클릭
6. **결과 확인** — Top 5 포스터 카드 (곡명, 아티스트, 점수, 세션, 편곡·믹싱 팁)
7. **입력 변경** — 조건 바꿔 점수/순위 변화 시연
8. **API 연동** — `/docs`에서 `/recommend` POST 또는 Network 탭 확인
9. **데이터 구조** — `songs.json` 구조와 곡 추가 방법 간략 소개
10. **마무리** — Docker front/back 분리, EC2 배포 가능

## API 요청 예시

```bash
curl -X POST http://localhost:8000/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "vocal_gender": "남자",
    "vocal_range": "중고음",
    "session_count": "4명",
    "available_instruments": ["기타", "베이스", "드럼", "키보드"],
    "mood": "감성적인"
  }'
```

## 라이선스

교육용 기말 과제 프로젝트
