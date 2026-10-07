import streamlit as st
import time

# =========================================================
# YES NO DETECTIVE
# STREAMLIT FINAL
# =========================================================

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# STYLE
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 75% 15%, rgba(0,130,255,.10), transparent 28%),
        radial-gradient(circle at 15% 85%, rgba(0,255,210,.06), transparent 25%),
        #050a10;
    color: #eaf3ff;
}

/* 전체 화면 */
.block-container {
    max-width: 1500px !important;
    padding-top: 20px !important;
    padding-bottom: 10px !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
}

/* Streamlit 기본 UI 숨기기 */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

/* 제목 */
.game-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    line-height: 1;
    margin-bottom: 3px;
}

.game-sub {
    color: #53cfff;
    font-size: 11px;
    letter-spacing: 4px;
    font-weight: 800;
}

/* 상단 카드 */
.stat {
    background: linear-gradient(145deg,#0d1721,#09111a);
    border: 1px solid #20384c;
    border-radius: 10px;
    padding: 13px 17px;
    height: 75px;
}

.stat-label {
    color: #7190a8;
    font-size: 11px;
    margin-bottom: 3px;
}

.stat-value {
    color: white;
    font-size: 23px;
    font-weight: 900;
}

/* 패널 */
.panel {
    background: rgba(8,16,24,.96);
    border: 1px solid #20384c;
    border-radius: 11px;
    overflow: hidden;
}

.panel-head {
    height: 43px;
    padding: 12px 16px;
    border-bottom: 1px solid #20384c;
    color: #aee7ff;
    font-weight: 800;
    font-size: 13px;
    letter-spacing: 1px;
}

.panel-body {
    padding: 16px;
}

/* 사건 이미지 */
.scene {
    height: 270px;
    border-radius: 8px;
    overflow: hidden;
    position: relative;
    border: 1px solid #29465b;
    background:
        linear-gradient(
            90deg,
            rgba(0,0,0,.58),
            rgba(0,0,0,.05)
        ),
        url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1200&q=85")
        center/cover;
}

.scene::after {
    content:"";
    position:absolute;
    inset:0;
    background:
        linear-gradient(
            180deg,
            rgba(0,0,0,.05),
            rgba(0,0,0,.7)
        );
}

.case-tag {
    position:absolute;
    z-index:2;
    top:13px;
    left:13px;
    padding:6px 10px;
    border:1px solid #48caff;
    color:#62d7ff;
    background:rgba(0,15,25,.85);
    border-radius:4px;
    font-size:10px;
    letter-spacing:2px;
    font-weight:800;
}

.scene-text {
    position:absolute;
    z-index:3;
    bottom:15px;
    left:17px;
    right:17px;
}

.scene-title {
    font-size:25px;
    font-weight:900;
    margin-bottom:4px;
}

.scene-meta {
    font-size:11px;
    color:#b6c8d6;
}

/* 사건 설명 */
.case-box {
    margin-top:10px;
    padding:13px 15px;
    border-left:3px solid #22b9ff;
    background:#0b1722;
    border-radius:5px;
}

.case-title {
    color:#5ed2ff;
    font-size:11px;
    font-weight:900;
    letter-spacing:2px;
    margin-bottom:7px;
}

.case-text {
    font-size:13px;
    line-height:1.55;
    color:#e1eaf1;
}

/* 질문 영역 */
.question-box {
    padding:15px;
}

.question-count {
    color:#54d2ff;
    font-size:12px;
    font-weight:800;
    margin-bottom:7px;
}

.answer-box {
    background:#09131d;
    border:1px solid #203b50;
    border-radius:7px;
    padding:11px;
    margin-top:8px;
    min-height:56px;
}

.answer-name {
    color:#64d8ff;
    font-weight:800;
    font-size:12px;
}

.answer-text {
    color:#e5edf4;
    font-size:13px;
    margin-top:4px;
}

/* 단서 */
.clue {
    background:#0d1922;
    border:1px solid #243b4d;
    border-radius:6px;
    padding:8px 10px;
    margin-bottom:6px;
    font-size:12px;
}

.clue strong {
    color:#5bd6ff;
}

/* 버튼 */
.stButton > button {
    width:100%;
    border-radius:7px;
    border:1px solid #28516b;
    background:#0d1b27;
    color:#eaf7ff;
    font-weight:700;
    min-height:38px;
}

.stButton > button:hover {
    border-color:#35caff;
    color:white;
    background:#112b3c;
}

div[data-testid="stTextInput"] input {
    background:#08121b !important;
    color:white !important;
    border:1px solid #294b62 !important;
    border-radius:7px !important;
}

div[data-testid="stSelectbox"] > div {
    background:#08121b !important;
}

/* 범인 선택 */
.accuse {
    background:linear-gradient(145deg,#101b26,#081018);
    border:1px solid #284559;
    border-radius:8px;
    padding:10px;
    text-align:center;
}

.accuse-name {
    font-size:17px;
    font-weight:900;
}

.accuse-role {
    color:#7890a2;
    font-size:10px;
    margin-top:2px;
}

/* 엔딩 */
.ending {
    padding:22px;
    border:1px solid #32c9ff;
    background:linear-gradient(145deg,#081923,#071018);
    border-radius:10px;
    text-align:center;
}

.ending-title {
    color:#65dbff;
    font-size:30px;
    font-weight:900;
}

.ending-text {
    margin-top:10px;
    color:#dce8f0;
    line-height:1.7;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# GAME STATE
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = True

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "trust" not in st.session_state:
    st.session_state.trust = 100

if "clues" not in st.session_state:
    st.session_state.clues = []

if "answers" not in st.session_state:
    st.session_state.answers = []

if "ending" not in st.session_state:
    st.session_state.ending = None

if "selected_suspect" not in st.session_state:
    st.session_state.selected_suspect = None


# =========================================================
# DATA
# =========================================================

suspects = {
    "김민재": {
        "role": "피해자의 직장 동료",
        "info": "사건 당일 피해자와 마지막으로 통화한 사람.",
        "clue": "승진 문제로 피해자와 크게 다툰 적이 있다."
    },
    "박서연": {
        "role": "피해자의 전 여자친구",
        "info": "헤어진 뒤에도 피해자와 연락을 이어가고 있었다.",
        "clue": "사건 당일 밤 피해자에게 세 번 전화했다."
    },
    "최도윤": {
        "role": "피해자의 이웃",
        "info": "사건 당시 같은 건물에 있었다.",
        "clue": "CCTV 사각지대를 가장 잘 알고 있었다."
    }
}

questions = {

    "현관에 들어온 흔적이 있습니까?": {
        "answer": "아니오.",
        "detail": "현관문과 손잡이에는 외부 침입 흔적이 없습니다.",
        "score": 5,
        "clue": "외부 침입 가능성이 낮다."
    },

    "피해자는 혼자 있었습니까?": {
        "answer": "아니오.",
        "detail": "사건 직전 누군가와 통화한 기록이 남아 있습니다.",
        "score": 5,
        "clue": "피해자는 사건 직전 누군가와 연락했다."
    },

    "CCTV에 수상한 사람이 찍혔습니까?": {
        "answer": "예.",
        "detail": "23시 41분, 건물 복도에서 모자를 쓴 사람이 확인됩니다.",
        "score": 10,
        "clue": "23:41 복도 CCTV에 수상한 인물이 찍혔다."
    },

    "피해자의 휴대전화가 조작됐습니까?": {
        "answer": "예.",
        "detail": "마지막 통화 기록 하나가 삭제되어 있습니다.",
        "score": 10,
        "clue": "마지막 통화 기록이 의도적으로 삭제됐다."
    },

    "범인은 피해자를 알고 있었습니까?": {
        "answer": "예.",
        "detail": "현관을 강제로 열지 않았고 피해자가 문을 열어준 정황이 있습니다.",
        "score": 10,
        "clue": "범인은 피해자와 아는 사이일 가능성이 높다."
    },

    "최도윤은 CCTV 위치를 알고 있었습니까?": {
        "answer": "예.",
        "detail": "최도윤은 이 건물에서 6년 동안 거주했습니다.",
        "score": 10,
        "clue": "최도윤은 CCTV 사각지대를 알고 있었다."
    },

    "박서연은 사건 당일 피해자에게 전화했습니까?": {
        "answer": "예.",
        "detail": "23시 18분, 23시 21분, 23시 27분 총 세 번 통화했습니다.",
        "score": 5,
        "clue": "박서연은 사건 직전 세 번 연락했다."
    },

    "김민재는 피해자와 다퉜습니까?": {
        "answer": "예.",
        "detail": "승진 문제로 사건 당일 오후 큰 말다툼이 있었다고 확인됩니다.",
        "score": 5,
        "clue": "김민재에게 강한 동기가 있었다."
    },

    "사건 현장에 지문이 남아 있습니까?": {
        "answer": "예.",
        "detail": "피해자의 지문 외에 한 사람의 지문이 발견됐습니다.",
        "score": 10,
        "clue": "피해자 외 제3자의 지문이 발견됐다."
    },

    "창문으로 침입했습니까?": {
        "answer": "아니오.",
        "detail": "창문은 안쪽에서 잠겨 있었습니다.",
        "score": 5,
        "clue": "창문 침입 가능성이 없다."
    },

    "피해자의 금품이 사라졌습니까?": {
        "answer": "아니오.",
        "detail": "지갑과 귀중품은 그대로 남아 있습니다.",
        "score": 5,
        "clue": "금품 목적의 범행이 아니다."
    },

    "범인은 사건 후 다시 현장을 확인했습니까?": {
        "answer": "예.",
        "detail": "사건 직후 현관 CCTV에 같은 인물로 추정되는 모습이 다시 포착됩니다.",
        "score": 15,
        "clue": "범인은 사건 후 현장에 다시 접근했다."
    },

    "범인은 CCTV 사각지대를 이용했습니까?": {
        "answer": "예.",
        "detail": "복도 카메라 두 대 사이의 17초 공백이 확인됐습니다.",
        "score": 15,
        "clue": "17초짜리 CCTV 공백이 존재한다."
    },

    "최도윤의 알리바이는 완벽합니까?": {
        "answer": "아니오.",
        "detail": "최도윤은 자신이 계속 집에 있었다고 주장했지만 통신 기록과 맞지 않습니다.",
        "score": 15,
        "clue": "최도윤의 알리바이에 모순이 있다."
    },

    "진짜 범인은 피해자와 친분이 있었습니까?": {
        "answer": "예.",
        "detail": "강제로 들어온 흔적이 없기 때문에 피해자가 스스로 문을 열어준 것으로 보입니다.",
        "score": 10,
        "clue": "범인은 피해자의 신뢰를 받고 있었다."
    }
}


# =========================================================
# HEADER
# =========================================================

c1, c2 = st.columns([2.2, 1])

with c1:
    st.markdown("""
    <div class="game-sub">CONFIDENTIAL · 34 CASE FILES</div>
    <div class="game-title">예스노 탐정</div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="
    text-align:right;
    color:#6e8ca3;
    font-size:11px;
    padding-top:25px;
    letter-spacing:1px;">
    CASE 001 · ROUND 01 / 03
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# STATS
# =========================================================

a,b,c,d = st.columns(4)

with a:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-label">질문</div>
        <div class="stat-value">{st.session_state.questions}/15</div>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-label">수사 점수</div>
        <div class="stat-value">{st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-label">신뢰도</div>
        <div class="stat-value">{st.session_state.trust}%</div>
    </div>
    """, unsafe_allow_html=True)

with d:
    st.markdown(f"""
    <div class="stat">
        <div class="stat-label">확보 단서</div>
        <div class="stat-value">{len(st.session_state.clues)}</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# =========================================================
# MAIN LAYOUT
# =========================================================

left, right = st.columns([1.7, 1], gap="medium")


# =========================================================
# LEFT : CASE
# =========================================================

with left:

    st.markdown("""
    <div class="panel">
        <div class="panel-head">
            CASE FILE // 현장 기록
            <span style="float:right;color:#46cfff;font-size:9px;">
            CONFIDENTIAL
            </span>
        </div>
        <div class="panel-body">
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="scene">
        <div class="case-tag">CASE #001 · EVIDENCE PHOTO</div>

        <div class="scene-text">
            <div class="scene-title">잠긴 방의 진실</div>
            <div class="scene-meta">
                서울 · 23:58 · 외부 침입 흔적 없음
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="case-box">
        <div class="case-title">CASE BRIEFING</div>

        <div class="case-text">
        새벽 1시 18분.<br>
        한 남자가 자신의 방 안에서 쓰러진 채 발견됐다.
        </div>

        <div class="case-text" style="margin-top:7px;">
        현관문은 잠겨 있었고 창문에서도 침입 흔적은 발견되지 않았다.
        </div>

        <div class="case-text" style="margin-top:7px;">
        그러나 이상한 점이 하나 있었다.<br>
        사건 당시 방 안의 에어컨은 <b style="color:#60d8ff;">18도</b>로 설정되어 있었고,
        피해자의 휴대전화에는 <b style="color:#60d8ff;">마지막 통화 기록 하나가 삭제</b>되어 있었다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # 최근 단서
    if st.session_state.clues:

        st.markdown("""
        <div style="
        margin-top:9px;
        color:#58d5ff;
        font-size:11px;
        font-weight:900;
        letter-spacing:1px;">
        확보한 단서
        </div>
        """, unsafe_allow_html=True)

        clue_html = ""

        for clue in st.session_state.clues[-3:]:
            clue_html += f"""
            <div class="clue">
                <strong>◆</strong> {clue}
            </div>
            """

        st.markdown(clue_html, unsafe_allow_html=True)


# =========================================================
# RIGHT : INTERROGATION
# =========================================================

with right:

    st.markdown("""
    <div class="panel">
        <div class="panel-head">
            INTERROGATION // 심문
            <span style="float:right;color:#46cfff;font-size:9px;">
            YES / NO ONLY
            </span>
        </div>
        <div class="question-box">
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="question-count">현재 질문 {st.session_state.questions}/15</div>',
        unsafe_allow_html=True
    )

    # 질문 선택
    question_list = list(questions.keys())

    selected_question = st.selectbox(
        "질문할 내용",
        question_list,
        key="question_select"
    )

    # 질문하기
    if st.button("🔎 이 질문 조사하기", use_container_width=True):

        if st.session_state.questions < 15:

            data = questions[selected_question]

            st.session_state.questions += 1
            st.session_state.score += data["score"]

            if data["answer"] == "예":
                st.session_state.trust = min(
                    100,
                    st.session_state.trust + 1
                )

            if data["clue"] not in st.session_state.clues:
                st.session_state.clues.append(data["clue"])

            st.session_state.answers.insert(
                0,
                {
                    "q": selected_question,
                    "answer": data["answer"],
                    "detail": data["detail"]
                }
            )

            st.rerun()

    # 마지막 답변
    if st.session_state.answers:

        last = st.session_state.answers[0]

        st.markdown(f"""
        <div class="answer-box">
            <div class="answer-name">
                탐정 기록 · {last["answer"]}
            </div>
            <div class="answer-text">
                {last["detail"]}
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="answer-box">
            <div class="answer-name">아직 심문하지 않았습니다.</div>
            <div class="answer-text">
                질문을 골라 조사하세요.
                대답은 모두 사건의 단서가 됩니다.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)

    # =====================================================
    # SUSPECT
    # =====================================================

    st.markdown("""
    <div style="
    margin-top:10px;
    color:#5ed6ff;
    font-size:11px;
    font-weight:900;
    letter-spacing:1px;">
    용의자
    </div>
    """, unsafe_allow_html=True)

    suspect_names = list(suspects.keys())

    selected_suspect = st.selectbox(
        "범인을 지목하세요",
        suspect_names,
        key="suspect_select"
    )

    s = suspects[selected_suspect]

    st.markdown(f"""
    <div class="accuse">
        <div class="accuse-name">{selected_suspect}</div>
        <div class="accuse-role">{s["role"]}</div>
        <div style="
        color:#b9cad6;
        font-size:11px;
        margin-top:5px;">
        {s["info"]}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 범인 지목
    if st.button(
        "🚨 이 사람을 범인으로 지목",
        use_container_width=True
    ):

        st.session_state.selected_suspect = selected_suspect

        if selected_suspect == "최도윤":

            st.session_state.ending = "TRUE"

        elif selected_suspect == "김민재":

            st.session_state.ending = "PARTIAL"

        else:

            st.session_state.ending = "BAD"

        st.rerun()


# =========================================================
# ENDING
# =========================================================

if st.session_state.ending:

    st.write("")

    if st.session_state.ending == "TRUE":

        st.markdown("""
        <div class="ending">

            <div class="ending-title">
                TRUE ENDING
            </div>

            <div style="
            color:#4fe0ff;
            font-size:12px;
            letter-spacing:3px;
            margin-top:4px;">
            CASE CLOSED
            </div>

            <div class="ending-text">
                범인은 <b>최도윤</b>이었다.<br><br>

                그는 건물의 CCTV 사각지대를 알고 있었고,
                피해자가 문을 열어주는 순간을 이용했다.<br><br>

                사건 이후 그는 다시 현장을 확인했고,
                마지막 통화 기록을 삭제했다.<br><br>

                하지만 17초짜리 CCTV 공백과
                그의 알리바이 사이의 모순을 숨기지는 못했다.
            </div>

            <div style="
            margin-top:14px;
            color:#6ae2ff;
            font-weight:900;">
            🔎 사건 해결 · 탐정 승리
            </div>

        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.ending == "PARTIAL":

        st.markdown("""
        <div class="ending">

            <div class="ending-title">
                PARTIAL ENDING
            </div>

            <div class="ending-text">
                김민재에게는 분명한 동기가 있었다.<br>
                하지만 그의 알리바이와 현장 증거는
                범인이라고 단정하기에는 부족했다.<br><br>

                당신은 너무 빨리 범인을 지목했다.
            </div>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="ending">

            <div class="ending-title">
                BAD ENDING
            </div>

            <div class="ending-text">
                잘못된 사람을 범인으로 지목했다.<br><br>

                진짜 범인은 아직 잡히지 않았다.
            </div>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div style="
text-align:center;
color:#496172;
font-size:9px;
letter-spacing:2px;
margin-top:8px;">
YES NO DETECTIVE · CASE MANAGEMENT SYSTEM · 001
</div>
""", unsafe_allow_html=True)
