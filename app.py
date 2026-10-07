import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide"
)

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
body {
    background-color: #0b1020;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    margin-bottom: 5px;
}

.sub-title {
    color: #9ca3af;
    font-size: 16px;
    margin-bottom: 20px;
}

.box {
    background-color: #151c30;
    border: 1px solid #29324a;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 15px;
}

.case-title {
    font-size: 25px;
    font-weight: 700;
    color: white;
}

.answer {
    background-color: #202a43;
    border-radius: 12px;
    padding: 18px;
    margin-top: 12px;
    color: white;
}

.answer-big {
    font-size: 30px;
    font-weight: 800;
    color: #7dd3fc;
}

.clue {
    background-color: #292218;
    border-left: 4px solid #f59e0b;
    padding: 15px;
    border-radius: 8px;
    color: #fde68a;
    margin-top: 10px;
}

.suspect {
    background-color: #151c30;
    border: 1px solid #29324a;
    border-radius: 12px;
    padding: 15px;
    min-height: 130px;
}

.small {
    color: #9ca3af;
    font-size: 14px;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 세션 상태
# -----------------------------
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


# -----------------------------
# 사건 데이터
# -----------------------------
CASE_TITLE = "새벽 2시 17분의 빈집"

CASE_TEXT = """
새벽 2시 17분, 한 남성이 자신의 집에서 쓰러진 채 발견되었습니다.

현관문은 잠겨 있었고 강제로 침입한 흔적은 없었습니다.
집 안에는 몸싸움의 흔적이 일부 남아 있었지만,
귀중품은 그대로였습니다.

이상한 점은 CCTV 기록에 **정확히 17초의 공백**이 있다는 것.

그리고 피해자의 휴대전화에서는 사건 직전에 걸려온
전화 기록 하나가 삭제되어 있었습니다.

당신은 사건의 진실을 밝혀야 합니다.
"""

SUSPECTS = {
    "김민재": {
        "role": "피해자의 직장 동료",
        "reason": "최근 승진 문제로 피해자와 심하게 다툼.",
    },
    "박서연": {
        "role": "피해자의 전 여자친구",
        "reason": "사건 당일 피해자에게 세 번 전화함.",
    },
    "최도윤": {
        "role": "피해자의 이웃",
        "reason": "CCTV 위치와 사각지대를 매우 잘 알고 있음.",
    },
}


# -----------------------------
# 질문 판정
# -----------------------------
def answer_question(q):
    q = q.strip().lower()

    if not q:
        return (
            "불명",
            "질문을 입력해주세요.",
            None,
            0
        )

    # 무관한 질문
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

    # 현관 / 침입
    if any(x in q for x in ["현관", "침입", "문을 부수", "강제로 들어"]):
        return (
            "아니오",
            "현관문에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 들어온 사람이 아닐 가능성이 높습니다.",
            2
        )

    # 창문
    if "창문" in q:
        return (
            "아니오",
            "창문 역시 깨졌거나 강제로 열린 흔적은 없습니다.",
            None,
            1
        )

    # CCTV
    if any(x in q for x in ["cctv", "카메라", "감시카메라"]):
        return (
            "예",
            "CCTV에는 사건 직전 약 17초 동안 기록이 비어 있습니다.",
            "17초의 CCTV 공백은 우연으로 보기 어렵습니다.",
            3
        )

    # 피해자
    if "피해자" in q:
        return (
            "예",
            "피해자는 사건 직전 누군가와 연락하고 있었습니다.",
            None,
            1
        )

    # 전화 / 휴대폰
    if any(x in q for x in ["전화", "통화", "휴대폰", "핸드폰", "문자"]):
        return (
            "예",
            "사건 직전 통화 기록 하나가 삭제되어 있습니다.",
            "삭제된 통화 기록의 상대를 확인해야 합니다.",
            3
        )

    # 김민재
    if "김민재" in q:
        return (
            "예",
            "김민재는 피해자와 승진 문제로 다툰 적이 있습니다.",
            "김민재에게는 동기가 있지만 결정적인 증거는 없습니다.",
            2
        )

    # 박서연
    if "박서연" in q:
        return (
            "예",
            "박서연은 사건 직전 피해자에게 세 차례 전화했습니다.",
            "하지만 전화만으로 범행을 증명할 수는 없습니다.",
            2
        )

    # 최도윤
    if "최도윤" in q:
        return (
            "예",
            "최도윤은 피해자의 이웃이며 CCTV 사각지대를 잘 알고 있었습니다.",
            "최도윤의 알리바이와 CCTV 공백을 함께 확인해야 합니다.",
            3
        )

    # 지문
    if "지문" in q:
        return (
            "예",
            "현장에서 여러 사람의 지문이 발견되었습니다.",
            "지문만으로는 범인을 특정하기 어렵습니다.",
            1
        )

    # 혈흔 / 상처
    if any(x in q for x in ["혈흔", "피", "상처", "폭행", "살해"]):
        return (
            "예",
            "피해자는 머리에 강한 충격을 받은 흔적이 있습니다.",
            "범행은 둔기를 이용한 공격일 가능성이 있습니다.",
            2
        )

    # 금품
    if any(x in q for x in ["돈", "금품", "도난", "훔", "귀중품"]):
        return (
            "아니오",
            "귀중품은 그대로 남아 있습니다. 단순 절도 사건은 아닙니다.",
            "범인의 목적은 돈이 아니었던 것으로 보입니다.",
            2
        )

    # 잠금
    if any(x in q for x in ["잠겨", "잠금", "문이 잠", "열쇠"]):
        return (
            "예",
            "현관문은 사건 발견 당시 잠겨 있었습니다.",
            "범인은 열쇠를 가지고 있었거나 피해자에게 문을 열어달라고 했을 가능성이 있습니다.",
            2
        )

    # 시간
    if any(x in q for x in ["몇 시", "시간", "언제", "새벽", "2시", "17분"]):
        return (
            "예",
            "사건이 발생한 것으로 추정되는 시간은 새벽 2시 17분입니다.",
            "CCTV의 17초 공백과 사건 시간이 일치합니다.",
            2
        )

    # 알리바이
    if "알리바이" in q:
        return (
            "예",
            "세 용의자의 알리바이를 비교하면 최도윤의 진술에 가장 큰 빈틈이 있습니다.",
            "최도윤의 알리바이를 다시 확인해보세요.",
            3
        )

    # 범인
    if any(x in q for x in ["범인", "누가 죽", "누가 했", "살인범"]):
        return (
            "불명",
            "아직 범인을 바로 특정할 수 없습니다. 용의자들의 행동과 증거를 연결해보세요.",
            "CCTV 17초 + 삭제된 통화 + 알리바이를 연결해보세요.",
            1
        )

    # 힌트
    if any(x in q for x in ["힌트", "도움", "모르겠", "어떻게"]):
        return (
            "힌트",
            "강제 침입이 없었다는 사실부터 생각해보세요.",
            "범인은 피해자가 안으로 들여보낸 사람일 가능성이 있습니다.",
            0
        )

    # 기본
    return (
        "불명",
        "그 질문만으로는 사건의 사실을 확인할 수 없습니다.",
        "현관, CCTV, 휴대전화, 용의자, 알리바이에 대해 질문해보세요.",
        0
    )


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div class="main-title">🔎 예스노 탐정</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">당신이 직접 질문하고 사건의 진실을 밝혀내세요.</div>',
    unsafe_allow_html=True
)


