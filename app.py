import streamlit as st
import random

# ============================================================
# 예스노 탐정
# ============================================================

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #080d12;
    color: #f4f7fa;
}

.block-container {
    max-width: 1200px;
    padding-top: 45px;
    padding-bottom: 80px;
}

h1, h2, h3 {
    color: #f4f7fa !important;
}

p, label {
    color: #d5dee7 !important;
}

/* 버튼 */
.stButton > button {
    width: 100%;
    min-height: 50px;
    background-color: #172536 !important;
    color: white !important;
    border: 1px solid #47627c !important;
    border-radius: 10px !important;
    font-weight: 800 !important;
}

.stButton > button:hover {
    background-color: #23405a !important;
    border-color: #72b7ee !important;
    color: white !important;
}

/* 시작 버튼 */
.start-game .stButton > button {
    min-height: 65px !important;
    font-size: 20px !important;
    background-color: #1265ad !important;
    border-color: #5bb5ff !important;
}

/* 입력창 */
.stTextInput input,
.stTextArea textarea {
    background-color: #111a23 !important;
    color: white !important;
    border: 1px solid #3a536b !important;
    border-radius: 9px !important;
}

/* 라디오 */
.stRadio label {
    color: #e4ebf1 !important;
}

/* 카드 */
.game-card {
    background-color: #101820;
    border: 1px solid #2b3d4d;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
}

.stat-card {
    background-color: #101820;
    border: 1px solid #2b3d4d;
    border-radius: 12px;
    padding: 15px;
    text-align: center;
}

.stat-title {
    color: #7f95a8;
    font-size: 13px;
}

.stat-number {
    color: white;
    font-size: 28px;
    font-weight: 900;
}

.clue-card {
    background-color: #0e1821;
    border-left: 4px solid #4ca7ed;
    border-radius: 7px;
    padding: 15px;
    margin-bottom: 10px;
}

.answer-yes {
    color: #55d99a;
    font-size: 28px;
    font-weight: 900;
}

.answer-no {
    color: #ff7474;
    font-size: 28px;
    font-weight: 900;
}

.answer-unknown {
    color: #ffd166;
    font-size: 28px;
    font-weight: 900;
}

.small-text {
    color: #879aaa;
}

.big-title {
    font-size: 48px;
    font-weight: 900;
}

