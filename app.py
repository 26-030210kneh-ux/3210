import streamlit as st
import random
import time

# =========================================================
# YES / NO DETECTIVE
# One-screen detective game
# =========================================================

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
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
    font-family: 'Noto Sans KR', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 70% 15%, rgba(0, 120, 180, .10), transparent 35%),
        radial-gradient(circle at 15% 80%, rgba(0, 70, 120, .08), transparent 30%),
        #070b10;
    color: #eaf3f8;
}

/* Streamlit 기본 요소 숨기기 */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent !important;
}

/* 전체 폭 */
.block-container {
    max-width: 1500px !important;
    padding-top: 0.4rem !important;
    padding-bottom: 0.2rem !important;
}

/* 스크롤 최소화 */
section.main > div {
    padding-bottom: 0 !important;
}

/* 제목 */
.game-title {
    font-size: 28px;
    font-weight: 900;
    letter-spacing: -1px;
    color: #f4f8fb;
}

.top-sub {
    color: #62cfff;
    font-size: 11px;
    letter-spacing: 4px;
    font-weight: 700;
}

.case-id {
    color: #71818c;
    font-size: 11px;
    letter-spacing: 2px;
}

/* 상단 상태 */
.status-box {
    height: 72px;
    background: rgba(14, 23, 31, .92);
    border: 1px solid #263743;
    border-radius: 9px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: 0 18px;
}

.status-label {
    color: #71838f;
    font-size: 10px;
    letter-spacing: 2px;
    margin-bottom: 3px;
}

.status-value {
    color: #edf7fc;
    font-size: 22px;
    font-weight: 800;
}

.status-small {
    color: #5bcaff;
    font-size: 10px;
}

/* 메인 패널 */
.panel {
    background: rgba(10, 16, 22, .95);
    border: 1px solid #263743;
    border-radius: 10px;
    overflow: hidden;
}

.panel-header {
    height: 45px;
    border-bottom: 1px solid #24323d;
    display: flex;
    align-items: center;
    padding: 0 17px;
    background: rgba(17, 27, 35, .85);
}

.panel-title {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #b9d5e2;
}

.panel-code {
    margin-left: auto;
    color: #4f6977;
    font-size: 9px;
    letter-spacing: 2px;
}

/* 사건 이미지 */
.scene {
    height: 330px;
    position: relative;
    overflow: hidden;
    background:
        linear-gradient(
            90deg,
            rgba(3, 8, 13, .30),
            rgba(3, 8, 13, .02)
        ),
        linear-gradient(
            180deg,
            rgba(0,0,0,.05),
            rgba(0,0,0,.78)
        ),
        url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1600&q=90");
    background-size: cover;
    background-position: center;
}

.scene:after {
    content: "";
    position: absolute;
    inset: 0;
    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,.20),
            transparent 50%,
            rgba(0,0,0,.35)
        );
    pointer-events: none;
}

.confidential {
    position: absolute;
    left: 18px;
    top: 16px;
    z-index: 2;
    padding: 7px 13px;
    border: 1px solid #2c6c8a;
    background: rgba(5, 17, 25, .85);
    color: #61cfff;
    font-size: 9px;
    letter-spacing: 3px;
}

.scene-label {
    position: absolute;
    left: 20px;
    bottom: 18px;
    z-index: 2;
}

.scene-title {
    font-size: 25px;
    font-weight: 900;
    color: white;
}

.scene-desc {
    margin-top: 5px;
    font-size: 11px;
    color: #b7c6ce;
}

/* 사건 설명 */
.case-story {
    min-height: 115px;
    padding: 17px 20px;
    border-top: 1px solid #24323d;
    background: #0a1117;
}

.case-tag {
    color: #51c8ff;
    font-size: 10px;
    letter-spacing: 2px;
    font-weight: 800;
}

.case-story-title {
    font-size: 19px;
    font-weight: 800;
    margin-top: 5px;
    color: #f2f7fa;
}

.case-story-text {
    color: #b5c2c9;
    font-size: 12px;
    line-height: 1.7;
    margin-top: 7px;
}

