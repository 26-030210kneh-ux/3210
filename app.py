import streamlit as st
import streamlit.components.v1 as components
import random

# ============================================================
# 페이지
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

html, body, [data-testid="stAppViewContainer"] {
    background:#070a0e !important;
}

[data-testid="stHeader"] {
    background:#070a0e !important;
}

[data-testid="stToolbar"] {
    display:none;
}

.block-container {
    max-width:1500px !important;
    padding-top:12px !important;
    padding-bottom:8px !important;
    padding-left:22px !important;
    padding-right:22px !important;
}

section.main > div {
    padding-bottom:0 !important;
}

/* 전체 페이지 스크롤 제거 */
html, body {
    overflow:hidden !important;
}

.main {
    overflow:hidden !important;
}

* {
    box-sizing:border-box;
}

/* 글자 */
body, p, span, label, div {
    font-family:
    "Malgun Gothic",
    "Noto Sans KR",
    Arial,
    sans-serif;
}

h1,h2,h3 {
    margin:0 !important;
}

/* 버튼 */
.stButton > button {
    width:100% !important;
    background:#172435 !important;
    color:#ffffff !important;
    border:1px solid #48647e !important;
    border-radius:6px !important;
    font-weight:800 !important;
    min-height:38px !important;
    padding:5px 10px !important;
}

.stButton > button:hover {
    background:#24445f !important;
    border-color:#65c2ff !important;
}

/* 입력 */
.stTextInput {
    margin-bottom:3px !important;
}

.stTextInput > div > div > input {
    background:#0c131b !important;
    color:#ffffff !important;
    border:1px solid #41566c !important;
    border-radius:6px !important;
    height:40px !important;
    font-size:13px !important;
}

/* 라디오 */
.stRadio > div {
    gap:4px !important;
}

.stRadio label {
    background:#0d141c !important;
    border:1px solid #263544 !important;
    border-radius:5px !important;
    padding:4px 7px !important;
    font-size:12px !important;
}

/* 알림 */
div[data-testid="stAlert"] {
    padding:8px 10px !important;
    margin:5px 0 !important;
    font-size:12px !important;
}

/* Streamlit 기본 여백 */
[data-testid="column"] {
    padding-left:5px !important;
    padding-right:5px !important;
}

/* 이미지 */
img {
    border-radius:7px !important;
}

/* Expander */
.streamlit-expanderHeader {
    font-size:12px !important;
}

/* 모바일 */
@media(max-width:900px) {

    html, body {
        overflow:auto !important;
    }

    .block-container {
        padding:10px !important;
    }

}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 세션 초기화
# ============================================================

if "questions" not in st.session_state:
    st.session_state.questions = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "trust" not in st.session_state:
    st.session_state.trust = 100

if "clues" not in st.session_state:
    st.session_state.clues = []

if "history" not in st.session_state:
    st.session_state.history = []

if "finished" not in st.session_state:
    st.session_state.finished = False

if "ending" not in st.session_state:
    st.session_state.ending = ""


# ============================================================
# 사건 데이터
# ============================================================

suspects = {

    "김민재": {
        "role":"피해자의 회사 동료",
        "desc":"사건 당일 피해자와 마지막으로 통화한 동료.",
        "secret":"승진 문제로 피해자와 크게 다툰 적이 있다."
    },

    "박서연": {
        "role":"피해자의 전 여자친구",
        "desc":"헤어진 뒤에도 피해자와 연락을 주고받았다.",
        "secret":"사건 당일 피해자에게 세 번 전화했다."
    },

    "최도윤": {
        "role":"건물 관리인",
        "desc":"건물 출입 시스템과 CCTV를 관리한다.",
        "secret":"CCTV 관리자 권한을 가지고 있다."
    },

    "한유진": {
        "role":"피해자의 동생",
        "desc":"피해자와 가족 문제로 갈등이 있었다.",
        "secret":"집의 예비 열쇠를 가지고 있었다."
    }
}