.center {
    text-align: center;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 세션 상태
# ============================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "question_count" not in st.session_state:
    st.session_state.question_count = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "trust" not in st.session_state:
    st.session_state.trust = 100

if "clues" not in st.session_state:
    st.session_state.clues = []

if "history" not in st.session_state:
    st.session_state.history = []

if "asked" not in st.session_state:
    st.session_state.asked = []

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "ending" not in st.session_state:
    st.session_state.ending = ""


# ============================================================
# 사건 정보
# ============================================================

suspects = {
    "김민재": {
        "직업": "피해자의 동료",
        "설명": "사건 당일 피해자와 마지막으로 통화한 동료.",
        "의심": "승진 문제로 피해자와 크게 다툰 적이 있다."
    },

    "박서연": {
        "직업": "피해자의 전 여자친구",
        "설명": "헤어진 뒤에도 피해자와 연락하고 있었다.",
        "의심": "사건 당일 밤 피해자에게 세 번 전화했다."
    },

    "최도윤": {
        "직업": "건물 관리인",
        "설명": "건물 출입 기록과 CCTV를 관리한다.",
        "의심": "사건 시간대의 CCTV 기록 일부가 사라졌다."
    },

    "한유진": {
        "직업": "피해자의 동생",
        "설명": "피해자와 가장 가까운 가족.",
        "의심": "가족 재산 문제로 피해자와 다툰 적이 있다."
    }
}


# ============================================================
# 질문 데이터
# ============================================================

questions = [

    {
        "키워드": ["김민재", "민재"],
        "질문": "김민재는 사건 당일 피해자와 통화했습니까?",
        "답": "YES",
        "단서": "통화 기록에 따르면 김민재는 밤 10시 47분 피해자와 통화했다.",
        "점수": 5
    },

    {
        "키워드": ["박서연", "서연", "전여친"],
        "질문": "박서연은 사건 당일 피해자에게 연락했습니까?",
        "답": "YES",
        "단서": "박서연은 사건 당일 밤 피해자에게 총 세 번 전화를 걸었다.",
        "점수": 5
    },

    {
        "키워드": ["최도윤", "도윤", "관리인"],
        "질문": "최도윤은 CCTV를 관리할 수 있었습니까?",
        "답": "YES",
        "단서": "최도윤은 건물 CCTV 관리 프로그램의 관리자 권한을 가지고 있었다.",
        "점수": 8
    },

    {
        "키워드": ["한유진", "유진", "동생"],
        "질문": "한유진은 피해자의 가족입니까?",
        "답": "YES",
        "단서": "한유진은 피해자의 친동생이다.",
        "점수": 3
    },

    {
        "키워드": ["cctv", "카메라", "영상"],
        "질문": "CCTV 영상이 완전히 정상적으로 남아 있습니까?",
        "답": "NO",
        "단서": "CCTV에는 정확히 11분 38초의 공백이 존재한다.",
        "점수": 10
    },

    {
        "키워드": ["출입", "기록"],
        "질문": "삭제된 출입 기록이 있습니까?",
        "답": "YES",
        "단서": "사건 발생 약 20분 전 출입 기록 하나가 삭제되어 있었다.",
        "점수": 10
    },

    {
        "키워드": ["창문"],
        "질문": "범인은 창문으로 침입했습니까?",
        "답": "NO",
        "단서": "창문에는 외부에서 침입한 흔적이 전혀 없었다.",
        "점수": 7
    },

    {
        "키워드": ["문", "현관"],
        "질문": "현관문에는 강제로 침입한 흔적이 있습니까?",
        "답": "NO",
        "단서": "현관문과 잠금장치에는 강제 침입 흔적이 없었다.",
        "점수": 7
    },

    {
        "키워드": ["전화", "통화"],
        "질문": "피해자는 사건 직전에 누군가와 통화했습니까?",
        "답": "YES",
        "단서": "피해자의 마지막 통화 상대는 네 명의 용의자 중 누구도 아니었다.",
        "점수": 8
    },

    {
        "키워드": ["usb", "USB", "파일"],
        "질문": "현장에서 USB가 발견됐습니까?",
        "답": "YES",
        "단서": "책상 아래에서 검은색 USB가 발견됐다.",
        "점수": 8
    },

    {
        "키워드": ["지문"],
        "질문": "USB에서 지문이 발견됐습니까?",
        "답": "NO",
        "단서": "USB 표면은 누군가 깨끗하게 닦아놓은 상태였다.",
        "점수": 6
    },

    {
        "키워드": ["돈", "금전", "재산"],
        "질문": "피해자는 돈 문제로 누군가와 갈등하고 있었습니까?",
        "답": "YES",
        "단서": "피해자의 휴대폰에서 '돈 문제는 오늘 끝내자'라는 메시지가 발견됐다.",
        "점수": 6
    },

    {
        "키워드": ["메시지", "문자"],
        "질문": "삭제된 메시지가 발견됐습니까?",
        "답": "YES",
        "단서": "휴대폰 백업에서 삭제된 메시지 일부가 복구됐다.",
        "점수": 8
    },

    {
        "키워드": ["알리바이"],
        "질문": "네 명 모두 완벽한 알리바이를 가지고 있습니까?",
        "답": "NO",
        "단서": "네 명 모두 알리바이에 작은 구멍이 하나씩 발견됐다.",
        "점수": 10
    },

    {
        "키워드": ["최도윤", "cctv"],
        "질문": "최도윤은 사건 시간대에 CCTV 시스템에 접근했습니까?",
        "답": "YES",
        "단서": "관리실 컴퓨터 접속 기록에 최도윤의 계정이 남아 있었다.",
        "점수": 12
    },

    {
        "키워드": ["최도윤", "알리바이"],
        "질문": "최도윤의 알리바이는 완벽합니까?",
        "답": "NO",
        "단서": "최도윤은 관리실에 있었다고 했지만 CCTV 공백 시간과 정확히 겹친다.",
        "점수": 12
    },

    {
        "키워드": ["김민재", "알리바이"],
        "질문": "김민재의 알리바이는 완벽합니까?",
        "답": "NO",
        "단서": "김민재가 제출한 편의점 영수증은 시간 조작 가능성이 있다.",
        "점수": 7
    },

    {
        "키워드": ["박서연", "알리바이"],
        "질문": "박서연의 알리바이는 완벽합니까?",
        "답": "NO",
        "단서": "박서연의 알리바이를 증명하는 사람은 친구 한 명뿐이었다.",
        "점수": 7
    },

    {
        "키워드": ["한유진", "알리바이"],
        "질문": "한유진의 알리바이는 완벽합니까?",
        "답": "NO",
        "단서": "한유진은 집에 있었다고 했지만 휴대폰 위치 기록에는 이동 흔적이 있었다.",
        "점수": 9
    },

    {
        "키워드": ["열쇠"],
        "질문": "한유진은 피해자의 집 열쇠를 가지고 있었습니까?",
        "답": "YES",
        "단서": "한유진은 가족용 예비 열쇠를 가지고 있었다.",
        "점수": 9
    }
]


# ============================================================
# 게임 시작
# ============================================================

if not st.session_state.started:

    st.markdown("<div style='height:80px'></div>", unsafe_allow_html=True)

    st.markdown(
        "<div class='center'><div class='big-title'>🕵️ 예스노 탐정</div></div>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<div class='center'><p class='small-text'>질문은 예 또는 아니오로 대답된다. 하지만 진실은 그렇게 간단하지 않다.</p></div>",
        unsafe_allow_html=True
    )

    st.write("")

    st.info(
        """
        ### 사건 개요

        새벽 1시 18분.

        한 남자가 자신의 집에서 의식을 잃은 채 발견되었습니다.

        현관문은 잠겨 있었습니다.

        창문도 닫혀 있었습니다.

        외부 침입 흔적도 없었습니다.

        그런데 이상한 점이 하나 있었습니다.

        **사건과 관련된 네 명의 사람 모두 서로 다른 거짓말을 하고 있었습니다.**

        당신은 담당 탐정입니다.

        질문을 통해 사건의 진실을 찾아내세요.
        """
    )

    st.write("")

    st.markdown("<div class='start-game'>", unsafe_allow_html=True)

    if st.button("🎮 수사 시작", key="start"):
        st.session_state.started = True
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.stop()


# ============================================================
# 게임 화면
# ============================================================

st.markdown(
    "<div class='center'><div class='big-title'>🕵️ 예스노 탐정</div></div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='center'><p class='small-text'>CASE 001 · 잠긴 방의 진실</p></div>",
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# 상태창
# ============================================================

a, b, c, d = st.columns(4)

with a:
    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-title">질문</div>
        <div class="stat-number">{st.session_state.question_count}/15</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with b:
    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-title">수사 점수</div>
        <div class="stat-number">{st.session_state.score}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c:
    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-title">신뢰도</div>
        <div class="stat-number">{st.session_state.trust}%</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d:
    st.markdown(
        f"""
        <div class="stat-card">
        <div class="stat-title">확보 단서</div>
        <div class="stat-number">{len(st.session_state.clues)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# 게임 진행
# ============================================================

if not st.session_state.game_over:

    left, right = st.columns([1.55, 1])

    # --------------------------------------------------------
    # 질문
    # --------------------------------------------------------

    with left:

        st.subheader("🔎 사건에 질문하기")

        st.write(
            "궁금한 것을 직접 질문하세요. "
            "예: `최도윤은 CCTV를 관리할 수 있었습니까?`"
        )

        question = st.text_input(
            "질문",
            placeholder="질문을 입력하세요...",
            key="question"
        )

        if st.button("🔍 질문하기", key="ask"):

            if not question.strip():

                st.warning("질문을 먼저 입력해주세요.")

            elif st.session_state.question_count >= 15:

                st.error("질문 기회를 모두 사용했습니다.")

            else:

                found = None

                for q in questions:

                    if q["질문"] in st.session_state.asked:
                        continue

                    for word in q["키워드"]:

                        if word.lower() in question.lower():

                            found = q
                            break

                    if found:
                        break

                # 질문을 알아듣지 못했을 경우
                if found is None:

                    found = random.choice([
                        {
                            "질문": question,
                            "답": "UNKNOWN",
                            "단서": "현재 확보된 증거만으로는 이 질문에 확실한 답을 내릴 수 없다.",
                            "점수": 2
                        },
                        {
                            "질문": question,
                            "답": "NO",
                            "단서": "현재까지의 수사 기록에서는 이를 뒷받침할 증거를 찾지 못했다.",
                            "점수": 1
                        },
                        {
                            "질문": question,
                            "답": "YES",
                            "단서": "그럴 가능성은 있다. 하지만 이것만으로 결론을 내릴 수는 없다.",
                            "점수": 2
                        }
                    ])

                st.session_state.question_count += 1
                st.session_state.score += found["점수"]

                st.session_state.history.append({
                    "질문": question,
                    "답": found["답"],
                    "단서": found["단서"]
                })

                st.session_state.asked.append(found["질문"])

                if found["단서"] not in st.session_state.clues:
                    st.session_state.clues.append(found["단서"])

                st.rerun()

        st.write("")

        if st.session_state.history:

            latest = st.session_state.history[-1]

            if latest["답"] == "YES":

                st.markdown(
                    '<div class="answer-yes">🟢 YES · 그렇다</div>',
                    unsafe_allow_html=True
                )

            elif latest["답"] == "NO":

                st.markdown(
                    '<div class="answer-no">🔴 NO · 아니다</div>',
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    '<div class="answer-unknown">🟡 UNKNOWN · 확실하지 않다</div>',
                    unsafe_allow_html=True
                )

            st.write("")

            st.success(
                "🔎 새로 확보한 단서\n\n"
                + latest["단서"]
            )

        else:

            st.info(
                "아직 질문한 것이 없습니다.\n\n"
                "용의자나 사건의 특정 부분부터 조사해보세요."
            )


    # --------------------------------------------------------
    # 용의자
    # --------------------------------------------------------

    with right:

        st.subheader("👤 용의자")

        for name, info in suspects.items():

            with st.container(border=True):

                st.markdown(f"### {name}")

                st.caption(info["직업"])

                st.write(info["설명"])

                st.warning(
                    "의심점: " + info["의심"]
                )


# ============================================================
# 증거
# ============================================================

st.divider()

st.subheader("📁 확보한 단서")

if not st.session_state.clues:

    st.info("아직 확보한 단서가 없습니다.")

else:

    for i, clue in enumerate(st.session_state.clues, 1):

        st.markdown(
            f"""
            <div class="clue-card">
            <b>증거 #{i}</b><br><br>
            {clue}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 수사 기록
# ============================================================

if st.session_state.history:

    st.divider()

    st.subheader("📜 수사 기록")

    for i, item in enumerate(
        reversed(st.session_state.history), 1
    ):

        if item["답"] == "YES":
            icon = "🟢"
        elif item["답"] == "NO":
            icon = "🔴"
        else:
            icon = "🟡"

        with st.expander(
            f"{icon} 질문 기록 #{len(st.session_state.history)-i+1}"
        ):

            st.write("**질문**")
            st.write(item["질문"])

            st.write("**답변**")
            st.write(item["답"])

            st.write("**획득 단서**")
            st.write(item["단서"])


# ============================================================
# 최종 추리
# ============================================================

st.divider()

st.subheader("🧠 최종 추리")

if not st.session_state.game_over:

    st.write(
        "충분한 단서를 확보했다면 범인을 지목하세요."
    )

    suspect = st.radio(
        "범인은 누구입니까?",
        list(suspects.keys()),
        horizontal=True
    )

    reason = st.text_area(
        "추리 이유",
        placeholder="왜 이 사람이 범인이라고 생각하는지 설명해주세요.",
        height=130
    )

    if st.button("🚨 최종 추리 제출", key="submit"):

        if len(st.session_state.clues) < 3:

            st.warning(
                "단서가 너무 적습니다. 최소 3개의 단서를 확보하세요."
            )

        elif len(reason.strip()) < 5:

            st.warning(
                "추리 이유를 조금 더 자세히 적어주세요."
            )

        else:

            # 진짜 범인
            if suspect == "최도윤" and st.session_state.score >= 65:

                st.session_state.ending = "TRUE"

            elif suspect == "최도윤":

                st.session_state.ending = "PARTIAL"

            else:

                st.session_state.ending = "BAD"

            st.session_state.game_over = True

            st.rerun()


# ============================================================
# 엔딩
# ============================================================

if st.session_state.game_over:

    st.divider()

    ending = st.session_state.ending

    if ending == "TRUE":

        st.success("## 🏆 TRUE ENDING · 사건 해결")

        st.markdown("""
        ### 당신의 추리는 정확했습니다.

        진짜 범인은 **최도윤**이었습니다.

        그는 건물 관리인이라는 위치를 이용해
        CCTV와 출입 기록에 접근할 수 있었습니다.

        사건 시간대에 발생한 11분 38초의 CCTV 공백.

        삭제된 출입 기록.

        관리실 컴퓨터에 남아 있는 접속 기록.

        이 세 가지 증거가 서로 연결되었습니다.

        다른 용의자들도 거짓말을 하고 있었습니다.

        하지만 그들의 거짓말은 사건을 숨기기 위한 것이 아니라
        각자의 사생활을 숨기기 위한 것이었습니다.

        당신은 그 차이를 찾아냈습니다.

        **사건 해결.**
        """)

    elif ending == "PARTIAL":

        st.warning("## 🟡 PARTIAL ENDING · 거의 해결")

        st.markdown("""
        ### 범인은 맞혔습니다.

        하지만 경찰에게 제출하기에는
        결정적인 증거가 부족합니다.

        최도윤을 의심한 것은 정확했습니다.

        그러나 CCTV 공백과 삭제된 기록을
        직접 연결하는 증거가 부족했습니다.

        조금 더 질문했다면
        완벽하게 사건을 해결할 수 있었을 것입니다.
        """)

    else:

        st.error("## 🔴 BAD ENDING · 잘못된 추리")

        st.markdown("""
        ### 당신은 잘못된 사람을 지목했습니다.

        가장 의심스러워 보이는 사람과
        진짜 범인은 같은 사람이 아니었습니다.

        사건 기록을 다시 보면
        중요한 단서들이 다른 방향을 가리키고 있습니다.

        탐정에게 가장 위험한 것은
        **첫 번째로 떠오른 결론을 진실이라고 믿는 것**입니다.
        """)

    st.write("")

    st.metric(
        "최종 수사 점수",
        st.session_state.score
    )

    st.metric(
        "확보한 단서",
        len(st.session_state.clues)
    )

    st.write("")

    if st.button("🔄 처음부터 다시 하기", key="restart"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()


# ============================================================
# 하단
# ============================================================

st.divider()

st.caption(
    "🕵️ 예스노 탐정 · CASE 001 | "
    "질문에는 답이 있지만, 답이 항상 진실인 것은 아니다."
)
