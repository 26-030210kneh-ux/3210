import streamlit as st
import re

# =========================================================
# PAGE
# =========================================================
st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# =========================================================
# CSS
# =========================================================
st.markdown("""
<style>
/* 전체 */
.stApp {
    background: #080b12;
    color: #e5e7eb;
}

.block-container {
    max-width: 1450px !important;
    padding-top: 8px !important;
    padding-bottom: 6px !important;
}

/* 기본 간격 제거 */
div[data-testid="stVerticalBlock"] {
    gap: 0.25rem;
}

hr {
    margin: 5px 0 !important;
    border-color: #202938;
}

/* 제목 */
.game-title {
    font-size: 25px;
    font-weight: 900;
    color: #f8fafc;
    margin: 0;
}

.game-subtitle {
    font-size: 11px;
    color: #7f8da3;
    margin-bottom: 6px;
}

/* 카드 */
.card {
    background: #101620;
    border: 1px solid #202a3a;
    border-radius: 9px;
    padding: 9px 11px;
    height: 100%;
}

.card-title {
    font-size: 14px;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 5px;
}

/* 사건 */
.case-title {
    font-size: 16px;
    font-weight: 900;
    color: #f8fafc;
    margin-bottom: 5px;
}

.case-text {
    font-size: 11px;
    line-height: 1.5;
    color: #cbd5e1;
}

/* 사진 고정 */
.photo-box img {
    height: 190px !important;
    width: 100% !important;
    object-fit: cover !important;
    border-radius: 7px !important;
}

/* 입력 */
.stTextInput input {
    height: 35px !important;
    background: #0d131d !important;
    border: 1px solid #303b4e !important;
    color: white !important;
    font-size: 12px !important;
}

.stTextInput label {
    display: none !important;
}

/* 버튼 */
.stButton button,
.stFormSubmitButton button {
    height: 35px !important;
    min-height: 35px !important;
    font-size: 12px !important;
    font-weight: 700 !important;
    border-radius: 6px !important;
}

/* 질문 로그 */
.chat-scroll {
    height: 180px;
    overflow-y: auto;
    padding-right: 5px;
}

.q {
    background: #172337;
    border-left: 3px solid #3b82f6;
    border-radius: 5px;
    padding: 6px 8px;
    margin-bottom: 3px;
}

.q-label {
    color: #60a5fa;
    font-size: 9px;
    font-weight: 800;
}

.q-text {
    color: #f8fafc;
    font-size: 11px;
    margin-top: 2px;
}

.a {
    background: #111821;
    border-left: 3px solid #64748b;
    border-radius: 5px;
    padding: 6px 8px;
    margin-bottom: 6px;
}

.a-label {
    color: #94a3b8;
    font-size: 9px;
    font-weight: 800;
}

.a-text {
    color: #e2e8f0;
    font-size: 11px;
    margin-top: 2px;
}

.clue-small {
    color: #fbbf24;
    font-size: 9px;
    margin-top: 3px;
}

/* 단서 */
.clue {
    background: #18160f;
    border: 1px solid #3b3018;
    border-radius: 5px;
    padding: 5px 7px;
    margin-bottom: 3px;
    color: #fcd34d;
    font-size: 10px;
}

/* 용의자 */
.suspect {
    background: #111821;
    border: 1px solid #242f40;
    border-radius: 6px;
    padding: 6px;
    min-height: 55px;
}

.suspect-name {
    font-size: 12px;
    font-weight: 800;
    color: white;
}

.suspect-role {
    font-size: 9px;
    color: #60a5fa;
}

.suspect-desc {
    font-size: 9px;
    color: #94a3b8;
    margin-top: 2px;
}

/* 메트릭 */
[data-testid="stMetric"] {
    background: #101620;
    border: 1px solid #202a3a;
    border-radius: 7px;
    padding: 3px 8px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 8px !important;
}

[data-testid="stMetricValue"] {
    font-size: 15px !important;
}

/* radio */
div[role="radiogroup"] {
    gap: 5px !important;
}

div[role="radiogroup"] label {
    font-size: 11px !important;
}

/* 안내문 */
.stAlert {
    padding: 5px 8px !important;
    font-size: 11px !important;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# SESSION
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

그러나 사건 직전 CCTV에는 정확히 17초의 공백이 있었고,
피해자의 휴대전화에서는 통화 기록 하나가 삭제되어 있었다.

범인은 피해자와 아는 사이일 가능성이 있다.
"""

# 너무 큰 사진이 화면을 먹지 않도록 고정 영역에서 사용
CASE_IMAGE = (
    "https://images.unsplash.com/"
    "photo-1511108690759-009324a90311"
    "?auto=format&fit=crop&w=800&q=70"
)

SUSPECTS = {
    "김민재": (
        "직장 동료",
        "피해자와 승진 문제로 다툼"
    ),
    "박서연": (
        "전 여자친구",
        "사건 직전 세 차례 전화"
    ),
    "최도윤": (
        "이웃",
        "CCTV 사각지대를 알고 있음"
    ),
}


# =========================================================
# QUESTION ENGINE
# =========================================================
def clean(text):
    text = text.strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


def answer_question(question):
    q = clean(question)

    # -----------------------------
    # 무관한 질문
    # -----------------------------
    if any(x in q for x in [
        "문어", "고양이", "강아지", "치킨",
        "축구", "날씨", "라면", "게임"
    ]):
        return (
            "아니오",
            "그 질문은 이 사건과 관련이 없습니다.",
            None,
            0
        )

    # -----------------------------
    # 현관 / 침입
    # -----------------------------
    if any(x in q for x in [
        "현관", "침입", "침입흔적",
        "강제로 들어", "문을 부수", "강제 침입"
    ]):
        return (
            "아니오",
            "현관문에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 들어온 사람이 아닐 가능성이 높습니다.",
            2
        )

    # -----------------------------
    # 창문
    # -----------------------------
    if "창문" in q:
        return (
            "아니오",
            "창문에도 침입 흔적은 발견되지 않았습니다.",
            None,
            1
        )

    # -----------------------------
    # CCTV
    # -----------------------------
    if any(x in q for x in [
        "cctv", "카메라", "감시카메라",
        "영상", "화면"
    ]):
        return (
            "예",
            "사건 직전 CCTV에 정확히 17초의 공백이 있습니다.",
            "CCTV의 17초 공백은 사건의 핵심 단서입니다.",
            3
        )

    # -----------------------------
    # 전화 / 통화
    # -----------------------------
    if any(x in q for x in [
        "전화", "통화", "휴대폰",
        "핸드폰", "문자", "연락"
    ]):
        return (
            "예",
            "사건 직전 통화 기록 하나가 삭제되어 있습니다.",
            "삭제된 통화의 상대를 확인해야 합니다.",
            3
        )

    # -----------------------------
    # 김민재
    # -----------------------------
    if "김민재" in q:
        return (
            "예",
            "김민재는 피해자와 승진 문제로 심하게 다툰 적이 있습니다.",
            "김민재에게는 동기가 있지만 결정적인 증거는 없습니다.",
            2
        )

    # -----------------------------
    # 박서연
    # -----------------------------
    if "박서연" in q:
        return (
            "예",
            "박서연은 사건 직전 피해자에게 세 번 전화했습니다.",
            "박서연의 행동은 수상하지만 이것만으로 범인이라고 할 수 없습니다.",
            2
        )

    # -----------------------------
    # 최도윤
    # -----------------------------
    if "최도윤" in q:
        return (
            "예",
            "최도윤은 피해자의 이웃이며 CCTV 사각지대를 알고 있었습니다.",
            "최도윤의 알리바이를 확인해보는 것이 중요합니다.",
            3
        )

    # -----------------------------
    # 알리바이
    # -----------------------------
    if "알리바이" in q:
        return (
            "예",
            "세 사람 중 최도윤의 알리바이에 가장 큰 의문점이 있습니다.",
            "최도윤의 진술과 삭제된 통화 기록을 비교해보세요.",
            3
        )

    # -----------------------------
    # 지문
    # -----------------------------
    if "지문" in q:
        return (
            "예",
            "현장에서는 여러 사람의 지문이 발견되었습니다.",
            "지문만으로 범인을 특정하기는 어렵습니다.",
            1
        )

    # -----------------------------
    # 돈 / 도난
    # -----------------------------
    if any(x in q for x in [
        "돈", "금품", "도난",
        "귀중품", "훔쳐", "훔겼"
    ]):
        return (
            "아니오",
            "귀중품은 그대로 남아 있습니다.",
            "범인의 목적은 금품이 아니었습니다.",
            2
        )

    # -----------------------------
    # 잠금 / 열쇠
    # -----------------------------
    if any(x in q for x in [
        "잠겨", "잠금", "열쇠",
        "잠갔", "잠궜"
    ]):
        return (
            "예",
            "피해자가 발견되었을 때 현관문은 잠겨 있었습니다.",
            "범인은 열쇠를 가지고 있었거나 피해자가 직접 들여보냈을 가능성이 있습니다.",
            2
        )

    # -----------------------------
    # 시간
    # -----------------------------
    if any(x in q for x in [
        "몇 시", "언제", "시간",
        "새벽", "2시", "17분"
    ]):
        return (
            "예",
            "사건 발생 추정 시간은 새벽 2시 17분입니다.",
            "사건 시간과 CCTV의 17초 공백을 연결해보세요.",
            2
        )

    # -----------------------------
    # 피해자
    # -----------------------------
    if any(x in q for x in [
        "피해자", "죽은 사람", "사망자"
    ]):
        return (
            "예",
            "피해자는 사건 당시 자신의 집 안에 혼자 있었습니다.",
            "범인은 피해자의 집 안으로 자연스럽게 들어갈 수 있었던 사람일 가능성이 있습니다.",
            1
        )

    # -----------------------------
    # 범인 질문
    # -----------------------------
    if any(x in q for x in [
        "범인이", "범인", "누가", "살인범"
    ]):
        return (
            "불명",
            "현재 정보만으로 범인을 확정할 수 없습니다.",
            "강제 침입 없음 → CCTV 17초 → 삭제된 통화 → 알리바이를 연결하세요.",
            1
        )

    # -----------------------------
    # 힌트
    # -----------------------------
    if any(x in q for x in [
        "힌트", "도움", "모르겠"
    ]):
        return (
            "힌트",
            "현관문이 잠겨 있었다는 사실만 보지 말고, 누가 자연스럽게 들어올 수 있었는지 생각해보세요.",
            "이웃 최도윤의 CCTV 지식과 알리바이를 확인하세요.",
            0
        )

    # -----------------------------
    # 알 수 없는 질문
    # -----------------------------
    return (
        "불명",
        "현재 사건 기록으로는 확인할 수 없습니다.",
        "현관, CCTV, 통화 기록, 용의자, 알리바이에 대해 질문해보세요.",
        0
    )


# =========================================================
# ENDING
# =========================================================
if st.session_state.ending:

    st.markdown(
        '<div class="game-title">🔎 예스노 탐정</div>',
        unsafe_allow_html=True
    )

    if st.session_state.ending == "WIN":
        st.success(
            "🎉 사건 해결! 범인은 **최도윤**입니다. "
            "CCTV 17초 공백 + 삭제된 통화 + 알리바이의 모순이 연결됩니다."
        )

    elif st.session_state.ending == "PARTIAL":
        st.warning(
            "⚠️ 김민재에게는 동기가 있었지만 결정적인 증거가 없습니다."
        )

    else:
        st.error(
            "❌ 범인을 잘못 지목했습니다. "
            "CCTV 17초와 삭제된 통화, 알리바이를 다시 확인하세요."
        )

    if st.button("🔄 다시 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.stop()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="game-title">🔎 예스노 탐정</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="game-subtitle">'
    '질문은 당신이 직접 합니다 · 탐정 시스템은 사건 정보에 따라 답합니다'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# TOP : 사건 + 사진
# =========================================================
left, right = st.columns([1.25, 0.75], gap="small")

with left:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        f'<div class="case-title">📁 {CASE_TITLE}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="case-text">{CASE_STORY}</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-title">📷 사건 현장</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="photo-box">', unsafe_allow_html=True)

    st.image(
        CASE_IMAGE,
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# STATS
# =========================================================
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("🕵️ 질문", len(st.session_state.history))

with m2:
    st.metric("🧩 단서", len(st.session_state.clues))

with m3:
    st.metric("⭐ 탐정 점수", st.session_state.score)


# =========================================================
# QUESTION
# =========================================================
st.markdown(
    '<div class="card-title">🕵️ 당신의 질문</div>',
    unsafe_allow_html=True
)

with st.form("question_form", clear_on_submit=True):

    q1, q2 = st.columns([5, 1])

    with q1:
        question = st.text_input(
            "question",
            placeholder="예: 현관에 강제로 들어온 흔적이 있습니까?",
            label_visibility="collapsed"
        )

    with q2:
        submit_question = st.form_submit_button(
            "🔎 질문하기",
            use_container_width=True
        )

    if submit_question and question.strip():

        answer, detail, clue, points = answer_question(question)

        st.session_state.history.append({
            "question": question.strip(),
            "answer": answer,
            "detail": detail,
            "clue": clue
        })

        if clue and clue not in st.session_state.clues:
            st.session_state.clues.append(clue)

        st.session_state.score += points

        st.rerun()


# =========================================================
# CHAT LOG
# =========================================================
st.markdown(
    '<div class="card-title">💬 탐정 기록</div>',
    unsafe_allow_html=True
)

with st.container(height=190, border=True):

    if not st.session_state.history:

        st.caption(
            "아직 질문이 없습니다. 위 입력창에 사건에 대해 자유롭게 질문하세요."
        )

    else:

        for item in st.session_state.history:

            st.markdown(
                f"""
                <div class="q">
                    <div class="q-label">🕵️ 나</div>
                    <div class="q-text">{item["question"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class="a">
                    <div class="a-label">🔎 탐정 시스템</div>
                    <div class="a-text">
                        <b>{item["answer"]}</b> · {item["detail"]}
                    </div>
                    {
                        f'<div class="clue-small">🧩 {item["clue"]}</div>'
                        if item["clue"] else ""
                    }
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# BOTTOM : CLUES + SUSPECTS
# =========================================================
left_bottom, right_bottom = st.columns([0.85, 1.15], gap="small")


# -------------------------
# clues
# -------------------------
with left_bottom:

    st.markdown(
        '<div class="card-title">🧩 발견한 단서</div>',
        unsafe_allow_html=True
    )

    if st.session_state.clues:

        for clue in st.session_state.clues[-5:]:

            st.markdown(
                f'<div class="clue">• {clue}</div>',
                unsafe_allow_html=True
            )

    else:

        st.caption("질문을 통해 단서를 찾아보세요.")


# -------------------------
# suspects
# -------------------------
with right_bottom:

    st.markdown(
        '<div class="card-title">👤 용의자</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    for col, (name, data) in zip(
        [s1, s2, s3],
        SUSPECTS.items()
    ):

        with col:

            role, desc = data

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
# ACCUSATION
# =========================================================
st.markdown("<hr>", unsafe_allow_html=True)

with st.form("accuse_form"):

    a1, a2 = st.columns([4, 1])

    with a1:

        suspect = st.radio(
            "🚨 최종 범인을 지목하세요",
            list(SUSPECTS.keys()),
            horizontal=True
        )

    with a2:

        st.write("")

        accuse = st.form_submit_button(
            "🚨 범인 지목",
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