answers = [

    (
        ["최도윤","도윤","관리인"],
        "YES",
        "최도윤은 건물 CCTV 관리자 권한을 가지고 있었습니다.",
        10
    ),

    (
        ["cctv","CCTV","카메라"],
        "NO",
        "CCTV에는 정확히 11분 38초의 영상 공백이 존재합니다.",
        10
    ),

    (
        ["출입","기록"],
        "YES",
        "사건 직전 출입 기록 하나가 시스템에서 삭제되어 있었습니다.",
        10
    ),

    (
        ["창문"],
        "NO",
        "창문에는 외부에서 침입한 흔적이 없습니다.",
        6
    ),

    (
        ["현관","문"],
        "NO",
        "현관문에는 강제 침입 흔적이 없습니다.",
        6
    ),

    (
        ["김민재","민재"],
        "YES",
        "김민재는 밤 10시 47분 피해자와 통화했습니다.",
        5
    ),

    (
        ["박서연","서연"],
        "YES",
        "박서연은 사건 당일 밤 피해자에게 세 차례 전화했습니다.",
        5
    ),

    (
        ["한유진","유진","동생"],
        "YES",
        "한유진은 피해자의 친동생이며 예비 열쇠를 가지고 있습니다.",
        8
    ),

    (
        ["전화","통화"],
        "YES",
        "피해자의 마지막 통화 상대는 네 명의 용의자 중 누구도 아닙니다.",
        8
    ),

    (
        ["usb","USB"],
        "YES",
        "책상 아래에서 검은색 USB가 발견됐습니다.",
        8
    ),

    (
        ["지문"],
        "NO",
        "USB 표면은 누군가 깨끗하게 닦아놓은 상태였습니다.",
        6
    ),

    (
        ["돈","재산"],
        "YES",
        "피해자의 휴대폰에는 돈 문제를 암시하는 메시지가 남아 있습니다.",
        6
    ),

    (
        ["메시지","문자"],
        "YES",
        "삭제된 메시지 일부가 복구되었습니다.",
        8
    ),

    (
        ["알리바이"],
        "NO",
        "네 명의 용의자 모두 알리바이에 작은 구멍이 존재합니다.",
        8
    ),

    (
        ["최도윤","알리바이"],
        "NO",
        "최도윤의 알리바이는 CCTV 공백 시간과 정확히 겹칩니다.",
        12
    ),

    (
        ["최도윤","접속"],
        "YES",
        "관리실 컴퓨터 접속 기록에 최도윤의 계정이 남아 있습니다.",
        12
    ),

    (
        ["열쇠"],
        "YES",
        "한유진은 가족용 예비 열쇠를 가지고 있습니다.",
        8
    ),

    (
        ["범인"],
        "UNKNOWN",
        "현재 증거만으로는 범인을 단정하면 안 됩니다.",
        3
    )

]


# ============================================================
# 사건 사진
# SVG로 직접 제작
# ============================================================

