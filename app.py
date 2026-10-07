import streamlit as st
import random
import time

# =========================================================
# PAGE
# =========================================================

st.set_page_config(
    page_title="YES NO DETECTIVE",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 75% 15%, rgba(0,150,255,0.08), transparent 30%),
        radial-gradient(circle at 15% 80%, rgba(0,100,180,0.05), transparent 30%),
        #070b10;
    color: #edf6ff;
}

/* 전체 화면에서 스크롤 최소화 */
[data-testid="stAppViewContainer"] {
    overflow: hidden !important;
}

[data-testid="stAppViewContainer"] > .main {
    overflow: hidden !important;
}

section.main > div {
    overflow: hidden !important;
}

.block-container {
    max-width: 1500px !important;
    height: calc(100vh - 15px) !important;
    padding-top: 8px !important;
    padding-bottom: 5px !important;
    padding-left: 20px !important;
    padding-right: 20px !important;
    overflow: hidden !important;
}

/* 상단 Streamlit 메뉴 */
#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* 제목 */
.game-title {
    font-size: 36px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
    margin: 0;
}

.game-subtitle {
    color: #5ecbff;
    font-size: 11px;
    letter-spacing: 4px;
    font-weight: 700;
    margin-top: 4px;
}

/* 위쪽 카드 */
.top-card {
    background: linear-gradient(145deg, #101a24, #0b121a);
    border: 1px solid #22384b;
    border-radius: 10px;
    padding: 10px 15px;
    min-height: 58px;
}

.top-label {
    color: #668195;
    font-size: 10px;
    letter-spacing: 2px;
}

.top-value {
    color: white;
    font-size: 20px;
    font-weight: 800;
    margin-top: 1px;
}

/* 메인 패널 */
.panel {
    background: rgba(10,17,24,0.97);
    border: 1px solid #213546;
    border-radius: 10px;
    overflow: hidden;
    height: 650px;
}

/* 패널 헤더 */
.panel-head {
    height: 42px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 16px;
    background: #0d151d;
    border-bottom: 1px solid #203443;
}

.panel-head-left {
    color: #dcecff;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1px;
}

.panel-head-right {
    color: #3bbcff;
    font-size: 9px;
    letter-spacing: 2px;
}

/* 사건 사진 */
.case-image {
    height: 270px;
    width: 100%;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid #263b4a;
}

/* 사건 내용 */
.case-content {
    padding: 15px 18px;
}

.case-number {
    color: #40c7ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 3px;
}

.case-title {
    font-size: 25px;
    font-weight: 900;
    margin-top: 5px;
    margin-bottom: 8px;
}

.case-description {
    color: #c4d0d9;
    font-size: 13px;
    line-height: 1.65;
}

.case-warning {
    margin-top: 10px;
    padding: 9px 12px;
    border-left: 3px solid #38bdf8;
    background: #0b1822;
    color: #9bdcff;
    font-size: 11px;
}

/* 용의자 */
.suspect-card {
    background: #0a1118;
    border: 1px solid #1f3444;
    border-radius: 8px;
    padding: 9px 11px;
    margin-bottom: 7px;
}

.suspect-card:hover {
    border-color: #2e8bb8;
}

.suspect-name {
    font-size: 15px;
    font-weight: 800;
}

.suspect-role {
    color: #708596;
    font-size: 9px;
    letter-spacing: 1px;
}

.suspect-info {
    color: #aebdc8;
    font-size: 10px;
    line-height: 1.45;
    margin-top: 5px;
}

/* 질문 영역 */
.question-box {
    background: #0b141d;
    border: 1px solid #23465c;
    border-radius: 8px;
    padding: 12px;
    margin-top: 9px;
}

.question-label {
    color: #4dc8ff;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 2px;
}

.question-text {
    color: white;
    font-size: 15px;
    font-weight: 700;
    line-height: 1.5;
    margin-top: 5px;
}

/* 답변 */
.answer-box {
    background: #0b1820;
    border: 1px solid #1d607d;
    border-radius: 7px;
    padding: 10px;
    margin-top: 8px;
    color: #c8ecff;
    font-size: 11px;
    line-height: 1.5;
}

.clue-box {
    background: #12180e;
    border: 1px solid #596a2c;
    border-radius: 7px;
    padding: 9px;
    margin-top: 7px;
    color: #d9e7a4;
    font-size: 10px;
    line-height: 1.45;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    height: 40px;
    border-radius: 7px !important;
    border: 1px solid #31556c !important;
    background: #102130 !important;
    color: #dff5ff !important;
    font-weight: 800 !important;
    font-size: 12px !important;
}

.stButton > button:hover {
    border-color: #35bfff !important;
    background: #123247 !important;
    color: white !important;
}

button[kind="primary"] {
    background: #087caf !important;
    border-color: #29bfff !important;
    color: white !important;
}

/* selectbox */
.stSelectbox > div > div {
    background: #0c151d !important;
    border-color: #274355 !important;
    color: white !important;
}

/* 입력창 */
.stTextInput input {
    background: #091119 !important;
    color: white !important;
    border: 1px solid #29485c !important;
}

/* 진행 바 */
.progress-wrap {
    background: #111b24;
    border-radius: 100px;
    height: 6px;
    overflow: hidden;
    margin-top: 7px;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #168fc4, #49d3ff);
}

/* 작은 텍스트 */
.muted {
    color: #617686;
    font-size: 10px;
}

.success {
    color: #66e3a1;
}

.danger {
    color: #ff7373;
}

.yellow {
    color: #e6dc73;
}

/* 추리 */
.final-box {
    background: linear-gradient(145deg, #0e1a24, #0a1117);
    border: 1px solid #315b75;
    border-radius: 10px;
    padding: 14px;
    margin-top: 8px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

CASES = [

    {
        "id": "001",
        "title": "잠긴 방의 진실",
        "location": "서울 · 마포구 · 23:58",
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=85",

        "story": """
        한 남자가 자신의 집 안에서 숨진 채 발견되었다.
        현관문은 안쪽에서 잠겨 있었고 창문에서도 침입 흔적은 발견되지 않았다.
        하지만 경찰이 현장을 확인했을 때 이상한 점 하나가 발견되었다.
        사건 발생 직전 집 안에 있던 사람들의 진술이 서로 맞지 않았다.
        """,

        "warning": "현장에는 외부 침입 흔적이 없다. 하지만 누군가는 거짓말을 하고 있다.",

        "suspects": [
            {
                "name": "김민재",
                "role": "피해자의 직장 동료",
                "info": "사건 당일 피해자와 마지막으로 통화했다.",
                "suspicion": "승진 문제로 피해자와 크게 다툰 적이 있다."
            },
            {
                "name": "박서연",
                "role": "피해자의 전 여자친구",
                "info": "헤어진 뒤에도 피해자와 연락을 유지하고 있었다.",
                "suspicion": "사건 당일 밤 피해자에게 세 번 전화했다."
            },
            {
                "name": "최도윤",
                "role": "피해자의 이웃",
                "info": "사건 발생 시각에 복도에서 이상한 소리를 들었다고 주장한다.",
                "suspicion": "하지만 경찰에게 처음에는 아무것도 못 들었다고 말했다."
            },
            {
                "name": "이하늘",
                "role": "피해자의 동생",
                "info": "피해자와 금전 문제로 갈등이 있었다.",
                "suspicion": "사건 당일 피해자의 집을 방문했다고 인정했다."
            }
        ],

        "questions": [
            ("남자는 사건 당일 밤 누군가와 통화했습니까?",
             "예. 피해자의 휴대전화에는 23시 31분에 마지막 통화 기록이 남아 있습니다.",
             "핵심 단서: 마지막 통화 시간이 사건 발생 직전이다.", True),

            ("현관문은 안쪽에서 잠겨 있었습니까?",
             "예. 보조 잠금장치까지 걸려 있었습니다.",
             "외부 침입만으로 설명하기 어려운 상황이다.", True),

            ("창문으로 들어온 흔적이 있습니까?",
             "아니요. 창문에는 외부에서 침입한 흔적이 없습니다.",
             "창문 침입설은 배제된다.", True),

            ("김민재는 피해자와 사건 당일 만났습니까?",
             "아니요. 김민재는 직접 만난 적이 없다고 진술했습니다.",
             "하지만 통화 기록은 존재한다.", False),

            ("박서연은 사건 당일 피해자의 집에 갔습니까?",
             "아니요. 본인은 집에 가지 않았다고 주장합니다.",
             "현재로서는 물증이 없습니다.", False),

            ("최도윤은 사건 당시 복도에 있었습니까?",
             "예. CCTV상 복도에 있었던 것이 확인되었습니다.",
             "그는 현장 근처에 있었다.", True),

            ("최도윤은 처음부터 소리를 들었다고 했습니까?",
             "아니요. 최초 진술에서는 아무 소리도 듣지 못했다고 했습니다.",
             "진술이 변경됐다.", True),

            ("피해자의 휴대전화가 사라졌습니까?",
             "아니요. 휴대전화는 침대 옆에서 발견되었습니다.",
             "범인은 휴대전화를 가져가지 않았다.", False),

            ("사망 시각은 23시 이후입니까?",
             "예. 법의학 기록상 23시 40분에서 23시 55분 사이입니다.",
             "마지막 통화와 매우 가깝다.", True),

            ("누군가 피해자의 비밀번호를 알고 있었습니까?",
             "예. 가족과 가까운 동료 몇 명이 알고 있었습니다.",
             "외부인이 아니어도 접근할 수 있었다.", True),

            ("집 안에서 몸싸움 흔적이 발견됐습니까?",
             "아니요. 큰 몸싸움의 흔적은 발견되지 않았습니다.",
             "피해자가 공격자를 경계하지 않았을 가능성이 있다.", True),

            ("김민재에게 사건 당시 알리바이가 있습니까?",
             "예. 동료 두 명이 함께 있었다고 진술했습니다.",
             "알리바이가 존재하지만 완전히 검증되지는 않았다.", False),

            ("박서연의 전화가 사건 발생 직전에 걸려왔습니까?",
             "예. 23시 42분에 전화가 걸려왔습니다.",
             "피해자와 마지막 연락을 주고받은 사람 중 한 명이다.", True),

            ("최도윤은 피해자의 집 내부를 알고 있었습니까?",
             "예. 이전에 여러 차례 피해자의 집에 방문한 적이 있습니다.",
             "집 구조를 알고 있었다.", True),

            ("사건 현장의 진술 중 하나가 거짓입니까?",
             "예. 최소 한 명은 중요한 부분에서 거짓말을 하고 있습니다.",
             "이제 범인을 특정할 수 있는 단계다.", True)
        ],

        "answer": "최도윤",
        "solution": "최도윤은 사건 당시 복도에 있었다고 진술했지만 최초 진술에서는 아무 소리도 듣지 못했다고 말했다. 그는 집 구조도 알고 있었고, 사건 직후 자신의 진술을 바꿨다. 결정적인 것은 '현장에 없었다'가 아니라 '처음과 나중의 이야기가 달라졌다'는 점이다."
    },

    {
        "id": "002",
        "title": "사라진 18분",
        "location": "부산 · 해운대 · 02:18",
        "image": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?auto=format&fit=crop&w=1200&q=85",

        "story": """
        한 회사의 중요한 설계 파일이 사라졌다.
        서버 기록에는 정확히 18분 동안 접속 기록이 비어 있었다.
        보안팀은 외부 해킹 가능성을 먼저 의심했지만,
        이상하게도 서버에 접속했던 사람은 모두 회사 내부 직원이었다.
        """,

        "warning": "18분의 공백. 누군가는 기록을 지웠거나 기록되지 않는 방법을 사용했다.",

        "suspects": [
            {
                "name": "정우진",
                "role": "보안 담당자",
                "info": "서버 관리자 권한을 가지고 있다.",
                "suspicion": "로그를 수정할 수 있는 몇 안 되는 사람이다."
            },
            {
                "name": "한유리",
                "role": "설계팀 직원",
                "info": "사라진 파일을 가장 먼저 발견했다.",
                "suspicion": "파일에 접근할 이유가 있었다."
            },
            {
                "name": "오현석",
                "role": "외주 개발자",
                "info": "사건 당일 원격 접속을 했다.",
                "suspicion": "회사 내부 시스템을 잘 알고 있다."
            }
        ],

        "questions": [
            ("삭제된 파일은 복구할 수 있습니까?",
             "예. 일부 백업 데이터에서 흔적이 남아 있습니다.",
             "완전히 사라진 것은 아니다.", True),

            ("18분 동안 서버 접속 기록이 없었습니까?",
             "예.",
             "이 사건의 가장 중요한 시간 공백이다.", True),

            ("외부 IP가 접속했습니까?",
             "아니요. 확인된 접속은 모두 내부 계정이었습니다.",
             "단순한 외부 해킹 가능성은 낮다.", True),

            ("정우진은 관리자 권한이 있습니까?",
             "예.",
             "로그를 조작할 수 있는 위치다.", True),

            ("한유리는 파일을 알고 있었습니까?",
             "예.",
             "파일의 존재와 중요도를 알고 있었다.", False),

            ("오현석은 원격 접속을 했습니까?",
             "예.",
             "외부인이지만 내부 계정을 사용했다.", True),

            ("로그가 삭제된 흔적이 있습니까?",
             "예.",
             "일부 로그 파일의 수정 시간이 이상하다.", True),

            ("파일은 복사된 흔적이 있습니까?",
             "예.",
             "삭제 전에 다른 위치로 복사된 흔적이 있다.", True),

            ("정우진이 사건 직후 자리를 비웠습니까?",
             "예.",
             "그는 약 20분 동안 자리를 비웠다.", True),

            ("한유리에게 범행 동기가 있습니까?",
             "확실하지 않습니다.",
             "동기는 약하지만 접근 권한은 있었다.", False),

            ("오현석은 서버 관리자 비밀번호를 알고 있었습니까?",
             "아니요.",
             "그가 단독으로 로그를 지우기는 어렵다.", True),

            ("누군가 백업 파일도 확인했습니까?",
             "예.",
             "사건 직후 관리자 계정이 백업 서버를 조회했다.", True),

            ("18분은 우연일 가능성이 있습니까?",
             "매우 낮습니다.",
             "정확히 필요한 작업 시간과 일치한다.", True),

            ("관리자 계정이 사용됐습니까?",
             "예.",
             "관리자 계정에서 파일 삭제 작업이 실행됐다.", True),

            ("정우진의 진술에는 모순이 있습니까?",
             "예.",
             "그는 해당 시간 서버에 접속하지 않았다고 했지만 기록은 다르다.", True)
        ],

        "answer": "정우진",
        "solution": "정우진은 관리자 권한을 가지고 있었고 로그 삭제가 가능한 위치에 있었다. 결정적인 것은 18분 동안의 기록 공백과 그의 진술 모순이다."
    },

    {
        "id": "003",
        "title": "마지막 메시지",
        "location": "인천 · 송도 · 21:06",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1200&q=85",

        "story": """
        한 남자가 친구들에게 마지막 메시지를 보낸 뒤 사라졌다.
        메시지는 단 세 글자였다.

        '괜찮아.'

        하지만 친구들은 모두 그 메시지가 이상하다고 말했다.
        평소 그가 쓰던 말투와 완전히 달랐기 때문이다.
        """,

        "warning": "문장은 짧지만 중요한 것은 내용이 아니라 '말투'다.",

        "suspects": [
            {
                "name": "강지훈",
                "role": "절친한 친구",
                "info": "피해자의 말투를 누구보다 잘 알고 있다.",
                "suspicion": "사건 당일 둘이 크게 싸웠다."
            },
            {
                "name": "윤채원",
                "role": "회사 동료",
                "info": "피해자의 컴퓨터에 접근할 수 있었다.",
                "suspicion": "사건 직전 피해자의 계정을 사용했다."
            },
            {
                "name": "서준호",
                "role": "동생",
                "info": "피해자의 휴대폰 비밀번호를 알고 있었다.",
                "suspicion": "마지막 메시지 이후 바로 연락을 끊었다."
            }
        ],

        "questions": [
            ("'괜찮아'는 평소 피해자가 자주 쓰던 표현입니까?",
             "아니요.",
             "첫 번째 이상점이다.", True),

            ("마지막 메시지가 피해자의 휴대폰에서 전송됐습니까?",
             "예.",
             "기기는 피해자의 것이 맞다.", True),

            ("메시지에는 오타가 없었습니까?",
             "예.",
             "평소보다 지나치게 정확하다.", True),

            ("강지훈은 피해자의 말투를 잘 알고 있습니까?",
             "예.",
             "오랜 친구이기 때문에 잘 알고 있다.", True),

            ("윤채원은 피해자의 컴퓨터를 사용할 수 있었습니까?",
             "예.",
             "회사 시스템 권한이 있었다.", True),

            ("서준호는 휴대폰 비밀번호를 알고 있었습니까?",
             "예.",
             "기기에 접근할 수 있었다.", True),

            ("메시지 전송 직전에 계정 접속 기록이 있습니까?",
             "예.",
             "다른 기기에서 접속한 흔적이 있다.", True),

            ("피해자는 메시지를 보내기 직전 통화를 했습니까?",
             "아니요.",
             "전화 기록은 없다.", False),

            ("메시지가 예약 전송됐을 가능성이 있습니까?",
             "있습니다.",
             "하지만 예약 기능 사용 흔적은 없다.", False),

            ("강지훈은 마지막 메시지를 이상하다고 생각했습니까?",
             "예.",
             "그는 즉시 말투가 다르다고 말했다.", True),

            ("윤채원은 사건 당일 피해자의 계정에 접속했습니까?",
             "예.",
             "접속 기록이 확인된다.", True),

            ("서준호는 마지막 메시지를 보고 바로 답장했습니까?",
             "아니요.",
             "약 30분 후에 답장했다.", False),

            ("마지막 메시지는 누군가 흉내 낸 것일 가능성이 있습니까?",
             "예.",
             "문장 스타일이 평소와 다르다.", True),

            ("윤채원이 계정 접근 권한을 가지고 있었습니까?",
             "예.",
             "업무상 접근할 수 있었다.", True),

            ("범인은 피해자의 말투를 알고 있었습니까?",
             "예.",
             "마지막 메시지는 피해자를 알고 있는 사람이 작성한 것으로 보인다.", True)
        ],

        "answer": "윤채원",
        "solution": "윤채원은 피해자의 컴퓨터와 계정에 접근할 수 있었고 마지막 메시지 직전 계정 접속 기록이 남아 있다. 결정적인 것은 메시지의 내용이 아니라 피해자의 평소 말투와 다르다는 점이다."
    }
]


# =========================================================
# SESSION
# =========================================================

if "case_index" not in st.session_state:
    st.session_state.case_index = 0

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "clues" not in st.session_state:
    st.session_state.clues = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "game_started" not in st.session_state:
    st.session_state.game_started = False

if "finished_case" not in st.session_state:
    st.session_state.finished_case = False

if "final_result" not in st.session_state:
    st.session_state.final_result = None


case = CASES[st.session_state.case_index]

questions = case["questions"]

q_index = st.session_state.question_index

if q_index >= len(questions):
    q_index = len(questions) - 1


# =========================================================
# TOP
# =========================================================

top1, top2, top3, top4, top5 = st.columns([2.4, 1, 1, 1, 1])

with top1:
    st.markdown("""
    <div class="game-subtitle">CONFIDENTIAL · 34 CASE FILES</div>
    <div class="game-title">예스노 탐정</div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown(f"""
    <div class="top-card">
        <div class="top-label">CASE</div>
        <div class="top-value">{case["id"]}</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown(f"""
    <div class="top-card">
        <div class="top-label">ROUND</div>
        <div class="top-value">{st.session_state.case_index + 1:02d} / {len(CASES):02d}</div>
    </div>
    """, unsafe_allow_html=True)

with top4:
    st.markdown(f"""
    <div class="top-card">
        <div class="top-label">질문</div>
        <div class="top-value">{st.session_state.question_index}/15</div>
    </div>
    """, unsafe_allow_html=True)

with top5:
    st.markdown(f"""
    <div class="top-card">
        <div class="top-label">점수</div>
        <div class="top-value">{st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# =========================================================
# MAIN
# =========================================================

left, right = st.columns([1.55, 1], gap="small")


# =========================================================
# LEFT : CASE
# =========================================================

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-head">
            <div class="panel-head-left">CASE FILE // 현장 기록</div>
            <div class="panel-head-right">CONFIDENTIAL</div>
        </div>
    """, unsafe_allow_html=True)

    st.image(case["image"], use_container_width=True)

    st.markdown(f"""
    <div class="case-content">

        <div class="case-number">CASE #{case["id"]} · EVIDENCE PHOTO</div>

        <div class="case-title">
            {case["title"]}
        </div>

        <div class="muted">
            {case["location"]}
        </div>

        <div class="case-description">
            {case["story"]}
        </div>

        <div class="case-warning">
            ⚠ {case["warning"]}
        </div>

    </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# RIGHT : INVESTIGATION
# =========================================================

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-head">
            <div class="panel-head-left">INTERROGATION // 심문</div>
            <div class="panel-head-right">YES / NO ONLY</div>
        </div>
    """, unsafe_allow_html=True)

    progress = int((st.session_state.question_index / 15) * 100)

    st.markdown(f"""
    <div style="padding:10px 13px 0 13px;">
        <div style="display:flex;justify-content:space-between;">
            <span class="question-label">현재 질문</span>
            <span class="muted">{st.session_state.question_index}/15</span>
        </div>
        <div class="progress-wrap">
            <div class="progress-fill" style="width:{progress}%"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # 용의자 선택
    suspect_names = [x["name"] for x in case["suspects"]]

    selected = st.selectbox(
        "심문 대상",
        suspect_names,
        key=f"suspect_{st.session_state.case_index}"
    )

    suspect = next(
        x for x in case["suspects"]
        if x["name"] == selected
    )

    st.markdown(f"""
    <div class="suspect-card">
        <div class="suspect-name">{suspect["name"]}</div>
        <div class="suspect-role">{suspect["role"]}</div>
        <div class="suspect-info">
            {suspect["info"]}<br>
            <span class="yellow">의심점 · {suspect["suspicion"]}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


    # 현재 질문
    current_question = questions[q_index][0]

    st.markdown(f"""
    <div class="question-box">
        <div class="question-label">DETECTIVE QUESTION</div>
        <div class="question-text">
            "{current_question}"
        </div>
    </div>
    """, unsafe_allow_html=True)


    # 답변 버튼
    yes_col, no_col = st.columns(2)

    with yes_col:
        yes_clicked = st.button(
            "✓ 예",
            use_container_width=True,
            key=f"yes_{st.session_state.case_index}_{q_index}"
        )

    with no_col:
        no_clicked = st.button(
            "✕ 아니오",
            use_container_width=True,
            key=f"no_{st.session_state.case_index}_{q_index}"
        )


    # 답변 처리
    if yes_clicked or no_clicked:

        user_answer = yes_clicked

        answer_text = questions[q_index][1]

        clue_text = questions[q_index][2]

        is_clue = questions[q_index][3]

        st.session_state.answers.append({
            "question": current_question,
            "answer": "예" if user_answer else "아니오",
            "text": answer_text
        })

        if is_clue:
            st.session_state.clues += 1
            st.session_state.score += 10

        st.session_state.last_answer = {
            "answer": "예" if user_answer else "아니오",
            "text": answer_text,
            "clue": clue_text,
            "correct": user_answer == questions[q_index][3]
        }

        if st.session_state.question_index < 15:
            st.session_state.question_index += 1

        st.rerun()


    # 마지막 답변
    if st.session_state.last_answer:

        last = st.session_state.last_answer

        st.markdown(f"""
        <div class="answer-box">
            <b>답변</b><br>
            {last["text"]}
        </div>

        <div class="clue-box">
            🔎 <b>확보된 정보</b><br>
            {last["clue"]}
        </div>
        """, unsafe_allow_html=True)


    # 추리 버튼
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    if st.button(
        "🔍 범인 추리하기",
        type="primary",
        use_container_width=True
    ):
        st.session_state.finished_case = True


    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# BOTTOM / RESULT
# =========================================================

if st.session_state.finished_case:

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="final-box">
        <div class="question-label">FINAL DEDUCTION</div>
        <div style="font-size:18px;font-weight:900;margin-top:5px;">
            최종 범인을 선택하세요
        </div>
    </div>
    """, unsafe_allow_html=True)

    final_names = [x["name"] for x in case["suspects"]]

    choice_cols = st.columns(len(final_names))

    for i, name in enumerate(final_names):

        with choice_cols[i]:

            if st.button(
                f"🕵️ {name}",
                key=f"final_{st.session_state.case_index}_{i}",
                use_container_width=True
            ):

                if name == case["answer"]:

                    st.session_state.score += 100

                    st.session_state.final_result = "correct"

                else:

                    st.session_state.final_result = "wrong"

                st.rerun()


# =========================================================
# FINAL RESULT
# =========================================================

if st.session_state.final_result:

    if st.session_state.final_result == "correct":

        st.success(
            f"🎯 정답입니다! 범인은 {case['answer']}입니다."
        )

        st.markdown(f"""
        <div class="answer-box">
            <b>사건 해결</b><br><br>
            {case["solution"]}
        </div>
        """, unsafe_allow_html=True)

        if st.session_state.case_index < len(CASES) - 1:

            if st.button(
                "▶ 다음 사건으로",
                type="primary",
                use_container_width=True
            ):

                st.session_state.case_index += 1
                st.session_state.question_index = 0
                st.session_state.clues = 0
                st.session_state.answers = []
                st.session_state.last_answer = None
                st.session_state.finished_case = False
                st.session_state.final_result = None

                st.rerun()

        else:

            st.balloons()

            st.markdown("""
            <div class="final-box">
                <div style="font-size:25px;font-weight:900;">
                    🏆 모든 사건 해결
                </div>
                <div style="color:#7dd3fc;margin-top:5px;">
                    당신은 진실을 찾아냈습니다.
                </div>
            </div>
            """, unsafe_allow_html=True)

    else:

        st.error(
            f"❌ 오답입니다. {case['answer']}는 범인이 아닙니다."
        )

        st.markdown(f"""
        <div class="answer-box">
            <b>수사 실패</b><br><br>
            진짜 범인: <b>{case["answer"]}</b><br><br>
            {case["solution"]}
        </div>
        """, unsafe_allow_html=True)

        if st.button(
            "↻ 사건 다시 시작",
            use_container_width=True
        ):

            st.session_state.question_index = 0
            st.session_state.score = 0
            st.session_state.clues = 0
            st.session_state.answers = []
            st.session_state.last_answer = None
            st.session_state.finished_case = False
            st.session_state.final_result = None

            st.rerun()


# =========================================================
# RESET
# =========================================================

st.markdown("""
<div style="
position:fixed;
bottom:4px;
left:50%;
transform:translateX(-50%);
color:#40515e;
font-size:8px;
letter-spacing:2px;
">
YES NO DETECTIVE · CASE MANAGEMENT SYSTEM
</div>
""", unsafe_allow_html=True)