/* 오른쪽 질문 */
.interrogation {
    padding: 15px;
}

.question-count {
    color: #61cfff;
    font-size: 12px;
}

.progress-track {
    width: 100%;
    height: 4px;
    background: #17242d;
    border-radius: 4px;
    margin: 8px 0 15px;
}

.progress-fill {
    height: 4px;
    border-radius: 4px;
    background: #39bff5;
}

/* 용의자 카드 */
.suspect {
    border: 1px solid #253640;
    background: #0b1218;
    border-radius: 7px;
    padding: 11px;
    margin-bottom: 8px;
}

.suspect.active {
    border-color: #36b9ee;
    box-shadow: 0 0 15px rgba(35, 180, 235, .08);
}

.suspect-name {
    font-size: 14px;
    font-weight: 800;
    color: #edf7fa;
}

.suspect-role {
    color: #61747f;
    font-size: 9px;
    margin-top: 2px;
}

.suspect-line {
    color: #aebcc4;
    font-size: 10px;
    line-height: 1.5;
    margin-top: 7px;
}

/* 답변 박스 */
.answer {
    border-left: 3px solid #35c0f5;
    background: #0b1a24;
    padding: 12px 14px;
    border-radius: 4px;
    margin-top: 10px;
}

.answer-label {
    color: #51caff;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 800;
}

.answer-text {
    color: #e5edf1;
    font-size: 13px;
    line-height: 1.65;
    margin-top: 4px;
}

/* 단서 */
.clue {
    background: #111a12;
    border: 1px solid #344c31;
    border-radius: 6px;
    padding: 10px;
    margin-top: 7px;
}

.clue-title {
    color: #9bcf73;
    font-size: 10px;
    font-weight: 800;
}

.clue-text {
    color: #c2d0c0;
    font-size: 10px;
    line-height: 1.5;
    margin-top: 3px;
}

/* 하단 */
.bottom-note {
    color: #4f636f;
    font-size: 9px;
    letter-spacing: 1px;
    text-align: center;
    padding-top: 6px;
}

/* Streamlit 버튼 */
.stButton > button {
    width: 100% !important;
    min-height: 42px !important;
    border-radius: 6px !important;
    border: 1px solid #2d5368 !important;
    background: #102330 !important;
    color: #d9f3ff !important;
    font-weight: 700 !important;
    font-size: 12px !important;
    transition: .15s !important;
}

.stButton > button:hover {
    border-color: #43caff !important;
    background: #15384b !important;
    color: white !important;
}

button[kind="primary"] {
    background: #0879aa !important;
    border-color: #39c7ff !important;
    color: white !important;
}

/* 입력 */
.stTextInput input {
    background: #081118 !important;
    color: #eaf7fb !important;
    border: 1px solid #294655 !important;
    border-radius: 6px !important;
    min-height: 43px !important;
}

.stTextInput input:focus {
    border-color: #3cc8ff !important;
    box-shadow: 0 0 0 1px #3cc8ff !important;
}

/* 라디오 */
div[role="radiogroup"] {
    gap: 5px !important;
}

div[role="radiogroup"] label {
    background: #0c161d !important;
    border: 1px solid #263d4a !important;
    border-radius: 5px !important;
    padding: 8px 12px !important;
}

/* 탭 */
button[data-baseweb="tab"] {
    color: #718894 !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #5ecbff !important;
}

/* 알림 */
div[data-testid="stAlert"] {
    background: #0b1720 !important;
    border: 1px solid #254554 !important;
}