scene_svg = """
<svg width="100%" height="100%" viewBox="0 0 1000 620"
     xmlns="http://www.w3.org/2000/svg">

<!-- 배경 -->
<rect width="1000" height="620" fill="#10161d"/>

<!-- 벽 -->
<rect x="0" y="0" width="1000" height="400"
      fill="#1a222b"/>

<!-- 벽 그림자 -->
<rect x="0" y="350" width="1000" height="50"
      fill="#151b21"/>

<!-- 바닥 -->
<rect x="0" y="400" width="1000" height="220"
      fill="#252c32"/>

<!-- 바닥 타일 -->
<path d="M0 455 L1000 455
         M0 510 L1000 510
         M0 565 L1000 565"
      stroke="#343d44"
      stroke-width="2"/>

<path d="M150 400 L100 620
         M330 400 L300 620
         M500 400 L500 620
         M680 400 L710 620
         M850 400 L920 620"
      stroke="#303940"
      stroke-width="2"/>


<!-- 창문 -->
<rect x="55" y="60" width="265" height="210"
      rx="5"
      fill="#0c2535"
      stroke="#657580"
      stroke-width="7"/>

<rect x="70" y="75" width="235" height="180"
      fill="#102c3d"/>

<line x1="187" y1="75" x2="187" y2="255"
      stroke="#657580" stroke-width="5"/>

<line x1="70" y1="165" x2="305" y2="165"
      stroke="#657580" stroke-width="5"/>

<!-- 창밖 빛 -->
<polygon points="75,90 175,90 175,150 75,130"
         fill="#1e4355" opacity="0.8"/>


<!-- 액자 -->
<rect x="410" y="45" width="200" height="150"
      fill="#101418"
      stroke="#555f66"
      stroke-width="7"/>

<rect x="430" y="65" width="160" height="110"
      fill="#2b3033"/>

<!-- 가족사진 실루엣 -->
<circle cx="475" cy="110" r="25" fill="#101418"/>
<circle cx="545" cy="105" r="25" fill="#101418"/>

<path d="M445 160 Q475 125 505 160
         M515 160 Q545 120 575 160"
      fill="#101418"/>


<!-- 문 -->
<rect x="765" y="65" width="180" height="335"
      fill="#151b20"
      stroke="#69757e"
      stroke-width="7"/>

<rect x="785" y="85" width="140" height="285"
      fill="#20272d"
      stroke="#4b555d"
      stroke-width="3"/>

<circle cx="895" cy="235" r="12"
        fill="#b6a06a"/>


<!-- 책상 -->
<rect x="390" y="260" width="285" height="32"
      rx="4"
      fill="#5a4334"/>

<rect x="410" y="292" width="25" height="155"
      fill="#443328"/>

<rect x="630" y="292" width="25" height="155"
      fill="#443328"/>


<!-- 램프 -->
<rect x="515" y="175" width="10" height="85"
      fill="#b99b62"/>

<path d="M465 175 L575 175 L550 215 L490 215 Z"
      fill="#d2b875"/>

<ellipse cx="520" cy="220" rx="38" ry="8"
         fill="#c3a966"/>


<!-- 人物 / 쓰러진 사람 -->
<ellipse cx="325" cy="385"
         rx="48" ry="43"
         fill="#111519"/>

<path d="
M345 410
Q410 405 490 455
L570 505
L530 550
L450 510
L360 470
L275 445
Z"
fill="#111519"/>

<!-- 팔 -->
<path d="M370 430 L275 500"
      stroke="#0d1115"
      stroke-width="38"
      stroke-linecap="round"/>

<path d="M445 445 L555 500"
      stroke="#0d1115"
      stroke-width="38"
      stroke-linecap="round"/>

<!-- 다리 -->
<path d="M475 495 L650 565"
      stroke="#0c1014"
      stroke-width="48"
      stroke-linecap="round"/>

<path d="M400 485 L270 565"
      stroke="#0c1014"
      stroke-width="48"
      stroke-linecap="round"/>


<!-- 바닥 혈흔 느낌 -->
<ellipse cx="325" cy="500"
         rx="65" ry="14"
         fill="#57252a"
         opacity="0.7"/>


<!-- 증거 A -->
<circle cx="270" cy="500" r="23"
        fill="#b63139"
        stroke="white"
        stroke-width="2"/>

<text x="262" y="508"
      fill="white"
      font-size="24"
      font-weight="bold">A</text>


<!-- 증거 B -->
<circle cx="600" cy="440" r="23"
        fill="#b63139"
        stroke="white"
        stroke-width="2"/>

<text x="592" y="448"
      fill="white"
      font-size="24"
      font-weight="bold">B</text>


<!-- 증거 C -->
<circle cx="850" cy="345" r="23"
        fill="#b63139"
        stroke="white"
        stroke-width="2"/>

<text x="842" y="353"
      fill="white"
      font-size="24"
      font-weight="bold">C</text>


<!-- 증거 D -->
<circle cx="185" cy="300" r="23"
        fill="#b63139"
        stroke="white"
        stroke-width="2"/>

<text x="177" y="308"
      fill="white"
      font-size="24"
      font-weight="bold">D</text>


<!-- 상단 사건 태그 -->
<rect x="22" y="18"
      width="280"
      height="42"
      rx="5"
      fill="#0b1015"
      stroke="#7a8994"/>

<text x="40" y="45"
      fill="#e7edf2"
      font-size="20"
      font-family="Arial"
      font-weight="bold">
CASE 001 · CRIME SCENE
</text>


<!-- 하단 현장 경고 -->
<rect x="0" y="575"
      width="1000"
      height="45"
      fill="#080b0e"/>

<text x="25" y="604"
      fill="#b8c5cf"
      font-size="18">
현장 보존 기록 · 외부 침입 흔적 없음 · CCTV 11분 38초 공백
</text>

</svg>
"""


