import streamlit as st
import random
import re

# =========================================================
# 예스노탐정
# =========================================================

st.set_page_config(
    page_title="예스노탐정",
    page_icon="🕵️",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 20% 0%, rgba(80,120,180,.12), transparent 30%),
        radial-gradient(circle at 90% 20%, rgba(180,80,60,.08), transparent 30%),
        #090c11;
    color: #eeeeee;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}

.title {
    text-align: center;
    padding: 20px 0 10px 0;
}

.title h1 {
    font-size: 52px;
    font-weight: 900;
    margin-bottom: 0;
}

.title p {
    color: #9ba4b0;
    font-size: 17px;
}

.case-card {
    background: linear-gradient(
        145deg,
        rgba(25,31,40,.98),
        rgba(13,17,23,.98)
    );
    border: 1px solid #303945;
    border-radius: 18px;
    padding: 30px;
    margin: 10px 0 20px 0;
    box-shadow: 0 12px 40px rgba(0,0,0,.25);
}

.case-number {
    color: #69b7ff;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
}

.case-title {
    font-size: 30px;
    font-weight: 900;
    margin: 8px 0 20px 0;
}

.case-story {
    color: #d8dde4;
    line-height: 2;
    font-size: 17px;
    white-space: pre-line;
}

.question-box {
    background: #111720;
    border: 1px solid #303b49;
    border-radius: 15px;
    padding: 22px;
}

.answer-yes {
    background: rgba(40,150,90,.15);
    border: 1px solid #328d5c;
    border-radius: 12px;
    padding: 18px;
    margin: 10px 0;
}

.answer-no {
    background: rgba(190,70,70,.12);
    border: 1px solid #9c4747;
    border-radius: 12px;
    padding: 18px;
    margin: 10px 0;
}

.answer-unknown {
    background: rgba(180,140,50,.12);
    border: 1px solid #967b31;
    border-radius: 12px;
    padding: 18px;
    margin: 10px 0;
}

.clue {
    background: #10151c;
    border-left: 4px solid #69b7ff;
    padding: 14px 18px;
    border-radius: 8px;
    margin: 8px 0;
}

