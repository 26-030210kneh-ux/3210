import streamlit as st
import re

st.set_page_config(
    page_title="예스노 탐정",
    page_icon="🔎",
    layout="wide"
)

# =========================================================
# CSS
# =========================================================

st.markdown("""
<style>

.stApp {
    background:#060b11;
    color:#edf6ff;
}

.block-container {
    max-width:1450px;
    padding-top:18px;
    padding-bottom:10px;
}

header {
    visibility:hidden;
}

#MainMenu {
    visibility:hidden;
}

footer {
    visibility:hidden;
}

.case-photo {
    height:285px;
    border-radius:12px;
    background:
    linear-gradient(rgba(0,0,0,.15),rgba(0,0,0,.78)),
    url("https://images.unsplash.com/photo-1505693416388-ac5ce068fe85?auto=format&fit=crop&w=1400&q=85")
    center/cover;
    position:relative;
}

.photo-title {
    position:absolute;
    bottom:20px;
    left:24px;
    font-size:29px;
    font-weight:900;
}

.photo-info {
    position:absolute;
    bottom:59px;
    left:24px;
    color:#b7cbd8;
    font-size:12px;
}

.card {
    background:#0c151e;
    border:1px solid #21394b;
    border-radius:10px;
    padding:17px;
    margin-top:10px;
}

.question-area {
    background:#09131c;
    border:1px solid #254357;
    border-radius:10px;
    padding:15px;
}

.answer {
    background:#081722;
    border:1px solid #28516a;
    border-radius:8px;
    padding:14px;
    margin-top:10px;
}

.yes {
    color:#42d5ff;
    font-size:23px;
    font-weight:900;
}

.no {
    color:#ffc36b;
    font-size:23px;
    font-weight:900;
}

.unknown {
    color:#b9a9ff;
    font-size:23px;
    font-weight:900;
}

.clue {
    background:#0b1720;
    border-left:3px solid #43d3ff;
    border-radius:5px;
    padding:8px 10px;
    margin:5px 0;
    font-size:12px;
}

.hint {
    background:#11172a;
    border:1px solid #514b8c;
    border-radius:8px;
    padding:13px;
    color:#ddd8ff;
}

.suspect {
    background:#0b151e;
    border:1px solid #203c50;
    border-radius:8px;
    padding:10px;
    margin-bottom:7px;
}

.ending {
    background:#07151e;
    border:2px solid #42d5ff;
    border-radius:12px;
    padding:28px;
    text-align:center;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# STATE
# =========================================================

defaults = {
    "questions": 0,
    "score": 0,
    "clues": [],
    "history": [],
    "last_answer": None,
    "hint_used": 0,
    "ending": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# CASE
# =========================================================

CASE_NAME = "잠긴 방의 진실"

suspects = {
    "김민재": {
        "role": "피해자의 직장 동료",
        "info": "승진 문제로 피해자와 크게 다퉜다.",
        "danger": "높음",
    },
    "박서연": {
        "role": "피해자의 전 여자친구",
        "info": "사건 직전 피해자에게 세 번 전화했다.",
        "danger": "중간",
    },
    "최도윤": {
        "role": "피해자의 이웃",
        "info": "건물 CCTV 위치와 사각지대를 잘 알고 있다.",
        "danger": "매우 높음",
    }
}


# =========================================================
# DIRECT QUESTION ENGINE
# =========================================================

def answer_question(question):

    q = question.strip().lower()

    if not q:
        return (
            "불명",
            "질문을 입력해주세요.",
            None,
            0
        )

    # -----------------------------------------
    # 이상한 질문
    # -----------------------------------------

    nonsense = [
        "문어",
        "고양이",
        "강아지",
        "공룡",
        "외계인",
        "로봇",
        "대통령",
        "축구",
        "게임",
        "라면",
        "치킨",
        "날씨",
        "내 이름",
        "몇살"
    ]

    for word in nonsense:
        if word in q:
            return (
                "아니오",
                "아니오. 그 질문은 현재 사건과 관련이 없습니다.",
                None,
                0
            )

    # -----------------------------------------
    # 현관 / 침입
    # -----------------------------------------

    if any(x in q for x in [
        "현관",
        "현관문",
        "문을",
        "문에",
        "침입",
        "들어온",
        "들어왔",
        "강제로"
    ]):

        if any(x in q for x in [
            "흔적",
            "침입",
            "강제로",
            "부서"
        ]):

            return (
                "아니오",
                "아니오. 현관문에는 강제로 침입한 흔적이 없습니다.",
                "현관 강제 침입 흔적 없음",
                5
            )

        return (
            "예",
            "예. 피해자는 사건 당시 현관문 근처에 있었습니다.",
            "현관 주변에 피해자의 흔적 발견",
            3
        )

    # -----------------------------------------
    # 창문
    # -----------------------------------------

    if any(x in q for x in [
        "창문",
        "베란다",
        "창으로",
        "창을"
    ]):

        return (
            "아니오",
            "아니오. 창문은 내부에서 잠겨 있었고 외부 침입 흔적도 없습니다.",
            "창문 침입 가능성 낮음",
            5
        )

    # -----------------------------------------
    # CCTV
    # -----------------------------------------

    if any(x in q for x in [
        "cctv",
        "씨씨티비",
        "카메라",
        "영상",
        "녹화"
    ]):

        return (
            "예",
            "예. 23시 41분부터 약 17초 동안 CCTV에 이상한 공백이 있습니다.",
            "CCTV에 17초 공백 발생",
            10
        )

    # -----------------------------------------
    # 피해자
    # -----------------------------------------

    if any(x in q for x in [
        "피해자",
        "피해자가"
    ]):

        if any(x in q for x in [
            "혼자",
            "혼자였",
            "혼자 있었"
        ]):

            return (
                "아니오",
                "아니오. 사건 직전 피해자는 누군가와 연락하고 있었습니다.",
                "피해자는 사건 직전 누군가와 연락함",
                7
            )

        if any(x in q for x in [
            "죽",
            "사망",
            "살해"
        ]):

            return (
                "예",
                "예. 피해자는 현장에서 사망한 상태로 발견됐습니다.",
                "피해자는 현장에서 사망",
                3
            )

    # -----------------------------------------
    # 휴대전화
    # -----------------------------------------

    if any(x in q for x in [
        "휴대폰",
        "휴대전화",
        "핸드폰",
        "전화",
        "통화"
    ]):

        if any(x in q for x in [
            "삭제",
            "지워",
            "조작",
            "없어"
        ]):

            return (
                "예",
                "예. 마지막 통화 기록 하나가 삭제되어 있습니다.",
                "마지막 통화 기록 삭제",
                10
            )

        if any(x in q for x in [
            "박서연",
            "서연"
        ]):

            return (
                "예",
                "예. 박서연은 사건 직전 피해자에게 세 차례 전화했습니다.",
                "박서연의 사건 직전 연락",
                7
            )

        return (
            "예",
            "예. 피해자의 휴대전화는 현장에서 발견됐습니다.",
            "피해자의 휴대전화 발견",
            3
        )

    # -----------------------------------------
    # 김민재
    # -----------------------------------------

    if "김민재" in q or "민재" in q:

        if any(x in q for x in [
            "싸움",
            "다툼",
            "갈등",
            "동기",
            "싫어",
            "원한"
        ]):

            return (
                "예",
                "예. 김민재는 사건 당일 피해자와 승진 문제로 크게 다퉜습니다.",
                "김민재에게 범행 동기 존재",
                8
            )

        if any(x in q for x in [
            "cctv",
            "현장",
            "알리바이"
        ]):

            return (
                "아니오",
                "아니오. 현재까지 김민재가 현장에 있었다는 직접적인 증거는 없습니다.",
                "김민재의 현장 증거 부족",
                6
            )

        return (
            "예",
            "예. 김민재는 피해자의 직장 동료입니다.",
            "김민재는 피해자의 직장 동료",
            2
        )

    # -----------------------------------------
    # 박서연
    # -----------------------------------------

    if "박서연" in q or "서연" in q:

        if any(x in q for x in [
            "전화",
            "통화",
            "연락"
        ]):

            return (
                "예",
                "예. 사건 직전 박서연이 피해자에게 세 차례 전화했습니다.",
                "박서연이 사건 직전 세 차례 연락",
                8
            )

        if any(x in q for x in [
            "현장",
            "cctv",
            "알리바이"
        ]):

            return (
                "아니오",
                "아니오. 박서연이 사건 현장에 있었다는 직접 증거는 발견되지 않았습니다.",
                "박서연의 현장 증거 부족",
                5
            )

        return (
            "예",
            "예. 박서연은 피해자의 전 여자친구입니다.",
            "박서연은 피해자의 전 여자친구",
            2
        )

    # -----------------------------------------
    # 최도윤
    # -----------------------------------------

    if "최도윤" in q or "도윤" in q or "관리인" in q or "이웃" in q:

        if any(x in q for x in [
            "cctv",
            "카메라",
            "사각",
            "위치"
        ]):

            return (
                "예",
                "예. 최도윤은 건물 CCTV 위치와 사각지대를 알고 있었습니다.",
                "최도윤은 CCTV 사각지대를 알고 있었다",
                12
            )

        if any(x in q for x in [
            "알리바이",
            "집",
            "외출",
            "나갔"
        ]):

            return (
                "아니오",
                "아니오. 최도윤은 계속 집에 있었다고 주장했지만 통신 기록과 맞지 않습니다.",
                "최도윤의 알리바이에 모순",
                15
            )

        if any(x in q for x in [
            "범인",
            "죽",
            "살해",
            "의심"
        ]):

            return (
                "예",
                "예. 현재 확보된 단서 중 가장 강하게 의심되는 인물입니다.",
                "최도윤이 가장 유력한 용의자",
                10
            )

        return (
            "예",
            "예. 최도윤은 피해자의 이웃이며 건물 내부 사정을 잘 알고 있습니다.",
            "최도윤은 피해자의 이웃",
            3
        )

    # -----------------------------------------
    # 지문
    # -----------------------------------------

    if any(x in q for x in [
        "지문",
        "손자국",
        "손 흔적"
    ]):

        return (
            "예",
            "예. 피해자의 것과 다른 지문이 하나 발견됐습니다.",
            "제3자의 지문 발견",
            10
        )

    # -----------------------------------------
    # 혈흔 / 상처
    # -----------------------------------------

    if any(x in q for x in [
        "피",
        "혈흔",
        "상처",
        "흉기"
    ]):

        return (
            "예",
            "예. 현장에는 사망과 관련된 미세한 혈흔이 발견됐습니다.",
            "현장에서 혈흔 발견",
            6
        )

    # -----------------------------------------
    # 금품
    # -----------------------------------------

    if any(x in q for x in [
        "돈",
        "금품",
        "지갑",
        "도난",
        "훔쳐",
        "훔친"
    ]):

        return (
            "아니오",
            "아니오. 지갑과 귀중품은 그대로 남아 있습니다.",
            "금품은 사라지지 않았다",
            5
        )

    # -----------------------------------------
    # 범인 / 살인
    # -----------------------------------------

    if any(x in q for x in [
        "범인",
        "살인",
        "살해",
        "죽였",
        "죽인"
    ]):

        return (
            "예",
            "예. 현재까지의 증거를 보면 타인의 개입 가능성이 매우 높습니다.",
            "타인의 개입 가능성 높음",
            8
        )

    # -----------------------------------------
    # 알리바이
    # -----------------------------------------

    if "알리바이" in q:

        return (
            "아니오",
            "아니오. 모든 용의자의 알리바이가 완벽하게 일치하지는 않습니다.",
            "용의자 알리바이에 모순 존재",
            8
        )

    # -----------------------------------------
    # 시간
    # -----------------------------------------

    if any(x in q for x in [
        "몇 시",
        "언제",
        "시간",
        "몇시"
    ]):

        return (
            "예",
            "예. 사건의 핵심 시간대는 23시 40분 전후입니다.",
            "핵심 사건 시간대 23:40 전후",
            5
        )

    # -----------------------------------------
    # 문 / 잠금
    # -----------------------------------------

    if any(x in q for x in [
        "잠겨",
        "잠금",
        "도어락",
        "열쇠",
        "비밀번호"
    ]):

        return (
            "예",
            "예. 현관문은 발견 당시 잠겨 있었습니다.",
            "현관문 잠김",
            5
        )

    # -----------------------------------------
    # 힌트 요청
    # -----------------------------------------

    if any(x in q for x in [
        "힌트",
        "도와",
        "모르겠",
        "어떻게",
        "뭘 물어"
    ]):

        return (
            "힌트",
            "CCTV, 휴대전화 기록, 그리고 최도윤의 알리바이를 연결해서 생각해보세요.",
            "핵심 추리 방향: CCTV + 휴대전화 + 최도윤",
            0
        )

    # -----------------------------------------
    # 모르는 질문
    # -----------------------------------------

    return (
        "불명",
        "그 질문에 대한 확실한 정보는 아직 없습니다. 현관, CCTV, 휴대전화, 용의자의 알리바이를 조사해보세요.",
        None,
        0
    )


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div style="color:#45d5ff;font-size:11px;letter-spacing:4px;font-weight:800;">CONFIDENTIAL INVESTIGATION</div>',
    unsafe_allow_html=True
)

st.title("🔎 예스노 탐정")

st.caption("CASE 001 · 잠긴 방의 진실 · 당신의 질문으로 진실을 찾아라")


# =========================================================
# STATUS
# =========================================================

a,b,c,d = st.columns(4)

a.metric(
    "질문",
    f"{st.session_state.questions}/15"
)

b.metric(
    "수사 점수",
    st.session_state.score
)

c.metric(
    "확보 단서",
    len(st.session_state.clues)
)

d.metric(
    "힌트 사용",
    f"{st.session_state.hint_used}/3"
)

st.divider()


# =========================================================
# MAIN
# =========================================================

left, right = st.columns([1.35, 1])


# =========================================================
# LEFT
# =========================================================

with left:

    st.subheader("📁 사건 파일")

    st.markdown("""
    <div class="case-photo">
        <div class="photo-info">
        CASE #001 · 서울 · 23:58
        </div>

        <div class="photo-title">
        잠긴 방의 진실
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">

    <b>사건 개요</b>

    <br><br>

    새벽 1시 18분.

    피해자는 자신의 방 안에서 쓰러진 채 발견됐다.

    <br><br>

    현관문은 잠겨 있었다.

    창문도 안쪽에서 잠겨 있었다.

    외부 침입 흔적은 없었다.

    <br><br>

    하지만 피해자의 휴대전화에서는
    <b>마지막 통화 기록 하나가 삭제</b>되어 있었다.

    <br><br>

    복도 CCTV에는
    <b>17초의 이상한 공백</b>이 존재한다.

    <br><br>

    당신은 예/아니오 질문을 통해
    사건의 진실을 밝혀야 한다.

    </div>
    """, unsafe_allow_html=True)

    st.write("")

    st.subheader("🧩 확보한 단서")

    if not st.session_state.clues:

        st.info("아직 단서가 없습니다.")

    else:

        for clue in st.session_state.clues:

            st.markdown(
                f'<div class="clue">◆ {clue}</div>',
                unsafe_allow_html=True
            )


# =========================================================
# RIGHT
# =========================================================

with right:

    st.subheader("🕵️ 직접 질문하기")

    st.write(
        "궁금한 것을 **직접 문장으로 입력하세요.**"
    )

    question = st.text_input(
        "질문",
        placeholder="예: 현관에 들어온 흔적은 있습니까?",
        key="player_question"
    )

    if st.button(
        "🔎 질문하기",
        use_container_width=True
    ):

        if st.session_state.questions >= 15:

            st.warning("질문을 모두 사용했습니다.")

        elif not question.strip():

            st.warning("질문을 먼저 입력하세요.")

        else:

            answer, detail, clue, points = answer_question(question)

            st.session_state.questions += 1
            st.session_state.score += points

            if clue and clue not in st.session_state.clues:

                st.session_state.clues.append(clue)

            st.session_state.last_answer = (
                answer,
                detail
            )

            st.session_state.history.insert(
                0,
                (question, answer, detail)
            )

            st.rerun()


    # =====================================================
    # ANSWER
    # =====================================================

    if st.session_state.last_answer:

        answer, detail = st.session_state.last_answer

        if answer == "예":

            st.markdown(
                f"""
                <div class="answer">
                <div class="yes">YES · 예</div>
                <div style="margin-top:6px;">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif answer == "아니오":

            st.markdown(
                f"""
                <div class="answer">
                <div class="no">NO · 아니오</div>
                <div style="margin-top:6px;">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        elif answer == "힌트":

            st.markdown(
                f"""
                <div class="hint">
                <b>💡 힌트</b>
                <br><br>
                {detail}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:

            st.markdown(
                f"""
                <div class="answer">
                <div class="unknown">?</div>
                <div style="margin-top:6px;">{detail}</div>
                </div>
                """,
                unsafe_allow_html=True
            )


    # =====================================================
    # HINT BUTTON
    # =====================================================

    st.write("")

    st.subheader("💡 탐정 보조")

    if st.button(
        "💡 힌트 받기",
        use_container_width=True
    ):

        if st.session_state.hint_used >= 3:

            st.warning("힌트는 최대 3개까지 사용할 수 있습니다.")

        else:

            st.session_state.hint_used += 1

            hints = [
                "현관에 강제 침입 흔적이 없다는 것은 범인이 피해자에게 문을 열게 했다는 뜻일 수 있습니다.",
                "CCTV의 17초 공백과 피해자의 삭제된 통화 기록을 연결해보세요.",
                "최도윤은 CCTV 사각지대를 알고 있었고, 그의 알리바이에는 통신 기록과 맞지 않는 부분이 있습니다."
            ]

            st.session_state.last_answer = (
                "힌트",
                hints[st.session_state.hint_used - 1]
            )

            st.rerun()


# =========================================================
# SUSPECTS
# =========================================================

st.divider()

st.subheader("👤 용의자")

s1, s2, s3 = st.columns(3)

for col, (name, data) in zip(
    [s1, s2, s3],
    suspects.items()
):

    with col:

        st.markdown(
            f"""
            <div class="suspect">

            <b>{name}</b>

            <br>

            <span style="color:#70b8d5;">
            {data["role"]}
            </span>

            <br><br>

            {data["info"]}

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# HISTORY
# =========================================================

if st.session_state.history:

    with st.expander("📋 내가 한 질문 기록 보기"):

        for q, answer, detail in st.session_state.history:

            st.write(f"**Q. {q}**")
            st.write(f"**{answer}** — {detail}")
            st.divider()


# =========================================================
# FINAL ACCUSATION
# =========================================================

st.divider()

st.subheader("🚨 최종 범인 지목")

st.write(
    "충분히 조사했다면 범인을 직접 선택하세요."
)

suspect_choice = st.radio(
    "범인은 누구입니까?",
    [
        "김민재",
        "박서연",
        "최도윤"
    ],
    horizontal=True
)

if st.button(
    "🚨 최종 범인으로 지목하기",
    use_container_width=True
):

    if suspect_choice == "최도윤":

        st.session_state.ending = "WIN"

    elif suspect_choice == "김민재":

        st.session_state.ending = "PARTIAL"

    else:

        st.session_state.ending = "LOSE"

    st.rerun()


# =========================================================
# ENDING
# =========================================================

if st.session_state.ending:

    st.divider()

    if st.session_state.ending == "WIN":

        st.markdown("""
        <div class="ending">

        <h1>🎉 TRUE ENDING</h1>

        <h2>사건 해결</h2>

        <p>
        당신이 지목한 <b>최도윤</b>이 진짜 범인이었다.
        </p>

        <p>
        그는 피해자의 이웃이었고,
        건물의 CCTV 구조를 누구보다 잘 알고 있었다.
        </p>

        <p>
        그는 CCTV 사각지대를 이용해 이동했고,
        사건 이후 피해자의 휴대전화에서
        마지막 통화 기록을 삭제했다.
        </p>

        <p>
        하지만 17초의 CCTV 공백,
        삭제된 통화 기록,
        그리고 그의 알리바이 모순이
        모든 거짓말을 무너뜨렸다.
        </p>

        <h2 style="color:#42d5ff;">
        🔎 CASE CLOSED
        </h2>

        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.ending == "PARTIAL":

        st.markdown("""
        <div class="ending">

        <h1>⚠️ PARTIAL ENDING</h1>

        <p>
        김민재에게는 범행 동기가 있었다.
        </p>

        <p>
        하지만 현장 증거가 부족하다.
        </p>

        <p>
        당신은 동기만 보고 너무 빨리 결론을 내렸다.
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="ending">

        <h1>❌ BAD ENDING</h1>

        <p>
        잘못된 사람을 범인으로 지목했다.
        </p>

        <p>
        진짜 범인은 아직 잡히지 않았다.
        </p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# RESET
# =========================================================

if st.session_state.ending:

    if st.button("🔄 다시 수사하기", use_container_width=True):

        for key in defaults:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()
