import streamlit as st
import random
import re

# =========================================================
# 예스노 탐정
# FINAL SINGLE SCREEN EDITION
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

html, body, [class*="css"], .stApp {
    font-family: 'Noto Sans KR', sans-serif !important;
}

.stApp {
    background:
        radial-gradient(circle at 85% 10%, rgba(0,130,210,.10), transparent 30%),
        radial-gradient(circle at 10% 80%, rgba(0,80,150,.08), transparent 35%),
        #070c12;
    color: #edf7ff;
}

/* 기본 여백 제거 */
section.main > div {
    padding-top: 0.4rem !important;
    padding-bottom: 0.2rem !important;
    max-width: 1500px !important;
}

/* Streamlit 상단 요소 숨김 */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* 모든 버튼 */
.stButton > button {
    border-radius: 7px !important;
    border: 1px solid #28465c !important;
    background: #101923 !important;
    color: #eaf7ff !important;
    font-weight: 700 !important;
    min-height: 38px !important;
    transition: all .15s ease !important;
}

.stButton > button:hover {
    border-color: #16c8ff !important;
    background: #132a38 !important;
    color: white !important;
    transform: translateY(-1px);
}

.stButton > button:active {
    transform: scale(.98);
}

/* 주요 버튼 */
.primary-btn .stButton > button {
    background: #087ca8 !important;
    border-color: #18caff !important;
    color: white !important;
}

/* 입력창 */
.stTextInput input,
.stSelectbox select {
    background: #0c141d !important;
    color: #f3fbff !important;
    border: 1px solid #29475b !important;
    border-radius: 7px !important;
}

.stTextInput input:focus {
    border-color: #16c8ff !important;
    box-shadow: 0 0 0 1px #16c8ff !important;
}

/* 제목 */
.game-title {
    font-size: 38px;
    line-height: 1;
    font-weight: 900;
    letter-spacing: -2px;
    color: #f5fbff;
}

.game-subtitle {
    color: #3ccfff;
    font-size: 10px;
    letter-spacing: 4px;
    font-weight: 800;
    margin-bottom: 5px;
}

