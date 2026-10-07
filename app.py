import streamlit as st

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 화면 크기 최적화 CSS
# =========================================================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-size: 13px !important;
}

.stApp {
    background: #080d18;
}

.block-container {
    max-width: 1500px !important;
    padding-top: 18px !important;
    padding-bottom: 10px !important;
    padding-left: 28px !important;
    padding-right: 28px !important;
}

/* 제목 */
.main-title {
    font-size: 28px;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}

.sub-title {
    font-size: 12px;
    color: #8b95a7;
    margin-top: -3px;
    margin-bottom: 10px;
}

/* 카드 */
.card {
    background: #111827;
    border: 1px solid #263149;
    border-radius: 10px;
    padding: 12px 14px;
    margin-bottom: 8px;
}

.card-title {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 6px;
}

/* 사건 설명 */
.case-text {
    color: #d7deea;
    font-size: 12px;
    line-height: 1.55;
}

/* 이미지 */
.stImage {
    margin: 0 !important;
}

.stImage img {
    height: 185px !important;
    object-fit: cover !important;
    border-radius: 8px !important;
}

/* 메트릭 */
[data-testid="stMetric"] {
    background: #111827;
    border: 1px solid #263149;
    padding: 7px 10px;
    border-radius: 8px;
}

[data-testid="stMetricLabel"] {
    font-size: 10px !important;
}

[data-testid="stMetricValue"] {
    font-size: 20px !important;
}

/* 버튼 */
.stButton button,
.stFormSubmitButton button {
    min-height: 36px !important;
    height: 36px !important;
    padding: 3px 10px !important;
    font-size: 13px !important;
    border-radius: 7px !important;
}

/* 입력창 */
.stTextInput input {
    height: 38px !important;
    font-size: 13px !important;
}

/* 라디오 */
.stRadio label {
    font-size: 12px !important;
}

/* 용의자 */
.suspect {
    background: #111827;
    border: 1px solid #263149;
    border-radius: 8px;
    padding: 9px;
    height: 92px;
}

.suspect-name {
    color: white;
    font-size: 14px;
    font-weight: 700;
}

.suspect-role {
    color: #60a5fa;
    font-size: 10px;
    margin-top: 2px;
}

.suspect-desc {
    color: #9ca3af;
    font-size: 10px;
    line-height: 1.3;
    margin-top: 4px;
}

/* 답변 */
.answer-box {
    background: #172036;
    border: 1px solid #34415e;
    border-radius: 8px;
    padding: 9px 12px;
    margin-top: 5px;
}

.answer-big {
    color: #7dd3fc;
    font-size: 18px;
    font-weight: 800;
}

.answer-detail {
    color: #d7deea;
    font-size: 12px;
}

/* 단서 */
.clue-box {
    background: #241f13;
    border-left: 3px solid #f59e0b;
    border-radius: 5px;
    padding: 6px 9px;
    color: #fde68a;
    font-size: 11px;
    margin-bottom: 4px;
}

/* 구분선 */
hr {
    margin: 8px 0 !important;
    border-color: #222c40 !important;
}

/* expander */
.streamlit-expanderHeader {
    font-size: 12px !important;
    padding: 5px !important;
}

