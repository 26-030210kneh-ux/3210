import streamlit as st

# =========================================================
# 설정
# =========================================================
st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide"
)

# =========================================================
# 화면 스타일
# =========================================================
st.markdown("""
<style>
.stApp {
    background: #080b12;
}

.block-container {
    max-width: 1400px;
    padding-top: 12px;
    padding-bottom: 8px;
}

/* 전체 글씨 크기 */
html, body {
    font-size: 13px;
}

/* 제목 */
.title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    line-height: 1;
}

.subtitle {
    color: #8d96a8;
    font-size: 12px;
    margin-top: 5px;
    margin-bottom: 10px;
}

/* 카드 */
.card {
    background: #111722;
    border: 1px solid #242d3d;
    border-radius: 10px;
    padding: 12px;
    margin-bottom: 8px;
}

.card h3 {
    margin: 0 0 7px 0;
    color: white;
    font-size: 16px;
}

/* 사건 내용 */
.case {
    color: #d6dbe5;
    font-size: 12px;
    line-height: 1.55;
}

/* 질문 */
.question-box {
    background: #18243a;
    border-radius: 8px;
    padding: 9px 11px;
    margin-bottom: 5px;
}

.question-label {
    color: #60a5fa;
    font-size: 10px;
    font-weight: bold;
}

.question-text {
    color: white;
    font-size: 13px;
    margin-top: 3px;
}

/* 답변 */
.answer-box {
    background: #141a26;
    border-radius: 8px;
    padding: 9px 11px;
    margin-bottom: 7px;
    border-left: 3px solid #64748b;
}

.answer-yes {
    color: #4ade80;
    font-size: 17px;
    font-weight: bold;
}

.answer-no {
    color: #f87171;
    font-size: 17px;
    font-weight: bold;
}

.answer-unknown {
    color: #fbbf24;
    font-size: 17px;
    font-weight: bold;
}

.answer-detail {
    color: #cbd5e1;
    font-size: 12px;
    margin-top: 3px;
}

/* 단서 */
.clue {
    background: #201b10;
    border-left: 3px solid #f59e0b;
    border-radius: 5px;
    padding: 7px 9px;
    margin-bottom: 4px;
    color: #fde68a;
    font-size: 11px;
}

/* 용의자 */
.suspect {
    background: #111722;
    border: 1px solid #242d3d;
    border-radius: 8px;
    padding: 8px;
    height: 85px;
}

.suspect-name {
    color: white;
    font-size: 14px;
    font-weight: bold;
}

.suspect-role {
    color: #60a5fa;
    font-size: 10px;
}

.suspect-info {
    color: #9ca3af;
    font-size: 10px;
    margin-top: 4px;
}

/* 버튼 */
.stButton button,
.stFormSubmitButton button {
    height: 36px;
    min-height: 36px;
    border-radius: 7px;
    font-size: 12px;
}

/* 입력창 */
.stTextInput input {
    height: 36px;
    font-size: 12px;
}

/* metric */
[data-testid="stMetric"] {
    background: #111722;
    border: 1px solid #242d3d;
    border-radius: 8px;
    padding: 6px 10px;
}

[data-testid="stMetricValue"] {
    font-size: 19px !important;
}

[data-testid="stMetricLabel"] {
    font-size: 10px !important;
}

hr {
    margin: 7px 0;
    border-color: #242d3d;
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# 상태
# =========================================================
if "messages" not in st.session_state:
    st.session_state.messages = []

if "clues" not in st.session_state:
    st.session_state.clues = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "ending" not in st.session_state:
    st.session_state.ending = None


# =========================================================
# 사건 정보
# =========================================================
CASE = {
    "title": "새벽 2시 17분의 빈집",
    "story": """
새벽 2시 17분, 피해자가 자신의 집에서 쓰러진 채 발견되었다.

현관문은 잠겨 있었지만 강제 침입 흔적은 없었다.
귀중품도 그대로였다.

하지만 사건 직전 CCTV에는 17초의 공백이 있었고,
피해자의 휴대전화에서는 통화 기록 하나가 삭제되어 있었다.

범인은 피해자와 아는 사이였을 가능성이 있다.
""",
    "image": "https://images.unsplash.com/photo-1511108690759-009324a90311?auto=format&fit=crop&w=1000&q=80"
}

SUSPECTS = {
    "김민재": {
        "role": "직장 동료",
        "info": "피해자와 승진 문제로 다툼."
    },
    "박서연": {
        "role": "전 여자친구",
        "info": "사건 직전 피해자에게 세 번 전화."
    },
    "최도윤": {
        "role": "이웃",
        "info": "CCTV 사각지대를 잘 알고 있음."
    }
}


# =========================================================
# 질문 분석
# =========================================================
def investigate(question):

    q = question.lower().strip()

    # 빈 질문
    if not q:
        return (
            "불명",
            "질문을 입력해주세요.",
            None,
            0
        )

    # 무관한 질문
    unrelated = [
        "문어",
        "고양이",
        "강아지",
        "날씨",
        "축구",
        "치킨",
        "라면",
        "연예인",
        "게임"
    ]

    if any(word in q for word in unrelated):
        return (
            "아니오",
            "아니오. 사건과 관련 없는 질문입니다.",
            None,
            0
        )

    # =====================================================
    # 현관
    # =====================================================
    if any(word in q for word in [
        "현관",
        "침입",
        "침입흔적",
        "문을 부수",
        "강제로 들어"
    ]):
        return (
            "아니오",
            "현관문에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 들어온 사람이 아닐 가능성이 높습니다.",
            2
        )

    # =====================================================
    # 창문
    # =====================================================
    if "창문" in q:
        return (
            "아니오",
            "창문에도 강제로 들어온 흔적은 없습니다.",
            None,
            1
        )

    # =====================================================
    # CCTV
    # =====================================================
    if any(word in q for word in [
        "cctv",
        "카메라",
        "감시카메라",
        "영상"
    ]):
        return (
            "예",
            "사건 직전 CCTV에 정확히 17초의 공백이 있습니다.",
            "CCTV의 17초 공백은 사건의 핵심 단서입니다.",
            3
        )

    # =====================================================
    # 전화
    # =====================================================
    if any(word in q for word in [
        "전화",
        "통화",
        "휴대폰",
        "핸드폰",
        "문자"
    ]):
        return (
            "예",
            "사건 직전 통화 기록 하나가 삭제되어 있습니다.",
            "삭제된 통화의 상대를 찾아야 합니다.",
            3
        )

    # =====================================================
    # 김민재
    # =====================================================
    if "김민재" in q:
        return (
            "예",
            "김민재는 피해자와 승진 문제로 심하게 다툰 적이 있습니다.",
            "김민재에게는 범행 동기가 있습니다. 하지만 결정적 증거는 없습니다.",
            2
        )

    # =====================================================
    # 박서연
    # =====================================================
    if "박서연" in q:
        return (
            "예",
            "박서연은 사건 직전 피해자에게 세 차례 전화했습니다.",
            "박서연은 수상하지만 통화만으로 범행을 증명할 수 없습니다.",
            2
        )

    # =====================================================
    # 최도윤
    # =====================================================
    if "최도윤" in q:
        return (
            "예",
            "최도윤은 피해자의 이웃이며 CCTV 사각지대를 알고 있었습니다.",
            "최도윤의 알리바이를 확인해보는 것이 중요합니다.",
            3
        )

    # =====================================================
    # 알리바이
    # =====================================================
    if "알리바이" in q:
        return (
            "예",
            "세 용의자 중 최도윤의 알리바이에 가장 큰 의문점이 있습니다.",
            "최도윤의 진술과 통화 기록을 비교해보세요.",
            3
        )

    # =====================================================
    # 지문
    # =====================================================
    if "지문" in q:
        return (
            "예",
            "현장에서는 여러 사람의 지문이 발견되었습니다.",
            "지문만으로 범인을 특정하기는 어렵습니다.",
            1
        )

    # =====================================================
    # 피 / 상처
    # =====================================================
    if any(word in q for word in [
        "피",
        "혈흔",
        "상처",
        "폭행",
        "머리"
    ]):
        return (
            "예",
            "피해자의 머리에서 강한 충격을 받은 흔적이 발견되었습니다.",
            "둔기를 이용한 공격일 가능성이 있습니다.",
            2
        )

    # =====================================================
    # 돈
    # =====================================================
    if any(word in q for word in [
        "돈",
        "금품",
        "도난",
        "귀중품",
        "훔"
    ]):
        return (
            "아니오",
            "귀중품은 그대로 남아 있습니다.",
            "범인의 목적은 금품이 아니었습니다.",
            2
        )

    # =====================================================
    # 잠금
    # =====================================================
    if any(word in q for word in [
        "잠겨",
        "잠금",
        "열쇠",
        "잠갔"
    ]):
        return (
            "예",
            "피해자가 발견되었을 때 현관문은 잠겨 있었습니다.",
            "범인은 열쇠를 가지고 있었거나 피해자가 직접 들여보냈을 가능성이 있습니다.",
            2
        )

    # =====================================================
    # 시간
    # =====================================================
    if any(word in q for word in [
        "언제",
        "몇 시",
        "시간",
        "새벽",
        "2시",
        "17분"
    ]):
        return (
            "예",
            "사건 발생 추정 시간은 새벽 2시 17분입니다.",
            "CCTV의 17초 공백과 사건 시간이 일치합니다.",
            2
        )

    # =====================================================
    # 범인
    # =====================================================
    if any(word in q for word in [
        "범인",
        "누가",
        "살인범"
    ]):
        return (
            "불명",
            "아직 범인을 확정할 수 없습니다.",
            "CCTV 17초 + 삭제된 통화 + 알리바이를 연결해보세요.",
            1
        )

    # =====================================================
    # 힌트
    # =====================================================
    if any(word in q for word in [
        "힌트",
        "도움",
        "모르겠",
        "어려워"
    ]):
        return (
            "힌트",
            "강제 침입이 없었다는 사실에 주목하세요.",
            "범인은 피해자가 안으로 들여보낸 사람일 가능성이 높습니다.",
            0
        )

    # =====================================================
    # 알 수 없는 질문
    # =====================================================
    return (
        "불명",
        "현재 확보된 정보만으로는 확인할 수 없습니다.",
        "현관, CCTV, 휴대전화, 용의자, 알리바이에 대해 질문해보세요.",
        0
    )


# =========================================================
# 엔딩
# =========================================================
if st.session_state.ending:

    st.markdown(
        '<div class="title">🔎 예스노 탐정</div>',
        unsafe_allow_html=True
    )

    st.markdown("<hr>", unsafe_allow_html=True)

    if st.session_state.ending == "WIN":

        st.success(
            """
            🎉 **사건 해결!**

            범인은 **최도윤**입니다.

            CCTV 17초의 공백,
            삭제된 통화 기록,
            그리고 최도윤의 알리바이 모순.

            세 가지 증거가 하나로 연결됩니다.
            """
        )

    elif st.session_state.ending == "PARTIAL":

        st.warning(
            """
            ⚠️ **의심은 맞았지만 증거 부족**

            김민재에게는 범행 동기가 있었지만
            결정적인 증거가 없습니다.
            """
        )

    else:

        st.error(
            """
            ❌ **범인을 잘못 지목했습니다.**

            CCTV 17초,
            삭제된 통화,
            알리바이를 다시 확인하세요.
            """
        )

    if st.button("🔄 사건 다시 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.stop()


# =========================================================
# 제목
# =========================================================
st.markdown(
    '<div class="title">🔎 예스노 탐정</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">질문은 당신이 직접 합니다. 탐정의 질문에 사건이 답합니다.</div>',
    unsafe_allow_html=True
)


# =========================================================
# 사건 영역
# =========================================================
left, right = st.columns([1.15, 0.85], gap="small")

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        f"<h3>📁 {CASE['title']}</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="case">{CASE["story"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        "<h3>📷 사건 현장</h3>",
        unsafe_allow_html=True
    )

    st.image(
        CASE["image"],
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 정보
# =========================================================
a, b, c = st.columns(3)

with a:
    st.metric(
        "질문",
        len(st.session_state.messages)
    )

with b:
    st.metric(
        "점수",
        st.session_state.score
    )

with c:
    st.metric(
        "단서",
        len(st.session_state.clues)
    )


# =========================================================
# 질문 입력
# =========================================================
st.markdown(
    '<div class="card-title">🕵️ 당신의 질문</div>',
    unsafe_allow_html=True
)

with st.form("question_form", clear_on_submit=True):

    question = st.text_input(
        "질문을 입력하세요",
        placeholder="예: 현관에 들어온 흔적은 없습니까?",
        label_visibility="collapsed"
    )

    ask = st.form_submit_button(
        "🔎 질문하기",
        use_container_width=True
    )

    if ask and question.strip():

        answer, detail, clue, points = investigate(question)

        st.session_state.messages.append({
            "question": question,
            "answer": answer,
            "detail": detail
        })

        st.session_state.score += points

        if clue and clue not in st.session_state.clues:
            st.session_state.clues.append(clue)


# =========================================================
# 질문 / 답변 기록
# =========================================================
if st.session_state.messages:

    st.markdown(
        '<div class="card-title">💬 탐정 기록</div>',
        unsafe_allow_html=True
    )

    # 최신 질문부터 표시
    for item in reversed(st.session_state.messages):

        st.markdown(
            f"""
            <div class="question-box">
                <div class="question-label">🕵️ 나의 질문</div>
                <div class="question-text">{item["question"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if item["answer"] == "예":
            answer_class = "answer-yes"
        elif item["answer"] == "아니오":
            answer_class = "answer-no"
        else:
            answer_class = "answer-unknown"

        st.markdown(
            f"""
            <div class="answer-box">
                <div class="{answer_class}">
                    🔎 {item["answer"]}
                </div>
                <div class="answer-detail">
                    {item["detail"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 하단 영역
# =========================================================
left2, right2 = st.columns([0.9, 1.1], gap="small")


# =========================================================
# 단서
# =========================================================
with left2:

    st.markdown(
        '<div class="card-title">🧩 발견한 단서</div>',
        unsafe_allow_html=True
    )

    if st.session_state.clues:

        for i, clue in enumerate(
            st.session_state.clues,
            1
        ):

            st.markdown(
                f"""
                <div class="clue">
                    <b>단서 {i}</b>　{clue}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption(
            "질문을 통해 단서를 찾아보세요."
        )

    if st.button(
        "💡 힌트 보기",
        use_container_width=True
    ):

        st.info(
            "강제 침입 없음 → CCTV 17초 → 삭제된 통화 → 최도윤 알리바이"
        )


# =========================================================
# 용의자
# =========================================================
with right2:

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

            st.markdown(
                f"""
                <div class="suspect">
                    <div class="suspect-name">{name}</div>
                    <div class="suspect-role">{data["role"]}</div>
                    <div class="suspect-info">{data["info"]}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 범인 지목
# =========================================================
st.markdown("<hr>", unsafe_allow_html=True)

with st.form("accuse_form"):

    col1, col2 = st.columns([1, 0.35])

    with col1:

        suspect = st.radio(
            "🚨 최종 범인은 누구입니까?",
            list(SUSPECTS.keys()),
            horizontal=True
        )

    with col2:

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
