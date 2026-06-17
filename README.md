# Band Setlist Recommender

Streamlit + FastAPI + Docker Compose 기반 **밴드 커버곡 추천 + 믹싱 방향 추천** 웹 애플리케이션입니다.

보컬 성별·음역대·세션 구성·보유 악기·분위기를 입력하면, 조건 점수 기반으로 **Top 5** 커버곡과 각 곡에 맞는 편곡·믹싱 팁을 제공합니다.

**GitHub:** https://github.com/dlwldn4824/opensource_final

---

## 목차

- [주요 기능](#주요-기능)
- [기술 스택](#기술-스택)
- [폴더 구조](#폴더-구조)
- [입력 항목](#입력-항목)
- [곡 데이터](#곡-데이터)
- [로컬 실행 방법](#로컬-실행-방법)
- [Docker 실행 방법](#docker-실행-방법)
- [EC2 배포 방법](#ec2-배포-방법)
- [API 요청 예시](#api-요청-예시)
- [데모 영상 체크리스트](#데모-영상-체크리스트)

---

## 주요 기능

### 1. 밴드 커버곡 추천

- `back/data/songs.json` (**552곡**) 데이터셋 기반
- 보컬 성별, 음역대, 세션 수, 분위기, 보유 악기 조건 **점수 매칭**
- 조건에 맞는 **Top 5** 곡 추천 (제목, 아티스트, 점수, 난이도, 세션 구성, 추천 이유)
- 세션 수가 부족한 경우 **간소화 편곡 가능** 여부 표시

### 2. 믹싱 방향 추천

추천된 각 곡별 믹싱 가이드를 제공합니다.

| 항목 | 설명 |
|------|------|
| 보컬 EQ | 보컬 존재감·치찰음 조정 방향 |
| 악기 밸런스 | 악기 mid-range 정리 및 보컬 분리 |
| 리버브/딜레이 | 곡 분위기에 맞는 공간감 처리 |
| 컴프레서/리미터 | 보컬·버스 컴프 설정 가이드 |
| 마스터링 팁 | 다이내믹·LUFS·ceiling 권장값 |

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| Frontend | Streamlit (그런지/펑크 포스터 UI) |
| Backend | FastAPI |
| Data | JSON (`songs.json`, 552곡) |
| Container | Docker, Docker Compose |
| 추천 로직 | Rule-based 점수 매칭 (if-else + weighted scoring) |
| 배포 | AWS EC2 |

---

## 폴더 구조

```
opensource_final/
├── front/
│   ├── app.py              # Streamlit UI
│   ├── Dockerfile
│   └── requirements.txt
├── back/
│   ├── main.py             # FastAPI 엔드포인트
│   ├── recommender.py      # 점수 기반 추천 엔진
│   ├── generate_songs.py   # songs.json 생성 스크립트
│   ├── data/
│   │   └── songs.json      # 곡 데이터 (552곡)
│   ├── Dockerfile
│   └── requirements.txt
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 입력 항목

| 항목 | 선택지 |
|------|--------|
| 보컬 성별 | 남자 / 여자 / 혼성 / 상관없음 |
| 보컬 음역대 | 낮은 음역 / 중저음 / 중고음 / 높은 음역 |
| 세션 수 | 1명 / 2명 / 3명 / 4명 / 5명 이상 / 풀세션 |
| 가능한 악기 | 기타, 베이스, 드럼, 카혼, 키보드, 신디, 스트링, 코러스 |
| 곡 분위기 | 감성적인 / 청량한 / 강한 / 몽환적인 / 신나는 / 잔잔한 |

---

## 곡 데이터

곡 데이터는 `back/data/songs.json`에 저장되어 있으며, 현재 **552곡**이 등록되어 있습니다.

### 항목 추가 예시

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

### 대량 생성

```bash
cd back
python generate_songs.py
```

---

## 로컬 실행 방법

### 사전 요구사항

- Python 3.11+
- pip

### 1) FastAPI 백엔드

```bash
cd back
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

> Cursor 등 IDE가 8000 포트를 점유하는 경우가 있어, **로컬 개발 시 FastAPI는 8001 포트**를 사용합니다.  
> Streamlit은 실행 중인 API 포트(8001 → 8000 → 8002)를 자동 감지합니다.

| 항목 | URL |
|------|-----|
| API 문서 | http://localhost:8001/docs |
| 헬스체크 | http://localhost:8001/health |

### 2) Streamlit 프론트 (새 터미널)

```bash
cd front
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

| 항목 | URL |
|------|-----|
| 웹 UI | http://localhost:8501 |

---

## Docker 실행 방법

프로젝트 루트에서 실행합니다.

```bash
docker compose up --build
```

| 서비스 | 컨테이너 | 포트 | 설명 |
|--------|----------|------|------|
| front | recommend-mix-front | 8501 | Streamlit UI |
| back | recommend-mix-back | 8000 | FastAPI API |

- Streamlit: http://localhost:8501
- FastAPI Docs: http://localhost:8000/docs
- Streamlit 컨테이너 내부 API 주소: `http://back:8000/recommend`

```bash
# 백그라운드 실행
docker compose up -d --build

# 종료
docker compose down
```

---

## EC2 배포 방법

### 1. 인스턴스 및 보안 그룹

- OS: Ubuntu 22.04 LTS 또는 Amazon Linux 2023
- 인바운드 규칙:

| 포트 | 프로토콜 | 용도 |
|------|----------|------|
| 22 | TCP | SSH |
| 8501 | TCP | Streamlit |
| 8000 | TCP | FastAPI (선택) |

### 2. Docker 설치 (Ubuntu 22.04)

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Docker 설치 (Amazon Linux 2023)

```bash
sudo dnf install -y docker git
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ec2-user
```

재접속 후 Docker Compose를 설치합니다.

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.7/docker-compose-linux-x86_64" \
  -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

### 4. 배포

```bash
git clone https://github.com/dlwldn4824/opensource_final.git
cd opensource_final
docker-compose up -d --build
```

Ubuntu에서 `docker compose`(플러그인)를 사용하는 경우:

```bash
git clone https://github.com/dlwldn4824/opensource_final.git
cd opensource_final
docker compose up -d --build
```

### 5. 상태 확인 및 접속

```bash
docker ps
```

| 항목 | URL |
|------|-----|
| Streamlit | `http://<EC2_PUBLIC_IP>:8501` |
| FastAPI Docs | `http://<EC2_PUBLIC_IP>:8000/docs` |

---

## API 요청 예시

### 로컬 (FastAPI 8001)

```bash
curl -X POST http://localhost:8001/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "vocal_gender": "남자",
    "vocal_range": "중고음",
    "session_count": "4명",
    "available_instruments": ["기타", "베이스", "드럼", "키보드"],
    "mood": "감성적인"
  }'
```

### Docker / EC2 (FastAPI 8000)

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

### 응답 형식 (요약)

```json
{
  "title": "Band Setlist 추천 결과",
  "summary": "...",
  "recommendations": [
    {
      "title": "곡 제목",
      "artist": "아티스트",
      "score": 95.0,
      "reason": "추천 이유",
      "difficulty": "보통",
      "vocal_range": "중고음",
      "session_description": "보컬 1, 기타 1, 베이스 1, 드럼 1",
      "arrangement_tip": "편곡 팁",
      "mixing_direction": { "vocal_eq": "...", "instrument_balance": "..." }
    }
  ],
  "caution": ["주의사항"]
}
```

---

## 데모 영상 체크리스트

1. **프로젝트 소개** — Band Setlist Recommender, 커버곡 추천 + 믹싱 방향 추천 설명
2. **GitHub 저장소** — https://github.com/dlwldn4824/opensource_final 화면
3. **실행 환경** — `docker compose up --build` 또는 EC2 URL (`http://<EC2_IP>:8501`)
4. **UI 소개** — 그런지/펑크 포스터 스타일, 입력 폼 5항목
5. **입력 시연** — 보컬 성별 / 음역대 / 세션 수 / 악기 / 분위기 선택
6. **추천 요청** — "커버곡 & 믹싱 추천 받기" 버튼 클릭
7. **결과 확인** — Top 5 카드 (곡명, 아티스트, 점수, 세션, 편곡·믹싱 팁)
8. **입력 변경** — 조건 변경 시 추천 결과·점수 변화 시연
9. **API 연동** — `http://<HOST>:8000/docs`에서 `/recommend` POST 확인
10. **EC2 확인** — 터미널에서 `docker ps`로 front/back 컨테이너 실행 확인

---

## 라이선스

교육용 기말 과제 프로젝트
