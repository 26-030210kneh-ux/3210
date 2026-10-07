import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import random
import io

# =========================================================
# 페이지 설정
# =========================================================

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# 디자인
# =========================================================

st.markdown("""
<style>

.stApp {
    background: #080b10;
    color: #eeeeee;
}

.block-container {
    max-width: 1250px;
    padding-top: 30px;
    padding-bottom: 100px;
}

/* 기본 글자 */
p, span, label {
    color: #dfe7ef !important;
}

/* 제목 */
h1 {
    font-weight: 900 !important;
    letter-spacing: -2px;
}

h2, h3 {
    font-weight: 800 !important;
}

/* 버튼 */
.stButton > button {
    background-color: #162232 !important;
    color: #ffffff !important;
    border: 1px solid #40566d !important;
    border-radius: 9px !important;
    min-height: 48px;
    font-weight: 800 !important;
}

.stButton > button:hover {
    background-color: #21405b !important;
    border-color: #61b7ff !important;
    color: white !important;
}

/* 입력창 */
.stTextInput input,
.stTextArea textarea {
    background-color: #101720 !important;
    color: white !important;
    border: 1px solid #40566d !important;
}

/* 정보 박스 */
div[data-testid="stAlert"] {
    border-radius: 10px;
}

/* 카드 */
.card {
    background: #10161e;
    border: 1px solid #293747;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
}

.case-header {
    background: linear-gradient(
        90deg,
        #101923,
        #0b1118
    );
    border: 1px solid #34495c;
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 20px;
}

.case-title {
    font-size: 30px;
    font-weight: 900;
}

.case-sub {
    color: #8fa4b8;
    margin-top: 5px;
}

.stat {
    background: #101720;
    border: 1px solid #29394a;
    border-radius: 10px;
    text-align: center;
    padding: 14px;
}

.stat-label {
    color: #8195a8;
    font-size: 13px;
}

.stat-value {
    font-size: 27px;
    font-weight: 900;
    color: white;
}

.clue {
    background: #101923;
    border-left: 4px solid #4da9ed;
    border-radius: 7px;
    padding: 15px;
    margin-bottom: 10px;
}

.evidence-number {
    color: #63b9ff;
    font-size: 13px;
    font-weight: 900;
}

.ending-true {
    background: #10271e;
    border: 1px solid #35b879;
    padding: 25px;
    border-radius: 12px;
}

.ending-bad {
    background: #291316;
    border: 1px solid #c8525c;
    padding: 25px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 세션
# =========================================================

defaults = {
    "started": True,
    "question_count": 0,
    "score": 0,
    "trust": 100,
    "clues": [],
    "history": [],
    "asked": [],
    "game_over": False,
    "ending": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# 사건 현장 이미지 직접 생성
# =========================================================

def make_scene():

    W = 1000
    H = 600

    img = Image.new("RGB", (W, H), "#111820")
    draw = ImageDraw.Draw(img)

    # 바닥
    draw.rectangle(
        [0, 390, W, H],
        fill="#202831"
    )

    # 벽
    draw.rectangle(
        [0, 0, W, 390],
        fill="#18212a"
    )

    # 바닥 선
    for y in range(390, H, 35):
        draw.line(
            [0, y, W, y],
            fill="#2b343d",
            width=2
        )

    # 문
    draw.rectangle(
        [720, 70, 910, 390],
        fill="#252d35",
        outline="#4b5965",
        width=5
    )

    draw.rectangle(
        [745, 100, 885, 370],
        fill="#1d252d",
        outline="#596774",
        width=3
    )

    # 문 손잡이
    draw.ellipse(
        [850, 230, 870, 250],
        fill="#c0a15a"
    )

    # 창문
    draw.rectangle(
        [60, 70, 300, 250],
        fill="#0e2637",
        outline="#627584",
        width=5
    )

    draw.line(
        [180, 70, 180, 250],
        fill="#627584",
        width=4
    )

    draw.line(
        [60, 160, 300, 160],
        fill="#627584",
        width=4
    )

    # 책상
    draw.rectangle(
        [380, 220, 650, 250],
        fill="#594536"
    )

    draw.rectangle(
        [395, 250, 420, 400],
        fill="#443529"
    )

    draw.rectangle(
        [610, 250, 635, 400],
        fill="#443529"
    )

    # 램프
    draw.rectangle(
        [470, 150, 480, 220],
        fill="#c7b179"
    )

    draw.polygon(
        [
            (430, 150),
            (520, 150),
            (500, 190),
            (450, 190)
        ],
        fill="#d4bd7b"
    )

    # 사람 실루엣
    # 머리
    draw.ellipse(
        [310, 310, 390, 390],
        fill="#111419"
    )

    # 몸
    draw.polygon(
        [
            (335, 370),
            (420, 385),
            (520, 445),
            (470, 485),
            (360, 430),
            (285, 405)
        ],
        fill="#111419"
    )

    # 팔
    draw.line(
        [360, 390, 270, 455],
        fill="#0c1014",
        width=30
    )

    draw.line(
        [430, 405, 530, 455],
        fill="#0c1014",
        width=30
    )

    # 다리
    draw.line(
        [430, 450, 560, 520],
        fill="#0c1014",
        width=38
    )

    draw.line(
        [370, 445, 250, 520],
        fill="#0c1014",
        width=38
    )

    # 사건 번호
    draw.rectangle(
        [25, 20, 300, 60],
        fill="#0b1015",
        outline="#657584"
    )

    draw.text(
        (40, 30),
        "CASE 001  //  CRIME SCENE",
        fill="#e8edf2"
    )

    # 증거 표시
    markers = [
        (280, 470, "A"),
        (535, 430, "B"),
        (850, 330, "C"),
        (180, 275, "D")
    ]

    for x, y, letter in markers:

        draw.ellipse(
            [x-18, y-18, x+18, y+18],
            fill="#c93636",
            outline="#ffffff",
            width=2
        )

        draw.text(
            (x-6, y-10),
            letter,
            fill="white"
        )

    # 하단 경고
    draw.rectangle(
        [0, 550, W, H],
        fill="#090d12"
    )

    draw.text(
        (25, 563),
        "WARNING // 모든 현장 정보는 수사 기록의 일부입니다.",
        fill="#d9e0e7"
    )

    return img


scene = make_scene()


# =========================================================
# 데이터
# =========================================================

suspects = {

    "김민재": {
        "직업": "피해자의 회사 동료",
        "설명": "사건 당일 피해자와 마지막으로 통화한 사람.",
        "의심": "승진 문제로 피해자와 크게 다툰 적이 있음."
    },

    "박서연": {
        "직업": "피해자의 전 여자친구",
        "설명": "헤어진 뒤에도 피해자와 연락을 주고받음.",
        "의심": "사건 당일 밤 피해자에게 세 차례 전화."
    },

    "최도윤": {
        "직업": "건물 관리인",
        "설명": "건물 출입 시스템과 CCTV를 관리함.",
        "의심": "사건 시간대 CCTV 기록에 이상이 발생."
    },

    "한유진": {
        "직업": "피해자의 동생",
        "설명": "피해자와 가장 가까운 가족.",
        "의심": "가족 재산 문제로 피해자와 갈등."
    }
}


questions = [

    {
        "키워드": ["최도윤", "도윤", "관리인"],
        "답": "YES",
        "단서": "최도윤은 건물 CCTV 관리 프로그램의 관리자 권한을 가지고 있었다.",
        "점수": 10
    },

    {
        "키워드": ["cctv", "카메라", "영상"],
        "답": "NO",
        "단서": "CCTV에는 정확히 11분 38초의 영상 공백이 존재한다.",
        "점수": 10
    },

    {
        "키워드": ["출입", "기록"],
        "답": "YES",
        "단서": "사건 발생 직전 출입 기록 하나가 시스템에서 삭제되어 있었다.",
        "점수": 9
    },

    {
        "키워드": ["창문"],
        "답": "NO",
        "단서": "창문에는 외부에서 침입한 흔적이 전혀 없다.",
        "점수": 7
    },

    {
        "키워드": ["문", "현관"],
        "답": "NO",
        "단서": "현관문에는 강제 침입 흔적이 없다.",
        "점수": 7
    },

    {
        "키워드": ["김민재", "민재"],
        "답": "YES",
        "단서": "김민재는 밤 10시 47분 피해자와 통화했다.",
        "점수": 5
    },

    {
        "키워드": ["박서연", "서연"],
        "답": "YES",
        "단서": "박서연은 사건 당일 밤 피해자에게 세 번 전화했다.",
        "점수": 5
    },

    {
        "키워드": ["한유진", "유진", "동생"],
        "답": "YES",
        "단서": "한유진은 피해자의 친동생이며 예비 열쇠를 가지고 있었다.",
        "점수": 8
    },

    {
        "키워드": ["전화", "통화"],
        "답": "YES",
        "단서": "피해자의 마지막 통화 상대는 네 명의 용의자 중 누구도 아니었다.",
        "점수": 8
    },

    {
        "키워드": ["usb", "USB"],
        "답": "YES",
        "단서": "책상 아래에서 검은색 USB가 발견됐다.",
        "점수": 8
    },

    {
        "키워드": ["지문"],
        "답": "NO",
        "단서": "USB 표면은 누군가 깨끗하게 닦아놓은 상태였다.",
        "점수": 6
    },

    {
        "키워드": ["돈", "재산"],
        "답": "YES",
        "단서": "피해자의 휴대폰에서 돈 문제를 암시하는 메시지가 발견됐다.",
        "점수": 6
    },

    {
        "키워드": ["메시지", "문자"],
        "답": "YES",
        "단서": "휴대폰 백업에서 삭제된 메시지 일부가 복구됐다.",
        "점수": 8
    },

    {
        "키워드": ["알리바이"],
        "답": "NO",
        "단서": "네 명의 용의자 모두 알리바이에 작은 구멍이 존재한다.",
        "점수": 10
    },

    {
        "키워드": ["최도윤", "알리바이"],
        "답": "NO",
        "단서": "최도윤의 알리바이는 CCTV 공백 시간과 정확히 겹친다.",
        "점수": 12
    },

    {
        "키워드": ["최도윤", "접속"],
        "답": "YES",
        "단서": "관리실 컴퓨터 접속 기록에 최도윤의 계정이 남아 있었다.",
        "점수": 12
    },

    {
        "키워드": ["김민재", "알리바이"],
        "답": "NO",
        "단서": "김민재가 제출한 영수증의 시간에는 조작 가능성이 있다.",
        "점수": 7
    },

    {
        "키워드": ["박서연", "알리바이"],
        "답": "NO",
        "단서": "박서연의 알리바이를 증명하는 사람은 친구 한 명뿐이었다.",
        "점수": 7
    },

    {
        "키워드": ["한유진", "알리바이"],
        "답": "NO",
        "단서": "한유진의 휴대폰 위치 기록에서 이동 흔적이 발견됐다.",
        "점수": 9
    },

    {
        "키워드": ["열쇠"],
        "답": "YES",
        "단서": "한유진은 가족용 예비 열쇠를 가지고 있었다.",
        "점수": 9
    }
]


# =========================================================
# 상단 제목
# =========================================================

st.markdown(
    """
    <div class="case-header">
        <div class="case-title">🕵️ 예스노 탐정</div>
        <div class="case-sub">
            CASE 001 · 잠긴 방의 진실
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# 사건 현장
# =========================================================

st.subheader("📸 사건 현장")

st.image(
    scene,
    use_container_width=True
)

st.caption(
    "현장 사진을 자세히 살펴보세요. 빨간색 A/B/C/D 표시는 조사할 만한 지점입니다."
)


# =========================================================
# 사건 개요 + 현장 정보
# =========================================================

left, right = st.columns([1.3, 1])


with left:

    st.subheader("📋 사건 개요")

    st.info(
        """
        **새벽 1시 18분.**

        한 남자가 자신의 집에서 의식을 잃은 채 발견되었습니다.

        현관문은 잠겨 있었습니다.

        창문도 닫혀 있었습니다.

        외부 침입 흔적은 발견되지 않았습니다.

        그런데 현장에는 이상한 점이 있었습니다.

        **사건과 관련된 네 명의 사람 모두 서로 다른 거짓말을 하고 있었습니다.**

        당신의 임무는 단순히 범인을 찾는 것이 아닙니다.

        **누가 거짓말을 하고 있는지,
        왜 거짓말을 하고 있는지,
        그리고 그 거짓말 속에서 실제 범행의 흔적을 찾아야 합니다.**
        """
    )


with right:

    st.subheader("🔍 현장 기록")

    st.write("🕐 발견 시각: 새벽 1시 18분")
    st.write("🚪 현관문: 잠겨 있음")
    st.write("🪟 창문: 닫혀 있음")
    st.write("📹 CCTV: 11분 38초 공백")
    st.write("💾 삭제된 출입 기록: 1건")
    st.write("🔑 예비 열쇠: 존재")
    st.write("💻 관리실 컴퓨터: 접속 기록 존재")


# =========================================================
# 상태
# =========================================================

st.divider()

a, b, c, d = st.columns(4)

with a:
    st.markdown(
        f"""
        <div class="stat">
        <div class="stat-label">질문</div>
        <div class="stat-value">
        {st.session_state.question_count}/15
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with b:
    st.markdown(
        f"""
        <div class="stat">
        <div class="stat-label">수사 점수</div>
        <div class="stat-value">
        {st.session_state.score}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c:
    st.markdown(
        f"""
        <div class="stat">
        <div class="stat-label">신뢰도</div>
        <div class="stat-value">
        {st.session_state.trust}%
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with d:
    st.markdown(
        f"""
        <div class="stat">
        <div class="stat-label">확보 단서</div>
        <div class="stat-value">
        {len(st.session_state.clues)}
        </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# 용의자
# =========================================================

st.divider()

st.subheader("👤 용의자")

cols = st.columns(4)

for index, (name, info) in enumerate(suspects.items()):

    with cols[index]:

        with st.container(border=True):

            st.markdown(f"### {name}")

            st.caption(info["직업"])

            st.write(info["설명"])

            st.warning(
                "의심점\n\n" + info["의심"]
            )


# =========================================================
# 질문
# =========================================================

st.divider()

st.subheader("🔎 용의자에게 질문하기")

st.write(
    "질문은 자유롭게 입력할 수 있습니다. "
    "예: `최도윤은 CCTV를 관리할 수 있었습니까?`"
)

question = st.text_input(
    "질문",
    placeholder="궁금한 것을 질문하세요...",
    key="question_input"
)

if st.button("🔍 질문하기"):

    if not question.strip():

        st.warning("질문을 입력해주세요.")

    elif st.session_state.question_count >= 15:

        st.error("질문 기회를 모두 사용했습니다.")

    else:

        found = None

        for q in questions:

            if q["질문"] if "질문" in q else False:
                pass

            for keyword in q["키워드"]:

                if keyword.lower() in question.lower():

                    found = q
                    break

            if found:
                break

        if found is None:

            found = {
                "답": random.choice(["YES", "NO", "UNKNOWN"]),
                "단서": "현재 증거만으로는 이 질문에 확실한 결론을 내릴 수 없다.",
                "점수": 2
            }

        st.session_state.question_count += 1
        st.session_state.score += found["점수"]

        if found["답"] == "NO":
            st.session_state.trust -= 2

        st.session_state.history.append(
            {
                "질문": question,
                "답": found["답"],
                "단서": found["단서"]
            }
        )

        if found["단서"] not in st.session_state.clues:
            st.session_state.clues.append(
                found["단서"]
            )

        st.rerun()


# =========================================================
# 최근 답변
# =========================================================

if st.session_state.history:

    latest = st.session_state.history[-1]

    st.divider()

    st.subheader("📢 최근 답변")

    if latest["답"] == "YES":

        st.success("🟢 YES · 그렇습니다.")

    elif latest["답"] == "NO":

        st.error("🔴 NO · 아닙니다.")

    else:

        st.warning("🟡 UNKNOWN · 확실하지 않습니다.")

    st.info(
        "새로운 단서\n\n" + latest["단서"]
    )


# =========================================================
# 단서
# =========================================================

st.divider()

st.subheader("📁 확보한 단서")

if not st.session_state.clues:

    st.info(
        "아직 확보한 단서가 없습니다. "
        "사건 현장을 보고 질문을 시작하세요."
    )

else:

    for i, clue in enumerate(
        st.session_state.clues,
        1
    ):

        st.markdown(
            f"""
            <div class="clue">
                <div class="evidence-number">
                    EVIDENCE #{i}
                </div>
                <br>
                {clue}
            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# 수사 기록
# =========================================================

if st.session_state.history:

    st.divider()

    st.subheader("📜 수사 기록")

    for i, record in enumerate(
        st.session_state.history,
        1
    ):

        with st.expander(
            f"수사 기록 #{i} · {record['답']}"
        ):

            st.write(
                "**질문:**",
                record["질문"]
            )

            st.write(
                "**답변:**",
                record["답"]
            )

            st.write(
                "**단서:**",
                record["단서"]
            )


# =========================================================
# 최종 추리
# =========================================================

st.divider()

st.subheader("🧠 최종 추리")

if not st.session_state.game_over:

    st.write(
        "충분한 증거를 모았다고 생각한다면 "
        "범인을 지목하세요."
    )

    suspect = st.radio(
        "누가 범인이라고 생각합니까?",
        list(suspects.keys()),
        horizontal=True
    )

    reason = st.text_area(
        "당신의 추리",
        placeholder=(
            "예: CCTV 공백 시간과 관리실 접속 기록이 "
            "최도윤의 알리바이와 겹친다."
        ),
        height=120
    )

    if st.button("🚨 최종 추리 제출"):

        if len(st.session_state.clues) < 3:

            st.warning(
                "단서가 부족합니다. "
                "최소 3개의 단서를 확보하세요."
            )

        elif len(reason.strip()) < 5:

            st.warning(
                "추리 이유를 적어주세요."
            )

        else:

            if suspect == "최도윤":

                if st.session_state.score >= 60:

                    st.session_state.ending = "TRUE"

                else:

                    st.session_state.ending = "PARTIAL"

            else:

                st.session_state.ending = "BAD"

            st.session_state.game_over = True

            st.rerun()


# =========================================================
# 엔딩
# =========================================================

if st.session_state.game_over:

    st.divider()

    if st.session_state.ending == "TRUE":

        st.markdown(
            """
            <div class="ending-true">

            # 🏆 TRUE ENDING

            ## 사건 해결

            당신의 추리는 정확했습니다.

            진짜 범인은 **최도윤**.

            그는 건물 관리인이라는 자신의 권한을 이용해
            CCTV와 출입 기록에 접근했습니다.

            사건 시간대에 발생한 11분 38초의 CCTV 공백.

            삭제된 출입 기록.

            관리실 컴퓨터에 남아 있는 접속 기록.

            이 세 가지 증거는 우연이 아니었습니다.

            다른 용의자들도 거짓말을 하고 있었습니다.

            하지만 그들의 거짓말은 범행을 숨기기 위한 것이 아니라
            각자의 사생활을 숨기기 위한 것이었습니다.

            당신은 그 차이를 찾아냈습니다.

            **CASE 001 — SOLVED**

            </div>
            """,
            unsafe_allow_html=True
        )

    elif st.session_state.ending == "PARTIAL":

        st.warning(
            """
            # 🟡 PARTIAL ENDING

            범인은 맞혔습니다.

            하지만 결정적인 증거가 부족합니다.

            최도윤을 의심한 방향은 정확했습니다.

            하지만 경찰을 설득하기에는 증거가 부족했습니다.

            조금 더 조사했다면 완벽하게 해결할 수 있었습니다.
            """
        )

    else:

        st.markdown(
            """
            <div class="ending-bad">

            # 🔴 BAD ENDING

            ## 잘못된 추리

            당신은 잘못된 사람을 지목했습니다.

            가장 수상해 보이는 사람과
            진짜 범인은 같은 사람이 아니었습니다.

            사건 기록을 다시 살펴보면
            중요한 단서들이 다른 방향을 가리키고 있습니다.

            탐정에게 가장 위험한 것은

            **첫 번째로 떠오른 결론을 진실이라고 믿는 것.**

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    x, y = st.columns(2)

    with x:

        st.metric(
            "최종 점수",
            st.session_state.score
        )

    with y:

        st.metric(
            "확보 단서",
            len(st.session_state.clues)
        )

    st.write("")

    if st.button("🔄 사건 다시 시작"):

        for key in list(st.session_state.keys()):

            del st.session_state[key]

        st.rerun()


# =========================================================
# 하단
# =========================================================

st.divider()

st.caption(
    "🕵️ 예스노 탐정 · CASE 001 · "
    "모든 답은 단서가 되지만, 모든 단서가 진실은 아니다."
)