/* 모바일이 아닌 PC 기준 */
@media (min-width: 1400px) {
    .block-container {
        padding-top: 12px !important;
    }

    .stImage img {
        height: 175px !important;
    }
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 상태
# =========================================================
if "history" not in st.session_state:
    st.session_state.history = []

if "clues" not in st.session_state:
    st.session_state.clues = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "ending" not in st.session_state:
    st.session_state.ending = None


# =========================================================
# 질문 엔진
# =========================================================
def answer_question(q):

    q = q.strip().lower()

    if not q:
        return "불명", "질문을 입력해주세요.", None, 0

    unrelated = [
        "문어", "고양이", "강아지", "날씨",
        "축구", "라면", "치킨", "학교",
        "연예인", "게임"
    ]

    for word in unrelated:
        if word in q:
            return (
                "아니오",
                "그 질문은 현재 사건과 관련이 없습니다.",
                None,
                0
            )

    if any(x in q for x in ["현관", "침입", "문을 부수", "강제로 들어"]):
        return (
            "아니오",
            "현관문에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 들어온 사람이 아닐 가능성이 높습니다.",
            2
        )

    if "창문" in q:
        return (
            "아니오",
            "창문에도 강제로 들어온 흔적은 없습니다.",
            None,
            1
        )

    if any(x in q for x in ["cctv", "카메라", "감시카메라"]):
        return (
            "예",
            "사건 직전 CCTV 기록에 정확히 17초의 공백이 있습니다.",
            "17초의 CCTV 공백은 중요한 단서입니다.",
            3
        )

    if any(x in q for x in ["전화", "통화", "휴대폰", "핸드폰", "문자"]):
        return (
            "예",
            "사건 직전 통화 기록 하나가 삭제되어 있습니다.",
            "삭제된 통화의 상대를 확인해야 합니다.",
            3
        )

    if "김민재" in q:
        return (
            "예",
            "피해자와 승진 문제로 다툰 적이 있습니다.",
            "김민재에게는 동기가 있지만 결정적인 증거는 없습니다.",
            2
        )

    if "박서연" in q:
        return (
            "예",
            "사건 직전 피해자에게 세 번 전화했습니다.",
            "통화 사실만으로 범행을 증명할 수는 없습니다.",
            2
        )

    if "최도윤" in q:
        return (
            "예",
            "피해자의 이웃이며 CCTV 사각지대를 알고 있었습니다.",
            "최도윤의 알리바이를 확인해야 합니다.",
            3
        )

    if "지문" in q:
        return (
            "예",
            "현장에서 여러 사람의 지문이 발견되었습니다.",
            "지문만으로 범인을 특정하기는 어렵습니다.",
            1
        )

    if any(x in q for x in ["혈흔", "피", "상처", "폭행", "살해"]):
        return (
            "예",
            "피해자는 머리에 강한 충격을 받은 흔적이 있습니다.",
            "둔기를 이용한 공격일 가능성이 있습니다.",
            2
        )

    if any(x in q for x in ["돈", "금품", "도난", "훔", "귀중품"]):
        return (
            "아니오",
            "귀중품은 그대로 남아 있습니다.",
            "범인의 목적은 돈이 아니었던 것으로 보입니다.",
            2
        )

    if any(x in q for x in ["잠겨", "잠금", "문이 잠", "열쇠"]):
        return (
            "예",
            "현관문은 발견 당시 잠겨 있었습니다.",
            "범인은 열쇠를 가지고 있었거나 피해자에게 문을 열어달라고 했을 수 있습니다.",
            2
        )

    if any(x in q for x in ["시간", "언제", "새벽", "2시", "17분"]):
        return (
            "예",
            "사건 발생 추정 시간은 새벽 2시 17분입니다.",
            "CCTV의 17초 공백과 사건 시간이 일치합니다.",
            2
        )

    if "알리바이" in q:
        return (
            "예",
            "세 용의자의 알리바이를 비교하면 최도윤의 진술에 가장 큰 빈틈이 있습니다.",
            "최도윤의 알리바이를 다시 확인해보세요.",
            3
        )

    if any(x in q for x in ["범인", "누가 죽", "누가 했", "살인범"]):
        return (
            "불명",
            "아직 범인을 바로 특정할 수 없습니다.",
            "CCTV 17초 + 삭제된 통화 + 알리바이를 연결해보세요.",
            1
        )

    if any(x in q for x in ["힌트", "도움", "모르겠", "어떻게"]):
        return (
            "힌트",
            "강제 침입이 없었다는 사실부터 생각해보세요.",
            "범인은 피해자가 들여보낸 사람일 가능성이 있습니다.",
            0
        )

    return (
        "불명",
        "그 질문만으로는 사건의 사실을 확인할 수 없습니다.",
        "현관, CCTV, 휴대전화, 용의자, 알리바이에 대해 질문해보세요.",
        0
    )


# =========================================================
# 엔딩
# =========================================================
if st.session_state.ending:

    st.markdown(
        '<div class="main-title">🔎 예스노 탐정</div>',
        unsafe_allow_html=True
    )

    if st.session_state.ending == "WIN":
        st.success(
            "🎉 사건 해결! 범인은 **최도윤**입니다. "
            "CCTV 17초 공백, 삭제된 통화 기록, 알리바이의 모순이 결정적인 증거였습니다."
        )

    elif st.session_state.ending == "PARTIAL":
        st.warning(
            "⚠️ 김민재에게 동기는 있었지만 결정적인 증거가 부족합니다."
        )

    else:
        st.error(
            "❌ 범인을 잘못 지목했습니다. "
            "CCTV 17초 + 삭제된 통화 + 알리바이를 다시 확인하세요."
        )

    if st.button("🔄 다시 시작", use_container_width=True):
        st.session_state.clear()
        st.rerun()

    st.stop()


# =========================================================
# HEADER
# =========================================================
st.markdown(
    '<div class="main-title">🔎 예스노 탐정</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">직접 질문해서 사건의 진실을 밝혀내세요.</div>',
    unsafe_allow_html=True
)


# =========================================================
# 상단 : 사건 / 사진
# =========================================================
left, right = st.columns([1.15, 0.85], gap="small")

with left:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-title">📁 새벽 2시 17분의 빈집</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="case-text">
        새벽 2시 17분, 한 남성이 자신의 집에서 쓰러진 채 발견되었습니다.<br>
        현관문은 잠겨 있었고 강제 침입 흔적은 없었습니다.<br>
        귀중품은 그대로였지만 CCTV에는 <b>17초의 공백</b>이 존재합니다.<br>
        피해자의 휴대전화에서는 사건 직전 통화 기록 하나가 삭제되어 있었습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


with right:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown(
        '<div class="card-title">📷 사건 현장</div>',
        unsafe_allow_html=True
    )

    st.image(
        "https://images.unsplash.com/photo-1511108690759-009324a90311?auto=format&fit=crop&w=1000&q=80",
        use_container_width=True
    )

    st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# 진행도
# =========================================================
m1, m2, m3 = st.columns(3)

with m1:
    st.metric("질문", len(st.session_state.history))

with m2:
    st.metric("점수", st.session_state.score)

with m3:
    st.metric("단서", len(st.session_state.clues))


# =========================================================
# 질문 + 최근 답변
# =========================================================
qcol, acol = st.columns([1.1, 0.9], gap="small")

with qcol:

    st.markdown(
        '<div class="card-title">🔎 탐정 질문</div>',
        unsafe_allow_html=True
    )

    with st.form("question_form", clear_on_submit=True):

        question = st.text_input(
            "질문",
            placeholder="예: 현관에 들어온 흔적은 있습니까?",
            label_visibility="collapsed"
        )

        submit = st.form_submit_button(
            "🔎 질문하기",
            use_container_width=True
        )

        if submit:

            answer, detail, clue, points = answer_question(question)

            if question.strip():

                st.session_state.history.append({
                    "question": question,
                    "answer": answer,
                    "detail": detail
                })

                st.session_state.last_answer = {
                    "answer": answer,
                    "detail": detail
                }

                st.session_state.score += points

                if clue and clue not in st.session_state.clues:
                    st.session_state.clues.append(clue)


with acol:

    st.markdown(
        '<div class="card-title">💬 최근 답변</div>',
        unsafe_allow_html=True
    )

    if st.session_state.last_answer:

        a = st.session_state.last_answer

        st.markdown(
            f"""
            <div class="answer-box">
                <div class="answer-big">{a["answer"]}</div>
                <div class="answer-detail">{a["detail"]}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.info("아직 질문하지 않았습니다.")


# =========================================================
# 하단 : 단서 / 용의자
# =========================================================
left2, right2 = st.columns([0.9, 1.1], gap="small")

with left2:

    st.markdown(
        '<div class="card-title">🧩 발견한 단서</div>',
        unsafe_allow_html=True
    )

    if st.session_state.clues:

        for i, clue in enumerate(st.session_state.clues, 1):

            st.markdown(
                f"""
                <div class="clue-box">
                <b>단서 {i}</b>　{clue}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.caption("질문을 통해 단서를 발견하세요.")

    if st.button("💡 힌트", use_container_width=True):

        st.info(
            "강제 침입 없음 → CCTV 17초 → 삭제된 통화 → "
            "최도윤의 알리바이를 순서대로 확인하세요."
        )


with right2:

    st.markdown(
        '<div class="card-title">👤 용의자</div>',
        unsafe_allow_html=True
    )

    s1, s2, s3 = st.columns(3)

    suspects = [
        ("김민재", "직장 동료", "승진 문제로 다툼"),
        ("박서연", "전 여자친구", "사건 직전 세 번 전화"),
        ("최도윤", "이웃", "CCTV 사각지대 파악")
    ]

    for col, (name, role, desc) in zip(
        [s1, s2, s3],
        suspects
    ):

        with col:

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
# 최종 범인 지목
# =========================================================
st.markdown("<hr>", unsafe_allow_html=True)

with st.form("accuse_form"):

    c1, c2 = st.columns([1, 0.55])

    with c1:

        suspect = st.radio(
            "🚨 최종 범인은 누구입니까?",
            ["김민재", "박서연", "최도윤"],
            horizontal=True
        )

    with c2:

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
