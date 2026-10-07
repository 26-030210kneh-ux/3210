import streamlit as st

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🕵️",
    layout="wide"
)

# -------------------------
# 세션 상태
# -------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "clues" not in st.session_state:
    st.session_state.clues = []

if "score" not in st.session_state:
    st.session_state.score = 0

if "ending" not in st.session_state:
    st.session_state.ending = None


# -------------------------
# 질문 판정
# -------------------------
def answer_question(question):
    q = question.strip().lower()

    # 아무것도 입력하지 않은 경우
    if not q:
        return "불명", "질문을 입력해주세요.", None, 0

    # 사건과 관계없는 질문
    unrelated = [
        "문어", "고양이", "강아지", "축구",
        "날씨", "치킨", "라면", "게임",
        "연예인", "나는 문어"
    ]

    if any(word in q for word in unrelated):
        return (
            "아니오",
            "그 질문은 이번 사건과 관련이 없습니다.",
            None,
            0
        )

    # 힌트
    if "힌트" in q:
        return (
            "힌트",
            "현관보다 사건 직전의 CCTV와 삭제된 통화 기록을 조사해보세요.",
            "CCTV 17초 공백과 삭제된 통화 기록",
            1
        )

    # 시간
    if "몇 시" in q or "시간" in q or "2시 17분" in q or "2:17" in q:
        return (
            "예",
            "사건이 발생한 것으로 추정되는 시간은 새벽 2시 17분입니다.",
            "사건 발생 추정 시각은 새벽 2시 17분",
            1
        )

    # CCTV
    if "cctv" in q or "카메라" in q:
        return (
            "예",
            "사건 직전 CCTV에 정확히 17초의 공백이 있습니다.",
            "CCTV에 17초의 공백이 존재한다",
            2
        )

    # 통화
    if "통화" in q or "전화" in q or "휴대폰" in q or "핸드폰" in q:
        return (
            "예",
            "피해자의 휴대전화에서 사건 직전 통화 기록 하나가 삭제되었습니다.",
            "사건 직전 삭제된 통화 기록이 있다",
            2
        )

    # 현관 / 침입
    if "현관" in q or "문" in q or "침입" in q or "들어" in q:
        return (
            "아니오",
            "현관문에는 강제로 침입한 흔적이 없습니다.",
            "범인은 강제로 침입하지 않았을 가능성이 높다",
            2
        )

    # 창문
    if "창문" in q or "창" in q:
        return (
            "아니오",
            "창문에서도 외부에서 침입한 흔적은 발견되지 않았습니다.",
            "창문을 통한 침입 가능성도 낮다",
            1
        )

    # 귀중품
    if "돈" in q or "귀중품" in q or "훔" in q or "도난" in q:
        return (
            "아니오",
            "현금과 귀중품은 그대로 남아 있었습니다.",
            "범인의 목적은 단순한 절도가 아니다",
            1
        )

    # 잠금
    if "잠겨" in q or "잠금" in q or "열쇠" in q or "문을 잠" in q:
        return (
            "예",
            "발견 당시 현관문은 잠겨 있었습니다.",
            "범행 후에도 현관문은 잠겨 있었다",
            1
        )

    # 피해자
    if "혼자" in q or "혼자였" in q:
        return (
            "예",
            "사건 당시 피해자는 집에 혼자 있었던 것으로 추정됩니다.",
            "피해자는 사건 당시 혼자였다",
            1
        )

    # 상해
    if "죽" in q or "살인" in q or "다쳤" in q or "상처" in q or "무기" in q:
        return (
            "예",
            "피해자는 머리에 강한 충격을 받은 흔적이 있습니다.",
            "피해자는 머리에 강한 충격을 받았다",
            1
        )

    # 김민재
    if "김민재" in q or "민재" in q:
        return (
            "불명",
            "김민재는 피해자와 승진 문제로 다툰 적이 있어 동기는 있습니다. "
            "하지만 결정적인 증거는 아직 없습니다.",
            "김민재에게는 승진 문제라는 동기가 있다",
            1
        )

    # 박서연
    if "박서연" in q or "서연" in q:
        return (
            "예",
            "박서연은 사건 직전 피해자에게 세 차례 전화를 걸었습니다.",
            "박서연은 사건 직전 피해자에게 세 번 전화했다",
            2
        )

    # 최도윤
    if "최도윤" in q or "도윤" in q:
        return (
            "예",
            "최도윤은 피해자의 집 주변 CCTV 위치와 사각지대를 알고 있었습니다.",
            "최도윤은 CCTV 사각지대를 알고 있었다",
            2
        )

    # 알리바이
    if "알리바이" in q or "범행 시간" in q:
        return (
            "불명",
            "세 사람 모두 알리바이를 주장했지만, "
            "최도윤의 진술에서 시간상 이상한 부분이 발견됩니다.",
            "최도윤의 알리바이에 의문점이 있다",
            2
        )

    # 범인 직접 질문
    if "범인" in q or "누가" in q or "누구" in q:
        return (
            "불명",
            "아직 범인을 단정할 수 없습니다. "
            "CCTV 17초 공백과 삭제된 통화를 연결해보세요.",
            "CCTV 공백과 통화 기록을 연결해야 한다",
            1
        )

    # 기본 답변
    return (
        "불명",
        "그 질문만으로는 판단하기 어렵습니다. "
        "현관, CCTV, 통화 기록, 용의자의 알리바이를 조사해보세요.",
        None,
        0
    )


# -------------------------
# 제목
# -------------------------
st.title("🕵️ 예스노 탐정")
st.caption("새벽 2시 17분의 빈집 — 당신은 질문만으로 범인을 찾아야 합니다.")