# -----------------------------
# 엔딩 화면
# -----------------------------
if st.session_state.ending:

    st.markdown("## 🚨 사건 수사 결과")

    if st.session_state.ending == "WIN":
        st.success(
            """
            ## 🎉 사건 해결!

            범인은 **최도윤**이었습니다.

            최도윤은 피해자의 이웃으로 CCTV 사각지대를 알고 있었습니다.
            사건 직전 CCTV에는 17초의 공백이 발생했고,
            피해자의 휴대전화에서는 수상한 통화 기록이 삭제되어 있었습니다.

            결정적으로 최도윤의 알리바이는 통화 기록과 맞지 않았습니다.

            **당신은 사건의 진실을 밝혀냈습니다. 🔎**
            """
        )

    elif st.session_state.ending == "PARTIAL":
        st.warning(
            """
            ## ⚠️ 의심은 맞았지만 증거가 부족합니다.

            김민재에게는 분명한 범행 동기가 있었습니다.

            하지만 CCTV 공백과 삭제된 통화 기록,
            그리고 알리바이까지 설명하지 못했습니다.

            **범인을 특정하기에는 증거가 부족합니다.**
            """
        )

    else:
        st.error(
            """
            ## ❌ 범인을 잘못 지목했습니다.

            사건의 핵심은 단순한 원한이 아닙니다.

            **CCTV 17초의 공백**
            +
            **삭제된 통화 기록**
            +
            **알리바이의 모순**

            이 세 가지를 연결해야 합니다.
            """
        )

    if st.button("🔄 사건 다시 시작", use_container_width=True):
        st.session_state.history = []
        st.session_state.clues = []
        st.session_state.score = 0
        st.session_state.last_answer = None
        st.session_state.ending = None
        st.rerun()

    st.stop()