/* 상단 카드 */
.stat-card {
    background: linear-gradient(145deg,#0e1822,#0a1119);
    border: 1px solid #203849;
    border-radius: 9px;
    padding: 10px 14px;
    height: 67px;
}

.stat-label {
    font-size: 9px;
    color: #7090a5;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.stat-value {
    font-size: 22px;
    font-weight: 900;
    color: white;
    margin-top: 2px;
}

/* 패널 */
.panel {
    background: rgba(10,17,25,.96);
    border: 1px solid #213b4d;
    border-radius: 9px;
    overflow: hidden;
}

.panel-head {
    height: 39px;
    padding: 10px 13px;
    border-bottom: 1px solid #21313e;
    background: #0d171f;
    color: #dff5ff;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.2px;
}

.panel-body {
    padding: 12px;
}

/* 사건 사진 */
.scene {
    height: 235px;
    border-radius: 7px;
    overflow: hidden;
    position: relative;
    background:
        linear-gradient(90deg,rgba(4,9,14,.25),rgba(4,9,14,.05)),
        url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=85");
    background-size: cover;
    background-position: center;
    border: 1px solid #243e50;
}

.scene-overlay {
    position: absolute;
    inset: 0;
    background:
        linear-gradient(to bottom,rgba(0,0,0,.05),rgba(0,0,0,.7));
}

.case-stamp {
    position: absolute;
    top: 12px;
    left: 12px;
    padding: 5px 8px;
    border: 1px solid rgba(35,204,255,.65);
    color: #6edfff;
    background: rgba(3,12,18,.8);
    font-size: 9px;
    letter-spacing: 2px;
    border-radius: 4px;
}

.scene-bottom {
    position: absolute;
    left: 14px;
    bottom: 12px;
}

.scene-title {
    font-size: 23px;
    font-weight: 900;
    color: white;
}

.scene-meta {
    color: #c7d8e1;
    font-size: 11px;
    margin-top: 3px;
}

/* 사건 설명 */
.case-box {
    margin-top: 9px;
    background: #0d1822;
    border: 1px solid #203b4d;
    border-radius: 7px;
    padding: 10px 12px;
}

.case-kicker {
    color: #20c8ff;
    font-size: 9px;
    font-weight: 900;
    letter-spacing: 2px;
}

.case-main {
    color: #f5fbff;
    font-size: 15px;
    font-weight: 800;
    line-height: 1.45;
    margin-top: 4px;
}

.case-text {
    color: #a9c0cf;
    font-size: 11px;
    line-height: 1.55;
    margin-top: 5px;
}

/* 질문 카드 */
.question-card {
    background: #0b141d;
    border: 1px solid #1f394b;
    border-radius: 7px;
    padding: 10px;
}

.question-number {
    color: #20caff;
    font-size: 9px;
    letter-spacing: 2px;
    font-weight: 900;
}

.question-text {
    color: white;
    font-size: 15px;
    font-weight: 800;
    margin-top: 4px;
    line-height: 1.35;
}

/* 답변 */
.answer-box {
    background: #09141c;
    border: 1px solid #27475b;
    border-radius: 7px;
    padding: 10px;
    margin-top: 8px;
}

.answer-title {
    color: #4dd8ff;
    font-size: 10px;
    font-weight: 900;
    letter-spacing: 1px;
}

.answer-text {
    color: #edf8ff;
    font-size: 12px;
    line-height: 1.55;
    margin-top: 4px;
}

/* 용의자 */
.suspect {
    background: #0b141d;
    border: 1px solid #1e3545;
    border-radius: 7px;
    padding: 9px;
    margin-bottom: 7px;
}

.suspect-name {
    font-weight: 900;
    font-size: 14px;
    color: white;
}

.suspect-role {
    font-size: 9px;
    color: #5f8296;
    margin-top: 1px;
}

.suspect-info {
    font-size: 10px;
    color: #a7bac6;
    margin-top: 4px;
    line-height: 1.45;
}

/* 단서 */
.clue {
    padding: 7px 9px;
    border-left: 2px solid #1fc9ff;
    background: #0c1720;
    margin-top: 5px;
    border-radius: 3px;
    color: #d5e6ef;
    font-size: 10px;
    line-height: 1.4;
}

/* 최종 */
.final-box {
    background: linear-gradient(145deg,#0e1d27,#091219);
    border: 1px solid #20bfe9;
    border-radius: 9px;
    padding: 13px;
}

.ending-good {
    color: #4dffb0;
    font-weight: 900;
    font-size: 18px;
}

.ending-mid {
    color: #ffd45a;
    font-weight: 900;
    font-size: 18px;
}

.ending-bad {
    color: #ff6c7a;
    font-weight: 900;
    font-size: 18px;
}

/* 작은 화면 */
@media (max-height: 800px) {
    .scene {
        height: 190px;
    }

    .game-title {
        font-size: 31px;
    }

    .case-main {
        font-size: 13px;
    }

    .case-text {
        font-size: 10px;
    }

    .suspect {
        padding: 6px;
        margin-bottom: 4px;
    }

    .panel-body {
        padding: 9px;
    }

    .stat-card {
        height: 59px;
        padding: 8px 12px;
    }

    .stat-value {
        font-size: 19px;
    }
}

/* 모바일 */
@media (max-width: 900px) {
    .game-title {
        font-size: 28px;
    }
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
        "image": "https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=85",
        "time": "23:58",
        "location": "서울 · 성북구 · 아파트 1403호",

        "main":
            "한 남자가 자신의 방 안에서 숨진 채 발견됐다. "
            "현관문은 잠겨 있었고 외부 침입 흔적은 없었다.",

        "story":
            "하지만 이상한 점이 하나 있었다. "
            "사건 당시 방 안의 에어컨은 18도로 설정되어 있었고, "
            "피해자의 휴대전화에는 마지막 통화 기록 하나가 삭제되어 있었다.",

        "victims": "김민재",
        "suspects": [
            {
                "name": "김민재",
                "role": "피해자",
                "info": "사건의 중심에 있는 인물. 사건 직전 누군가와 통화했다."
            },
            {
                "name": "박서연",
                "role": "피해자의 전 여자친구",
                "info": "사건 당일 밤 피해자에게 세 번 전화했다."
            },
            {
                "name": "최도윤",
                "role": "피해자의 직장 동료",
                "info": "사건 당일 오후 피해자와 크게 다퉜다."
            }
        ],

        "truth": "박서연",
        "explanation":
            "현관으로 들어간 것이 아니라 사건 전에 미리 들어와 있었다. "
            "그리고 창문을 이용한 것처럼 보이게 흔적을 만들었다. "
            "삭제된 마지막 통화가 결정적인 단서였다.",

        "questions": [
            ("현관에 외부인이 들어온 흔적이 있습니까?",
             "아니오. 현관문과 도어락에는 강제로 연 흔적이 없습니다.",
             "entrance"),
            ("피해자는 사건 당시 혼자였습니까?",
             "아니오. 정확히는 혼자였다고 단정할 수 없습니다. 다른 사람의 흔적이 남아 있습니다.",
             "alone"),
            ("창문으로 사람이 드나들 수 있었습니까?",
             "예. 창문은 열 수 있었지만, 밖에서 올라온 흔적은 발견되지 않았습니다.",
             "window"),
            ("박서연은 사건 당일 피해자에게 전화했습니까?",
             "예. 밤 11시 전후로 세 차례 전화 기록이 있습니다.",
             "seoyeon_call"),
            ("최도윤은 피해자와 다툰 적이 있습니까?",
             "예. 사건 당일 오후 회사에서 크게 언쟁을 벌였습니다.",
             "doyun_fight"),
            ("피해자의 마지막 통화 기록이 남아 있습니까?",
             "아니오. 마지막 통화 하나만 이상하게 삭제되어 있습니다.",
             "deleted_call"),
            ("삭제된 통화는 사건과 관련이 있습니까?",
             "예. 삭제된 시간은 사망 추정 시각과 매우 가깝습니다.",
             "important"),
            ("방 안에 다른 사람의 지문이 있었습니까?",
             "예. 컵과 문손잡이에서 피해자 외의 흔적이 확인됐습니다.",
             "finger"),
            ("그 지문은 박서연의 것입니까?",
             "확인된 흔적 중 하나는 박서연과 일치합니다.",
             "seoyeon_print"),
            ("최도윤에게 현관 열쇠가 있었습니까?",
             "아니오. 도윤은 비밀번호를 모른다고 주장합니다.",
             "key"),
            ("방의 에어컨이 평소와 다르게 설정되어 있었습니까?",
             "예. 사건 당시 18도로 설정되어 있었습니다.",
             "aircon"),
            ("에어컨 설정이 사건과 관련이 있습니까?",
             "예. 실내 온도를 이용해 사망 시각을 늦춰 보이게 했을 가능성이 있습니다.",
             "time"),
            ("박서연은 이 집에 들어올 수 있었습니까?",
             "예. 이전에 함께 살았기 때문에 출입 방법을 알고 있었습니다.",
             "access"),
            ("범인은 피해자의 휴대전화를 만졌습니까?",
             "예. 삭제된 기록 외에도 잠금 해제 흔적이 있습니다.",
             "phone"),
            ("박서연이 범인입니까?",
             "예. 현재까지 확보된 단서만 보면 가장 유력한 인물입니다.",
             "final")
        ]
    },

    {
        "id": "002",
        "title": "사라진 23분",
        "image": "https://images.unsplash.com/photo-1519608487953-e999c86e7455?auto=format&fit=crop&w=1200&q=85",
        "time": "02:17",
        "location": "부산 · 해운대 · 오피스텔",

        "main":
            "새벽 2시 17분, 한 개발자가 사무실에서 의식을 잃은 채 발견됐다. "
            "CCTV에는 정확히 23분 동안 아무도 찍히지 않았다.",

        "story":
            "문제는 CCTV가 고장난 것이 아니었다는 것이다. "
            "누군가가 직접 그 23분을 삭제했다. "
            "그리고 서버에는 마지막 접속자 이름이 남아 있었다.",

        "victims": "한지우",
        "suspects": [
            {
                "name": "한지우",
                "role": "피해자",
                "info": "회사 내부 보안 시스템을 담당했다."
            },
            {
                "name": "이준혁",
                "role": "팀장",
                "info": "사건 직전 서버 권한을 요청했다."
            },
            {
                "name": "윤하린",
                "role": "동료 개발자",
                "info": "피해자와 프로젝트 문제로 갈등이 있었다."
            }
        ],

        "truth": "이준혁",
        "explanation":
            "팀장 이준혁은 관리자 권한으로 CCTV 기록을 삭제했다. "
            "하지만 23분 동안 서버 접근 기록까지 완벽하게 지우지는 못했다.",

        "questions": [
            ("CCTV가 실제로 고장난 것입니까?",
             "아니오. 장비 자체에는 이상이 없습니다.",
             "cctv"),
            ("누군가 CCTV 기록을 삭제했습니까?",
             "예. 정확히 23분의 기록만 삭제되어 있습니다.",
             "deleted"),
            ("23분 동안 아무도 건물에 들어오지 않았습니까?",
             "아니오. 출입 기록과 CCTV 기록이 서로 맞지 않습니다.",
             "entry"),
            ("이준혁에게 CCTV를 수정할 권한이 있었습니까?",
             "예. 관리자 계정에 접근할 수 있었습니다.",
             "admin"),
            ("윤하린도 관리자 권한이 있었습니까?",
             "아니오. 일반 개발자 권한만 가지고 있었습니다.",
             "harin"),
            ("서버 기록에도 이상이 있습니까?",
             "예. CCTV가 사라진 직후 관리자 접속이 발생했습니다.",
             "server"),
            ("마지막 관리자 접속자는 이준혁입니까?",
             "예.",
             "junhyuk"),
            ("피해자와 이준혁은 사건 전날 다퉜습니까?",
             "예. 프로젝트 책임 문제로 충돌했습니다.",
             "fight"),
            ("CCTV 삭제 시간과 관리자 접속 시간이 일치합니까?",
             "예. 거의 정확하게 일치합니다.",
             "match"),
            ("피해자의 컴퓨터가 사용되었습니까?",
             "예. 사건 직전 화면이 잠금 해제되어 있었습니다.",
             "computer"),
            ("윤하린이 피해자의 컴퓨터를 사용할 수 있었습니까?",
             "가능했지만 해당 시간의 출입 기록은 없습니다.",
             "harin2"),
            ("범인은 관리자 권한을 사용했습니까?",
             "예.",
             "authority"),
            ("이준혁이 거짓말을 했습니까?",
             "예. 처음에는 그 시간에 서버에 접속하지 않았다고 말했습니다.",
             "lie"),
            ("23분은 의도적으로 만들어진 시간입니까?",
             "예. 누군가의 행동을 숨기기 위한 시간으로 보입니다.",
             "intent"),
            ("이준혁이 범인입니까?",
             "예. 현재 단서로는 이준혁이 범인일 가능성이 가장 높습니다.",
             "final")
        ]
    },

    {
        "id": "003",
        "title": "마지막 메시지",
        "image": "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=1200&q=85",
        "time": "18:42",
        "location": "대전 · 연구소 · B동",

        "main":
            "연구원 정하윤이 퇴근 직전 동료들에게 이상한 메시지를 남겼다. "
            "그날 밤 연구소의 보안문이 열렸지만 출입 기록에는 아무도 없었다.",

        "story":
            "메시지에는 단 세 글자가 적혀 있었다. "
            "\"믿지 마.\" "
            "그리고 연구실 컴퓨터에는 예약된 이메일 하나가 남아 있었다.",

        "victims": "정하윤",
        "suspects": [
            {
                "name": "정하윤",
                "role": "피해자",
                "info": "연구소의 핵심 프로젝트를 담당했다."
            },
            {
                "name": "강태성",
                "role": "연구 책임자",
                "info": "프로젝트 자료에 가장 큰 이해관계가 있다."
            },
            {
                "name": "서유진",
                "role": "연구원",
                "info": "피해자와 마지막으로 대화했다."
            }
        ],

        "truth": "강태성",
        "explanation":
            "강태성은 보안카드를 복제해 출입 기록을 우회했다. "
            "하지만 예약 이메일의 메타데이터 때문에 흔적이 남았다.",

        "questions": [
            ("보안문은 강제로 열린 것입니까?",
             "아니오.",
             "door"),
            ("누군가 정상적인 카드 없이 들어갔습니까?",
             "예. 출입 기록과 실제 센서 기록이 다릅니다.",
             "card"),
            ("강태성에게 보안 권한이 있었습니까?",
             "예. 연구 책임자라 높은 권한을 가지고 있습니다.",
             "taesung"),
            ("서유진에게도 같은 권한이 있었습니까?",
             "아니오.",
             "yujin"),
            ("피해자는 강태성과 갈등이 있었습니까?",
             "예. 프로젝트 자료 공개 문제로 갈등이 있었습니다.",
             "conflict"),
            ("마지막 메시지는 피해자가 직접 보낸 것입니까?",
             "예. 피해자의 휴대전화에서 직접 작성된 기록이 있습니다.",
             "message"),
            ("예약 이메일이 있습니까?",
             "예.",
             "email"),
            ("예약 이메일은 사건 전에 만들어졌습니까?",
             "예. 사건 발생 약 세 시간 전에 예약되어 있었습니다.",
             "scheduled"),
            ("이메일 작성자는 강태성입니까?",
             "메타데이터에는 강태성의 계정과 연결된 흔적이 있습니다.",
             "metadata"),
            ("강태성이 거짓말을 했습니까?",
             "예. 사건 당시 연구소에 없었다고 했지만 접속 흔적이 있습니다.",
             "lie"),
            ("서유진이 사건 현장에 있었습니까?",
             "아니오. 마지막 출입 기록이 오후 6시 이전입니다.",
             "yujin2"),
            ("보안카드가 복제되었습니까?",
             "예. 기존 카드와 다른 인증 패턴이 발견됐습니다.",
             "clone"),
            ("누군가 출입 기록을 조작했습니까?",
             "예.",
             "log"),
            ("피해자는 누군가를 경고하려 했습니까?",
             "예. 마지막 메시지가 그것을 암시합니다.",
             "warning"),
            ("강태성이 범인입니까?",
             "예. 현재 증거를 종합하면 강태성이 가장 유력합니다.",
             "final")
        ]
    }
]


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "case_index": 0,
    "question_count": 0,
    "score": 0,
    "trust": 100,
    "clues": [],
    "last_answer": "",
    "last_question": "",
    "selected_suspect": None,
    "game_finished": False,
    "ending": "",
    "history": [],
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


case = CASES[st.session_state.case_index]


# =========================================================
# FUNCTIONS
# =========================================================

def reset_game(case_index=0):
    st.session_state.case_index = case_index
    st.session_state.question_count = 0
    st.session_state.score = 0
    st.session_state.trust = 100
    st.session_state.clues = []
    st.session_state.last_answer = ""
    st.session_state.last_question = ""
    st.session_state.selected_suspect = None
    st.session_state.game_finished = False
    st.session_state.ending = ""
    st.session_state.history = []


def answer_question(question_text):

    if st.session_state.question_count >= 15:
        return

    # 질문 찾기
    best = None

    for q, answer, clue in case["questions"]:
        words = re.findall(r"[가-힣A-Za-z0-9]+", q.lower())
        score = sum(1 for w in words if len(w) >= 2 and w in question_text.lower())

        if score > 0:
            if best is None or score > best[0]:
                best = (score, q, answer, clue)

    # 질문을 못 알아들었을 경우
    if best is None:

        generic_answers = [
            "현재 확보된 자료만으로는 명확하게 확인할 수 없습니다.",
            "그 부분은 아직 증거가 부족합니다.",
            "가능성은 있지만 결정적인 단서는 아닙니다.",
            "현장 기록을 더 확인해야 합니다.",
            "아직 확실한 증거가 없습니다."
        ]

        answer = random.choice(generic_answers)
        clue = None
        matched_question = question_text

        st.session_state.trust -= 3

    else:
        _, matched_question, answer, clue = best

        # 맞는 질문일수록 점수 증가
        st.session_state.score += 7

    st.session_state.question_count += 1
    st.session_state.last_question = question_text
    st.session_state.last_answer = answer

    # 단서 추가
    if clue and clue not in st.session_state.clues:
        st.session_state.clues.append(clue)
        st.session_state.score += 3

    # 기록
    st.session_state.history.append({
        "question": question_text,
        "answer": answer
    })

    # 질문이 많아질수록 신뢰도 조금 감소
    if st.session_state.question_count >= 10:
        st.session_state.trust = max(
            60,
            st.session_state.trust - 1
        )


def make_ending():

    suspect = st.session_state.selected_suspect

    if not suspect:
        st.session_state.ending = "no_suspect"
        return

    truth = case["truth"]

    if suspect == truth and st.session_state.score >= 50:
        st.session_state.ending = "true"

    elif suspect == truth:
        st.session_state.ending = "partial"

    else:
        st.session_state.ending = "wrong"

    st.session_state.game_finished = True


# =========================================================
# TOP HEADER
# =========================================================

top_left, top_right = st.columns([1.4, 1])

with top_left:
    st.markdown(
        '<div class="game-subtitle">CONFIDENTIAL · 34 CASE FILES</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="game-title">예스노 탐정</div>',
        unsafe_allow_html=True
    )

with top_right:
    st.markdown(
        f"""
        <div style="text-align:right;
                    color:#587587;
                    font-size:10px;
                    letter-spacing:1px;
                    padding-top:16px;">
            CASE {case["id"]} · ROUND {st.session_state.case_index + 1}/3
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# STATS
# =========================================================

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">질문</div>
            <div class="stat-value">
                {st.session_state.question_count}/15
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">수사 점수</div>
            <div class="stat-value">
                {st.session_state.score}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">신뢰도</div>
            <div class="stat-value">
                {st.session_state.trust}%
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with s4:
    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-label">확보 단서</div>
            <div class="stat-value">
                {len(st.session_state.clues)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# MAIN GAME
# =========================================================

left, right = st.columns([1.55, 1], gap="medium")


# =========================================================
# LEFT : CASE FILE
# =========================================================

with left:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-head">
                CASE FILE // 현장 기록
                <span style="float:right;color:#26c9ff;font-size:8px;">
                    CONFIDENTIAL
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 이미지
    st.markdown(
        f"""
        <div class="scene">
            <div class="scene-overlay"></div>

            <div class="case-stamp">
                CASE #{case["id"]} · EVIDENCE PHOTO
            </div>

            <div class="scene-bottom">
                <div class="scene-title">
                    {case["title"]}
                </div>

                <div class="scene-meta">
                    {case["location"]} · {case["time"]} · 외부 침입 흔적 없음
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 사건 내용
    st.markdown(
        f"""
        <div class="case-box">

            <div class="case-kicker">
                CASE BRIEFING
            </div>

            <div class="case-main">
                {case["main"]}
            </div>

            <div class="case-text">
                {case["story"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # 용의자 3명
    c1, c2, c3 = st.columns(3)

    for col, suspect in zip([c1, c2, c3], case["suspects"]):

        with col:
            st.markdown(
                f"""
                <div class="suspect">

                    <div class="suspect-name">
                        {suspect["name"]}
                    </div>

                    <div class="suspect-role">
                        {suspect["role"]}
                    </div>

                    <div class="suspect-info">
                        {suspect["info"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# RIGHT : INTERROGATION
# =========================================================

with right:

    st.markdown(
        """
        <div class="panel">
            <div class="panel-head">
                INTERROGATION // 심문
                <span style="float:right;color:#26c9ff;font-size:8px;">
                    YES / NO ONLY
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            margin-top:8px;
            margin-bottom:5px;
            font-size:10px;
            color:#42d6ff;
            font-weight:800;
        ">
            현재 질문 {st.session_state.question_count}/15
        </div>
        """,
        unsafe_allow_html=True
    )

    # 용의자 선택
    suspect_names = [x["name"] for x in case["suspects"]]

    selected = st.selectbox(
        "심문 대상",
        suspect_names,
        index=(
            suspect_names.index(st.session_state.selected_suspect)
            if st.session_state.selected_suspect in suspect_names
            else 0
        ),
        key="suspect_select"
    )

    st.session_state.selected_suspect = selected

    # 현재 질문
    if st.session_state.last_question:

        st.markdown(
            f"""
            <div class="question-card">

                <div class="question-number">
                    LAST QUESTION
                </div>

                <div class="question-text">
                    {st.session_state.last_question}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # 답변
    if st.session_state.last_answer:

        st.markdown(
            f"""
            <div class="answer-box">

                <div class="answer-title">
                    🔎 조사 기록
                </div>

                <div class="answer-text">
                    {st.session_state.last_answer}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    # 입력
    st.markdown(
        """
        <div style="
            color:#9db5c4;
            font-size:10px;
            margin-top:7px;
            margin-bottom:3px;
        ">
            예 / 아니오로 답할 수 있는 질문을 입력하세요.
        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input(
        "질문",
        placeholder="예: 현관에 들어온 흔적이 있습니까?",
        label_visibility="collapsed",
        key="question_input"
    )

    # 질문 버튼
    if st.button(
        "🔎 질문하기",
        use_container_width=True,
        disabled=(
            st.session_state.question_count >= 15
            or not question.strip()
        )
    ):
        answer_question(question)
        st.rerun()

    # 빠른 질문
    st.markdown(
        """
        <div style="
            color:#587587;
            font-size:9px;
            margin-top:6px;
            margin-bottom:3px;
        ">
            QUICK QUESTIONS
        </div>
        """,
        unsafe_allow_html=True
    )

    q1, q2 = st.columns(2)

    quick_questions = [
        "현관에 들어온 흔적이 있습니까?",
        "피해자는 혼자였습니까?",
        "CCTV 기록에 이상이 있습니까?",
        "범인은 피해자의 휴대전화를 만졌습니까?"
    ]

    with q1:
        if st.button(
            "현관 침입 흔적?",
            use_container_width=True,
            disabled=st.session_state.question_count >= 15
        ):
            answer_question(quick_questions[0])
            st.rerun()

        if st.button(
            "피해자는 혼자였나?",
            use_container_width=True,
            disabled=st.session_state.question_count >= 15
        ):
            answer_question(quick_questions[1])
            st.rerun()

    with q2:
        if st.button(
            "CCTV 이상?",
            use_container_width=True,
            disabled=st.session_state.question_count >= 15
        ):
            answer_question(quick_questions[2])
            st.rerun()

        if st.button(
            "휴대전화 조작?",
            use_container_width=True,
            disabled=st.session_state.question_count >= 15
        ):
            answer_question(quick_questions[3])
            st.rerun()


# =========================================================
# LOWER SECTION
# =========================================================

st.write("")


lower_left, lower_right = st.columns([1.55, 1], gap="medium")


# =========================================================
# CLUES
# =========================================================

with lower_left:

    st.markdown(
        """
        <div style="
            font-size:11px;
            color:#61d8ff;
            font-weight:900;
            letter-spacing:1px;
            margin-bottom:5px;
        ">
            🔐 확보된 단서
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.clues:

        st.markdown(
            """
            <div class="clue">
                아직 확보된 단서가 없습니다.
                질문을 통해 사건의 빈칸을 채우세요.
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        # 화면에 너무 많이 쌓이지 않도록 최대 4개
        for clue in st.session_state.clues[-4:]:

            st.markdown(
                f"""
                <div class="clue">
                    {clue}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# FINAL
# =========================================================

with lower_right:

    if not st.session_state.game_finished:

        st.markdown(
            """
            <div style="
                color:#61d8ff;
                font-size:10px;
                font-weight:900;
                letter-spacing:1px;
                margin-bottom:5px;
            ">
                FINAL DEDUCTION
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.session_state.question_count < 5:

            st.markdown(
                """
                <div class="clue">
                    최소 5개의 질문을 해보는 것을 추천합니다.
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="clue">
                    지금까지의 단서를 바탕으로 범인을 선택할 수 있습니다.
                </div>
                """,
                unsafe_allow_html=True
            )

        final_names = [x["name"] for x in case["suspects"]]

        final_choice = st.selectbox(
            "범인 지목",
            final_names,
            key="final_choice"
        )

        if st.button(
            "🚨 최종 범인 지목",
            use_container_width=True,
            disabled=st.session_state.question_count < 5
        ):

            st.session_state.selected_suspect = final_choice
            make_ending()
            st.rerun()

    else:

        if st.session_state.ending == "true":

            st.markdown(
                """
                <div class="final-box">
                    <div class="ending-good">
                        TRUE ENDING
                    </div>

                    <div style="
                        color:white;
                        font-size:14px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        완벽한 추리입니다.
                    </div>

                    <div style="
                        color:#a9c0cf;
                        font-size:10px;
                        line-height:1.5;
                        margin-top:5px;
                    ">
                        모든 핵심 단서를 연결했습니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif st.session_state.ending == "partial":

            st.markdown(
                """
                <div class="final-box">
                    <div class="ending-mid">
                        PARTIAL ENDING
                    </div>

                    <div style="
                        color:white;
                        font-size:14px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        범인은 맞혔지만 증거가 부족합니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                """
                <div class="final-box">
                    <div class="ending-bad">
                        WRONG ENDING
                    </div>

                    <div style="
                        color:white;
                        font-size:14px;
                        font-weight:800;
                        margin-top:5px;
                    ">
                        잘못된 사람을 지목했습니다.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown(
            f"""
            <div class="clue">
                <b>진범:</b> {case["truth"]}<br>
                {case["explanation"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        b1, b2 = st.columns(2)

        with b1:
            if st.button(
                "🔄 다시 수사",
                use_container_width=True
            ):
                reset_game(st.session_state.case_index)
                st.rerun()

        with b2:
            if st.button(
                "➡ 다음 사건",
                use_container_width=True,
                disabled=st.session_state.case_index >= len(CASES)-1
            ):
                reset_game(st.session_state.case_index + 1)
                st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#314b5b;
        font-size:8px;
        letter-spacing:2px;
        margin-top:7px;
    ">
        YES NO DETECTIVE · CASE MANAGEMENT SYSTEM · 2026
    </div>
    """,
    unsafe_allow_html=True
)
