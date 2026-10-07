import streamlit as st
import random
import time

# ============================================================
# 예스노 탐정
# YES / NO DETECTIVE
# Streamlit Single File Edition
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

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 50% -10%, rgba(70,110,160,0.18), transparent 35%),
        linear-gradient(180deg, #070b10 0%, #0b1118 50%, #070a0e 100%);
    color: #f2f5f8;
}

/* 전체 폭 */
.block-container {
    max-width: 1250px;
    padding-top: 2rem !important;
    padding-bottom: 5rem !important;
}

/* 기본 버튼 */
.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 10px;
    border: 1px solid #3c5268;
    background: #172330;
    color: #ffffff !important;
    font-weight: 800;
    font-size: 15px;
    transition: all 0.15s ease;
}

.stButton > button:hover {
    border-color: #63b3ed;
    background: #22364a;
    color: #ffffff !important;
    transform: translateY(-1px);
}

.stButton > button:focus {
    color: #ffffff !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.25);
}

/* 게임 시작 버튼 */
.start-button .stButton > button {
    background: linear-gradient(135deg, #1d79d8, #1557a0);
    border: 1px solid #65b7ff;
    color: white !important;
    min-height: 65px;
    font-size: 20px;
    box-shadow: 0 8px 30px rgba(30,120,220,0.22);
}

.start-button .stButton > button:hover {
    background: linear-gradient(135deg, #268df2, #1767ba);
    color: white !important;
}

/* 카드 */
.card {
    background: rgba(14, 22, 31, 0.92);
    border: 1px solid #263746;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 12px 35px rgba(0,0,0,0.18);
}

.card-small {
    background: #101923;
    border: 1px solid #273847;
    border-radius: 12px;
    padding: 17px;
    margin-bottom: 12px;
}

.case-title {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -2px;
    margin-bottom: 8px;
}

.subtitle {
    color: #8fa6bb;
    font-size: 16px;
    margin-bottom: 30px;
}

.section-title {
    font-size: 24px;
    font-weight: 900;
    margin: 10px 0 16px 0;
}

.small-label {
    color: #7890a5;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
}

.big-number {
    font-size: 30px;
    font-weight: 900;
}

.progress-box {
    background: #111a23;
    border: 1px solid #293c4c;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 16px;
}

.question-box {
    background: linear-gradient(135deg, #111d28, #0d151e);
    border: 1px solid #35516a;
    border-radius: 16px;
    padding: 24px;
    margin: 18px 0;
}

.answer-yes {
    color: #6ee7b7;
    font-weight: 900;
}

.answer-no {
    color: #fca5a5;
    font-weight: 900;
}

.answer-unknown {
    color: #fcd34d;
    font-weight: 900;
}

.clue {
    background: #0d171f;
    border-left: 4px solid #4da3ff;
    padding: 15px 18px;
    border-radius: 8px;
    margin-bottom: 10px;
}

.clue strong {
    color: #e8f4ff;
}

.warning {
    background: rgba(170, 45, 45, 0.12);
    border: 1px solid #713535;
    border-radius: 12px;
    padding: 16px;
}

.success {
    background: rgba(35, 150, 100, 0.12);
    border: 1px solid #2f7f62;
    border-radius: 12px;
    padding: 16px;
}

.ending {
    background: linear-gradient(135deg, #101d28, #0c141d);
    border: 1px solid #54728d;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}

.divider {
    height: 1px;
    background: #22313f;
    margin: 25px 0;
}

.locked {
    opacity: 0.45;
}

.footer {
    text-align: center;
    color: #566b7e;
    font-size: 12px;
    padding-top: 35px;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 세션 초기화
# ============================================================

def init_game():

    defaults = {
        "started": False,
        "question_count": 0,
        "score": 0,
        "trust": 100,
        "clues": [],
        "asked_questions": [],
        "history": [],
        "unlocked": [],
        "ending": None,
        "final_suspect": None,
        "final_reason": None,
        "game_over": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_game()


# ============================================================
# 사건 데이터
# ============================================================

SUSPECTS = {
    "김민재": {
        "role": "피해자의 동료",
        "description": "사건 당일 피해자와 마지막으로 통화한 사람.",
        "motive": "승진 문제로 피해자와 갈등이 있었다.",
        "secret": "사건 당일 밤 자신의 차를 숨겼다.",
    },

    "박서연": {
        "role": "피해자의 전 여자친구",
        "description": "헤어진 뒤에도 피해자와 연락을 주고받았다.",
        "motive": "피해자가 가지고 있던 중요한 물건을 돌려받고 싶었다.",
        "secret": "사건 당일 피해자에게 세 번 전화했다.",
    },

    "최도윤": {
        "role": "건물 관리인",
        "description": "사건 현장의 출입 기록을 관리한다.",
        "motive": "돈 문제 때문에 피해자에게 협박을 받았다.",
        "secret": "사건 시간대 출입 기록 하나를 삭제했다.",
    },

    "한유진": {
        "role": "피해자의 동생",
        "description": "피해자와 가장 가까운 가족.",
        "motive": "가족 재산 문제로 피해자와 다툰 적이 있다.",
        "secret": "사건 전날 피해자의 집에 몰래 들어갔다.",
    }
}


# ============================================================
# 질문 데이터
# ============================================================

QUESTIONS = [

    {
        "keywords": ["김민재", "동료", "민재"],
        "answer": "YES",
        "text": "김민재는 사건 당일 피해자와 통화했습니까?",
        "clue": "통화 기록을 확인했다. 김민재는 밤 10시 47분에 피해자와 4분 12초 동안 통화했다.",
        "score": 5,
    },

    {
        "keywords": ["박서연", "전여친", "서연"],
        "answer": "YES",
        "text": "박서연은 사건 당일 피해자에게 연락했습니까?",
        "clue": "박서연은 사건 당일 밤 피해자에게 세 차례 전화를 걸었다.",
        "score": 5,
    },

    {
        "keywords": ["최도윤", "관리인", "도윤"],
        "answer": "YES",
        "text": "최도윤은 사건 현장 출입 기록을 관리했습니까?",
        "clue": "최도윤은 건물 전체의 출입카드와 CCTV 관리 권한을 가지고 있었다.",
        "score": 5,
    },

    {
        "keywords": ["한유진", "동생", "유진"],
        "answer": "YES",
        "text": "한유진은 피해자의 가족입니까?",
        "clue": "한유진은 피해자의 친동생이다.",
        "score": 3,
    },

    {
        "keywords": ["차", "자동차", "김민재"],
        "answer": "YES",
        "text": "김민재는 사건 당일 자신의 차량을 숨겼습니까?",
        "clue": "주차장 CCTV에는 김민재의 차량이 평소 위치가 아닌 지하 2층 구석에 세워져 있었다.",
        "score": 8,
    },

    {
        "keywords": ["출입", "기록", "최도윤"],
        "answer": "YES",
        "text": "사건 시간대에 삭제된 출입 기록이 존재합니까?",
        "clue": "삭제된 기록은 사건 발생 약 20분 전이었다.",
        "score": 10,
    },

    {
        "keywords": ["cctv", "카메라", "영상"],
        "answer": "NO",
        "text": "CCTV 영상 전체가 정상적으로 남아 있습니까?",
        "clue": "CCTV에는 정확히 11분 38초 동안의 공백이 있다.",
        "score": 10,
    },

    {
        "keywords": ["전화", "통화"],
        "answer": "YES",
        "text": "피해자는 사건 직전에 누군가와 통화했습니까?",
        "clue": "피해자의 마지막 통화 상대는 사건 용의자 중 한 명이 아니다.",
        "score": 8,
    },

    {
        "keywords": ["문", "잠금", "현관"],
        "answer": "YES",
        "text": "현관문은 강제로 열린 흔적이 있었습니까?",
        "clue": "강제 침입의 흔적은 발견되지 않았다.",
        "score": 7,
    },

    {
        "keywords": ["창문"],
        "answer": "NO",
        "text": "범인은 창문으로 침입했습니까?",
        "clue": "창문에는 외부에서 침입한 흔적이 없었다.",
        "score": 7,
    },

    {
        "keywords": ["돈", "금전", "재산"],
        "answer": "YES",
        "text": "피해자는 사건 직전 금전 문제로 누군가와 갈등하고 있었습니까?",
        "clue": "피해자는 사건 당일 오후 '돈 문제는 오늘 끝내자'라는 메시지를 보냈다.",
        "score": 6,
    },

    {
        "keywords": ["메시지", "문자"],
        "answer": "YES",
        "text": "피해자의 휴대폰에서 삭제된 메시지가 발견됐습니까?",
        "clue": "삭제된 메시지 일부가 백업 서버에서 복구됐다.",
        "score": 9,
    },

    {
        "keywords": ["usb", "USB", "파일"],
        "answer": "YES",
        "text": "사건 현장에서 USB 저장장치가 발견됐습니까?",
        "clue": "책상 아래에서 검은색 USB가 발견됐다. 하지만 지문은 닦여 있었다.",
        "score": 8,
    },

    {
        "keywords": ["지문"],
        "answer": "NO",
        "text": "USB에서 범인의 지문이 그대로 발견됐습니까?",
        "clue": "USB 표면에는 지문이 남아 있지 않았다.",
        "score": 6,
    },

    {
        "keywords": ["시계", "시간"],
        "answer": "YES",
        "text": "현장에 사건 시간을 추정할 수 있는 물건이 있었습니까?",
        "clue": "깨진 벽시계가 11시 18분을 가리키고 있었다.",
        "score": 4,
    },

    {
        "keywords": ["알리바이"],
        "answer": "NO",
        "text": "네 명의 용의자 모두 완벽한 알리바이를 가지고 있습니까?",
        "clue": "모든 용의자의 알리바이에는 작은 구멍이 하나씩 존재한다.",
        "score": 10,
    },

    {
        "keywords": ["박서연", "전화"],
        "answer": "YES",
        "text": "박서연의 세 번째 전화가 사건 직전이었습니까?",
        "clue": "세 번째 전화는 밤 11시 07분. 사건 추정 시각보다 약 10분 전이었다.",
        "score": 8,
    },

    {
        "keywords": ["한유진", "집", "열쇠"],
        "answer": "YES",
        "text": "한유진은 피해자의 집 열쇠를 가지고 있었습니까?",
        "clue": "한유진은 가족용 예비 열쇠를 가지고 있었다.",
        "score": 9,
    },

    {
        "keywords": ["최도윤", "cctv", "관리"],
        "answer": "YES",
        "text": "최도윤은 CCTV를 직접 수정할 수 있었습니까?",
        "clue": "관리실 컴퓨터에는 CCTV 관리 프로그램의 접속 기록이 남아 있었다.",
        "score": 12,
    },

    {
        "keywords": ["김민재", "알리바이"],
        "answer": "NO",
        "text": "김민재의 알리바이는 완벽합니까?",
        "clue": "김민재는 편의점 영수증을 알리바이로 제출했지만 시간은 조작될 수 있었다.",
        "score": 8,
    },

    {
        "keywords": ["박서연", "알리바이"],
        "answer": "NO",
        "text": "박서연의 알리바이는 완벽합니까?",
        "clue": "박서연의 알리바이를 증명하는 사람은 실제로 그녀의 친구 한 명뿐이었다.",
        "score": 7,
    },

    {
        "keywords": ["한유진", "알리바이"],
        "answer": "NO",
        "text": "한유진의 알리바이는 완벽합니까?",
        "clue": "한유진은 집에 있었다고 주장했지만 휴대폰 위치 기록에는 이동 흔적이 있다.",
        "score": 9,
    },

    {
        "keywords": ["최도윤", "알리바이"],
        "answer": "NO",
        "text": "최도윤의 알리바이는 완벽합니까?",
        "clue": "최도윤은 관리실에 있었다고 했지만 CCTV 공백 시간과 정확히 겹친다.",
        "score": 12,
    },

]


# ============================================================
# 시작 화면
# ============================================================

def reset_game():
    st.session_state.started = True
    st.session_state.question_count = 0
    st.session_state.score = 0
    st.session_state.trust = 100
    st.session_state.clues = []
    st.session_state.asked_questions = []
    st.session_state.history = []
    st.session_state.unlocked = []
    st.session_state.ending = None
    st.session_state.final_suspect = None
    st.session_state.final_reason = None
    st.session_state.game_over = False


if not st.session_state.started:

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center; padding:55px 30px;">
        <div class="small-label">CASE FILE 001</div>
        <div class="case-title">🕵️ 예스노 탐정</div>
        <div class="subtitle">
            질문은 예 또는 아니오로 대답된다.<br>
            하지만 진실은 그렇게 간단하지 않다.
        </div>

        <div style="
            max-width:800px;
            margin:30px auto;
            padding:25px;
            background:#0b131b;
            border:1px solid #263c50;
            border-radius:15px;
            text-align:left;
        ">
            <b style="font-size:20px;">사건 개요</b>
            <br><br>
            새벽 1시 18분.<br>
            한 남자가 자신의 집에서 의식을 잃은 채 발견되었다.
            <br><br>
            현관문은 잠겨 있었다.
            창문은 닫혀 있었다.
            외부 침입 흔적도 없었다.
            <br><br>
            그런데 이상한 것이 하나 있었다.
            <br><br>
            <b>사건 현장에 있던 네 사람 모두 서로 다른 거짓말을 하고 있었다.</b>
        </div>

        <div style="
            max-width:800px;
            margin:0 auto;
            color:#8fa6bb;
            line-height:1.9;
        ">
            당신은 사건 담당 탐정이다.<br>
            용의자와 사건에 대해 질문할 수 있다.<br>
            단, 질문은 <b style="color:white;">예 / 아니오</b>로 답할 수 있는 형태여야 한다.
            <br><br>
            너무 많은 질문을 던지면 상대가 눈치챈다.<br>
            하지만 질문하지 않으면 중요한 단서를 놓친다.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='start-button'>", unsafe_allow_html=True)

    if st.button("🎮 수사 시작", key="start_game"):
        reset_game()
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="footer">
        YES / NO DETECTIVE · A STREAMLIT MYSTERY GAME
    </div>
    """, unsafe_allow_html=True)

    st.stop()


# ============================================================
# 게임 상단
# ============================================================

st.markdown("""
<div style="text-align:center;">
    <div class="small-label">CASE FILE 001 · INVESTIGATION MODE</div>
    <h1 style="
        font-size:42px;
        margin:5px 0 0 0;
        font-weight:900;
        letter-spacing:-2px;
    ">🕵️ 예스노 탐정</h1>
    <p style="color:#7890a5;">
        사건의 진실을 찾아라.
    </p>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 상태
# ============================================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="progress-box">
        <div class="small-label">질문 횟수</div>
        <div class="big-number">%d / 15</div>
    </div>
    """ % min(st.session_state.question_count, 15), unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="progress-box">
        <div class="small-label">수사 점수</div>
        <div class="big-number">%d</div>
    </div>
    """ % st.session_state.score, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="progress-box">
        <div class="small-label">신뢰도</div>
        <div class="big-number">%d%%</div>
    </div>
    """ % st.session_state.trust, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="progress-box">
        <div class="small-label">확보 단서</div>
        <div class="big-number">%d</div>
    </div>
    """ % len(st.session_state.clues), unsafe_allow_html=True)


# ============================================================
# 게임 종료 상태가 아닐 때
# ============================================================

if not st.session_state.game_over:

    left, right = st.columns([1.65, 1])

    # ========================================================
    # 왼쪽 - 질문
    # ========================================================

    with left:

        st.markdown("""
        <div class="section-title">
            🔎 질문하기
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="question-box">
            <b style="font-size:18px;">수사관에게 필요한 것은 질문입니다.</b>
            <br><br>
            예시:
            <br>
            • "김민재는 사건 당일 피해자와 통화했습니까?"
            <br>
            • "CCTV에 공백이 있었습니까?"
            <br>
            • "범인은 창문으로 들어왔습니까?"
            <br><br>
            <span style="color:#7890a5;">
            질문 속에 핵심 단어가 들어가면 사건 기록에서 관련 증거를 찾아줍니다.
            </span>
        </div>
        """, unsafe_allow_html=True)

        question = st.text_input(
            "질문",
            placeholder="예: 최도윤은 CCTV를 관리할 수 있었습니까?",
            key="question_input",
            label_visibility="collapsed"
        )

        if st.button("🔍 질문하기", key="ask_question"):

            if not question.strip():

                st.warning("질문을 입력하세요.")

            elif st.session_state.question_count >= 15:

                st.warning("질문 횟수를 모두 사용했습니다.")

            else:

                matched = None

                for item in QUESTIONS:

                    if item["text"] in st.session_state.asked_questions:
                        continue

                    for keyword in item["keywords"]:
                        if keyword.lower() in question.lower():
                            matched = item
                            break

                    if matched:
                        break

                if matched is None:

                    # 랜덤 일반 답변
                    generic = random.choice([
                        {
                            "answer": "UNKNOWN",
                            "text": "그 질문만으로는 확실한 결론을 낼 수 없습니다.",
                            "clue": "하지만 질문 자체가 사건의 중요한 부분을 건드리고 있다는 느낌이 든다.",
                            "score": 2
                        },
                        {
                            "answer": "NO",
                            "text": "현재 확보된 증거로는 그렇다고 볼 수 없습니다.",
                            "clue": "확실한 증거가 부족하다. 다른 방향으로 질문해보자.",
                            "score": 1
                        },
                        {
                            "answer": "YES",
                            "text": "가능성이 있습니다.",
                            "clue": "하지만 이것만으로 범인을 특정하기에는 부족하다.",
                            "score": 2
                        }
                    ])

                    matched = generic

                st.session_state.question_count += 1
                st.session_state.score += matched["score"]

                if matched["answer"] == "YES":
                    st.session_state.trust = max(
                        0,
                        st.session_state.trust - random.randint(1, 3)
                    )

                st.session_state.asked_questions.append(matched["text"])
                st.session_state.history.append({
                    "question": question,
                    "answer": matched["answer"],
                    "text": matched["text"],
                    "clue": matched["clue"]
                })

                if matched["clue"] not in st.session_state.clues:
                    st.session_state.clues.append(matched["clue"])

                st.rerun()

        # 최근 답변
        if st.session_state.history:

            last = st.session_state.history[-1]

            if last["answer"] == "YES":
                answer_class = "answer-yes"
                answer_text = "YES · 그렇다"
            elif last["answer"] == "NO":
                answer_class = "answer-no"
                answer_text = "NO · 아니다"
            else:
                answer_class = "answer-unknown"
                answer_text = "UNKNOWN · 확실하지 않다"

            st.markdown(f"""
            <div class="card">
                <div class="small-label">최근 답변</div>
                <h2 class="{answer_class}">{answer_text}</h2>

                <p style="font-size:17px;">
                    {last["text"]}
                </p>

                <div class="clue">
                    <b>🔎 새로 발견한 단서</b><br><br>
                    {last["clue"]}
                </div>
            </div>
            """, unsafe_allow_html=True)

        else:

            st.markdown("""
            <div class="card">
                <div class="small-label">수사 기록</div>
                <h3>아직 질문하지 않았습니다.</h3>
                <p style="color:#7890a5;">
                    사건의 핵심을 찌르는 질문을 해보세요.
                </p>
            </div>
            """, unsafe_allow_html=True)


    # ========================================================
    # 오른쪽 - 용의자
    # ========================================================

    with right:

        st.markdown("""
        <div class="section-title">
            👤 용의자
        </div>
        """, unsafe_allow_html=True)

        for name, data in SUSPECTS.items():

            st.markdown(f"""
            <div class="card-small">
                <div style="font-size:20px;font-weight:900;">
                    {name}
                </div>

                <div style="
                    color:#68a7d9;
                    font-size:13px;
                    margin-top:4px;
                ">
                    {data["role"]}
                </div>

                <div style="
                    color:#9db0c0;
                    font-size:13px;
                    margin-top:10px;
                    line-height:1.6;
                ">
                    {data["description"]}
                </div>
            </div>
            """, unsafe_allow_html=True)


# ============================================================
# 확보 단서
# ============================================================

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
    📁 확보한 증거
</div>
""", unsafe_allow_html=True)

if not st.session_state.clues:

    st.markdown("""
    <div class="card">
        <span style="color:#63788b;">
        아직 확보된 증거가 없습니다.
        질문을 통해 증거를 확보하세요.
        </span>
    </div>
    """, unsafe_allow_html=True)

else:

    for i, clue in enumerate(st.session_state.clues, 1):

        st.markdown(f"""
        <div class="clue">
            <b>증거 #{i}</b><br>
            {clue}
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 수사 기록
# ============================================================

if st.session_state.history:

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="section-title">
        📜 수사 기록
    </div>
    """, unsafe_allow_html=True)

    for i, item in enumerate(reversed(st.session_state.history), 1):

        if item["answer"] == "YES":
            icon = "🟢"
        elif item["answer"] == "NO":
            icon = "🔴"
        else:
            icon = "🟡"

        st.markdown(f"""
        <div class="card-small">
            <b>{icon} Q. {item["question"]}</b>
            <br><br>
            <span style="color:#8fa6bb;">
            {item["text"]}
            </span>
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# 최종 추리
# ============================================================

st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

st.markdown("""
<div class="section-title">
    🧠 최종 추리
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="card">
    <b style="font-size:18px;">
        이제 범인을 지목할 시간입니다.
    </b>
    <br><br>
    모든 단서를 종합해 가장 의심스러운 사람을 선택하세요.
    <br>
    <span style="color:#7890a5;">
    한 번 제출하면 되돌릴 수 없습니다.
    </span>
</div>
""", unsafe_allow_html=True)


# ============================================================
# 최종 추리 폼
# ============================================================

if not st.session_state.game_over:

    suspect_choice = st.radio(
        "범인은 누구라고 생각합니까?",
        list(SUSPECTS.keys()),
        horizontal=True
    )

    reason = st.text_area(
        "왜 그렇게 생각했습니까?",
        placeholder="예: CCTV 공백과 출입 기록 삭제가 연결되어 있기 때문입니다.",
        height=120
    )

    if st.button("🚨 최종 추리 제출", key="final_answer"):

        if len(st.session_state.clues) < 3:

            st.warning(
                "증거가 너무 부족합니다. 최소 3개의 단서를 확보하고 다시 생각해보세요."
            )

        elif not reason.strip():

            st.warning("추리 이유를 적어주세요.")

        else:

            st.session_state.final_suspect = suspect_choice
            st.session_state.final_reason = reason
            st.session_state.game_over = True

            # ================================================
            # 엔딩 계산
            # ================================================

            if suspect_choice == "최도윤":

                if st.session_state.score >= 70:

                    st.session_state.ending = "TRUE"

                else:

                    st.session_state.ending = "PARTIAL"

            elif suspect_choice == "김민재":

                st.session_state.ending = "WRONG"

            elif suspect_choice == "박서연":

                st.session_state.ending = "WRONG"

            elif suspect_choice == "한유진":

                st.session_state.ending = "WRONG"

            st.rerun()


# ============================================================
# 엔딩
# ============================================================

if st.session_state.game_over:

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    ending = st.session_state.ending

    if ending == "TRUE":

        st.markdown("""
        <div class="ending">

            <div class="small-label">
                TRUE ENDING
            </div>

            <h1 style="font-size:40px;">
                사건 해결
            </h1>

            <div style="
                font-size:21px;
                color:#6ee7b7;
                font-weight:800;
                margin:20px 0;
            ">
                당신은 진짜 범인을 찾아냈습니다.
            </div>

            <p style="
                color:#a7b9c8;
                line-height:2;
                font-size:16px;
            ">
                최도윤은 CCTV 관리 권한을 이용해 사건 시간대의
                기록을 삭제했습니다.
                <br><br>
                그는 자신이 관리하는 시스템에서 일부 기록을 없앤 뒤,
                자신에게 불리한 증거를 다른 용의자들의 행동과
                섞어버렸습니다.
                <br><br>
                그러나 완벽한 범죄는 아니었습니다.
                <br><br>
                삭제된 출입 기록과 CCTV 공백 시간이 정확히 겹쳤고,
                관리실 접속 기록까지 남아 있었습니다.
            </p>

            <div class="success" style="margin-top:25px;">
                <b>최종 판단</b><br><br>
                범인: 최도윤<br>
                수사 점수: """ + str(st.session_state.score) + """<br>
                확보 단서: """ + str(len(st.session_state.clues)) + """
            </div>

        </div>
        """, unsafe_allow_html=True)

    elif ending == "PARTIAL":

        st.markdown("""
        <div class="ending">

            <div class="small-label">
                PARTIAL ENDING
            </div>

            <h1 style="font-size:40px;">
                거의 다 왔다.
            </h1>

            <div style="
                font-size:20px;
                color:#fcd34d;
                font-weight:800;
                margin:20px 0;
            ">
                범인은 맞혔지만 결정적인 증거가 부족합니다.
            </div>

            <p style="
                color:#a7b9c8;
                line-height:2;
                font-size:16px;
            ">
                최도윤을 의심한 판단은 정확했습니다.
                <br><br>
                하지만 경찰에게 제출하기에는 증거가 부족합니다.
                <br>
                범행 동기와 직접적인 증거를 연결하지 못했습니다.
                <br><br>
                조금 더 질문했다면 완전한 사건 해결에 도달할 수 있었을 것입니다.
            </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="ending">

            <div class="small-label">
                BAD ENDING
            </div>

            <h1 style="font-size:40px;">
                잘못된 사람을 지목했다.
            </h1>

            <div style="
                font-size:20px;
                color:#fca5a5;
                font-weight:800;
                margin:20px 0;
            ">
                범인은 당신이 생각한 사람이 아니었습니다.
            </div>

            <p style="
                color:#a7b9c8;
                line-height:2;
                font-size:16px;
            ">
                사건 기록을 다시 확인해보니,
                당신이 놓친 단서들이 서로 연결되고 있었습니다.
                <br><br>
                가장 눈에 띄는 사람을 범인이라고 생각했지만
                눈에 띄는 것과 범인이라는 것은 같은 의미가 아닙니다.
                <br><br>
                진짜 범인은 사건의 중심에서
                조용히 모든 것을 지켜보고 있었습니다.
            </p>

        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    if st.button("🔄 처음부터 다시 수사하기", key="restart"):

        for key in [
            "started",
            "question_count",
            "score",
            "trust",
            "clues",
            "asked_questions",
            "history",
            "unlocked",
            "ending",
            "final_suspect",
            "final_reason",
            "game_over"
        ]:
            if key in st.session_state:
                del st.session_state[key]

        st.rerun()


# ============================================================
# 게임 하단
# ============================================================

st.markdown("""
<div class="footer">
    ─────────────────────────────<br>
    예스노 탐정 · CASE FILE 001<br>
    질문에는 답이 있지만, 답이 항상 진실인 것은 아니다.
</div>
""", unsafe_allow_html=True)