# ============================================================
# 상단
# ============================================================

st.markdown("""
<div style="
display:flex;
align-items:center;
justify-content:space-between;
height:48px;
border-bottom:1px solid #26323e;
margin-bottom:8px;
">

<div>
<span style="
font-size:25px;
font-weight:900;
color:white;
">🕵️ 예스노 탐정</span>

<span style="
font-size:12px;
color:#7890a5;
margin-left:12px;
">
CASE 001 · 잠긴 방의 진실
</span>
</div>

<div style="
font-size:12px;
color:#9eb2c4;
">
수사관 모드 · 사건 진행 중
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# 상단 통계
# ============================================================

s1, s2, s3, s4 = st.columns(4)

with s1:
    st.markdown(
        f"""
        <div style="
        background:#0e151d;
        border:1px solid #263746;
        border-radius:6px;
        padding:7px;
        text-align:center;
        height:53px;
        ">
        <div style="font-size:10px;color:#718598;">질문</div>
        <b style="font-size:20px;color:white;">
        {st.session_state.questions}/15
        </b>
        </div>
        """,
        unsafe_allow_html=True
    )

with s2:
    st.markdown(
        f"""
        <div style="
        background:#0e151d;
        border:1px solid #263746;
        border-radius:6px;
        padding:7px;
        text-align:center;
        height:53px;
        ">
        <div style="font-size:10px;color:#718598;">수사 점수</div>
        <b style="font-size:20px;color:white;">
        {st.session_state.score}
        </b>
        </div>
        """,
        unsafe_allow_html=True
    )

with s3:
    st.markdown(
        f"""
        <div style="
        background:#0e151d;
        border:1px solid #263746;
        border-radius:6px;
        padding:7px;
        text-align:center;
        height:53px;
        ">
        <div style="font-size:10px;color:#718598;">신뢰도</div>
        <b style="font-size:20px;color:#70d4a0;">
        {st.session_state.trust}%
        </b>
        </div>
        """,
        unsafe_allow_html=True
    )

with s4:
    st.markdown(
        f"""
        <div style="
        background:#0e151d;
        border:1px solid #263746;
        border-radius:6px;
        padding:7px;
        text-align:center;
        height:53px;
        ">
        <div style="font-size:10px;color:#718598;">확보 단서</div>
        <b style="font-size:20px;color:#67baff;">
        {len(st.session_state.clues)}
        </b>
        </div>
        """,
        unsafe_allow_html=True
    )


st.write("")


# ============================================================
# 메인 3분할
# ============================================================

left, middle, right = st.columns(
    [1.55, 1, 0.95],
    gap="small"
)


# ============================================================
# LEFT — 사건 현장
# ============================================================

with left:

    st.markdown("""
    <div style="
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:5px;
    ">
    <b style="font-size:19px;color:white;">
    📸 사건 현장
    </b>
    <span style="
    font-size:10px;
    color:#7e92a4;
    ">
    현장 사진 #001
    </span>
    </div>
    """, unsafe_allow_html=True)

    components.html(
        scene_svg,
        height=470,
        scrolling=False
    )

    st.markdown("""
    <div style="
    margin-top:5px;
    background:#0d141b;
    border:1px solid #253440;
    border-radius:5px;
    padding:7px 10px;
    font-size:11px;
    color:#9eb0bf;
    ">
    🔴 <b>A</b> 쓰러진 피해자　
    🔴 <b>B</b> 책상 주변　
    🔴 <b>C</b> 현관　
    🔴 <b>D</b> 창문
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# MIDDLE — 심문
# ============================================================

with middle:

    st.markdown("""
    <div style="
    font-size:19px;
    font-weight:900;
    color:white;
    margin-bottom:4px;
    ">
    🔎 기록실 심문
    </div>

    <div style="
    font-size:11px;
    color:#7f93a5;
    margin-bottom:7px;
    ">
    용의자와 사건에 대해 질문하세요.
    대답은 항상 진실이라고 할 수 없습니다.
    </div>
    """, unsafe_allow_html=True)

    question = st.text_input(
        "질문",
        placeholder="예: 최도윤은 CCTV를 관리할 수 있었나요?",
        label_visibility="collapsed",
        key="question"
    )

    if st.button("🔍 질문하기", key="ask"):

        if not question.strip():

            st.warning("질문을 입력하세요.")

        elif st.session_state.questions >= 15:

            st.error("질문 기회를 모두 사용했습니다.")

        else:

            found = None

            for keywords, answer, clue, score in answers:

                for keyword in keywords:

                    if keyword.lower() in question.lower():

                        found = (
                            answer,
                            clue,
                            score
                        )
                        break

                if found:
                    break

            if found is None:

                found = (
                    random.choice(
                        ["YES", "NO", "UNKNOWN"]
                    ),
                    "현재 증거만으로는 확실한 결론을 내릴 수 없습니다.",
                    2
                )

            answer, clue, score = found

            st.session_state.questions += 1
            st.session_state.score += score

            if answer == "NO":
                st.session_state.trust = max(
                    0,
                    st.session_state.trust - 2
                )

            if clue not in st.session_state.clues:
                st.session_state.clues.append(clue)

            st.session_state.history.append(
                {
                    "q":question,
                    "a":answer,
                    "clue":clue
                }
            )

            st.rerun()


    # 최근 답변

    if st.session_state.history:

        latest = st.session_state.history[-1]

        color = {
            "YES":"#6fd3a0",
            "NO":"#ff7373",
            "UNKNOWN":"#e6c66c"
        }.get(latest["a"], "white")

        st.markdown(
            f"""
            <div style="
            background:#0d1822;
            border:1px solid #263b4d;
            border-radius:6px;
            padding:10px;
            margin-top:8px;
            min-height:105px;
            ">

            <div style="
            font-size:10px;
            color:#71889a;
            ">
            LAST RESPONSE
            </div>

            <div style="
            color:{color};
            font-size:21px;
            font-weight:900;
            margin:3px 0;
            ">
            {latest["a"]}
            </div>

            <div style="
            font-size:12px;
            line-height:1.5;
            color:#d2dce4;
            ">
            {latest["clue"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown("""
        <div style="
        background:#0d1822;
        border:1px solid #263b4d;
        border-radius:6px;
        padding:12px;
        margin-top:8px;
        height:105px;
        color:#7f95a7;
        font-size:12px;
        ">
        아직 질문하지 않았습니다.<br><br>
        사건 사진과 용의자를 먼저 확인하세요.
        </div>
        """, unsafe_allow_html=True)


    # 최근 질문 기록

    st.markdown("""
    <div style="
    font-size:13px;
    font-weight:800;
    color:white;
    margin-top:10px;
    margin-bottom:3px;
    ">
    📜 최근 수사 기록
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.history:

        recent = st.session_state.history[-3:]

        for i, record in enumerate(
            reversed(recent),
            1
        ):

            st.markdown(
                f"""
                <div style="
                background:#0a1118;
                border-bottom:1px solid #1d2a35;
                padding:5px;
                font-size:10px;
                color:#a9b8c4;
                ">
                <b style="color:#6db9ef;">
                Q
                </b>
                {record["q"][:38]}
                <span style="float:right;">
                {record["a"]}
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# RIGHT — 용의자
# ============================================================

with right:

    st.markdown("""
    <div style="
    font-size:19px;
    font-weight:900;
    color:white;
    margin-bottom:5px;
    ">
    👤 용의자
    </div>
    """, unsafe_allow_html=True)

    for name, data in suspects.items():

        st.markdown(
            f"""
            <div style="
            background:#0d141b;
            border:1px solid #263542;
            border-radius:6px;
            padding:8px;
            margin-bottom:5px;
            ">

            <div style="
            font-size:16px;
            font-weight:900;
            color:#f2f5f7;
            ">
            {name}
            </div>

            <div style="
            font-size:9px;
            color:#70879a;
            margin-top:2px;
            ">
            {data["role"]}
            </div>

            <div style="
            font-size:10px;
            color:#b8c6d1;
            margin-top:5px;
            line-height:1.35;
            ">
            {data["desc"]}
            </div>

            <div style="
            background:#171e0d;
            color:#d5d99b;
            border-radius:3px;
            padding:5px;
            margin-top:5px;
            font-size:9px;
            ">
            의심점 · {data["secret"]}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 하단 단서
# ============================================================

st.markdown("""
<div style="
border-top:1px solid #25313c;
margin-top:7px;
padding-top:7px;
display:flex;
align-items:center;
">
<div style="
font-size:14px;
font-weight:900;
color:white;
margin-right:12px;
">
📁 확보 단서
</div>
""", unsafe_allow_html=True)

if st.session_state.clues:

    clue_text = ""

    for i, clue in enumerate(
        st.session_state.clues[-5:],
        1
    ):

        clue_text += f"""
        <span style="
        display:inline-block;
        background:#101a23;
        border:1px solid #294052;
        border-radius:4px;
        padding:5px 7px;
        margin-right:4px;
        font-size:9px;
        color:#a9c8dd;
        ">
        {i}. {clue[:34]}
        </span>
        """

    st.markdown(
        clue_text,
        unsafe_allow_html=True
    )

else:

    st.markdown(
        """
        <span style="
        font-size:10px;
        color:#617383;
        ">
        아직 확보된 단서가 없습니다.
        </span>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# 최종 추리
# ============================================================

st.markdown("""
<div style="
border-top:1px solid #25313c;
margin-top:7px;
padding-top:5px;
">
</div>
""", unsafe_allow_html=True)

if not st.session_state.finished:

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:

        suspect_choice = st.selectbox(
            "범인",
            list(suspects.keys()),
            key="suspect"
        )

    with col2:

        reason = st.text_input(
            "최종 추리",
            placeholder="왜 이 사람이 범인인지 한 줄로 설명하세요.",
            key="reason"
        )

    with col3:

        if st.button(
            "🚨 최종 추리 제출",
            key="finish"
        ):

            if len(st.session_state.clues) < 3:

                st.warning(
                    "단서를 최소 3개 확보하세요."
                )

            elif len(reason.strip()) < 3:

                st.warning(
                    "추리 이유를 적어주세요."
                )

            else:

                st.session_state.finished = True

                if (
                    suspect_choice == "최도윤"
                    and st.session_state.score >= 45
                ):

                    st.session_state.ending = "TRUE"

                elif suspect_choice == "최도윤":

                    st.session_state.ending = "PARTIAL"

                else:

                    st.session_state.ending = "BAD"

                st.rerun()


# ============================================================
# 엔딩
# ============================================================

else:

    if st.session_state.ending == "TRUE":

        st.success(
            "🏆 TRUE ENDING · 범인은 최도윤입니다. "
            "CCTV 공백과 관리실 접속 기록이 결정적인 증거였습니다."
        )

    elif st.session_state.ending == "PARTIAL":

        st.warning(
            "🟡 PARTIAL ENDING · 범인은 맞혔지만 결정적인 증거가 부족합니다."
        )

    else:

        st.error(
            "🔴 BAD ENDING · 잘못된 사람을 지목했습니다. "
            "사건 기록을 다시 살펴보세요."
        )

    if st.button("🔄 사건 다시 시작"):

        for key in list(st.session_state.keys()):
            del st.session_state[key]

        st.rerun()


# ============================================================
# 아주 작은 하단
# ============================================================

st.markdown("""
<div style="
text-align:center;
color:#455563;
font-size:8px;
margin-top:2px;
">
예스노 탐정 · CASE 001 · 모든 단서가 진실을 말하는 것은 아니다.
</div>
""", unsafe_allow_html=True)