/* 모바일 */
@media(max-width: 900px) {
    .scene {
        height: 260px;
    }

    .game-title {
        font-size: 23px;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# DATA
# =========================================================

SUSPECTS = {
    "김민재": {
        "role": "피해자의 직장 동료",
        "description": "사건 당일 피해자와 마지막으로 통화한 사람.",
        "secret": "승진 문제로 피해자와 크게 다퉜다.",
    },
    "박서연": {
        "role": "피해자의 전 여자친구",
        "description": "헤어진 뒤에도 피해자와 연락을 이어갔다.",
        "secret": "사건 당일 밤 피해자에게 세 번 전화했다.",
    },
    "최도윤": {
        "role": "건물 관리인",
        "description": "사건 현장의 출입기록과 CCTV를 관리한다.",
        "secret": "CCTV 일부가 23:40부터 18분간 저장되지 않았다.",
    },
    "한유진": {
        "role": "피해자의 동생",
        "description": "피해자와 가장 가까운 가족.",
        "secret": "사건 전날 피해자와 돈 문제로 다퉜다.",
    },
}


# 질문에 대한 YES / NO 데이터
QUESTIONS = {

    "현관문": {
        "answer": "아니오",
        "text": "현관문에는 강제로 들어온 흔적이 없습니다.",
        "clue": "범인은 피해자가 직접 문을 열어줬을 가능성이 있습니다.",
        "points": 5,
    },

    "문": {
        "answer": "아니오",
        "text": "현관문에는 강제로 들어온 흔적이 없습니다.",
        "clue": "외부 침입 가능성이 낮습니다.",
        "points": 5,
    },

    "cctv": {
        "answer": "예",
        "text": "CCTV는 사건 당일 밤 11시 40분부터 약 18분간 기록이 비어 있습니다.",
        "clue": "누군가 CCTV의 공백을 이용했을 가능성이 있습니다.",
        "points": 10,
    },

    "카메라": {
        "answer": "예",
        "text": "CCTV 기록에는 이상한 공백이 존재합니다.",
        "clue": "사건 시간대에 기록이 사라졌습니다.",
        "points": 10,
    },

    "전화": {
        "answer": "예",
        "text": "피해자는 사망 직전 누군가에게 전화를 걸었습니다.",
        "clue": "마지막 통화가 사건의 핵심 단서입니다.",
        "points": 8,
    },

    "통화": {
        "answer": "예",
        "text": "사건 직전 피해자의 휴대전화에서 마지막 통화 기록이 발견되었습니다.",
        "clue": "마지막 통화 상대를 확인해야 합니다.",
        "points": 8,
    },

    "지문": {
        "answer": "예",
        "text": "현장에는 용의자 중 한 명의 지문이 발견되었습니다.",
        "clue": "지문은 사건 당일 이전에 남겨졌을 수도 있습니다.",
        "points": 7,
    },

    "혈흔": {
        "answer": "아니오",
        "text": "현장에서 대량의 혈흔은 발견되지 않았습니다.",
        "clue": "사망 원인은 일반적인 흉기 사건과 다릅니다.",
        "points": 6,
    },

    "무기": {
        "answer": "아니오",
        "text": "현장에서는 명확한 살해 도구가 발견되지 않았습니다.",
        "clue": "범행 도구가 현장에서 제거됐을 가능성이 있습니다.",
        "points": 7,
    },

    "술": {
        "answer": "예",
        "text": "피해자의 혈액에서 소량의 알코올 성분이 확인됐습니다.",
        "clue": "누군가와 술을 마시고 있었을 가능성이 있습니다.",
        "points": 4,
    },

    "싸움": {
        "answer": "예",
        "text": "피해자는 사건 전날 누군가와 심하게 다툰 기록이 있습니다.",
        "clue": "피해자의 주변 관계를 조사해야 합니다.",
        "points": 5,
    },

    "돈": {
        "answer": "예",
        "text": "피해자는 최근 큰 금액의 돈을 누군가에게 요구받았습니다.",
        "clue": "금전 문제가 범행 동기일 수 있습니다.",
        "points": 8,
    },

    "열쇠": {
        "answer": "예",
        "text": "현관 열쇠는 피해자의 집 안에서 발견되었습니다.",
        "clue": "범인이 열쇠를 가지고 들어온 것이 아닐 가능성이 큽니다.",
        "points": 8,
    },

    "창문": {
        "answer": "아니오",
        "text": "창문에는 외부에서 침입한 흔적이 없습니다.",
        "clue": "창문을 통한 침입은 배제됩니다.",
        "points": 5,
    },

    "도망": {
        "answer": "예",
        "text": "사건 이후 한 명의 용의자가 평소보다 빠르게 현장을 떠났습니다.",
        "clue": "이동 기록을 비교해야 합니다.",
        "points": 8,
    },

    "거짓말": {
        "answer": "예",
        "text": "현재까지 확보된 진술 중 최소 한 개는 사실과 일치하지 않습니다.",
        "clue": "진술의 시간대를 비교하십시오.",
        "points": 12,
    },

    "범인": {
        "answer": "아니오",
        "text": "그 질문에는 직접 답할 수 없습니다. 직접 단서를 조합해야 합니다.",
        "clue": "질문보다 모순을 찾는 것이 중요합니다.",
        "points": 1,
    },

    "살해": {
        "answer": "예",
        "text": "경찰은 이 사건을 타살 가능성이 높은 사건으로 보고 있습니다.",
        "clue": "단순 사고가 아닐 가능성이 높습니다.",
        "points": 5,
    },

    "혼자": {
        "answer": "아니오",
        "text": "피해자가 사건 직전 혼자 있었다고 단정할 수 없습니다.",
        "clue": "다른 사람이 현장에 있었을 가능성이 있습니다.",
        "points": 5,
    },
}


# 용의자별 특수 질문
SUSPECT_ANSWERS = {

    "김민재": {
        "cctv": ("아니오", "나는 CCTV를 관리하지 않습니다."),
        "전화": ("예", "마지막 통화는 내가 맞습니다. 하지만 1분도 안 되는 짧은 통화였습니다."),
        "싸움": ("예", "승진 문제로 다툰 건 맞지만 그게 살인 이유는 아닙니다."),
        "돈": ("아니오", "피해자에게 돈을 빌린 적은 없습니다."),
        "현관": ("아니오", "나는 그날 집에 들어간 적이 없습니다."),
        "도망": ("예", "회사에 급한 일이 있어서 먼저 떠났습니다."),
    },

    "박서연": {
        "cctv": ("아니오", "CCTV가 끊겼다는 건 지금 처음 들었습니다."),
        "전화": ("예", "전화한 건 맞지만 받지 않았습니다."),
        "싸움": ("예", "헤어진 뒤에도 서로 감정이 남아 있었습니다."),
        "돈": ("아니오", "돈 때문에 싸운 적은 없습니다."),
        "현관": ("아니오", "그날 그 집에 가지 않았습니다."),
        "도망": ("아니오", "나는 현장을 떠난 적이 없습니다."),
    },

    "최도윤": {
        "cctv": ("예", "CCTV에 문제가 있었던 건 사실입니다."),
        "전화": ("아니오", "피해자와 직접 통화한 적은 없습니다."),
        "싸움": ("아니오", "나는 피해자와 개인적인 관계가 없습니다."),
        "돈": ("아니오", "돈 문제도 없습니다."),
        "현관": ("예", "관리인이라 건물에 들어갈 수 있습니다."),
        "도망": ("아니오", "나는 근무를 마치고 정상적으로 퇴근했습니다."),
    },

    "한유진": {
        "cctv": ("아니오", "나는 CCTV에 접근할 수 없습니다."),
        "전화": ("예", "사건 전에 형에게 전화했습니다."),
        "싸움": ("예", "돈 문제 때문에 말다툼했습니다."),
        "돈": ("예", "형에게 돈을 빌려달라고 했습니다."),
        "현관": ("예", "가족이라 비밀번호를 알고 있습니다."),
        "도망": ("아니오", "나는 현장에 가지 않았습니다."),
    },
}


# =========================================================
# SESSION
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = True

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "clues" not in st.session_state:
    st.session_state.clues = []

if "history" not in st.session_state:
    st.session_state.history = []

if "current_suspect" not in st.session_state:
    st.session_state.current_suspect = "김민재"

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "game_finished" not in st.session_state:
    st.session_state.game_finished = False


# =========================================================
# TOP BAR
# =========================================================

top1, top2, top3 = st.columns([4, 1, 1])

with top1:
    st.markdown("""
    <div class="top-sub">CONFIDENTIAL • 34 CASE FILES</div>
    <div class="game-title">예스노 탐정</div>
    """, unsafe_allow_html=True)

with top2:
    st.markdown("""
    <div class="status-box">
        <div class="status-label">CASE</div>
        <div class="status-value">001</div>
        <div class="status-small">잠긴 방의 진실</div>
    </div>
    """, unsafe_allow_html=True)

with top3:
    st.markdown("""
    <div class="status-box">
        <div class="status-label">ROUND</div>
        <div class="status-value">01 / 03</div>
        <div class="status-small">INVESTIGATION</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# =========================================================
# SCORE BAR
# =========================================================

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">질문</div>
        <div class="status-value">{st.session_state.questions}/15</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">수사 점수</div>
        <div class="status-value">{st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)

with s3:
    trust = max(0, 100 - max(0, st.session_state.questions - 10) * 5)
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">신뢰도</div>
        <div class="status-value">{trust}%</div>
    </div>
    """, unsafe_allow_html=True)

with s4:
    st.markdown(f"""
    <div class="status-box">
        <div class="status-label">확보 단서</div>
        <div class="status-value">{len(st.session_state.clues)}</div>
    </div>
    """, unsafe_allow_html=True)


st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)


# =========================================================
# MAIN SCREEN
# =========================================================

left, right = st.columns([1.55, 1], gap="small")


# =========================================================
# LEFT — CASE
# =========================================================

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">CASE FILE // 현장 기록</div>
            <div class="panel-code">CONFIDENTIAL • CASE 001</div>
        </div>

        <div class="scene">

            <div class="confidential">
                CASE #001 • EVIDENCE PHOTO
            </div>

            <div class="scene-label">
                <div class="scene-title">잠긴 방의 진실</div>
                <div class="scene-desc">
                    서울 • 23:58 • 외부 침입 흔적 없음
                </div>
            </div>

        </div>

        <div class="case-story">

            <div class="case-tag">CASE BRIEFING</div>

            <div class="case-story-title">
                한 남자가 자신의 방 안에서 쓰러진 채 발견됐다.
            </div>

            <div class="case-story-text">
                현관은 잠겨 있었고 창문에는 침입 흔적이 없었다.
                그런데 사건 당일 밤, 건물 CCTV에는
                <b style="color:#66d3ff;">18분의 공백</b>이 존재한다.
                <br>
                현장에 있었던 사람들은 서로 다른 이야기를 하고 있다.
                당신은 질문 하나씩으로 거짓말을 찾아야 한다.
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # 사건 핵심 단서
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="clue">
            <div class="clue-title">EVIDENCE 01</div>
            <div class="clue-text">
                현관 강제침입 흔적 없음
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="clue">
            <div class="clue-title">EVIDENCE 02</div>
            <div class="clue-text">
                CCTV 18분 기록 공백
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="clue">
            <div class="clue-title">EVIDENCE 03</div>
            <div class="clue-text">
                마지막 통화 기록 존재
            </div>
        </div>
        """, unsafe_allow_html=True)

    # 확보 단서
    if st.session_state.clues:

        st.markdown("""
        <div style="
            margin-top:8px;
            color:#5bcaff;
            font-size:10px;
            letter-spacing:2px;
            font-weight:800;
        ">
        RECOVERED CLUES
        </div>
        """, unsafe_allow_html=True)

        recent = st.session_state.clues[-3:]

        for clue in recent:
            st.markdown(
                f"""
                <div class="clue">
                    <div class="clue-title">+ 단서 확보</div>
                    <div class="clue-text">{clue}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# RIGHT — INTERROGATION
# =========================================================

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-header">
            <div class="panel-title">INTERROGATION // 심문</div>
            <div class="panel-code">YES / NO ONLY</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="interrogation">
    """, unsafe_allow_html=True)

    # 진행률
    progress = min(100, int(st.session_state.questions / 15 * 100))

    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;">
        <div class="question-count">
            현재 질문 {st.session_state.questions} / 15
        </div>
        <div style="color:#667984;font-size:10px;">
            YES / NO
        </div>
    </div>

    <div class="progress-track">
        <div class="progress-fill" style="width:{progress}%"></div>
    </div>
    """, unsafe_allow_html=True)


    # 용의자 선택
    st.markdown("""
    <div style="
        color:#8195a0;
        font-size:10px;
        letter-spacing:1px;
        margin-bottom:5px;
    ">
    심문 대상
    </div>
    """, unsafe_allow_html=True)

    suspect_names = list(SUSPECTS.keys())

    selected = st.selectbox(
        "심문 대상",
        suspect_names,
        index=suspect_names.index(st.session_state.current_suspect),
        label_visibility="collapsed"
    )

    st.session_state.current_suspect = selected

    suspect = SUSPECTS[selected]

    st.markdown(f"""
    <div class="suspect active">

        <div class="suspect-name">
            {selected}
        </div>

        <div class="suspect-role">
            {suspect["role"]}
        </div>

        <div class="suspect-line">
            {suspect["description"]}
        </div>

        <div style="
            margin-top:7px;
            color:#8ea4ae;
            font-size:9px;
        ">
            의심점: {suspect["secret"]}
        </div>

    </div>
    """, unsafe_allow_html=True)


    # 질문 입력
    question = st.text_input(
        "질문",
        placeholder="예: CCTV를 본 적이 있습니까?",
        label_visibility="collapsed"
    )


    # 질문 처리
    ask = st.button(
        "🔎  질문하기",
        type="primary",
        use_container_width=True
    )


    if ask:

        if not question.strip():

            st.warning("질문을 입력해주세요.")

        elif st.session_state.questions >= 15:

            st.error("질문 횟수를 모두 사용했습니다.")

        else:

            q = question.lower().strip()

            found_key = None

            for key in QUESTIONS.keys():
                if key in q:
                    found_key = key
                    break

            if found_key is None:

                # 모르는 질문도 게임처럼 처리
                generic = [
                    (
                        "아니오",
                        "현재 확보된 증거로는 그 사실을 확인할 수 없습니다.",
                        "이 질문만으로는 새로운 단서를 얻지 못했습니다.",
                        1
                    ),
                    (
                        "예",
                        "그럴 가능성은 있습니다. 하지만 결정적인 증거는 아닙니다.",
                        "다른 증거와 비교해볼 필요가 있습니다.",
                        2
                    ),
                    (
                        "아니오",
                        "그 부분은 현재 사건 기록과 일치하지 않습니다.",
                        "다른 시간대의 진술을 확인해보십시오.",
                        2
                    ),
                ]

                answer, text, clue, points = random.choice(generic)

            else:

                answer, text, clue, points = QUESTIONS[found_key]

                # 특정 용의자에 대한 답변이 존재하면 적용
                if (
                    selected in SUSPECT_ANSWERS
                    and found_key in SUSPECT_ANSWERS[selected]
                ):
                    answer, text = SUSPECT_ANSWERS[selected][found_key]

            st.session_state.questions += 1
            st.session_state.score += points

            st.session_state.last_answer = answer
            st.session_state.last_question = question

            if clue not in st.session_state.clues:
                st.session_state.clues.append(clue)

            st.session_state.history.append({
                "suspect": selected,
                "question": question,
                "answer": answer,
                "clue": clue,
            })

            st.rerun()


    # 답변
    if st.session_state.last_answer:

        st.markdown(f"""
        <div class="answer">

            <div class="answer-label">
                {st.session_state.current_suspect}의 답변
            </div>

            <div class="answer-text">
                <b style="color:#58ccff;">
                    {st.session_state.last_answer}
                </b>
                · {text if 'text' in locals() else ''}
            </div>

        </div>
        """, unsafe_allow_html=True)


    st.markdown("</div></div>", unsafe_allow_html=True)


