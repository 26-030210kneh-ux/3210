import streamlit as st
import re
import base64
import html

# =========================================================
# 기본 설정
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

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

.stApp {
    background:
        radial-gradient(circle at 15% 10%, #102338 0%, transparent 30%),
        radial-gradient(circle at 90% 20%, #111d31 0%, transparent 28%),
        #05080c;
    color:#eaf2f8;
}

.block-container {
    max-width:1500px !important;
    padding:14px 20px 10px 20px !important;
}

* {
    font-family:
    "Malgun Gothic",
    "Noto Sans KR",
    Arial,
    sans-serif;
}

.main-title {
    font-size:30px;
    font-weight:900;
    letter-spacing:-1px;
}

.subtitle {
    color:#7f96ab;
    font-size:12px;
}

.top-card {
    background:linear-gradient(145deg,#0c1723,#09111a);
    border:1px solid #20384d;
    border-radius:9px;
    padding:9px 12px;
    text-align:center;
    box-shadow:0 0 18px rgba(0,120,255,.05);
}

.top-label {
    color:#6d879c;
    font-size:10px;
}

.top-value {
    color:#f5fbff;
    font-size:21px;
    font-weight:900;
}

.panel {
    background:linear-gradient(145deg,#0a121b,#080e15);
    border:1px solid #1d3346;
    border-radius:10px;
    padding:13px;
}

.panel-title {
    font-size:17px;
    font-weight:900;
    color:#f2f7fb;
    margin-bottom:8px;
}

.small {
    font-size:11px;
    color:#8198aa;
}

.case-box {
    background:#0b151f;
    border:1px solid #20384c;
    border-radius:8px;
    padding:12px;
    line-height:1.65;
}

.case-title {
    color:#59b9ff;
    font-weight:900;
    font-size:14px;
}

.case-highlight {
    color:#ff6370;
    font-weight:900;
}

.suspect {
    background:linear-gradient(145deg,#0d1721,#091017);
    border:1px solid #20384c;
    border-radius:8px;
    padding:9px;
    margin-bottom:7px;
}

.suspect-name {
    color:white;
    font-weight:900;
    font-size:15px;
}

.suspect-role {
    color:#5db9f4;
    font-size:10px;
}

.suspect-text {
    color:#9fb0bd;
    font-size:10px;
    line-height:1.45;
    margin-top:4px;
}

.suspect-danger {
    color:#ff6872;
    font-size:10px;
    margin-top:4px;
}

.clue {
    background:#0b1824;
    border:1px solid #24435b;
    border-radius:7px;
    padding:8px;
    margin-bottom:5px;
}

.clue-title {
    color:#6dc8ff;
    font-weight:900;
    font-size:11px;
}

.clue-text {
    color:#aebdca;
    font-size:10px;
    margin-top:2px;
}

.answer-box {
    background:#08131e;
    border:1px solid #2a4961;
    border-radius:9px;
    padding:13px;
    min-height:120px;
}

.yes {
    color:#62e3a3;
    font-size:28px;
    font-weight:900;
}

.no {
    color:#ff6570;
    font-size:28px;
    font-weight:900;
}

.unknown {
    color:#e9cf70;
    font-size:28px;
    font-weight:900;
}

.answer-text {
    color:#d1dde6;
    font-size:12px;
    line-height:1.6;
    margin-top:5px;
}

.stTextInput input {
    background:#09131d !important;
    color:white !important;
    border:1px solid #34536b !important;
    border-radius:7px !important;
}

.stButton button {
    background:linear-gradient(135deg,#1268a3,#1889ce) !important;
    color:white !important;
    border:1px solid #42baff !important;
    border-radius:7px !important;
    font-weight:900 !important;
}

.stButton button:hover {
    background:linear-gradient(135deg,#1986c9,#20a4ed) !important;
}

div[data-testid="stAlert"] {
    padding:8px !important;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 세션
# =========================================================

defaults = {
    "questions": 0,
    "score": 0,
    "trust": 100,
    "clues": [],
    "history": [],
    "last_answer": None,
    "game_over": False,
    "ending": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 사건
# =========================================================

CASE = {
    "title": "잠긴 방의 진실",
    "time": "새벽 1시 18분",
    "victim": "김민수",
    "location": "아파트 14층 1407호",
}


# =========================================================
# 용의자
# =========================================================

SUSPECTS = [
    {
        "name": "김민재",
        "role": "피해자의 회사 동료",
        "desc": "승진 문제로 피해자와 크게 다툰 적이 있다.",
        "suspicion": "사건 직전 피해자와 마지막으로 통화했다."
    },
    {
        "name": "박서연",
        "role": "피해자의 전 여자친구",
        "desc": "헤어진 뒤에도 피해자와 계속 연락하고 있었다.",
        "suspicion": "사건 당일 피해자에게 세 번 전화했다."
    },
    {
        "name": "최도윤",
        "role": "건물 관리인",
        "desc": "건물 출입 시스템과 CCTV를 관리한다.",
        "suspicion": "CCTV 관리자 권한을 가지고 있다."
    },
    {
        "name": "한유진",
        "role": "피해자의 동생",
        "desc": "가족 문제로 피해자와 갈등이 있었다.",
        "suspicion": "피해자의 집 예비 열쇠를 가지고 있다."
    }
]


# =========================================================
# 사건 정보
# 질문의 의미를 여러 표현으로 인식
# =========================================================

FACTS = [

    {
        "keywords": [
            "현관", "문으로", "문을 통해", "문을 이용",
            "침입", "들어온 흔적", "강제로 들어", "강제 침입"
        ],
        "answer": "NO",
        "response": "현관문에는 강제로 침입한 흔적이 없습니다.",
        "clue": "현관문에는 강제 침입 흔적이 없다.",
        "score": 8
    },

    {
        "keywords": [
            "창문", "창으로", "창문으로",
            "창문을 통해", "창문 침입"
        ],
        "answer": "NO",
        "response": "창문은 사건 당시 안쪽에서 잠겨 있었고 외부 침입 흔적도 없습니다.",
        "clue": "창문을 통한 외부 침입 가능성이 낮다.",
        "score": 8
    },

    {
        "keywords": [
            "cctv", "씨씨티비", "카메라", "감시카메라"
        ],
        "answer": "YES",
        "response": "CCTV에는 사건 직전 정확히 11분 38초의 영상 공백이 존재합니다.",
        "clue": "CCTV 영상에 11분 38초의 공백이 있다.",
        "score": 10
    },

    {
        "keywords": [
            "삭제", "지워", "사라진 기록",
            "출입기록", "출입 기록"
        ],
        "answer": "YES",
        "response": "사건 직전 출입 기록 하나가 시스템에서 삭제되어 있습니다.",
        "clue": "출입 기록 하나가 삭제되어 있다.",
        "score": 10
    },

    {
        "keywords": [
            "도윤", "최도윤", "관리인"
        ],
        "answer": "YES",
        "response": "최도윤은 건물 CCTV와 출입 시스템의 관리자 권한을 가지고 있습니다.",
        "clue": "최도윤에게 CCTV와 출입 시스템 접근 권한이 있다.",
        "score": 10
    },

    {
        "keywords": [
            "민재", "김민재"
        ],
        "answer": "YES",
        "response": "김민재는 사건 직전 피해자와 마지막으로 통화한 회사 동료입니다.",
        "clue": "김민재는 사건 직전 피해자와 통화했다.",
        "score": 6
    },

    {
        "keywords": [
            "서연", "박서연"
        ],
        "answer": "YES",
        "response": "박서연은 사건 당일 피해자에게 세 차례 전화를 걸었습니다.",
        "clue": "박서연은 사건 당일 피해자에게 세 차례 전화했다.",
        "score": 6
    },

    {
        "keywords": [
            "유진", "한유진", "동생"
        ],
        "answer": "YES",
        "response": "한유진은 피해자의 친동생이며 집의 예비 열쇠를 가지고 있습니다.",
        "clue": "한유진은 예비 열쇠를 가지고 있다.",
        "score": 7
    },

    {
        "keywords": [
            "열쇠", "키", "예비키", "예비 열쇠"
        ],
        "answer": "YES",
        "response": "피해자의 집에는 가족이 가지고 있는 예비 열쇠가 하나 더 존재합니다.",
        "clue": "예비 열쇠가 존재한다.",
        "score": 7
    },

    {
        "keywords": [
            "USB", "usb", "유에스비"
        ],
        "answer": "YES",
        "response": "책상 아래에서 검은색 USB가 발견되었습니다.",
        "clue": "책상 아래에서 검은색 USB가 발견됐다.",
        "score": 8
    },

    {
        "keywords": [
            "휴대폰", "핸드폰", "폰", "전화기"
        ],
        "answer": "YES",
        "response": "피해자의 휴대폰에는 삭제된 메시지 일부가 남아 있었습니다.",
        "clue": "피해자의 휴대폰에서 삭제된 메시지가 발견됐다.",
        "score": 7
    },

    {
        "keywords": [
            "메시지", "문자", "카톡", "대화"
        ],
        "answer": "YES",
        "response": "휴대폰에서 일부 삭제된 메시지가 복구되었습니다.",
        "clue": "삭제된 메시지 일부가 복구됐다.",
        "score": 7
    },

    {
        "keywords": [
            "마지막 통화", "마지막 전화"
        ],
        "answer": "NO",
        "response": "피해자의 마지막 통화 상대는 네 명의 용의자 중 누구도 아닙니다.",
        "clue": "마지막 통화 상대는 용의자가 아니다.",
        "score": 10
    },

    {
        "keywords": [
            "알리바이"
        ],
        "answer": "UNKNOWN",
        "response": "현재 확보된 자료만으로는 누구의 알리바이가 완벽하다고 말할 수 없습니다.",
        "clue": "네 명의 알리바이 모두 작은 빈틈이 있다.",
        "score": 5
    },

    {
        "keywords": [
            "돈", "돈 문제", "재산", "금전"
        ],
        "answer": "YES",
        "response": "피해자의 휴대폰에는 금전 문제를 암시하는 대화가 남아 있습니다.",
        "clue": "피해자에게 금전 문제와 관련된 갈등이 있었다.",
        "score": 6
    },

    {
        "keywords": [
            "외부", "외부인"
        ],
        "answer": "NO",
        "response": "현장에서는 외부에서 침입했다는 명확한 흔적이 발견되지 않았습니다.",
        "clue": "외부 침입 흔적이 발견되지 않았다.",
        "score": 7
    },

    {
        "keywords": [
            "관리실", "관리실 컴퓨터", "컴퓨터"
        ],
        "answer": "YES",
        "response": "관리실 컴퓨터에는 사건 직전 관리자 계정 접속 기록이 남아 있습니다.",
        "clue": "사건 직전 관리자 계정이 접속했다.",
        "score": 10
    },

    {
        "keywords": [
            "범인", "누가 죽", "누가 했", "누가 범인"
        ],
        "answer": "UNKNOWN",
        "response": "아직 범인을 단정할 단계가 아닙니다. CCTV 공백과 출입 기록을 먼저 확인하세요.",
        "clue": "범인을 특정하기에는 증거가 부족하다.",
        "score": 3
    }
]


# =========================================================
# 질문 분석
# =========================================================

def normalize(text):
    text = text.lower()
    text = text.replace(" ", "")
    text = text.replace("습니까", "")
    text = text.replace("나요", "")
    text = text.replace("인가요", "")
    text = text.replace("인가", "")
    text = text.replace("있나요", "")
    text = text.replace("있습니까", "")
    return text


def find_fact(question):

    q = normalize(question)

    # 특수 우선순위
    for fact in FACTS:

        for keyword in fact["keywords"]:

            if normalize(keyword) in q:

                return fact

    return None


# =========================================================
# 질문 처리
# =========================================================

def ask_question(question):

    if not question.strip():
        return

    if st.session_state.questions >= 15:
        st.warning("질문 기회를 모두 사용했습니다.")
        return

    fact = find_fact(question)

    if fact is None:

        result = {
            "answer": "UNKNOWN",
            "response": "현재 사건 기록에서는 그 질문에 대한 확실한 증거를 찾을 수 없습니다.",
            "clue": "새로운 질문이 필요하다.",
            "score": 1
        }

    else:
        result = fact

    st.session_state.questions += 1
    st.session_state.score += result["score"]

    if result["answer"] == "UNKNOWN":
        st.session_state.trust -= 1

    if result["clue"] not in st.session_state.clues:
        st.session_state.clues.append(result["clue"])

    record = {
        "question": question,
        "answer": result["answer"],
        "response": result["response"]
    }

    st.session_state.history.append(record)
    st.session_state.last_answer = record


# =========================================================
# 헤더
# =========================================================

header1, header2 = st.columns([3, 2])

with header1:

    st.markdown(
        """
        <div class="main-title">
        🕵️ 예스노 탐정
        </div>
        <div class="subtitle">
        CASE 001 · 잠긴 방의 진실
        </div>
        """,
        unsafe_allow_html=True
    )

with header2:

    h1, h2, h3, h4 = st.columns(4)

    with h1:
        st.markdown(
            f"""
            <div class="top-card">
            <div class="top-label">질문</div>
            <div class="top-value">
            {st.session_state.questions}/15
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h2:
        st.markdown(
            f"""
            <div class="top-card">
            <div class="top-label">수사 점수</div>
            <div class="top-value">
            {st.session_state.score}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h3:
        st.markdown(
            f"""
            <div class="top-card">
            <div class="top-label">신뢰도</div>
            <div class="top-value">
            {st.session_state.trust}%
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with h4:
        st.markdown(
            f"""
            <div class="top-card">
            <div class="top-label">단서</div>
            <div class="top-value">
            {len(st.session_state.clues)}
            </div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# =========================================================
# 메인 3열
# =========================================================

left, center, right = st.columns(
    [1.25, 1.05, 0.9],
    gap="small"
)


# =========================================================
# 왼쪽 — 사건
# =========================================================

with left:

    st.markdown(
        """
        <div class="panel-title">
        📁 사건 개요
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="case-box">

        <div class="case-title">
        CASE 001 · 잠긴 방의 진실
        </div>

        <br>

        <b>{CASE["time"]}</b>.

        <br>

        한 남자가 자신의 집에서
        의식을 잃은 채 발견되었습니다.

        <br><br>

        피해자는 <b>{CASE["victim"]}</b>.

        <br><br>

        현관문은 잠겨 있었고,
        창문 역시 닫혀 있었습니다.

        <br>

        외부 침입 흔적은 발견되지 않았습니다.

        <br><br>

        그런데 이상한 점이 하나 있습니다.

        <br><br>

        <span class="case-highlight">
        CCTV에 정확히 11분 38초의 공백이 존재합니다.
        </span>

        <br><br>

        사건 당시 건물 안에 있었던 사람은
        네 명.

        <br><br>

        <b>
        김민재 · 박서연 · 최도윤 · 한유진
        </b>

        <br><br>

        <span style="color:#64c5ff">
        당신은 사건 담당 탐정입니다.
        </span>

        <br>

        질문은 최대 15번.

        <br>

        모든 질문에는 YES / NO / UNKNOWN 중
        하나로 답이 나옵니다.

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="panel-title" style="margin-top:10px;">
        🔎 현장 기록
        </div>
        """,
        unsafe_allow_html=True
    )

    records = [
        ("발견 시각", "새벽 1시 18분"),
        ("현관문", "잠겨 있음"),
        ("창문", "닫혀 있음"),
        ("외부 침입", "흔적 없음"),
        ("CCTV", "11분 38초 공백"),
        ("삭제 기록", "출입 기록 1건"),
        ("예비 열쇠", "존재"),
        ("관리실", "접속 기록 존재"),
    ]

    for title, value in records:

        st.markdown(
            f"""
            <div style="
            display:flex;
            justify-content:space-between;
            border-bottom:1px solid #172936;
            padding:5px 2px;
            font-size:10px;
            ">
            <span style="color:#72889a;">{title}</span>
            <b style="color:#d9e5ed;">{value}</b>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 가운데 — 질문
# =========================================================

with center:

    st.markdown(
        """
        <div class="panel-title">
        🔍 예스노 심문
        </div>

        <div class="small">
        사건에 대해 자유롭게 질문하세요.
        질문 표현이 조금 달라도 같은 의미라면
        관련 증거를 찾아드립니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    question = st.text_input(
        "질문",
        placeholder="예: 현관으로 들어온 흔적은 없습니까?",
        label_visibility="collapsed"
    )

    if st.button(
        "🔍 질문하기",
        use_container_width=True
    ):

        ask_question(question)
        st.rerun()

    # 질문 예시
    st.markdown(
        """
        <div style="
        color:#647d91;
        font-size:9px;
        margin:7px 0;
        ">
        질문 예시
        </div>
        """,
        unsafe_allow_html=True
    )

    examples = [
        "현관으로 들어온 흔적은 없습니까?",
        "CCTV가 조작됐습니까?",
        "최도윤은 CCTV를 관리합니까?",
        "창문으로 들어왔나요?"
    ]

    for example in examples:

        if st.button(
            example,
            key="example_" + example,
            use_container_width=True
        ):

            ask_question(example)
            st.rerun()


    # 최근 답변
    st.markdown(
        """
        <div class="panel-title" style="margin-top:10px;">
        💬 최근 답변
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.last_answer:

        ans = st.session_state.last_answer

        css_class = {
            "YES": "yes",
            "NO": "no",
            "UNKNOWN": "unknown"
        }[ans["answer"]]

        st.markdown(
            f"""
            <div class="answer-box">

            <div class="{css_class}">
            {ans["answer"]}
            </div>

            <div class="answer-text">
            {html.escape(ans["response"])}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="answer-box">

            <div class="unknown">
            ?
            </div>

            <div class="answer-text">
            아직 질문하지 않았습니다.<br>
            사건에 대해 궁금한 것을 물어보세요.
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # 질문 기록
    st.markdown(
        """
        <div class="panel-title" style="margin-top:10px;">
        📜 질문 기록
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.history:

        for record in st.session_state.history[-4:][::-1]:

            color = {
                "YES": "#61dfa0",
                "NO": "#ff6671",
                "UNKNOWN": "#e5ce6c"
            }[record["answer"]]

            st.markdown(
                f"""
                <div style="
                border-bottom:1px solid #172936;
                padding:4px 2px;
                font-size:9px;
                ">
                <span style="color:#6c8497;">
                Q.
                </span>

                {html.escape(record["question"])}

                <span style="
                float:right;
                color:{color};
                font-weight:900;
                ">
                {record["answer"]}
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.markdown(
            """
            <div class="small">
            아직 질문 기록이 없습니다.
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 오른쪽 — 용의자
# =========================================================

with right:

    st.markdown(
        """
        <div class="panel-title">
        👤 용의자
        </div>
        """,
        unsafe_allow_html=True
    )

    for suspect in SUSPECTS:

        st.markdown(
            f"""
            <div class="suspect">

            <div class="suspect-name">
            {suspect["name"]}
            </div>

            <div class="suspect-role">
            {suspect["role"]}
            </div>

            <div class="suspect-text">
            {suspect["desc"]}
            </div>

            <div class="suspect-danger">
            ⚠ {suspect["suspicion"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 하단 — 단서
# =========================================================

st.markdown(
    """
    <div class="panel-title" style="margin-top:8px;">
    📌 확보한 단서
    </div>
    """,
    unsafe_allow_html=True
)

if st.session_state.clues:

    clue_cols = st.columns(
        min(len(st.session_state.clues), 5)
    )

    for i, clue in enumerate(
        st.session_state.clues[-5:]
    ):

        with clue_cols[i]:

            st.markdown(
                f"""
                <div class="clue">

                <div class="clue-title">
                단서 {i+1}
                </div>

                <div class="clue-text">
                {clue}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )

else:

    st.markdown(
        """
        <div class="small">
        질문을 통해 단서를 확보하세요.
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 최종 추리
# =========================================================

st.markdown(
    """
    <div style="
    border-top:1px solid #1b2c39;
    margin-top:8px;
    padding-top:8px;
    ">
    </div>
    """,
    unsafe_allow_html=True
)

if not st.session_state.game_over:

    a, b, c = st.columns([1, 1.8, 0.8])

    with a:

        final_suspect = st.selectbox(
            "범인 지목",
            [x["name"] for x in SUSPECTS]
        )

    with b:

        final_reason = st.text_input(
            "최종 추리",
            placeholder="왜 이 사람이 범인이라고 생각합니까?"
        )

    with c:

        if st.button(
            "🚨 추리 제출",
            use_container_width=True
        ):

            if len(st.session_state.clues) < 3:

                st.warning(
                    "단서를 최소 3개 확보하세요."
                )

            elif not final_reason.strip():

                st.warning(
                    "추리 이유를 입력하세요."
                )

            else:

                st.session_state.game_over = True

                if (
                    final_suspect == "최도윤"
                    and st.session_state.score >= 45
                ):

                    st.session_state.ending = "TRUE"

                elif final_suspect == "최도윤":

                    st.session_state.ending = "PARTIAL"

                else:

                    st.session_state.ending = "BAD"

                st.rerun()


# =========================================================
# 엔딩
# =========================================================

if st.session_state.game_over:

    if st.session_state.ending == "TRUE":

        st.success(
            "🏆 TRUE ENDING — 최도윤이 범인입니다. "
            "CCTV 공백, 삭제된 출입 기록, 관리자 계정 접속 기록이 "
            "하나의 흐름으로 연결됩니다."
        )

    elif st.session_state.ending == "PARTIAL":

        st.warning(
            "🟡 PARTIAL ENDING — 범인은 맞혔지만 "
            "결정적인 증거가 충분하지 않습니다."
        )

    else:

        st.error(
            "🔴 BAD ENDING — 잘못된 사람을 지목했습니다."
        )

    if st.button("🔄 사건 다시 시작"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()
