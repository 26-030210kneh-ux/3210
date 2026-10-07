import streamlit as st
import time
import re

# =========================================================
# YES NO DETECTIVE
# 최종판
# =========================================================

st.set_page_config(
    page_title="예스노 탐정",
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

* {
    font-family: 'Noto Sans KR', sans-serif;
}

html, body {
    margin: 0;
    padding: 0;
    background: #060b10;
    color: #edf5fa;
}

body {
    overflow: hidden;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 80% 10%, rgba(0,150,210,.10), transparent 30%),
        radial-gradient(circle at 10% 80%, rgba(0,90,130,.08), transparent 30%),
        #060b10;
}

[data-testid="stHeader"] {
    background: transparent;
}

.block-container {
    max-width: 1500px;
    padding-top: 14px !important;
    padding-bottom: 8px !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* 제목 */

.game-title {
    font-size: 34px;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
    margin-bottom: 3px;
}

.game-subtitle {
    color: #51c9ff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 4px;
}

/* 상단 정보 */

.top-box {
    background: linear-gradient(145deg, #0d151d, #091018);
    border: 1px solid #243745;
    border-radius: 10px;
    padding: 10px 16px;
    min-height: 60px;
}

.top-label {
    color: #7190a4;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.top-number {
    color: #f4fbff;
    font-size: 21px;
    font-weight: 900;
    margin-top: 2px;
}

.top-small {
    color: #45c9ff;
    font-size: 9px;
    margin-top: -3px;
}

/* 카드 */

.panel {
    background: linear-gradient(145deg, #0d151d, #091018);
    border: 1px solid #233743;
    border-radius: 12px;
    overflow: hidden;
}

.panel-head {
    height: 42px;
    padding: 12px 16px;
    border-bottom: 1px solid #263945;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #dcecf4;
}

.panel-head span {
    color: #40caff;
}

/* 사건 화면 */

.scene {
    height: 420px;
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(180deg, rgba(0,0,0,.05), rgba(0,0,0,.70)),
        linear-gradient(135deg, #1b242b 0%, #0b1117 55%, #05080b 100%);
}

/* 창문 */

.window {
    position: absolute;
    left: 7%;
    top: 9%;
    width: 39%;
    height: 47%;
    background:
        linear-gradient(90deg, transparent 48%, rgba(110,145,160,.28) 49%, transparent 51%),
        linear-gradient(0deg, transparent 48%, rgba(110,145,160,.22) 49%, transparent 51%),
        linear-gradient(135deg, #172a36, #07131c);
    border: 5px solid #252e34;
    box-shadow: 0 0 35px rgba(0,150,210,.10);
}

.window:after {
    content: "";
    position: absolute;
    inset: 12px;
    background:
        radial-gradient(circle at 20% 70%, #61a5d8 0 1px, transparent 2px),
        radial-gradient(circle at 35% 55%, #73c2ef 0 1px, transparent 2px),
        radial-gradient(circle at 70% 45%, #60a7dc 0 1px, transparent 2px),
        radial-gradient(circle at 83% 73%, #70c8f5 0 1px, transparent 2px),
        linear-gradient(180deg, #071522, #102536);
    opacity: .75;
}

/* 침대 */

.bed {
    position: absolute;
    left: 15%;
    bottom: 12%;
    width: 57%;
    height: 25%;
    background: linear-gradient(180deg, #6d7378, #30383d);
    transform: skewX(-5deg);
    border-radius: 4px;
    box-shadow: 0 15px 30px rgba(0,0,0,.6);
}

.pillow {
    position: absolute;
    left: 22%;
    bottom: 30%;
    width: 22%;
    height: 11%;
    background: #aab0b3;
    border-radius: 20px;
    transform: rotate(-5deg);
}

.body {
    position: absolute;
    left: 35%;
    bottom: 24%;
    width: 27%;
    height: 13%;
    background: #555c61;
    border-radius: 50% 45% 40% 45%;
    transform: rotate(-7deg);
}

.head {
    position: absolute;
    left: 31%;
    bottom: 28%;
    width: 7%;
    height: 10%;
    background: #b88d74;
    border-radius: 50%;
    transform: rotate(-20deg);
}

.arm {
    position: absolute;
    left: 49%;
    bottom: 20%;
    width: 19%;
    height: 4%;
    background: #4b5155;
    border-radius: 20px;
    transform: rotate(18deg);
}

/* 문 */

.door {
    position: absolute;
    right: 7%;
    top: 8%;
    width: 20%;
    height: 75%;
    background: linear-gradient(90deg, #3d3027, #241b17);
    border: 6px solid #1b1613;
    box-shadow: 0 0 25px rgba(0,0,0,.5);
}

.door-handle {
    position: absolute;
    right: 11%;
    top: 51%;
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #b8a46c;
}

/* 바닥 */

.floor {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    height: 17%;
    background: repeating-linear-gradient(
        90deg,
        #10171c 0px,
        #10171c 100px,
        #172128 101px,
        #172128 102px
    );
}

/* 사건 라벨 */

.case-label {
    position: absolute;
    left: 18px;
    top: 16px;
    padding: 7px 12px;
    border: 1px solid #2f647d;
    color: #62d5ff;
    background: rgba(3,12,18,.75);
    font-size: 9px;
    font-weight: 800;
    letter-spacing: 2px;
    z-index: 5;
}

.scene-tag {
    position: absolute;
    left: 20px;
    bottom: 17px;
    z-index: 5;
    color: #fff;
    font-size: 10px;
    background: rgba(3,7,10,.75);
    border-left: 3px solid #38c9ff;
    padding: 8px 12px;
}

/* 사건 설명 */

.case-text {
    padding: 14px 17px;
    border-top: 1px solid #263945;
    background: #091118;
}

.case-title {
    font-size: 18px;
    font-weight: 900;
    line-height: 1.45;
    color: #f4f9fc;
}

.case-desc {
    color: #9db0bb;
    font-size: 11px;
    line-height: 1.65;
    margin-top: 7px;
}

.keyword {
    display: inline-block;
    color: #52caff;
    border: 1px solid #20526a;
    border-radius: 5px;
    padding: 2px 7px;
    margin-right: 4px;
    font-size: 9px;
}

/* 오른쪽 */

.interrogation {
    min-height: 585px;
}

/* 용의자 */

.suspect-box {
    background: #0a1118;
    border: 1px solid #263944;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 10px;
}

.suspect-name {
    font-size: 21px;
    font-weight: 900;
}

.suspect-role {
    color: #718895;
    font-size: 10px;
    margin-top: -2px;
}

.suspect-line {
    color: #b6c6ce;
    font-size: 11px;
    margin-top: 7px;
    line-height: 1.5;
}

.suspicion {
    margin-top: 8px;
    padding: 8px 10px;
    background: rgba(120,130,20,.13);
    border-left: 3px solid #9ba52c;
    color: #d4daaa;
    font-size: 10px;
}

/* 질문 */

.question-box {
    background: #081018;
    border: 1px solid #29404d;
    border-radius: 9px;
    padding: 13px;
    margin-top: 8px;
}

.question-label {
    color: #4fcaff;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 800;
}

.answer {
    margin-top: 12px;
    background: #0c1820;
    border: 1px solid #263f4b;
    border-radius: 8px;
    padding: 12px;
}

.answer-big {
    font-size: 24px;
    font-weight: 900;
    color: #ffffff;
}

.answer-text {
    color: #b9c9d1;
    font-size: 11px;
    line-height: 1.65;
    margin-top: 5px;
}

/* 단서 */

.clue {
    background: linear-gradient(90deg, rgba(26,84,106,.28), rgba(10,25,32,.4));
    border: 1px solid #28536a;
    border-radius: 7px;
    padding: 9px 11px;
    margin-top: 8px;
    color: #aee8ff;
    font-size: 10px;
    line-height: 1.5;
}

/* Streamlit input */

.stTextInput input {
    background: #071018 !important;
    color: #f2f8fb !important;
    border: 1px solid #2e4a59 !important;
    border-radius: 7px !important;
    height: 42px !important;
    font-size: 13px !important;
}

.stTextInput input:focus {
    border: 1px solid #35c8ff !important;
    box-shadow: 0 0 0 1px #35c8ff !important;
}

/* select */

.stSelectbox div[data-baseweb="select"] > div {
    background: #071018 !important;
    border-color: #2e4a59 !important;
    color: white !important;
    min-height: 42px !important;
}

/* 버튼 */

.stButton > button {
    width: 100%;
    min-height: 40px;
    background: #0d2634 !important;
    color: #eaf9ff !important;
    border: 1px solid #31647b !important;
    border-radius: 7px !important;
    font-weight: 800 !important;
    font-size: 11px !important;
}

.stButton > button:hover {
    background: #12394b !important;
    border-color: #43ccff !important;
    color: white !important;
}

/* 주요 버튼 */

.primary-button button {
    background: #168fc1 !important;
    border: 1px solid #53d7ff !important;
    color: white !important;
}

/* 진행바 */

.progress-track {
    width: 100%;
    height: 5px;
    background: #16242c;
    border-radius: 5px;
    overflow: hidden;
    margin: 8px 0;
}

.progress-fill {
    height: 100%;
    background: linear-gradient(90deg, #19a9df, #6ae2ff);
}

/* 알림 */

.notice {
    background: #0b1a25;
    border: 1px solid #23485d;
    border-radius: 8px;
    padding: 10px 12px;
    color: #bcd2dc;
    font-size: 10px;
    line-height: 1.6;
}

.success {
    border-color: #2c8064;
    background: #0b211b;
    color: #a9f0d5;
}

.danger {
    border-color: #824b4b;
    background: #210f12;
    color: #f2b7bd;
}

/* 모바일 */

@media (max-width: 900px) {

    body {
        overflow: auto;
    }

    .block-container {
        padding-left: 10px !important;
        padding-right: 10px !important;
    }

    .game-title {
        font-size: 26px;
    }

    .scene {
        height: 330px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# GAME DATA
# =========================================================

CASE = {
    "title": "잠긴 방의 진실",
    "number": "001",
    "round": "01 / 03",
    "time": "23:58",
    "location": "서울 마포구 / 아파트 1204호",
    "victim": "김도윤",
    "summary": (
        "밤 11시 58분, 김도윤이 자신의 방에서 쓰러진 채 발견됐다. "
        "현관은 잠겨 있었고 외부인의 침입 흔적도 없다."
    ),
    "story": (
        "경찰은 처음에 단순한 사고라고 판단했다. "
        "하지만 현장에는 이상한 점이 몇 가지 있었다. "
        "피해자의 휴대폰에는 마지막 통화 기록이 삭제되어 있었고, "
        "CCTV에는 사건 직전 누군가가 복도를 지나간 흔적이 남아 있었다."
    )
}

SUSPECTS = {
    "김민재": {
        "role": "피해자의 직장 동료",
        "line": "사건 당일 피해자와 마지막으로 통화한 사람.",
        "suspicion": "승진 문제로 피해자와 크게 다툰 적이 있다.",
        "truth": {
            "cctv": (True, "CCTV에 찍힌 사람은 나다. 하지만 피해자를 만나러 간 건 아니다."),
            "현관": (False, "나는 현관으로 들어가지 않았다."),
            "전화": (True, "그날 밤 피해자와 통화했다."),
            "마지막": (True, "내가 마지막 통화 상대인 건 맞다."),
            "다툼": (True, "회사에서 피해자와 말다툼을 했다."),
            "집": (False, "그날 피해자의 집에 들어간 적은 없다."),
            "방": (False, "피해자의 방에 들어간 적은 없다."),
            "열쇠": (False, "피해자의 집 열쇠는 가지고 있지 않다."),
            "문": (False, "현관문을 직접 연 적은 없다."),
            "시간": (True, "23시 40분쯤 회사에서 나왔다."),
            "알리바이": (True, "택시 기록이 남아 있다."),
            "휴대폰": (True, "통화가 끝난 뒤 바로 전화를 끊었다."),
        }
    },

    "박서연": {
        "role": "피해자의 전 여자친구",
        "line": "헤어진 뒤에도 피해자와 연락을 이어가고 있었다.",
        "suspicion": "사건 일주일 전 피해자에게 다시 만나자고 요구했다.",
        "truth": {
            "cctv": (False, "CCTV에 찍힌 사람은 내가 아니다."),
            "현관": (False, "현관 안으로 들어간 적이 없다."),
            "전화": (True, "그날 피해자에게 세 번 전화했다."),
            "마지막": (False, "마지막 통화 상대는 내가 아니다."),
            "다툼": (True, "며칠 전 피해자와 크게 다퉜다."),
            "집": (True, "그날 오후에는 피해자의 집에 있었다."),
            "방": (True, "피해자의 방에 들어간 적은 있다."),
            "열쇠": (True, "예전에 받은 비상용 열쇠가 하나 있었다."),
            "문": (True, "예전에는 그 열쇠로 문을 열어본 적이 있다."),
            "시간": (False, "23시 이후에는 집에 있었다."),
            "알리바이": (True, "친구와 영상통화를 하고 있었다."),
            "휴대폰": (False, "통화 기록을 삭제하지 않았다."),
        }
    },

    "최도현": {
        "role": "아파트 관리 직원",
        "line": "사건 당시 복도 CCTV를 관리하고 있었다.",
        "suspicion": "CCTV 기록 일부가 사건 직후 수정됐다.",
        "truth": {
            "cctv": (True, "CCTV 시스템을 관리할 수 있는 권한은 있다."),
            "현관": (True, "복도에 들어간 것은 맞다."),
            "전화": (False, "피해자와 직접 통화하지 않았다."),
            "마지막": (False, "마지막 통화 상대는 아니다."),
            "다툼": (False, "피해자와 다툰 적은 없다."),
            "집": (True, "사건 전에 점검 때문에 방문한 적이 있다."),
            "방": (False, "피해자의 방에는 들어가지 않았다."),
            "열쇠": (True, "관리용 마스터키를 가지고 있다."),
            "문": (True, "관리용 열쇠로 현관을 열 수 있다."),
            "시간": (True, "23시 45분쯤 복도 CCTV를 확인했다."),
            "알리바이": (False, "확실한 목격자는 없다."),
            "휴대폰": (False, "피해자의 휴대폰에는 손대지 않았다."),
        }
    },

    "한지우": {
        "role": "피해자의 이웃",
        "line": "사건 당일 밤 이상한 소리를 들었다고 주장한다.",
        "suspicion": "경찰에게 처음 말한 내용과 실제 기록이 다르다.",
        "truth": {
            "cctv": (False, "CCTV에 찍힌 사람은 내가 아니다."),
            "현관": (False, "피해자의 집에는 들어가지 않았다."),
            "전화": (False, "피해자에게 전화하지 않았다."),
            "마지막": (False, "마지막 통화 상대가 아니다."),
            "다툼": (False, "피해자와 다툰 적이 없다."),
            "집": (False, "피해자의 집에 방문한 적이 없다."),
            "방": (False, "방에 들어간 적이 없다."),
            "열쇠": (False, "열쇠가 없다."),
            "문": (False, "문을 열지 않았다."),
            "시간": (True, "23시 50분에 복도에서 소리를 들었다."),
            "알리바이": (True, "집에서 TV를 보고 있었다."),
            "휴대폰": (False, "휴대폰에는 손대지 않았다."),
        }
    }
}


# =========================================================
# SESSION
# =========================================================

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "trust" not in st.session_state:
    st.session_state.trust = 100

if "clues" not in st.session_state:
    st.session_state.clues = []

if "history" not in st.session_state:
    st.session_state.history = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "game_over" not in st.session_state:
    st.session_state.game_over = False


# =========================================================
# QUESTION ENGINE
# =========================================================

def classify_question(q):
    q = q.lower().replace(" ", "")

    keywords = {
        "cctv": ["cctv", "카메라", "영상", "찍혔", "녹화"],
        "현관": ["현관", "들어", "침입", "집에왔", "방문"],
        "전화": ["전화", "통화", "연락", "전화했"],
        "마지막": ["마지막", "최후", "마지막으로"],
        "다툼": ["싸움", "다툼", "싸웠", "갈등", "말다툼"],
        "집": ["집", "아파트", "1204"],
        "방": ["방", "침실", "피해자방"],
        "열쇠": ["열쇠", "키", "마스터키"],
        "문": ["문", "문을"],
        "시간": ["몇시", "시간", "언제", "시각", "밤"],
        "알리바이": ["알리바이", "증명", "어디있", "목격"],
        "휴대폰": ["휴대폰", "핸드폰", "폰", "스마트폰"],
    }

    for key, words in keywords.items():
        for word in words:
            if word in q:
                return key

    return None


def ask_question(suspect, question):

    key = classify_question(question)

    if key is None:
        return (
            "알 수 없음",
            "그 질문에는 명확한 예/아니오 답변을 할 수 없습니다. "
            "CCTV, 현관, 전화, 시간, 알리바이처럼 구체적으로 물어보세요.",
            False,
            None
        )

    yes, answer = SUSPECTS[suspect]["truth"].get(
        key,
        (False, "그 질문에 대해서는 할 말이 없다.")
    )

    return (
        "예" if yes else "아니오",
        answer,
        True,
        key
    )


# =========================================================
# HEADER
# =========================================================

head1, head2 = st.columns([2.8, 1.2])

with head1:
    st.markdown("""
    <div class="game-subtitle">CONFIDENTIAL · 34 CASE FILES</div>
    <div class="game-title">예스노 탐정</div>
    """, unsafe_allow_html=True)

with head2:
    st.markdown("""
    <div style="text-align:right; padding-top:7px; color:#617783; font-size:9px; letter-spacing:2px;">
    INVESTIGATION SYSTEM<br>
    <span style="color:#43caff; font-size:11px;">ONLINE</span>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# TOP STATS
# =========================================================

a, b, c, d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="top-box">
        <div class="top-label">질문</div>
        <div class="top-number">{st.session_state.questions}/15</div>
        <div class="top-small">QUESTION COUNT</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="top-box">
        <div class="top-label">수사 점수</div>
        <div class="top-number">{st.session_state.score}</div>
        <div class="top-small">INVESTIGATION SCORE</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="top-box">
        <div class="top-label">신뢰도</div>
        <div class="top-number">{st.session_state.trust}%</div>
        <div class="top-small">DETECTIVE TRUST</div>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="top-box">
        <div class="top-label">확보 단서</div>
        <div class="top-number">{len(st.session_state.clues)}</div>
        <div class="top-small">CLUES FOUND</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns([1.55, 1], gap="medium")


# =========================================================
# LEFT - CASE
# =========================================================

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-head">
            CASE FILE <span>//</span> 현장 기록
            <span style="float:right; font-size:8px;">CONFIDENTIAL · CASE 001</span>
        </div>

        <div class="scene">

            <div class="case-label">
                CASE #001 · EVIDENCE PHOTO
            </div>

            <div class="window"></div>

            <div class="door">
                <div class="door-handle"></div>
            </div>

            <div class="bed"></div>
            <div class="pillow"></div>
            <div class="body"></div>
            <div class="head"></div>
            <div class="arm"></div>

            <div class="floor"></div>

            <div class="scene-tag">
                23:58 · 침실 내부 · 외부 침입 흔적 없음
            </div>

        </div>

        <div class="case-text">

            <div class="case-title">
                한 남자가 자신의 방 안에서 쓰러진 채 발견됐다.
            </div>

            <div class="case-desc">
                현관문은 잠겨 있었고 창문도 안쪽에서 잠겨 있었다.
                그런데 사건 당일 밤, 누군가 피해자의 집 주변을 오갔다는 기록이 남아 있다.
                피해자의 휴대폰에서는 마지막 통화 기록 하나가 삭제되어 있다.
            </div>

            <div style="margin-top:8px;">
                <span class="keyword">CCTV</span>
                <span class="keyword">잠긴 현관</span>
                <span class="keyword">삭제된 통화</span>
                <span class="keyword">마지막 목격자</span>
            </div>

        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# RIGHT - INTERROGATION
# =========================================================

with right:

    st.markdown("""
    <div class="panel interrogation">
        <div class="panel-head">
            INTERROGATION <span>//</span> 심문
            <span style="float:right;">YES / NO ONLY</span>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div style="padding:10px 13px 0 13px;">
            <div style="display:flex; justify-content:space-between;">
                <span style="color:#47caff; font-size:10px; font-weight:800;">
                    현재 질문 {st.session_state.questions}/15
                </span>
                <span style="color:#667d88; font-size:9px;">
                    INVESTIGATION
                </span>
            </div>
            <div class="progress-track">
                <div class="progress-fill"
                     style="width:{min(100, st.session_state.questions / 15 * 100)}%;">
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 용의자 선택

    st.markdown(
        '<div style="padding:4px 13px 0 13px; color:#8197a3; font-size:10px;">심문 대상</div>',
        unsafe_allow_html=True
    )

    suspect = st.selectbox(
        "용의자",
        list(SUSPECTS.keys()),
        label_visibility="collapsed"
    )

    data = SUSPECTS[suspect]

    st.markdown(f"""
    <div class="suspect-box">

        <div class="suspect-name">
            {suspect}
        </div>

        <div class="suspect-role">
            {data["role"]}
        </div>

        <div class="suspect-line">
            {data["line"]}
        </div>

        <div class="suspicion">
            의심점 · {data["suspicion"]}
        </div>

    </div>
    """, unsafe_allow_html=True)

    # 질문

    st.markdown("""
    <div class="question-box">
        <div class="question-label">
            QUESTION // 예 또는 아니오로 답할 수 있게 물어보세요
        </div>
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "질문",
        placeholder="예: 사건 당일 피해자의 집에 들어갔습니까?",
        label_visibility="collapsed",
        key="question_input"
    )

    q1, q2 = st.columns([1, 1])

    with q1:
        ask = st.button("🔎 질문하기", use_container_width=True)

    with q2:
        clear = st.button("↻ 질문 초기화", use_container_width=True)

    if clear:
        st.session_state.question_input = ""
        st.rerun()

    # 빠른 질문

    st.markdown(
        '<div style="color:#687f8b; font-size:9px; margin-top:5px;">추천 질문</div>',
        unsafe_allow_html=True
    )

    r1, r2, r3, r4 = st.columns(4)

    quick_questions = [
        "CCTV에 찍혔습니까?",
        "피해자에게 전화했습니까?",
        "현관으로 들어갔습니까?",
        "알리바이가 있습니까?"
    ]

    for col, q in zip([r1, r2, r3, r4], quick_questions):
        with col:
            if st.button(q, key="quick_" + q, use_container_width=True):
                result = ask_question(suspect, q)

                if st.session_state.questions < 15:
                    st.session_state.questions += 1

                ans, txt, valid, key = result

                st.session_state.last_answer = {
                    "suspect": suspect,
                    "answer": ans,
                    "text": txt,
                    "key": key
                }

                st.session_state.history.append(
                    (suspect, q, ans)
                )

                if valid:
                    st.session_state.score += 5

                st.rerun()

    # 실제 질문 처리

    if ask and question.strip():

        if st.session_state.questions >= 15:
            st.session_state.trust = max(
                0,
                st.session_state.trust - 5
            )
        else:

            ans, txt, valid, key = ask_question(
                suspect,
                question
            )

            st.session_state.questions += 1

            st.session_state.last_answer = {
                "suspect": suspect,
                "answer": ans,
                "text": txt,
                "key": key
            }

            st.session_state.history.append(
                (suspect, question, ans)
            )

            if valid:

                st.session_state.score += 5

                # 중요한 단서

                important = {
                    ("최도현", "cctv"),
                    ("최도현", "열쇠"),
                    ("최도현", "문"),
                    ("박서연", "열쇠"),
                    ("박서연", "집"),
                    ("김민재", "마지막"),
                    ("김민재", "전화")
                }

                if (suspect, key) in important:

                    clue = f"{suspect}의 진술에서 이상한 점을 발견했다."

                    if clue not in st.session_state.clues:
                        st.session_state.clues.append(clue)
                        st.session_state.score += 10

            else:
                st.session_state.trust = max(
                    0,
                    st.session_state.trust - 2
                )

            st.rerun()

    # 답변

    if st.session_state.last_answer:

        la = st.session_state.last_answer

        st.markdown(f"""
        <div class="answer">

            <div style="font-size:9px; color:#6d8490; letter-spacing:2px;">
                {la["suspect"]}의 답변
            </div>

            <div class="answer-big">
                {la["answer"]}
            </div>

            <div class="answer-text">
                {la["text"]}
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="notice">
            아직 질문한 내용이 없습니다.<br>
            용의자에게 질문해서 서로 다른 진술을 찾아내세요.
        </div>
        """, unsafe_allow_html=True)

    # 단서

    if st.session_state.clues:

        st.markdown(
            '<div style="margin-top:8px; color:#56ccf2; font-size:9px; letter-spacing:2px;">EVIDENCE FOUND</div>',
            unsafe_allow_html=True
        )

        for clue in st.session_state.clues[-3:]:
            st.markdown(
                f'<div class="clue">◆ {clue}</div>',
                unsafe_allow_html=True
            )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# BOTTOM INVESTIGATION
# =========================================================

st.write("")

b1, b2, b3 = st.columns([1.1, 1.1, 1.8])

with b1:

    if st.button(
        "📁 확보한 단서 보기",
        use_container_width=True
    ):

        if not st.session_state.clues:
            st.info("아직 확보한 단서가 없습니다.")
        else:
            for i, clue in enumerate(st.session_state.clues, 1):
                st.write(f"**단서 {i}** — {clue}")


with b2:

    if st.button(
        "🧹 수사 기록 초기화",
        use_container_width=True
    ):

        st.session_state.questions = 0
        st.session_state.score = 0
        st.session_state.trust = 100
        st.session_state.clues = []
        st.session_state.history = []
        st.session_state.last_answer = None
        st.rerun()


with b3:

    if st.button(
        "🧠 최종 추리 제출",
        use_container_width=True
    ):

        if st.session_state.questions < 5:

            st.warning(
                "단서가 너무 부족합니다. 최소 5번 이상 질문해보세요."
            )

        else:

            st.session_state.game_over = True

            st.markdown("""
            <div class="notice success">

            <b>FINAL INVESTIGATION</b><br><br>

            수사가 종료되었습니다.<br>
            확보한 단서와 용의자들의 진술을 비교하세요.

            <br><br>

            가장 중요한 것은 단순히 거짓말을 찾는 것이 아닙니다.<br>
            <b>서로 다른 진술이 어디에서 충돌하는지</b> 확인해야 합니다.

            </div>
            """, unsafe_allow_html=True)


# =========================================================
# HISTORY
# =========================================================

if st.session_state.history:

    st.markdown("""
    <div style="
        margin-top:8px;
        padding:9px 12px;
        border:1px solid #1c303b;
        background:#081017;
        border-radius:8px;
        color:#728995;
        font-size:9px;
    ">
    <b style="color:#9cb0ba;">최근 수사 기록</b>
    """, unsafe_allow_html=True)

    recent = st.session_state.history[-3:]

    for suspect_name, q, answer in recent:

        safe_q = q[:70]

        st.markdown(
            f"""
            <div style="margin-top:5px;">
            <span style="color:#42caff;">{suspect_name}</span>
            · {safe_q}
            · <b style="color:#fff;">{answer}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
    text-align:center;
    color:#334954;
    font-size:8px;
    letter-spacing:3px;
    margin-top:8px;
">
YES NO DETECTIVE · CASE SYSTEM v1.0 · CONFIDENTIAL
</div>
""", unsafe_allow_html=True)
