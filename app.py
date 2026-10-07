import streamlit as st

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 사건 데이터
# =========================================================

CASE = {
    "title": "잠긴 방의 진실",
    "time": "23:58",
    "place": "서울 · 아파트 1204호",
    "victim": "한도윤",

    "summary":
        "한 남자가 자신의 방 안에서 숨진 채 발견됐다. "
        "현관문은 잠겨 있었고 외부 침입 흔적은 발견되지 않았다.",

    "detail":
        "경찰은 자살 가능성을 먼저 생각했다. "
        "하지만 사건 당시 방의 에어컨은 18도로 설정되어 있었고, "
        "침대 옆에는 평소보다 하나 많은 컵이 놓여 있었다. "
        "무엇보다 피해자의 휴대전화에서 마지막 통화 기록 하나가 사라져 있었다."
}

SUSPECTS = {
    "김민재": (
        "피해자의 직장 동료",
        "사건 당일 피해자와 승진 문제로 크게 다퉜다."
    ),

    "박서연": (
        "피해자의 전 여자친구",
        "헤어진 뒤에도 피해자와 연락을 주고받고 있었다."
    ),

    "최도윤": (
        "아파트 관리인",
        "공동현관과 CCTV 기록에 접근할 수 있었다."
    )
}


# =========================================================
# 질문 데이터
# =========================================================

QA = [

    (
        ["현관", "침입", "문", "강제"],
        "아니오",
        "현관문과 잠금장치에는 강제로 들어온 흔적이 없습니다.",
        1
    ),

    (
        ["창문", "베란다", "외부"],
        "아니오",
        "창문과 베란다에서도 외부 침입 흔적은 발견되지 않았습니다.",
        1
    ),

    (
        ["cctv", "카메라", "영상"],
        "아니오",
        "CCTV에는 외부인이 건물 안으로 들어오는 장면이 없습니다.",
        2
    ),

    (
        ["휴대전화", "핸드폰", "전화", "폰"],
        "예",
        "피해자의 휴대전화는 방 안에서 발견됐습니다.",
        1
    ),

    (
        ["통화", "전화기록", "통화기록", "마지막 통화"],
        "예",
        "사건 직전 약 7분간의 통화 기록이 있었지만 이후 삭제됐습니다.",
        2
    ),

    (
        ["삭제", "지웠", "지워", "기록"],
        "예",
        "마지막 통화 기록 하나가 수동으로 삭제된 흔적이 있습니다.",
        2
    ),

    (
        ["컵", "잔", "음료"],
        "예",
        "침대 옆에는 평소보다 하나 많은 컵이 놓여 있었습니다.",
        1
    ),

    (
        ["혼자", "혼자 살", "동거"],
        "예",
        "피해자는 사건 당시 혼자 거주하고 있었습니다.",
        1
    ),

    (
        ["민재", "김민재"],
        "예",
        "김민재는 사건 당일 밤 피해자와 승진 문제로 크게 다퉜습니다.",
        2
    ),

    (
        ["서연", "박서연"],
        "예",
        "박서연은 사건 당일 피해자에게 세 차례 연락했습니다.",
        2
    ),

    (
        ["최도윤", "관리인", "관리자"],
        "예",
        "최도윤은 공동현관과 CCTV 기록에 접근할 수 있습니다.",
        2
    ),

    (
        ["에어컨", "18도", "온도"],
        "예",
        "에어컨은 비정상적으로 낮은 18도로 설정되어 있었습니다.",
        1
    ),

    (
        ["지문", "손자국"],
        "아니오",
        "지문이 하나도 없는 것은 아닙니다. 피해자 외의 희미한 흔적도 발견됐습니다.",
        2
    ),

    (
        ["혈흔", "피", "상처"],
        "예",
        "현장에는 사망 원인과 관련된 미세한 혈흔이 남아 있습니다.",
        1
    ),

    (
        ["시간", "몇 시", "23:58", "밤"],
        "예",
        "최초 신고 시각은 23시 58분입니다.",
        1
    ),

    (
        ["자살", "극단", "스스로"],
        "아니오",
        "현재 증거만으로 자살이라고 단정할 수 없습니다.",
        2
    ),

    (
        ["범인", "살인", "죽였"],
        "예",
        "타인의 개입 가능성을 배제할 수 없습니다.",
        2
    ),

    (
        ["열쇠", "비밀번호", "잠금"],
        "예",
        "문은 잠겨 있었지만 잠금 방식 때문에 내부자 가능성이 남습니다.",
        2
    )
]


# =========================================================
# 질문 처리
# =========================================================

def answer_question(question):

    question = question.strip().lower()

    if not question:
        return None

    for keywords, answer, reply, points in QA:

        for keyword in keywords:

            if keyword.lower() in question:

                return answer, reply, points

    return (
        "정보없음",
        "그 질문만으로는 확인할 수 없습니다. "
        "현관, CCTV, 휴대전화, 통화 기록, 용의자에 대해 물어보세요.",
        0
    )