# -----------------------------
# 사건 + 이미지
# -----------------------------
left, right = st.columns([1, 1])

with left:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.markdown(
        '<div class="case-title">📁 사건 파일</div>',
        unsafe_allow_html=True
    )

    st.markdown(f"### {CASE_TITLE}")
    st.write(CASE_TEXT)

    st.info("💡 사건을 읽은 뒤, 궁금한 것을 직접 질문하세요.")

    st.markdown("</div>", unsafe_allow_html=True)


with right:
    st.markdown('<div class="box">', unsafe_allow_html=True)
    st.markdown("### 📷 사건 현장")

    # 외부 이미지가 안 뜨더라도 게임 자체는 정상 작동
    st.image(
        "https://images.unsplash.com/photo-1511108690759-009324a90311?auto=format&fit=crop&w=1200&q=80",
        use_container_width=True
    )

    st.caption("새벽 2시 17분 — 피해자의 집")
    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------
# 진행 정보
# -----------------------------
a, b, c = st.columns(3)

with a:
    st.metric("질문 횟수", len(st.session_state.history))

with b:
    st.metric("획득 점수", st.session_state.score)

with c:
    st.metric("발견한 단서", len(st.session_state.clues))


# -----------------------------
# 질문
# -----------------------------
st.markdown("## 🔎 직접 질문하세요")

st.write(
    "예: `현관에 들어온 흔적은 있습니까?`  "
    "`CCTV에 이상이 있습니까?`  "
    "`최도윤은 수상합니까?`"
)

with st.form("question_form", clear_on_submit=True):

    question = st.text_input(
        "탐정의 질문",
        placeholder="여기에 질문을 직접 입력하세요..."
    )

    submitted = st.form_submit_button(
        "🔎 질문하기",
        use_container_width=True
    )

    if submitted:

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


# -----------------------------
# 최근 답변
# -----------------------------
if st.session_state.last_answer:

    st.markdown("## 💬 탐정 기록")

    result = st.session_state.last_answer

    st.markdown(
        f"""
        <div class="answer">
            <div class="answer-big">{result["answer"]}</div>
            <br>
            {result["detail"]}
        </div>
        """,
        unsafe_allow_html=True
    )


# -----------------------------
# 단서
# -----------------------------
if st.session_state.clues:

    st.markdown("## 🧩 발견한 단서")

    for i, clue in enumerate(st.session_state.clues, 1):
        st.markdown(
            f"""
            <div class="clue">
                <b>단서 {i}</b><br>
                {clue}
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# 힌트
# -----------------------------
st.markdown("## 💡 탐정 힌트")

if st.button("💡 힌트 보기", use_container_width=True):

    hints = [
        "① 강제 침입 흔적이 없습니다. 범인은 피해자가 들여보낸 사람일 수 있습니다.",
        "② CCTV에는 정확히 17초의 공백이 있습니다.",
        "③ 피해자의 휴대전화에서 사건 직전 통화 기록 하나가 삭제되었습니다.",
        "④ 최도윤은 CCTV 사각지대를 알고 있었습니다.",
        "⑤ 최도윤의 알리바이와 통화 기록을 비교해보세요."
    ]

    for hint in hints:
        st.info(hint)


# -----------------------------
# 용의자
# -----------------------------
st.markdown("## 👤 용의자")

cols = st.columns(3)

for col, (name, data) in zip(cols, SUSPECTS.items()):

    with col:
        st.markdown(
            f"""
            <div class="suspect">
                <h3>{name}</h3>
                <b>{data["role"]}</b>
                <p class="small">{data["reason"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )


# -----------------------------
# 질문 기록
# -----------------------------
if st.session_state.history:

    with st.expander("📜 지금까지의 질문 기록"):

        for i, item in enumerate(
            st.session_state.history,
            1
        ):
            st.write(
                f"**{i}. {item['question']}**"
            )
            st.write(
                f"→ {item['answer']} : {item['detail']}"
            )


# -----------------------------
# 범인 지목
# -----------------------------
st.markdown("## 🚨 최종 범인 지목")

st.write(
    "충분한 단서를 모았다면 범인을 지목하세요."
)

with st.form("accuse_form"):

    suspect = st.radio(
        "범인은 누구입니까?",
        [
            "김민재",
            "박서연",
            "최도윤"
        ],
        horizontal=True
    )

    accuse = st.form_submit_button(
        "🚨 최종 범인으로 지목하기",
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
