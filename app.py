import streamlit as st
import re

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide"
)

# =========================================================
# COMPACT STYLE
# =========================================================
st.markdown("""
<style>
.stApp {
    background:#080b11;
    color:#e5e7eb;
}

.block-container {
    max-width:1280px !important;
    padding-top:5px !important;
    padding-bottom:3px !important;
}

/* 전체 간격 축소 */
div[data-testid="stVerticalBlock"] {
    gap:0.15rem;
}

h1,h2,h3,p {
    margin-top:0 !important;
    margin-bottom:3px !important;
}

hr {
    margin:3px 0 !important;
    border-color:#202735;
}

/* 제목 */
.title {
    font-size:21px;
    font-weight:900;
    color:#f8fafc;
}

.sub {
    font-size:9px;
    color:#718096;
    margin-bottom:3px;
}

/* 사건 카드 */
.case-card {
    background:#0e141d;
    border:1px solid #202938;
    border-radius:7px;
    padding:7px 9px;
}

.case-title {
    font-size:13px;
    font-weight:800;
    color:#f8fafc;
}

.case-text {
    font-size:9px;
    line-height:1.35;
    color:#b9c3d2;
}

/* 섹션 */
.section {
    font-size:11px;
    font-weight:800;
    color:#e2e8f0;
    margin:3px 0 2px;
}

/* 입력 */
.stTextInput input {
    height:30px !important;
    min-height:30px !important;
    background:#0d131c !important;
    border:1px solid #293447 !important;
    color:#fff !important;
    font-size:10px !important;
}

.stTextInput label {
    display:none !important;
}

/* 버튼 */
.stButton button,
.stFormSubmitButton button {
    height:30px !important;
    min-height:30px !important;
    padding:0 7px !important;
    font-size:10px !important;
    border-radius:5px !important;
}

/* 기록 */
.chatbox {
    background:#0c1119;
    border:1px solid #202938;
    border-radius:7px;
    height:205px;
    overflow-y:auto;
    padding:6px;
}

.question {
    background:#142036;
    border-left:2px solid #3b82f6;
    border-radius:4px;
    padding:4px 6px;
    margin-bottom:2px;
}

.question-label {
    font-size:8px;
    color:#60a5fa;
    font-weight:800;
}

.question-text {
    font-size:10px;
    color:#f8fafc;
}

.answer {
    background:#111821;
    border-left:2px solid #64748b;
    border-radius:4px;
    padding:4px 6px;
    margin-bottom:4px;
}

.answer-label {
    font-size:8px;
    color:#94a3b8;
    font-weight:800;
}

.answer-text {
    font-size:10px;
    color:#dbe4ef;
}

.clue-inline {
    font-size:8px;
    color:#fbbf24;
}

/* 단서 */
.clue {
    background:#17150e;
    border:1px solid #332b17;
    border-radius:4px;
    padding:4px 6px;
    margin-bottom:2px;
    color:#fcd34d;
    font-size:9px;
}

/* 용의자 */
.suspect {
    background:#10161f;
    border:1px solid #222d3d;
    border-radius:5px;
    padding:5px;
    height:48px;
}

.suspect-name {
    color:white;
    font-size:10px;
    font-weight:800;
}

.suspect-role {
    color:#60a5fa;
    font-size:8px;
}

.suspect-desc {
    color:#7f8da0;
    font-size:7px;
}

/* metric */
[data-testid="stMetric"] {
    background:#0e141d;
    border:1px solid #202938;
    border-radius:5px;
    padding:2px 6px !important;
}

[data-testid="stMetricLabel"] {
    font-size:7px !important;
}

[data-testid="stMetricValue"] {
    font-size:13px !important;
}

/* radio */
div[role="radiogroup"] {
    gap:4px !important;
}

div[role="radiogroup"] label {
    font-size:9px !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# STATE
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "clues" not in st.session_state:
    st.session_state.clues = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "ending" not in st.session_state:
    st.session_state.ending = None


# =========================================================
# DATA
# =========================================================
CASE_TITLE = "새벽 2시 17분의 빈집"

CASE_STORY = """
새벽 2시 17분, 피해자가 자신의 집에서 쓰러진 채 발견되었다.
현관문은 잠겨 있었고 강제 침입 흔적은 없었다.
귀중품도 그대로였다.
하지만 사건 직전 CCTV에는 17초의 공백이 있었고,
피해자의 휴대전화에서는 통화 기록 하나가 삭제되어 있었다.
범인은 피해자와 아는 사이일 가능성이 있다.
"""

SUSPECTS = {
    "김민재": ("직장 동료", "승진 문제로 피해자와 다툼"),
    "박서연": ("전 여자친구", "사건 직전 세 차례 전화"),
    "최도윤": ("이웃", "CCTV 사각지대를 알고 있음")
}


# =========================================================
# QUESTION LOGIC
# =========================================================
def clean(q):
    return re.sub(r"\s+", " ", q.strip().lower())


def investigate(question):
    q = clean(question)

    if not q:
        return "불명", "질문을 입력해주세요.", None, 0

    # 무관한 질문
    if any(x in q for x in [
        "문어", "고양이", "강아지",
        "축구", "치킨", "날씨", "라면"
    ]):
        return (
            "아니오",
            "그 질문은 사건과 관련이 없습니다.",
            None,
            0
        )

    # 현관
    if any(x in q for x in [
        "현관", "침입", "강제로 들어",
        "강제 침입", "문을 부수"
    ]):
        return (
            "아니오",
            "현관에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 들어온 사람이 아닐 가능성이 높습니다.",
            2
        )

    # CCTV
    if any(x in q for x in [
        "cctv", "카메라", "감시카메라", "영상"
    ]):
        return (
            "예",
            "사건 직전 CCTV에 정확히 17초의 공백이 있습니다.",
            "CCTV의 17초 공백이 핵심 단서입니다.",
            3
        )

    # 전화
    if any(x in q for x in [
        "전화", "통화", "휴대폰", "핸드폰", "문자"
    ]):
        return (
            "예",
            "사건 직전 통화 기록 하나가 삭제되어 있습니다.",
            "삭제된 통화의 상대를 확인해야 합니다.",
            3
        )

    # 용의자
    if "김민재" in q:
        return (
            "예",
            "김민재는 피해자와 승진 문제로 다툰 적이 있습니다.",
            "동기는 있지만 결정적인 증거는 없습니다.",
            2
        )

    if "박서연" in q:
        return (
            "예",
            "박서연은 사건 직전 피해자에게 세 번 전화했습니다.",
            "수상하지만 이것만으로 범인이라고 할 수 없습니다.",
            2
        )

    if "최도윤" in q:
        return (
            "예",
            "최도윤은 CCTV 사각지대를 알고 있었습니다.",
            "최도윤의 알리바이를 확인해보세요.",
            3
        )

    # 알리바이
    if "알리바이" in q:
        return (
            "예",
            "최도윤의 알리바이에 가장 큰 의문점이 있습니다.",
            "최도윤의 진술과 통화 기록을 비교하세요.",
            3
        )

    # 금품
    if any(x in q for x in [
        "돈", "금품", "귀중품",
        "도난", "훔쳐", "훔겼"
    ]):
        return (
            "아니오",
            "귀중품은 그대로 남아 있습니다.",
            "범인의 목적은 금품이 아니었습니다.",
            2
        )

    # 창문
    if "창문" in q:
        return (
            "아니오",
            "창문에도 침입 흔적은 없습니다.",
            None,
            1
        )

    # 잠금
    if any(x in q for x in [
        "잠겨", "잠금", "열쇠", "잠갔"
    ]):
        return (
            "예",
            "발견 당시 현관문은 잠겨 있었습니다.",
            "범인은 자연스럽게 집 안으로 들어왔을 가능성이 있습니다.",
            2
        )

    # 시간
    if any(x in q for x in [
        "시간", "몇 시", "언제", "2시", "17분", "새벽"
    ]):
        return (
            "예",
            "사건 발생 추정 시간은 새벽 2시 17분입니다.",
            "CCTV의 17초 공백과 연결해보세요.",
            2
        )

    # 피해자
    if any(x in q for x in [
        "피해자", "혼자", "사망자"
    ]):
        return (
            "예",
            "피해자는 사건 당시 집 안에 혼자 있었습니다.",
            "범인은 피해자가 경계하지 않았던 사람일 가능성이 있습니다.",
            1
        )

    # 범인
    if any(x in q for x in [
        "범인", "누가", "살인범"
    ]):
        return (
            "불명",
            "현재 정보만으로 범인을 확정할 수 없습니다.",
            "CCTV + 삭제된 통화 + 알리바이를 연결하세요.",
            1
        )

    # 힌트
    if any(x in q for x in [
        "힌트", "도움", "모르겠"
    ]):
        return (
            "힌트",
            "강제 침입이 없었다는 사실에 집중하세요.",
            "피해자가 경계하지 않았던 사람을 찾아보세요.",
            0
        )

    return (
        "불명",
        "현재 확보된 사건 정보만으로는 확인할 수 없습니다.",
        "현관, CCTV, 통화, 용의자, 알리바이에 대해 질문해보세요.",
        0
    )


# =========================================================
# END
# =========================================================
if st.session_state.ending:

    st.markdown(
        '<div class="title">🔎 예스노 탐정</div>',
        unsafe_allow_html=True
    )

    if st.session_state.ending == "WIN":
        st.success(
            "🎉 사건 해결! 범인은 **최도윤**입니다. "
            "CCTV 17초 공백, 삭제된 통화, 알리바이의 모순이 연결됩니다."
        )

    elif st.session_state.ending == "PARTIAL":
        st.warning(
            "⚠️ 김민재에게 동기는 있었지만 결정적인 증거가 없습니다."
        )

    else:
        st.error(
            "❌ 범인을 잘못 지목했습니다. 단서를 다시 확인하세요."
        )

    if st.button("🔄 다시 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.stop()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="title">🔎 예스노 탐정</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub">사건을 읽고 원하는 질문을 직접 입력하세요.</div>',
    unsafe_allow_html=True
)


# =========================================================
# CASE
# =========================================================
st.markdown('<div class="case-card">', unsafe_allow_html=True)

st.markdown(
    f'<div class="case-title">📁 {CASE_TITLE}</div>',
    unsafe_allow_html=True
)

st.markdown(
    f'<div class="case-text">{CASE_STORY}</div>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# STATS
# =========================================================
x1, x2, x3 = st.columns(3)

with x1:
    st.metric("질문", len(st.session_state.history))

with x2:
    st.metric("단서", len(st.session_state.clues))

with x3:
    st.metric("점수", st.session_state.score)


# =========================================================
# QUESTION
# =========================================================
st.markdown(
    '<div class="section">🕵️ 질문하기</div>',
    unsafe_allow_html=True
)

with st.form("question_form", clear_on_submit=True):

    q1, q2 = st.columns([6, 0.8])

    with q1:
        question = st.text_input(
            "question",
            placeholder="예: 현관에 강제로 들어온 흔적이 있습니까?",
            label_visibility="collapsed"
        )

    with q2:
        submit = st.form_submit_button(
            "질문",
            use_container_width=True
        )

    if submit and question.strip():

        answer, detail, clue, points = investigate(question)

        st.session_state.history.append({
            "question": question.strip(),
            "answer": answer,
            "detail": detail,
            "clue": clue
        })

        st.session_state.score += points

        if clue and clue not in st.session_state.clues:
            st.session_state.clues.append(clue)

        st.rerun()


# =========================================================
# CHAT
# =========================================================
st.markdown(
    '<div class="section">💬 탐정 기록</div>',
    unsafe_allow_html=True
)

with st.container(height=205, border=True):

    if not st.session_state.history:

        st.caption("아직 질문이 없습니다.")

    else:

        for item in st.session_state.history:

            st.markdown(
                f"""
                <div class="question">
                    <div class="question-label">🕵️ 나</div>
                    <div class="question-text">
                        {item["question"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            clue_html = ""

            if item["clue"]:
                clue_html = f"""
                <div class="clue-inline">
                    🧩 {item["clue"]}
                </div>
                """

            st.markdown(
                f"""
                <div class="answer">
                    <div class="answer-label">🔎 탐정 시스템</div>
                    <div class="answer-text">
                        <b>{item["answer"]}</b> · {item["detail"]}
                    </div>
                    {clue_html}
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# CLUE + SUSPECT
# =========================================================
c1, c2 = st.columns([1, 2])

with c1:

    st.markdown(
        '<div class="section">🧩 단서</div>',
        unsafe_allow_html=True
    )

    if st.session_state.clues:

        for clue in st.session_state.clues[-4:]:

            st.markdown(
                f'<div class="clue">• {clue}</div>',
                unsafe_allow_html=True
            )

    else:
        st.caption("아직 발견한 단서가 없습니다.")


with c2:

    st.markdown(
        '<div class="section">👤 용의자</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    for col, (name, info) in zip(
        [s1, s2, s3],
        SUSPECTS.items()
    ):

        with col:

            role, desc = info

            st.markdown(
                f"""
                <div class="suspect">
                    <div class="suspect-name">{name}</div>
                    <div class="suspect-role">{role}</div>
                    <div class="suspect-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# ACCUSE
# =========================================================
st.markdown("<hr>", unsafe_allow_html=True)

with st.form("accuse_form"):

    a1, a2 = st.columns([5, 1])

    with a1:

        suspect = st.radio(
            "🚨 범인 지목",
            list(SUSPECTS.keys()),
            horizontal=True
        )

    with a2:

        st.write("")

        accuse = st.form_submit_button(
            "범인 지목",
            use_container_width=True
        )

    if accuse:

        if suspect == "최도윤":
            st.session_state.ending = "WIN"

        elif suspect == "김민재":
            st.session_state.ending = "PARTIAL"

        else:
            st.session_state.ending = "LOSE"

        st.rerun()