st.divider()


# -------------------------
# 사건 개요
# -------------------------
st.subheader("📁 사건 개요")

st.write(
    """
    새벽 2시 17분, 한 남자가 자신의 집에서 쓰러진 채 발견되었다.

    현관문은 잠겨 있었고 강제로 침입한 흔적은 없었다.
    집 안의 귀중품도 그대로였다.

    그런데 사건 직전 CCTV에는 정확히 17초의 공백이 발생했다.
    또한 피해자의 휴대전화에서는 사건 직전 통화 기록 하나가 삭제되어 있었다.

    경찰은 피해자와 관계가 있는 세 명을 용의자로 보고 있다.

    **당신의 임무는 질문을 통해 단서를 모아 진짜 범인을 찾아내는 것이다.**
    """
)

st.divider()


# -------------------------
# 사건 정보
# -------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("수집한 단서", len(st.session_state.clues))

with col2:
    st.metric("탐정 점수", st.session_state.score)

with col3:
    st.metric("질문 횟수", len(st.session_state.history))


# -------------------------
# 질문
# -------------------------
st.subheader("🔎 사건에 대해 질문하세요")

st.write(
    "예: `현관에 침입한 흔적이 있습니까?` / "
    "`CCTV에 이상한 점이 있습니까?` / "
    "`최도윤은 어디에 있었습니까?`"
)

with st.form("question_form", clear_on_submit=True):
    question = st.text_input(
        "질문",
        placeholder="궁금한 것을 직접 입력하세요."
    )

    submitted = st.form_submit_button(
        "질문하기",
        use_container_width=True
    )

if submitted and question.strip():
    answer, detail, clue, points = answer_question(question)

    st.session_state.history.append({
        "question": question,
        "answer": answer,
        "detail": detail,
        "clue": clue
    })

    st.session_state.score += points

    if clue and clue not in st.session_state.clues:
        st.session_state.clues.append(clue)

    st.rerun()


# -------------------------
# 질문 기록
# -------------------------
st.subheader("💬 탐정 기록")

if not st.session_state.history:
    st.info("아직 질문한 내용이 없습니다. 사건에 대해 자유롭게 질문해보세요.")

else:
    with st.container(height=260, border=True):

        for item in st.session_state.history:

            # 플레이어가 실제로 입력한 질문
            st.write(f"🕵️ 나: {item['question']}")

            # 탐정 시스템 답변
            if item["answer"] == "예":
                st.success(f"🔎 탐정 시스템 — 예\n\n{item['detail']}")

            elif item["answer"] == "아니오":
                st.error(f"🔎 탐정 시스템 — 아니오\n\n{item['detail']}")

            elif item["answer"] == "힌트":
                st.warning(f"🔎 탐정 시스템 — 힌트\n\n{item['detail']}")

            else:
                st.info(f"🔎 탐정 시스템 — 불명\n\n{item['detail']}")

            if item["clue"]:
                st.caption(f"🧩 새로운 단서: {item['clue']}")

            st.divider()


# -------------------------
# 단서
# -------------------------
st.subheader("🧩 발견한 단서")

if st.session_state.clues:
    for i, clue in enumerate(st.session_state.clues, 1):
        st.write(f"**{i}.** {clue}")
else:
    st.caption("아직 발견한 단서가 없습니다.")


st.divider()


# -------------------------
# 용의자
# -------------------------
st.subheader("👤 용의자")

c1, c2, c3 = st.columns(3)

with c1:
    st.write("### 김민재")
    st.write("피해자의 직장 동료")
    st.caption("승진 문제로 피해자와 다툰 적이 있음.")

with c2:
    st.write("### 박서연")
    st.write("피해자의 전 연인")
    st.caption("사건 직전 피해자에게 세 차례 전화함.")

with c3:
    st.write("### 최도윤")
    st.write("피해자의 이웃")
    st.caption("CCTV 위치와 사각지대를 알고 있음.")


# -------------------------
# 범인 지목
# -------------------------
st.divider()

st.subheader("🎯 범인 지목")

with st.form("culprit_form"):

    culprit = st.radio(
        "범인은 누구라고 생각합니까?",
        ["김민재", "박서연", "최도윤"],
        horizontal=True
    )

    accuse = st.form_submit_button(
        "범인 지목하기",
        use_container_width=True
    )

if accuse:

    if culprit == "최도윤":
        st.session_state.ending = "win"

    else:
        st.session_state.ending = "lose"


# -------------------------
# 엔딩
# -------------------------
if st.session_state.ending == "win":

    st.success(
        """
        ## 🎉 사건 해결

        범인은 **최도윤**이었습니다.

        최도윤은 CCTV 사각지대를 알고 있었고,
        그 지식을 이용해 CCTV에 17초의 공백을 만들었습니다.

        또한 사건 직전 피해자와 관련된 통화 기록을 삭제했습니다.

        **당신은 사건의 핵심 단서를 정확히 연결해냈습니다.**
        """
    )

elif st.session_state.ending == "lose":

    st.error(
        """
        ## ❌ 범인을 잘못 지목했습니다.

        아직 핵심 단서를 충분히 연결하지 못했습니다.

        CCTV의 **17초 공백**과
        **삭제된 통화 기록**을 다시 조사해보세요.
        """
    )


# -------------------------
# 다시 시작
# -------------------------
if st.session_state.ending:

    if st.button("🔄 사건 다시 시작"):
        st.session_state.history = []
        st.session_state.clues = []
        st.session_state.score = 0
        st.session_state.ending = None
        st.rerun()