# =========================================================
# 세션 상태
# =========================================================

defaults = {
    "questions": 0,
    "score": 0,
    "clues": 0,
    "history": [],
    "last_answer": "",
    "last_reply": ""
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 디자인
# =========================================================

st.markdown(
"""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800&display=swap'
);

html, body, [class*="css"] {
    font-family:'Noto Sans KR',sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 80% 5%,
            rgba(0,180,255,.08),
            transparent 28%
        ),

        radial-gradient(
            circle at 10% 100%,
            rgba(0,100,150,.08),
            transparent 30%
        ),

        #050a0f;

    color:#edf8ff;
}


header,
footer,
[data-testid="stSidebar"] {

    display:none !important;
}


.block-container {

    max-width:1500px !important;

    padding:
        15px
        30px
        10px !important;

    margin:auto !important;
}


/* 제목 */

.kicker {

    color:#39d0ff;

    font-size:10px;

    letter-spacing:5px;

    font-weight:800;
}


.title {

    font-size:34px;

    font-weight:800;

    letter-spacing:-2px;

    line-height:1;

    margin-top:4px;

    margin-bottom:8px;
}


.meta {

    color:#7891a1;

    font-size:10px;

    line-height:1.6;
}


/* 상단 정보 */

.metric {

    background:#0a131c;

    border:1px solid #1b3547;

    border-radius:9px;

    padding:9px 13px;

    height:65px;
}


.metric-label {

    color:#6e8b9e;

    font-size:10px;
}


.metric-value {

    color:#f3fbff;

    font-size:23px;

    font-weight:800;

    margin-top:2px;
}


/* 패널 */

.panel {

    background:#081019;

    border:1px solid #1b3547;

    border-radius:9px;

    overflow:hidden;
}


.panel-title {

    height:39px;

    padding:11px 14px;

    border-bottom:1px solid #1b3547;

    font-size:11px;

    font-weight:800;

    letter-spacing:1px;
}


.panel-title span {

    float:right;

    color:#38cfff;

    font-size:8px;

    letter-spacing:2px;
}


.content {

    padding:12px 14px;
}


/* 사건 사진 */

.photo {

    height:240px;

    border-radius:8px;

    border:1px solid #294b60;

    overflow:hidden;

    position:relative;

    background-image:

        linear-gradient(
            90deg,
            rgba(0,0,0,.08),
            rgba(0,0,0,.28)
        ),

        url(
        'https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=90'
        );

    background-size:cover;

    background-position:center;
}


.photo::after {

    content:"CASE 001 · EVIDENCE PHOTO";

    position:absolute;

    top:12px;

    left:12px;

    padding:6px 9px;

    background:rgba(2,8,12,.88);

    border:1px solid #28617a;

    border-radius:4px;

    color:#d8f7ff;

    font-size:8px;

    letter-spacing:2px;
}


/* 사건 설명 */

.case-box {

    background:#0b151e;

    border:1px solid #1d3b4d;

    border-radius:8px;

    padding:11px 13px;

    margin-top:9px;
}


.case-label {

    color:#35cfff;

    font-size:9px;

    letter-spacing:2px;

    font-weight:800;

    margin-bottom:6px;
}


.case-heading {

    font-size:18px;

    font-weight:800;

    margin-bottom:3px;
}


.case-text {

    color:#d5e4eb;

    font-size:12px;

    line-height:1.6;

    margin-top:7px;
}


.highlight {

    color:#51d8ff;

    font-weight:700;
}


/* 용의자 */

.suspect {

    background:#0b141c;

    border:1px solid #1d3544;

    border-radius:7px;

    padding:8px;

}


.suspect b {

    font-size:13px;
}


.suspect small {

    display:block;

    color:#7893a3;

    margin-top:2px;

    font-size:9px;
}


.suspect div {

    color:#a9bdc7;

    font-size:9px;

    line-height:1.4;

    margin-top:4px;
}


/* 답변 */

.answer {

    background:#071923;

    border:1px solid #17637d;

    border-radius:8px;

    padding:10px 12px;

    margin-top:8px;

    color:#e4f8ff;

    font-size:11px;

    line-height:1.5;
}


.answer b {

    color:#40d6ff;

    font-size:13px;
}


/* 입력 */

div[data-testid="stTextInput"] input {

    background:#0b141d !important;

    color:white !important;

    border:1px solid #31546a !important;

    border-radius:7px !important;

}


/* 선택 */

div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {

    background:#0b141d !important;

    color:white !important;

    border-color:#31546a !important;
}


/* 버튼 */

.stButton > button {

    background:#0c1a25 !important;

    color:#ecf9ff !important;

    border:1px solid #31566c !important;

    border-radius:7px !important;

    min-height:36px !important;

    font-weight:700 !important;
}


.stButton > button:hover {

    border-color:#38d4ff !important;

    color:#38d4ff !important;
}


button[kind="primary"] {

    background:#087fa9 !important;

    border-color:#2bd4ff !important;

    color:white !important;
}


/* 기록 */

.history {

    background:#071019;

    border:1px solid #1a3040;

    border-radius:7px;

    padding:8px;

    color:#9db3c0;

    font-size:9px;

    line-height:1.5;

    height:58px;

    overflow:hidden;
}


/* 경고 */

div[data-testid="stAlert"] {

    background:#071923 !important;

}


/* 모바일 */

@media(max-width:900px) {

    .block-container {

        padding:10px !important;
    }

    .title {

        font-size:28px;
    }

    .photo {

        height:200px;
    }

}

</style>
""",
unsafe_allow_html=True
)


# =========================================================
# 상단
# =========================================================

header_left, header_right = st.columns([2, 1])

with header_left:

    st.markdown(
        """
        <div class="kicker">
        CONFIDENTIAL · 34 CASE FILES
        </div>

        <div class="title">
        예스노 탐정
        </div>
        """,
        unsafe_allow_html=True
    )


with header_right:

    st.markdown(
        """
        <div style="
        text-align:right;
        color:#607b8b;
        font-size:9px;
        margin-top:10px;
        ">
        CASE 001 · ROUND 01 / 03<br>
        YES / NO ONLY
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 점수
# =========================================================

m1, m2, m3, m4 = st.columns(4)


with m1:

    st.markdown(
        f"""
        <div class="metric">
        <div class="metric-label">질문</div>
        <div class="metric-value">
        {st.session_state.questions}/15
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m2:

    st.markdown(
        f"""
        <div class="metric">
        <div class="metric-label">수사 점수</div>
        <div class="metric-value">
        {st.session_state.score}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m3:

    trust = max(
        55,
        100 - st.session_state.questions * 2
    )

    st.markdown(
        f"""
        <div class="metric">
        <div class="metric-label">신뢰도</div>
        <div class="metric-value">
        {trust}%
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with m4:

    st.markdown(
        f"""
        <div class="metric">
        <div class="metric-label">확보 단서</div>
        <div class="metric-value">
        {st.session_state.clues}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# =========================================================
# 메인
# =========================================================

left, right = st.columns(
    [1.55, .85],
    gap="medium"
)


# =========================================================
# 왼쪽 : 사건
# =========================================================

with left:

    st.markdown(
        """
        <div class="panel">

        <div class="panel-title">
        CASE FILE // 현장 기록

        <span>
        CONFIDENTIAL
        </span>

        </div>

        <div class="content">
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="case-box">

        <div class="case-label">
        CASE #001 · EVIDENCE
        </div>

        <div class="case-heading">
        {CASE["title"]}
        </div>

        <div class="meta">
        {CASE["place"]}
        ·
        {CASE["time"]}
        ·
        외부 침입 흔적 없음
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # 사진

    st.markdown(
        '<div class="photo"></div>',
        unsafe_allow_html=True
    )


    st.markdown(
        """
        <div class="meta" style="margin-top:5px;">
        ※ 사건 현장을 재구성한 증거 사진
        </div>
        """,
        unsafe_allow_html=True
    )


    # 사건 내용

    st.markdown(
        f"""
        <div class="case-box">

        <div class="case-label">
        CASE BRIEFING
        </div>

        <div class="case-text">
        {CASE["summary"]}
        </div>

        <div class="case-text">
        {CASE["detail"]}
        </div>

        <div class="case-text">

        <span class="highlight">
        당신의 목표
        </span>

        :
        질문 15개 안에 핵심 단서를 찾아내고
        사건의 진실을 밝혀내세요.

        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "</div></div>",
        unsafe_allow_html=True
    )


# =========================================================
# 오른쪽 : 심문
# =========================================================

with right:

    st.markdown(
        """
        <div class="panel">

        <div class="panel-title">

        INTERROGATION // 심문

        <span>
        YES / NO ONLY
        </span>

        </div>

        <div class="content">
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="meta">
        현재 질문
        {st.session_state.questions}/15
        </div>
        """,
        unsafe_allow_html=True
    )


    # 용의자 선택

    suspect = st.selectbox(
        "심문 대상",
        list(SUSPECTS.keys())
    )


    role, clue = SUSPECTS[suspect]


    st.markdown(
        f"""
        <div class="suspect">

        <b>
        {suspect}
        </b>

        <small>
        {role}
        </small>

        <div>
        {clue}
        </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.write("")


    # 질문 입력

    question = st.text_input(
        "예 / 아니오로 답할 수 있는 질문",
        placeholder="예: 현관에 들어온 흔적이 있습니까?",
        label_visibility="visible"
    )


    # 질문 버튼

    if st.button(
        "🔎 질문하기",
        type="primary",
        use_container_width=True
    ):

        if question.strip():

            if st.session_state.questions < 15:

                result = answer_question(question)

                answer, reply, points = result

                st.session_state.questions += 1

                st.session_state.score += points

                if points >= 2:

                    st.session_state.clues += 1


                st.session_state.last_answer = answer

                st.session_state.last_reply = reply


                record = (
                    f"Q{st.session_state.questions}. "
                    f"{question[:28]} → {answer}"
                )

                st.session_state.history.insert(
                    0,
                    record
                )

                st.session_state.history = (
                    st.session_state.history[:3]
                )

                st.rerun()


    # =====================================================
    # 빠른 질문
    # =====================================================

    st.markdown(
        """
        <div class="meta"
        style="margin-top:10px;margin-bottom:5px;">
        QUICK QUESTIONS
        </div>
        """,
        unsafe_allow_html=True
    )


    quick_questions = [

        "현관 침입 흔적?",

        "CCTV에 이상?",

        "피해자는 혼자였나?",

        "휴대전화 조작?",

        "마지막 통화가 있었나?",

        "김민재와 다퉜나?"
    ]


    q1, q2 = st.columns(2)


    for index, text in enumerate(quick_questions):

        col = q1 if index % 2 == 0 else q2

        with col:

            if st.button(
                text,
                key=f"quick_{index}",
                use_container_width=True
            ):

                if st.session_state.questions < 15:

                    result = answer_question(text)

                    answer, reply, points = result

                    st.session_state.questions += 1

                    st.session_state.score += points

                    if points >= 2:

                        st.session_state.clues += 1

                    st.session_state.last_answer = answer

                    st.session_state.last_reply = reply

                    st.session_state.history.insert(
                        0,
                        f"Q{st.session_state.questions}. "
                        f"{text} → {answer}"
                    )

                    st.session_state.history = (
                        st.session_state.history[:3]
                    )

                    st.rerun()


    # 답변

    if st.session_state.last_reply:

        st.markdown(
            f"""
            <div class="answer">

            <b>
            {st.session_state.last_answer}
            </b>

            ·

            {st.session_state.last_reply}

            </div>
            """,
            unsafe_allow_html=True
        )


    # 최근 기록

    st.markdown(
        """
        <div class="meta"
        style="margin-top:8px;">
        최근 수사 기록
        </div>
        """,
        unsafe_allow_html=True
    )


    if st.session_state.history:

        history_text = "<br>".join(
            st.session_state.history
        )

    else:

        history_text = (
            "아직 질문 기록이 없습니다."
        )


    st.markdown(
        f"""
        <div class="history">
        {history_text}
        </div>
        """,
        unsafe_allow_html=True
    )


    # 용의자 3명

    st.markdown(
        """
        <div class="meta"
        style="margin-top:8px;margin-bottom:5px;">
        SUSPECTS
        </div>
        """,
        unsafe_allow_html=True
    )


    s1, s2, s3 = st.columns(3)


    with s1:

        st.markdown(
            """
            <div class="suspect">
            <b>김민재</b>
            <small>직장 동료</small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with s2:

        st.markdown(
            """
            <div class="suspect">
            <b>박서연</b>
            <small>전 여자친구</small>
            </div>
            """,
            unsafe_allow_html=True
        )


    with s3:

        st.markdown(
            """
            <div class="suspect">
            <b>최도윤</b>
            <small>관리인</small>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        "</div></div>",
        unsafe_allow_html=True
    )


# =========================================================
# 결론
# =========================================================

st.write("")


a, b = st.columns([1, 2])


with a:

    if st.button(
        "🔄 수사 초기화",
        use_container_width=True
    ):

        for key in defaults:

            st.session_state[key] = defaults[key]

        st.rerun()


with b:

    if st.button(
        "🔐 15문제 후 최종 결론 확인",
        use_container_width=True
    ):

        if st.session_state.questions < 15:

            st.warning(
                "아직 수사가 끝나지 않았습니다. "
                f"현재 {st.session_state.questions}/15 질문을 사용했습니다."
            )

        else:

            st.success(
                "최종 분석: "
                "외부 침입 흔적은 없지만 내부자의 개입 가능성이 높습니다. "
                "특히 마지막 통화 기록 삭제와 사건 현장의 두 번째 컵이 "
                "핵심 단서입니다."
            )


st.markdown(
    """
    <div style="
    text-align:center;
    color:#456170;
    font-size:8px;
    letter-spacing:2px;
    margin-top:5px;
    ">
    YES NO DETECTIVE · CASE MANAGEMENT SYSTEM
    </div>
    """,
    unsafe_allow_html=True
)
