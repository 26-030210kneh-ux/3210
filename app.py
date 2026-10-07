import streamlit as st

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
.stApp {
    background:#060b11;
    color:white;
}

.block-container {
    max-width:1400px;
    padding-top:20px;
    padding-bottom:10px;
}

h1 {
    font-size:42px !important;
    margin-bottom:0 !important;
}

.case-photo {
    height:300px;
    border-radius:12px;
    background:
    linear-gradient(rgba(0,0,0,.15),rgba(0,0,0,.75)),
    url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=85")
    center/cover;
    position:relative;
}

.photo-title {
    position:absolute;
    bottom:20px;
    left:25px;
    font-size:30px;
    font-weight:900;
}

.photo-info {
    position:absolute;
    bottom:58px;
    left:25px;
    color:#a9c9dd;
}

.case-card {
    background:#0d151e;
    border:1px solid #21394b;
    border-radius:10px;
    padding:18px;
    margin-top:12px;
}

.answer {
    background:#0b1823;
    border:1px solid #25465c;
    border-radius:8px;
    padding:15px;
    margin-top:12px;
}

.answer-yes {
    color:#49d7ff;
    font-size:22px;
    font-weight:900;
}

.answer-no {
    color:#ffbd68;
    font-size:22px;
    font-weight:900;
}

.clue {
    background:#0c1821;
    border-left:3px solid #38c8ff;
    padding:9px;
    margin:5px 0;
    border-radius:4px;
}

.ending {
    padding:25px;
    border:2px solid #38c8ff;
    border-radius:12px;
    background:#07141d;
    text-align:center;
}

.ending h2 {
    color:#50d8ff;
}