.final-box {
    background: linear-gradient(
        145deg,
        rgba(35,65,50,.5),
        rgba(15,25,20,.9)
    );
    border: 1px solid #4b936b;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}

.failed-box {
    background: rgba(90,25,25,.25);
    border: 1px solid #914747;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}

.score {
    font-size: 42px;
    font-weight: 900;
    text-align: center;
}

.small {
    color: #89929e;
    font-size: 13px;
}

div[data-testid="stSidebar"] {
    background: #0c1016;
    border-right: 1px solid #252d38;
}

.stButton button {
    border-radius: 10px;
    min-height: 45px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 사건 데이터
# =========================================================

CASES = [

    {
        "id": 1,
        "title": "사라진 시계",
        "difficulty": "⭐",
        "story": """
한 남자가 자신의 방에서 죽은 채 발견되었다.

방문은 안에서 잠겨 있었고,
창문도 닫혀 있었다.

경찰은 처음에 자살이라고 생각했다.

그런데 형사가 현장을 한 번 둘러본 뒤
곧바로 살인이라고 판단했다.

왜일까?
""",
        "keywords": [
            "시계",
            "시간",
            "시간대",
            "시각",
            "죽은시간",
            "사망시간",
            "알리바이"
        ],
        "answers": {
            "시계": "YES",
            "시간": "YES",
            "시간대": "YES",
            "시각": "YES",
            "죽은시간": "YES",
            "사망시간": "YES",
            "알리바이": "YES",
            "가족": "NO",
            "창문": "NO",
            "문": "NO",
            "독": "NO",
            "총": "NO",
            "범인": "UNKNOWN"
        },
        "clues": [
            "현장에 있던 시계가 사건의 핵심이다.",
            "사망 시각에 대한 경찰의 판단이 틀렸다.",
            "누군가 사건 발생 시간을 조작하려 했다."
        ],
        "solution": """
범인은 시계를 조작해서 사망 시간을 속였다.

즉, 피해자가 죽은 시간에
범인이 현장에 있었다는 사실을 숨기려고 한 것이다.

잠긴 방 자체가 핵심이 아니라
'언제 죽었는가'가 핵심이었다.
"""
    },

    {
        "id": 2,
        "title": "잠긴 방",
        "difficulty": "⭐⭐",
        "story": """
한 여성이 자신의 집에서 쓰러진 채 발견되었다.

현관문은 잠겨 있었다.
창문도 모두 닫혀 있었다.

집 안에는 피해자 외에 아무도 없었다.

그런데 경찰은
외부 침입자가 있었다고 확신했다.

어떻게 가능했을까?
""",
        "keywords": [
            "열쇠",
            "복제",
            "열쇠복제",
            "열쇠를",
            "열쇠가",
            "원격",
            "밖",
            "외부"
        ],
        "answers": {
            "열쇠": "YES",
            "복제": "YES",
            "열쇠복제": "YES",
            "원격": "NO",
            "가족": "NO",
            "창문": "NO",
            "독": "NO",
            "총": "NO",
            "자살": "NO"
        },
        "clues": [
            "문이 잠겨 있다는 사실만으로 외부인이 없었다고 할 수 없다.",
            "범인은 정상적인 열쇠를 사용했을 가능성이 있다.",
            "핵심은 '열쇠를 누가 가지고 있었는가'이다."
        ],
        "solution": """
범인은 피해자의 열쇠를 미리 복제해 두었다.

범행 후 문을 잠그고 떠났기 때문에
현장에서는 침입 흔적이 발견되지 않았다.

'잠긴 방'이 완벽한 밀실은 아니었던 것이다.
"""
    },

    {
        "id": 3,
        "title": "멈춘 CCTV",
        "difficulty": "⭐⭐⭐",
        "story": """
은행에서 현금이 사라졌다.

CCTV를 확인한 경찰은
범행 시간대의 영상을 확인했다.

그런데 이상하게도
범행이 일어난 정확한 10분 동안만
영상이 멈춰 있었다.

경찰은 내부자의 소행이라고 판단했다.

왜 그랬을까?
""",
        "keywords": [
            "내부자",
            "직원",
            "cctv",
            "카메라",
            "시간",
            "전원",
            "전기",
            "녹화"
        ],
        "answers": {
            "내부자": "YES",
            "직원": "YES",
            "cctv": "YES",
            "카메라": "YES",
            "시간": "YES",
            "전원": "YES",
            "전기": "YES",
            "녹화": "YES",
            "손님": "NO",
            "강도": "NO",
            "창문": "NO"
        },
        "clues": [
            "CCTV는 우연히 고장난 것이 아니다.",
            "범인은 CCTV가 멈추는 시간을 알고 있었다.",
            "범행 시간과 CCTV 정지 시간이 정확히 일치한다."
        ],
        "solution": """
범인은 은행 내부 시스템을 알고 있는 사람이었다.

CCTV의 전원을 차단하거나
녹화 시스템을 조작할 수 있는 사람만
정확히 10분 동안 영상을 없앨 수 있었다.

따라서 경찰은 내부자의 소행이라고 판단했다.
"""
    },

    {
        "id": 4,
        "title": "범인이 건 전화",
        "difficulty": "⭐⭐⭐⭐",
        "story": """
새벽 2시,
경찰서에 전화가 걸려왔다.

전화한 사람은 말했다.

"사람을 죽였습니다."

경찰이 주소를 묻자
전화는 바로 끊겼다.

경찰이 추적한 결과,
전화는 피해자의 집에서 걸려온 것이었다.

그런데 경찰이 도착했을 때
피해자는 아직 살아 있었다.

그렇다면 전화한 사람은
누구였을까?
""",
        "keywords": [
            "피해자",
            "범인",
            "전화",
            "미래",
            "녹음",
            "자동",
            "예약",
            "녹음된"
        ],
        "answers": {
            "피해자": "YES",
            "범인": "NO",
            "전화": "YES",
            "미래": "NO",
            "녹음": "YES",
            "자동": "YES",
            "예약": "YES",
            "녹음된": "YES",
            "가족": "NO",
            "경찰": "NO"
        },
        "clues": [
            "전화한 사람이 반드시 그 순간 직접 말한 것은 아니다.",
            "미리 녹음된 음성을 사용할 수 있다.",
            "전화는 자동으로 걸리도록 설정되어 있었을 가능성이 있다."
        ],
        "solution": """
피해자가 미리 자신의 목소리를 녹음해 두었다.

그리고 특정 시간에 자동으로 경찰에게
전화가 걸리도록 설정했다.

피해자는 자신에게 위험이 생길 것을 예상하고
미리 신고 장치를 준비했던 것이다.
"""
    },

    {
        "id": 5,
        "title": "탐정이 범인",
        "difficulty": "⭐⭐⭐⭐⭐",
        "story": """
한 남자가 살해되었다.

경찰은 현장을 조사했지만
범인을 찾지 못했다.

그런데 현장에 있던 탐정이 말했다.

"범인은 분명히 피해자의 오른손에
반지를 끼워 놓았을 겁니다."

경찰은 즉시 탐정을 체포했다.

왜일까?
""",
        "keywords": [
            "오른손",
            "반지",
            "현장",
            "시체",
            "손",
            "알고",
            "보지",
            "정보"
        ],
        "answers": {
            "오른손": "YES",
            "반지": "YES",
            "현장": "YES",
            "시체": "YES",
            "손": "YES",
            "알고": "YES",
            "보지": "YES",
            "정보": "YES",
            "피해자": "YES",
            "경찰": "NO"
        },
        "clues": [
            "탐정은 현장에 도착한 뒤 시체를 처음 보았다.",
            "그런데 아무도 알려주지 않은 정보를 알고 있었다.",
            "그 정보는 범인만 알 수 있는 정보였다."
        ],
        "solution": """
탐정은 범인이었다.

아직 경찰에게 공개되지 않은
시체의 손과 반지에 관한 정보를
탐정이 알고 있었기 때문이다.

탐정은 자신이 현장에서 본 것처럼 말했지만,
사실은 범행 당시 이미 그 사실을 알고 있었다.
"""
    }
]


# =========================================================
# 세션 상태
# =========================================================

if "started" not in st.session_state:
    st.session_state.started = False

if "case_index" not in st.session_state:
    st.session_state.case_index = 0

if "questions_left" not in st.session_state:
    st.session_state.questions_left = 15

if "question_history" not in st.session_state:
    st.session_state.question_history = []

if "clues" not in st.session_state:
    st.session_state.clues = []

if "case_finished" not in st.session_state:
    st.session_state.case_finished = False

if "case_won" not in st.session_state:
    st.session_state.case_won = False

if "score" not in st.session_state:
    st.session_state.score = 0

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "hint_used" not in st.session_state:
    st.session_state.hint_used = False

if "final_answer" not in st.session_state:
    st.session_state.final_answer = ""


case = CASES[st.session_state.case_index]


# =========================================================
# 함수
# =========================================================

def normalize(text):
    text = text.lower()
    text = re.sub(r"\s+", "", text)
    return text


def get_answer(question):

    q = normalize(question)

    for keyword, answer in case["answers"].items():
        if normalize(keyword) in q:
            return answer

    return "UNKNOWN"


def add_clue():

    if len(st.session_state.clues) < len(case["clues"]):

        clue = case["clues"][len(st.session_state.clues)]

        if clue not in st.session_state.clues:
            st.session_state.clues.append(clue)


def reset_case():

    st.session_state.questions_left = 15
    st.session_state.question_history = []
    st.session_state.clues = []
    st.session_state.case_finished = False
    st.session_state.case_won = False
    st.session_state.hint_used = False
    st.session_state.final_answer = ""


def next_case():

    if st.session_state.case_index < len(CASES) - 1:

        st.session_state.case_index += 1

        reset_case()

    else:

        st.session_state.game_over = True


# =========================================================
# 상단 제목
# =========================================================

st.markdown("""
<div class="title">

<h1>🕵️ 예스노탐정</h1>

<p>
질문은 자유롭지만, 대답은 YES 또는 NO뿐이다.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 게임 시작 화면
# =========================================================

if not st.session_state.started:

    st.markdown("""
    <div class="case-card">

    <div class="case-number">
    DETECTIVE SYSTEM // ONLINE
    </div>

    <div class="case-title">
    당신은 탐정입니다.
    </div>

    <div class="case-story">

    사건의 진실은 이미 존재합니다.

    하지만 당신이 가진 정보는 부족합니다.

    당신이 할 수 있는 것은 단 하나.

    <b>질문하는 것.</b>

    용의자에게 직접 질문할 수도 있고,
    사건 자체에 대해 질문할 수도 있습니다.

    하지만 대답은 오직

    <b>YES / NO / 알 수 없음</b>

    세 가지뿐입니다.

    질문을 통해 단서를 모으고
    마지막에 사건의 진실을 설명하세요.

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.info("""
    🎮 플레이 방법

    ① 사건을 읽는다
    ② 궁금한 것을 질문한다
    ③ YES / NO 답변을 받는다
    ④ 단서를 모은다
    ⑤ 마지막에 사건의 진실을 적는다

    질문은 최대 15번입니다.
    """)

    if st.button(
        "🚨 첫 번째 사건 시작",
        use_container_width=True
    ):

        st.session_state.started = True
        st.rerun()

    st.stop()


# =========================================================
# 게임 종료
# =========================================================

if st.session_state.game_over:

    st.markdown("""
    <div class="final-box">

    <h1>🏆 사건 해결 완료</h1>

    <h2>당신은 모든 사건을 해결했습니다.</h2>

    <p>
    이제 당신은 진짜 예스노탐정입니다.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f'<div class="score">{st.session_state.score} 점</div>',
        unsafe_allow_html=True
    )

    if st.button("🔄 처음부터 다시 하기"):

        st.session_state.case_index = 0
        st.session_state.score = 0
        st.session_state.started = False
        st.session_state.game_over = False

        reset_case()

        st.rerun()

    st.stop()


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    st.markdown("## 🕵️ 탐정 수첩")

    st.metric(
        "현재 사건",
        f"{case['id']} / {len(CASES)}"
    )

    st.metric(
        "남은 질문",
        st.session_state.questions_left
    )

    st.metric(
        "현재 점수",
        st.session_state.score
    )

    st.divider()

    st.markdown("### 📌 조사 규칙")

    st.write("• 질문은 최대 15번")
    st.write("• 답변은 YES / NO")
    st.write("• 애매한 질문은 '알 수 없음'")
    st.write("• 마지막에 직접 추리")

    st.divider()

    if not st.session_state.hint_used:

        if st.button(
            "💡 긴급 단서 +10점",
            use_container_width=True
        ):

            st.session_state.hint_used = True
            st.session_state.score += 10

            add_clue()

            st.rerun()


# =========================================================
# 사건 표시
# =========================================================

st.markdown(f"""
<div class="case-card">

<div class="case-number">
CASE #{case['id']:03d} // 난이도 {case['difficulty']}
</div>

<div class="case-title">
{case['title']}
</div>

<div class="case-story">
{case['story']}
</div>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 이미 끝난 사건
# =========================================================

if st.session_state.case_finished:

    if st.session_state.case_won:

        st.markdown("""
        <div class="final-box">

        <h1>🟢 CASE CLOSED</h1>

        <h2>사건 해결 성공!</h2>

        <p>
        당신은 사건의 핵심을 찾아냈습니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("📖 사건의 진실")

        st.write(case["solution"])

        st.divider()

        st.subheader("🏆 점수")

        st.markdown(
            f'<div class="score">+{st.session_state.score}점</div>',
            unsafe_allow_html=True
        )

        if st.session_state.case_index < len(CASES) - 1:

            if st.button(
                "➡️ 다음 사건",
                use_container_width=True
            ):

                next_case()
                st.rerun()

        else:

            if st.button(
                "🏆 모든 사건 클리어",
                use_container_width=True
            ):

                st.session_state.game_over = True
                st.rerun()

    else:

        st.markdown("""
        <div class="failed-box">

        <h1>🔴 CASE FAILED</h1>

        <h2>사건 해결에 실패했습니다.</h2>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("📖 진짜 사건의 진실")

        st.write(case["solution"])

        if st.button(
            "🔄 이 사건 다시 하기",
            use_container_width=True
        ):

            reset_case()
            st.rerun()

    st.stop()


# =========================================================
# 질문 영역
# =========================================================

st.subheader("🔎 질문하기")

st.markdown("""
<div class="question-box">

<b>탐정의 질문</b>

<br><br>

예시:

<br>

• 범인은 가족입니까?<br>
• 피해자는 혼자였습니까?<br>
• 시계가 중요한 단서입니까?<br>
• 범인은 남자입니까?<br>

</div>
""", unsafe_allow_html=True)

st.write("")

question = st.text_input(
    "질문을 입력하세요",
    placeholder="예: 시계가 사건과 관련 있습니까?",
    disabled=st.session_state.questions_left <= 0
)


if st.button(
    "🔍 질문하기",
    use_container_width=True,
    disabled=(
        st.session_state.questions_left <= 0
        or not question.strip()
    )
):

    answer = get_answer(question)

    st.session_state.questions_left -= 1

    st.session_state.question_history.append(
        {
            "question": question,
            "answer": answer
        }
    )

    # 질문하면 점수 조금 증가
    if answer in ["YES", "NO"]:

        st.session_state.score += 5

        add_clue()

    st.rerun()


# =========================================================
# 답변 기록
# =========================================================

if st.session_state.question_history:

    st.divider()

    st.subheader("💬 질문 기록")

    for item in reversed(
        st.session_state.question_history
    ):

        answer = item["answer"]

        if answer == "YES":

            st.markdown(
                f"""
                <div class="answer-yes">

                <b>Q.</b> {item['question']}<br><br>

                <b>🟢 YES</b>

                </div>
                """,
                unsafe_allow_html=True
            )

        elif answer == "NO":

            st.markdown(
                f"""
                <div class="answer-no">

                <b>Q.</b> {item['question']}<br><br>

                <b>🔴 NO</b>

                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="answer-unknown">

                <b>Q.</b> {item['question']}<br><br>

                <b>🟡 그 질문만으로는 알 수 없습니다.</b>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# 단서
# =========================================================

if st.session_state.clues:

    st.divider()

    st.subheader("📓 탐정 수첩 — 발견한 단서")

    for clue in st.session_state.clues:

        st.markdown(
            f"""
            <div class="clue">
            🔎 {clue}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 질문 소진
# =========================================================

if (
    st.session_state.questions_left <= 0
    and not st.session_state.case_finished
):

    st.warning(
        "⚠️ 질문을 모두 사용했습니다. "
        "이제 최종 추리를 제출하세요."
    )


# =========================================================
# 최종 추리
# =========================================================

st.divider()

st.subheader("🧠 최종 추리")

st.write(
    "충분히 조사했다면 사건의 진실을 직접 설명하세요."
)

final_answer = st.text_area(
    "당신의 추리",
    placeholder=(
        "예: 범인은 피해자의 시계를 조작해서 "
        "사망 시간을 속였습니다."
    ),
    value=st.session_state.final_answer
)

st.session_state.final_answer = final_answer


if st.button(
    "🚨 최종 추리 제출",
    use_container_width=True
):

    if len(final_answer.strip()) < 8:

        st.error(
            "조금 더 자세하게 설명해주세요."
        )

    else:

        answer_normalized = normalize(
            final_answer
        )

        matched = 0

        for keyword in case["keywords"]:

            if normalize(keyword) in answer_normalized:
                matched += 1

        # 키워드 2개 이상이면 성공
        if matched >= 2:

            st.session_state.case_finished = True
            st.session_state.case_won = True

            st.session_state.score += 50

        else:

            st.session_state.case_finished = True
            st.session_state.case_won = False

        st.rerun()


# =========================================================
# 하단
# =========================================================

st.divider()

st.caption(
    "🕵️ 예스노탐정 — 질문으로 진실을 밝혀라."
)