# =========================================================
# BOTTOM AREA
# =========================================================

st.markdown("<div style='height:7px'></div>", unsafe_allow_html=True)

b1, b2, b3 = st.columns([1, 1, 1])

with b1:

    if st.button(
        "📋 수사 기록 보기",
        use_container_width=True
    ):

        if not st.session_state.history:
            st.info("아직 질문한 기록이 없습니다.")
        else:
            for h in st.session_state.history[-5:]:
                st.markdown(
                    f"""
                    <div class="clue">
                        <div class="clue-title">
                            {h["suspect"]} · {h["answer"]}
                        </div>
                        <div class="clue-text">
                            Q. {h["question"]}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


with b2:

    if st.button(
        "🧠 최종 추리하기",
        use_container_width=True
    ):

        if len(st.session_state.clues) < 3:

            st.warning(
                "아직 단서가 부족합니다. 최소 3개의 단서를 확보하세요."
            )

        else:

            st.session_state.game_finished = True


with b3:

    if st.button(
        "↻ 사건 초기화",
        use_container_width=True
    ):

        st.session_state.questions = 0
        st.session_state.score = 0
        st.session_state.clues = []
        st.session_state.history = []
        st.session_state.last_answer = None
        st.session_state.last_question = ""
        st.session_state.current_suspect = "김민재"
        st.session_state.game_finished = False

        st.rerun()


# =========================================================
# FINAL DEDUCTION
# =========================================================

if st.session_state.game_finished:

    st.markdown("""
    <div class="panel" style="margin-top:8px;">

        <div class="panel-header">
            <div class="panel-title">
                FINAL DEDUCTION // 최종 추리
            </div>
        </div>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        "### 🔎 범인은 누구라고 생각합니까?"
    )

    final_suspect = st.radio(
        "범인",
        list(SUSPECTS.keys()),
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown(
        "### 당신의 최종 판단"
    )

    final_reason = st.text_input(
        "최종 판단",
        placeholder="범인과 그렇게 판단한 이유를 적어주세요.",
        label_visibility="collapsed"
    )

    if st.button(
        "🚨 최종 판결",
        type="primary",
        use_container_width=True
    ):

        # 정답을 하나로 고정하지 않고
        # 여러 단서 조합을 기반으로 판단

        score = st.session_state.score
        clue_count = len(st.session_state.clues)

        # 기본 정답
        correct = "최도윤"

        if final_suspect == correct:

            st.success("TRUE ENDING")

            st.markdown(f"""
            <div class="panel" style="
                padding:30px;
                margin-top:15px;
                text-align:center;
                border-color:#2f9fc8;
            ">

                <div style="
                    color:#5ed0ff;
                    font-size:11px;
                    letter-spacing:4px;
                ">
                    CASE CLOSED
                </div>

                <div style="
                    font-size:36px;
                    font-weight:900;
                    margin-top:10px;
                    color:white;
                ">
                    당신이 사건을 해결했다.
                </div>

                <div style="
                    color:#aabcc5;
                    margin-top:10px;
                    line-height:1.8;
                ">
                    CCTV의 공백과 출입 기록,
                    그리고 서로 맞지 않는 진술을 조합한 결과
                    최도윤의 진술이 사건 기록과 충돌한다.
                </div>

                <div style="
                    margin-top:20px;
                    color:#60cdfc;
                    font-size:13px;
                ">
                    수사 점수 {score} · 확보 단서 {clue_count}
                </div>

            </div>
            """, unsafe_allow_html=True)

        elif final_suspect == "김민재":

            st.warning("PARTIAL ENDING")

            st.markdown("""
            <div class="answer">
                <div class="answer-label">부분적으로 맞았다.</div>
                <div class="answer-text">
                    김민재는 중요한 거짓말을 하고 있었지만
                    사건의 핵심은 CCTV 기록에 있었다.
                    한 사람만 의심해서는 진실에 도달할 수 없다.
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.error("BAD ENDING")

            st.markdown("""
            <div class="answer">
                <div class="answer-label">수사 실패</div>
                <div class="answer-text">
                    당신은 가장 눈에 띄는 사람을 범인으로 지목했다.
                    하지만 탐정에게 필요한 것은 의심이 아니라
                    서로 맞지 않는 사실을 찾아내는 것이다.
                </div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="bottom-note">
    YES / NO DETECTIVE · CASE 001 · 질문은 단서가 되고 단서는 진실이 된다.
</div>
""", unsafe_allow_html=True)