button {
    min-height:42px !important;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# 상태
# -----------------------------
if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "clues" not in st.session_state:
    st.session_state.clues = []

if "last_answer" not in st.session_state:
    st.session_state.last_answer = None

if "ending" not in st.session_state:
    st.session_state.ending = None


# -----------------------------
# 질문 데이터
# -----------------------------
questions = {
    "현관에 들어온 흔적이 있습니까?": (
        "아니오",
        "현관문과 손잡이에는 강제로 들어온 흔적이 없습니다.",
        "외부 침입 가능성이 낮다.",
        5
    ),

    "피해자는 사건 전에 누군가와 통화했습니까?": (
        "예",
        "사건 직전 누군가와 통화한 기록이 확인됩니다.",
        "피해자는 사건 직전 누군가와 연락했다.",
        5
    ),

    "CCTV에 수상한 사람이 찍혔습니까?": (
        "예",
        "23시 41분 복도 CCTV에 모자를 쓴 사람이 찍혔습니다.",
        "23:41 복도 CCTV에 수상한 인물이 등장했다.",
        10
    ),

    "피해자의 휴대전화 기록이 삭제됐습니까?": (
        "예",
        "마지막 통화 기록 하나가 삭제되어 있습니다.",
        "누군가 마지막 통화 기록을 삭제했다.",
        10
    ),

    "범인은 피해자를 알고 있었습니까?": (
        "예",
        "강제 침입 흔적이 없으므로 피해자가 직접 문을 열어준 것으로 보입니다.",
        "범인은 피해자와 아는 사이일 가능성이 높다.",
        10
    ),

    "최도윤은 CCTV 사각지대를 알고 있었습니까?": (
        "예",
        "최도윤은 이 건물에서 6년째 살고 있어 CCTV 위치를 잘 알고 있었습니다.",
        "최도윤은 CCTV 사각지대를 알고 있었다.",
        10
    ),

    "박서연은 사건 당일 피해자에게 전화했습니까?": (
        "예",
        "23시 18분, 23시 21분, 23시 27분 총 세 번 전화했습니다.",
        "박서연은 사건 직전 세 번 연락했다.",
        5
    ),

    "김민재는 피해자와 다퉜습니까?": (
        "예",
        "사건 당일 오후 승진 문제로 큰 말다툼을 했습니다.",
        "김민재에게 강한 동기가 있었다.",
        5
    ),

    "현장에서 제3자의 지문이 발견됐습니까?": (
        "예",
        "피해자의 지문 외에 다른 사람의 지문이 발견됐습니다.",
        "피해자 외 제3자의 지문이 발견됐다.",
        10
    ),

    "창문으로 침입했습니까?": (
        "아니오",
        "창문은 안쪽에서 잠겨 있었습니다.",
        "창문 침입 가능성이 없다.",
        5
    ),

    "금품이 사라졌습니까?": (
        "아니오",
        "지갑과 귀중품은 그대로 남아 있습니다.",
        "금품 목적의 범행이 아니다.",
        5
    ),

    "범인은 사건 후 현장에 다시 왔습니까?": (
        "예",
        "사건 직후 현관 CCTV에 같은 인물로 보이는 사람이 다시 나타났습니다.",
        "범인은 사건 후 현장을 다시 확인했다.",
        15
    ),

    "CCTV에 이상한 공백이 있었습니까?": (
        "예",
        "두 카메라 사이에 정확히 17초의 영상 공백이 존재합니다.",
        "17초짜리 CCTV 공백이 발견됐다.",
        15
    ),

    "최도윤의 알리바이는 완벽합니까?": (
        "아니오",
        "최도윤은 계속 집에 있었다고 주장했지만 통신 기록과 맞지 않습니다.",
        "최도윤의 알리바이에 모순이 있다.",
        15
    ),

    "범인은 피해자에게 신뢰받던 사람입니까?": (
        "예",
        "피해자가 스스로 문을 열어준 정황이 확인됩니다.",
        "범인은 피해자의 신뢰를 받고 있었다.",
        10
    )
}


# -----------------------------
# 제목
# -----------------------------
st.markdown(
    '<div style="color:#48d5ff;font-size:11px;letter-spacing:4px;font-weight:bold;">CONFIDENTIAL · 34 CASE FILES</div>',
    unsafe_allow_html=True
)

st.title("🔎 예스노 탐정")

st.caption("CASE 001 · 잠긴 방의 진실")


# -----------------------------
# 상단 정보
# -----------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("질문", f"{st.session_state.question_count}/15")
c2.metric("수사 점수", st.session_state.score)
c3.metric("확보 단서", len(st.session_state.clues))
c4.metric("현재 상태", "수사 중" if not st.session_state.ending else "종료")


st.divider()


# -----------------------------
# 메인 화면
# -----------------------------
left, right = st.columns([1.55, 1])


# =========================================================
# 왼쪽
# =========================================================
with left:

    st.subheader("📁 사건 기록")

    st.markdown("""
    <div class="case-photo">
        <div class="photo-info">CASE #001 · 서울 · 23:58</div>
        <div class="photo-title">잠긴 방의 진실</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="case-card">

    <b>사건 개요</b>

    <br><br>

    새벽 1시 18분.

    한 남자가 자신의 방 안에서 쓰러진 채 발견됐다.

    <br><br>

    현관문은 잠겨 있었고 창문에서도 외부 침입 흔적은 발견되지 않았다.

    <br><br>

    그런데 이상한 점이 하나 있었다.

    사건 당시 방의 에어컨은 <b>18도</b>로 설정되어 있었고,
    피해자의 휴대전화에서는 <b>마지막 통화 기록 하나가 삭제</b>되어 있었다.

    <br><br>

    경찰은 사고 가능성을 검토했지만,
    현장에는 피해자 외 다른 사람의 흔적이 발견됐다.

    <br><br>

    <b>당신은 15번의 질문으로 사건의 진실을 밝혀야 한다.</b>

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.subheader("🧩 확보한 단서")

    if len(st.session_state.clues) == 0:
        st.info("아직 확보한 단서가 없습니다. 오른쪽에서 질문하세요.")
    else:
        for clue in st.session_state.clues:
            st.markdown(
                f'<div class="clue">◆ {clue}</div>',
                unsafe_allow_html=True
            )


# =========================================================
# 오른쪽
# =========================================================
with right:

    st.subheader("🎤 심문")

    st.write(
        f"현재 질문: **{st.session_state.question_count}/15**"
    )

    selected_question = st.selectbox(
        "조사할 질문",
        list(questions.keys()),
        key="question_box"
    )

    if st.button(
        "🔎 질문하기",
        key="ask_button",
        use_container_width=True
    ):

        if st.session_state.question_count >= 15:

            st.warning("질문을 모두 사용했습니다.")

        else:

            answer, detail, clue, points = questions[selected_question]

            st.session_state.question_count += 1
            st.session_state.score += points

            if clue not in st.session_state.clues:
                st.session_state.clues.append(clue)

            st.session_state.last_answer = (
                answer,
                detail
            )

            st.rerun()


    # 답변
    if st.session_state.last_answer:

        answer, detail = st.session_state.last_answer

        if answer == "예":

            st.markdown("""
            <div class="answer">
                <div class="answer-yes">YES · 예</div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="answer">
                <div class="answer-no">NO · 아니오</div>
            """, unsafe_allow_html=True)

        st.write(detail)

        st.markdown("</div>", unsafe_allow_html=True)

    else:

        st.info("질문을 선택하고 질문하기를 누르세요.")


    st.divider()

    # =====================================================
    # 범인 지목
    # =====================================================

    st.subheader("🚨 범인 지목")

    st.write("모든 단서를 검토한 뒤 범인을 선택하세요.")

    suspect = st.radio(
        "누가 범인이라고 생각합니까?",
        [
            "김민재",
            "박서연",
            "최도윤"
        ],
        key="suspect_radio"
    )

    if suspect == "김민재":
        st.caption("피해자의 직장 동료 · 승진 문제로 갈등")

    elif suspect == "박서연":
        st.caption("피해자의 전 여자친구 · 사건 직전 세 차례 연락")

    else:
        st.caption("피해자의 이웃 · CCTV 사각지대를 알고 있음")


    if st.button(
        "🚨 최종 범인으로 지목하기",
        key="accuse_button",
        use_container_width=True
    ):

        # ★★★ 진짜 범인
        if suspect == "최도윤":
            st.session_state.ending = "WIN"

        elif suspect == "김민재":
            st.session_state.ending = "PARTIAL"

        else:
            st.session_state.ending = "LOSE"

        st.rerun()


# =========================================================
# 엔딩
# =========================================================

if st.session_state.ending:

    st.divider()

    if st.session_state.ending == "WIN":

        st.markdown("""
        <div class="ending">

        <h2>🎉 사건 해결</h2>

        <h3>TRUE ENDING</h3>

        <p>
        당신의 추리는 정확했다.
        </p>

        <p>
        범인은 <b>최도윤</b>.
        </p>

        <p>
        그는 건물의 CCTV 사각지대를 알고 있었고,
        피해자가 직접 문을 열어주도록 접근했다.
        </p>

        <p>
        사건 이후 다시 현장으로 돌아와
        휴대전화의 마지막 통화 기록까지 삭제했다.
        </p>

        <p>
        하지만 17초의 CCTV 공백과
        그의 알리바이 사이의 모순을 숨기지는 못했다.
        </p>

        <h3 style="color:#50d8ff;">
        🔎 CASE CLOSED
        </h3>

        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.ending == "PARTIAL":

        st.markdown("""
        <div class="ending">

        <h2>⚠️ 부분 해결</h2>

        <p>
        김민재에게는 분명한 동기가 있었다.
        </p>

        <p>
        하지만 결정적인 현장 증거가 부족하다.
        </p>

        <p>
        당신은 범인을 너무 빨리 지목했다.
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="ending">

        <h2>❌ 수사 실패</h2>

        <p>
        잘못된 사람을 범인으로 지목했다.
        </p>

        <p>
        진짜 범인은 아직 잡히지 않았다.
        </p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# 다시 시작
# =========================================================

if st.session_state.ending:

    if st.button(
        "🔄 새 사건 시작",
        use_container_width=True
    ):

        for key in [
            "question_count",
            "score",
            "clues",
            "last_answer",
            "ending"
        ]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
