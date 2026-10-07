import streamlit as st
import re
import random
from datetime import datetime


# ============================================================
# 🕵️ YES NO DETECTIVE
# 최종 확장판
# ============================================================

st.set_page_config(
    page_title="예스노탐정",
    page_icon="🕵️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 🎨 디자인
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Noto Sans KR', sans-serif;
}

.stApp {
    background:
        radial-gradient(
            circle at 10% 0%,
            rgba(60,120,190,.13),
            transparent 30%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(190,70,60,.08),
            transparent 28%
        ),
        #080b10;
    color: #edf2f7;
}

.block-container {
    max-width: 1250px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

.title-wrap {
    text-align: center;
    padding: 20px 0 28px;
}

.title-wrap h1 {
    font-size: 54px;
    font-weight: 900;
    margin: 0;
    letter-spacing: -3px;
}

.title-wrap .subtitle {
    color: #8d98a6;
    margin-top: 8px;
    font-size: 17px;
}

.case-card {
    background:
        linear-gradient(
            145deg,
            rgba(25,31,40,.98),
            rgba(10,14,20,.98)
        );
    border: 1px solid #303945;
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 20px;
    box-shadow:
        0 15px 45px rgba(0,0,0,.28);
}

.case-id {
    color: #68b7ff;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
}

.case-title {
    font-size: 34px;
    font-weight: 900;
    margin-top: 7px;
    margin-bottom: 20px;
}

.story {
    white-space: pre-line;
    line-height: 2;
    font-size: 17px;
    color: #d7dee7;
}

.story strong {
    color: white;
}

.panel {
    background: #10151c;
    border: 1px solid #27303b;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 16px;
}

.question-panel {
    background:
        linear-gradient(
            145deg,
            rgba(18,27,38,.95),
            rgba(11,16,23,.98)
        );
    border: 1px solid #354557;
    border-radius: 18px;
    padding: 25px;
}

.answer-yes {
    background: rgba(35,150,90,.12);
    border: 1px solid #2d8c5b;
    border-left: 5px solid #43d27f;
    border-radius: 12px;
    padding: 17px;
    margin: 9px 0;
}

.answer-no {
    background: rgba(190,60,60,.10);
    border: 1px solid #914343;
    border-left: 5px solid #e45a5a;
    border-radius: 12px;
    padding: 17px;
    margin: 9px 0;
}

.answer-unknown {
    background: rgba(190,150,50,.09);
    border: 1px solid #806c35;
    border-left: 5px solid #d7b64c;
    border-radius: 12px;
    padding: 17px;
    margin: 9px 0;
}

.clue {
    background: #10161e;
    border: 1px solid #263443;
    border-left: 4px solid #55a9ef;
    border-radius: 10px;
    padding: 15px 18px;
    margin: 9px 0;
}

.suspect {
    background: #10151c;
    border: 1px solid #2c3743;
    border-radius: 14px;
    padding: 18px;
    height: 100%;
}

.suspect-name {
    font-size: 20px;
    font-weight: 800;
}

.suspect-role {
    color: #6eb7ee;
    font-size: 13px;
    margin-top: 4px;
}

.timeline-item {
    border-left: 3px solid #3d7cab;
    padding: 4px 0 16px 20px;
    margin-left: 7px;
}

.timeline-time {
    color: #6fbaff;
    font-weight: 800;
    font-size: 13px;
}

.timeline-text {
    color: #c8d0d9;
    margin-top: 3px;
}

.badge {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    background: #17212d;
    border: 1px solid #334455;
    color: #b8c7d6;
    font-size: 12px;
    margin-right: 5px;
}

.success-box {
    background:
        linear-gradient(
            145deg,
            rgba(25,95,58,.28),
            rgba(10,30,20,.7)
        );
    border: 1px solid #3f9563;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}

.fail-box {
    background:
        linear-gradient(
            145deg,
            rgba(100,30,30,.25),
            rgba(30,10,10,.7)
        );
    border: 1px solid #954b4b;
    border-radius: 18px;
    padding: 30px;
    text-align: center;
}

.hint-box {
    background: rgba(70,110,160,.10);
    border: 1px solid #426586;
    border-left: 5px solid #64b7ff;
    border-radius: 12px;
    padding: 17px;
}

.warning-box {
    background: rgba(160,120,40,.09);
    border: 1px solid #806b32;
    border-left: 5px solid #d5b34c;
    border-radius: 12px;
    padding: 17px;
}

.stat-number {
    font-size: 32px;
    font-weight: 900;
    text-align: center;
}

.rank {
    text-align: center;
    font-size: 46px;
    font-weight: 900;
    margin: 10px 0;
}

.footer {
    text-align: center;
    color: #58626d;
    padding: 25px;
    font-size: 12px;
}

div[data-testid="stSidebar"] {
    background: #0b0f15;
    border-right: 1px solid #232c36;
}

.stButton button {
    border-radius: 10px;
    min-height: 44px;
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 🧠 사건 데이터
# ============================================================

CASES = [

    {
        "id": 1,
        "title": "사라진 시계",
        "difficulty": "⭐",
        "category": "밀실 / 시간",
        "questions": 20,

        "story": """
한 남자가 자신의 방에서 죽은 채 발견되었다.

방문은 안에서 잠겨 있었고,
창문도 모두 닫혀 있었다.

방 안에는 쓰러진 의자와 깨진 시계가 있었다.

경찰은 처음에는 자살이라고 생각했다.

하지만 현장을 조사한 형사는
불과 몇 분 만에 고개를 저었다.

"이건 자살이 아닙니다."

형사는 시계를 가리켰다.

왜일까?
""",

        "suspects": [
            {
                "name": "민준",
                "role": "피해자의 동생",
                "info": "사건 당시 집 근처에 있었다고 주장한다."
            },
            {
                "name": "서연",
                "role": "피해자의 동료",
                "info": "피해자와 사건 당일 통화했다."
            },
            {
                "name": "도현",
                "role": "이웃",
                "info": "사건 당시 큰 소리를 들었다고 말했다."
            }
        ],

        "timeline": [
            ("21:10", "피해자가 마지막으로 친구와 통화함"),
            ("21:30", "이웃이 둔탁한 소리를 들음"),
            ("21:40", "피해자의 동생이 집 근처에 도착"),
            ("22:05", "경찰이 현장 도착"),
            ("22:12", "형사가 깨진 시계를 발견")
        ],

        "rules": {
            "시계": "YES",
            "시간": "YES",
            "시간대": "YES",
            "사망시간": "YES",
            "사망시각": "YES",
            "죽은시간": "YES",
            "알리바이": "YES",
            "자살": "NO",
            "가족": "NO",
            "동생": "NO",
            "창문": "NO",
            "문": "NO",
            "총": "NO",
            "독": "NO",
            "살인": "YES",
            "범인": "UNKNOWN"
        },

        "clues": [
            "깨진 시계가 사건의 핵심 단서다.",
            "피해자의 실제 사망 시각은 처음 알려진 시간과 다르다.",
            "누군가 사건 발생 시간을 조작하려 했다.",
            "잠긴 방 자체보다 시간 조작이 더 중요하다."
        ],

        "keywords": [
            "시계",
            "시간",
            "사망시간",
            "사망시각",
            "시간조작",
            "사망",
            "알리바이"
        ],

        "solution": """
범인은 시계를 일부러 깨뜨려
사망 시간을 다른 시간으로 보이게 만들었다.

즉, 범인은 자신이 현장에 있었던 시간대를
숨기기 위해 사건의 시간을 조작한 것이다.

잠긴 방은 사람들의 시선을 다른 곳으로 돌리기 위한 장치였다.

이 사건의 핵심은 '누가 방에 들어갔는가'가 아니라
'왜 시계가 깨져 있었는가'였다.
"""
    },


    {
        "id": 2,
        "title": "잠긴 방",
        "difficulty": "⭐⭐",
        "category": "밀실 / 열쇠",
        "questions": 20,

        "story": """
한 여성이 자신의 집에서 쓰러진 채 발견되었다.

현관문은 잠겨 있었다.
창문도 모두 닫혀 있었다.

집 안에는 피해자 외에는 아무도 없었다.

경찰은 처음에 완벽한 밀실이라고 생각했다.

그런데 형사는 현관문을 확인하더니 말했다.

"범인은 밖에서 들어왔습니다."

어떻게 가능했을까?
""",

        "suspects": [
            {
                "name": "지훈",
                "role": "피해자의 남편",
                "info": "집 열쇠를 가지고 있었다."
            },
            {
                "name": "하은",
                "role": "청소업체 직원",
                "info": "과거 피해자의 집 열쇠를 사용했다."
            },
            {
                "name": "성호",
                "role": "이웃",
                "info": "피해자와 거의 교류하지 않았다."
            }
        ],

        "timeline": [
            ("08:00", "피해자가 출근 준비를 시작함"),
            ("09:10", "청소업체 직원이 건물에서 나감"),
            ("10:30", "피해자의 남편이 출근"),
            ("12:20", "이웃이 이상한 소리를 들음"),
            ("12:45", "경찰이 현장 도착")
        ],

        "rules": {
            "열쇠": "YES",
            "복제": "YES",
            "복제열쇠": "YES",
            "열쇠복제": "YES",
            "외부": "YES",
            "밖": "YES",
            "밀실": "NO",
            "창문": "NO",
            "가족": "NO",
            "남편": "UNKNOWN",
            "독": "NO",
            "총": "NO",
            "자살": "NO"
        },

        "clues": [
            "문이 잠겨 있다고 해서 범인이 안에서 나간 것은 아니다.",
            "범인은 정상적인 열쇠를 이용했을 가능성이 높다.",
            "과거 집에 출입했던 사람을 조사해야 한다.",
            "열쇠의 복제 여부가 핵심이다."
        ],

        "keywords": [
            "열쇠",
            "복제",
            "복제열쇠",
            "외부",
            "침입",
            "출입"
        ],

        "solution": """
범인은 피해자의 열쇠를 미리 복제했다.

범행 후 문을 정상적으로 잠그고 떠났기 때문에
현장에는 강제 침입 흔적이 남지 않았다.

따라서 잠긴 문은 범인이 없었다는 증거가 아니라
오히려 정상적인 열쇠를 사용했다는 증거였다.
"""
    },


    {
        "id": 3,
        "title": "멈춘 CCTV",
        "difficulty": "⭐⭐⭐",
        "category": "CCTV / 내부자",
        "questions": 20,

        "story": """
은행에서 현금 3억 원이 사라졌다.

경찰은 CCTV를 확인했다.

그런데 범행이 일어난 정확히 10분 동안만
모든 CCTV 영상이 멈춰 있었다.

범행 전과 후의 영상은 정상적으로 존재했다.

경찰은 외부 침입보다는
은행 내부자의 소행일 가능성이 높다고 판단했다.

왜 그랬을까?
""",

        "suspects": [
            {
                "name": "현우",
                "role": "은행 경비원",
                "info": "CCTV 모니터를 담당한다."
            },
            {
                "name": "유진",
                "role": "창구 직원",
                "info": "금고 위치를 알고 있다."
            },
            {
                "name": "태식",
                "role": "고객",
                "info": "사건 당시 은행을 방문했다."
            }
        ],

        "timeline": [
            ("14:02", "현우가 CCTV 시스템을 점검"),
            ("14:17", "은행에 고객들이 들어옴"),
            ("14:31", "CCTV 녹화 중단"),
            ("14:41", "CCTV 녹화 재개"),
            ("15:00", "현금 부족이 발견됨")
        ],

        "rules": {
            "cctv": "YES",
            "카메라": "YES",
            "내부자": "YES",
            "직원": "YES",
            "경비": "YES",
            "전원": "YES",
            "전기": "YES",
            "녹화": "YES",
            "금고": "YES",
            "손님": "NO",
            "우연": "NO",
            "외부인": "NO"
        },

        "clues": [
            "CCTV는 우연히 고장난 것이 아니다.",
            "누군가는 정확히 10분 동안 녹화를 멈출 수 있었다.",
            "범행 시간과 CCTV 중단 시간이 완전히 일치한다.",
            "은행 내부 시스템에 접근할 수 있는 사람을 조사해야 한다."
        ],

        "keywords": [
            "cctv",
            "카메라",
            "내부자",
            "직원",
            "경비",
            "녹화",
            "전원",
            "금고"
        ],

        "solution": """
범인은 은행 내부 시스템을 알고 있는 사람이었다.

CCTV를 정확한 시간에 중단하고
다시 작동시킬 수 있는 접근 권한이 필요했기 때문이다.

따라서 단순한 외부 강도보다
내부자의 가능성이 훨씬 높았다.
"""
    },


    {
        "id": 4,
        "title": "범인이 건 전화",
        "difficulty": "⭐⭐⭐",
        "category": "전화 / 녹음",
        "questions": 20,

        "story": """
새벽 2시,
경찰서에 전화가 걸려왔다.

전화한 사람은 말했다.

"사람을 죽였습니다."

경찰이 주소를 묻자
전화는 바로 끊겼다.

경찰이 추적한 결과
전화는 피해자의 집에서 걸려온 것이었다.

그런데 경찰이 도착했을 때
피해자는 아직 살아 있었다.

전화한 사람은 누구였을까?
""",

        "suspects": [
            {
                "name": "피해자",
                "role": "사건의 중심 인물",
                "info": "경찰 도착 당시 살아 있었다."
            },
            {
                "name": "범인",
                "role": "불명",
                "info": "아직 신원이 밝혀지지 않았다."
            },
            {
                "name": "이웃",
                "role": "목격자",
                "info": "새벽에 이상한 소리를 들었다."
            }
        ],

        "timeline": [
            ("01:40", "피해자가 집에 있음"),
            ("01:55", "피해자가 무언가를 준비함"),
            ("02:00", "경찰서에 전화가 걸림"),
            ("02:07", "경찰이 전화 위치를 추적"),
            ("02:15", "경찰이 현장 도착")
        ],

        "rules": {
            "전화": "YES",
            "녹음": "YES",
            "녹음된": "YES",
            "자동": "YES",
            "예약": "YES",
            "피해자": "YES",
            "범인": "NO",
            "경찰": "NO",
            "미래": "NO",
            "가족": "NO",
            "직접": "NO"
        },

        "clues": [
            "전화한 사람이 그 순간 직접 말했을 필요는 없다.",
            "미리 녹음된 음성을 사용할 수 있다.",
            "전화는 자동으로 걸리도록 설정할 수 있다.",
            "피해자가 자신의 목소리를 이용했을 가능성이 있다."
        ],

        "keywords": [
            "전화",
            "녹음",
            "자동",
            "예약",
            "피해자",
            "음성"
        ],

        "solution": """
피해자가 미리 자신의 목소리를 녹음해 두었다.

그리고 특정 시간이 되면
자동으로 경찰에게 전화하도록 설정했다.

피해자는 자신에게 위험이 생길 것을 예상하고
미리 신고 장치를 준비했던 것이다.
"""
    },


    {
        "id": 5,
        "title": "탐정이 범인",
        "difficulty": "⭐⭐⭐⭐",
        "category": "추리 / 정보",
        "questions": 20,

        "story": """
한 남자가 살해되었다.

경찰은 현장을 조사했지만
범인을 찾지 못했다.

현장에 있던 탐정이 말했다.

"범인은 분명히 피해자의 오른손에
반지를 끼워 놓았을 겁니다."

경찰은 그 말을 듣자마자
탐정을 체포했다.

왜일까?
""",

        "suspects": [
            {
                "name": "탐정",
                "role": "사건 담당자",
                "info": "경찰보다 먼저 현장에 도착했다."
            },
            {
                "name": "동료",
                "role": "피해자의 친구",
                "info": "피해자와 최근 갈등이 있었다."
            },
            {
                "name": "가족",
                "role": "피해자의 가족",
                "info": "현장에 도착했을 때 시신을 처음 봤다."
            }
        ],

        "timeline": [
            ("08:10", "경찰에 신고 접수"),
            ("08:18", "탐정이 현장 도착"),
            ("08:25", "경찰관들이 현장 도착"),
            ("08:30", "현장 보존 시작"),
            ("08:35", "탐정이 반지 이야기를 함")
        ],

        "rules": {
            "오른손": "YES",
            "반지": "YES",
            "손": "YES",
            "현장": "YES",
            "시체": "YES",
            "정보": "YES",
            "알고": "YES",
            "보지": "YES",
            "범인": "YES",
            "탐정": "YES",
            "경찰": "NO"
        },

        "clues": [
            "탐정은 공개되지 않은 정보를 알고 있었다.",
            "피해자의 손에 대한 정보는 아직 공개되지 않았다.",
            "그 정보를 정확히 알고 있을 수 있는 사람은 매우 제한적이다.",
            "탐정은 현장에 경찰보다 먼저 도착했다."
        ],

        "keywords": [
            "오른손",
            "반지",
            "정보",
            "탐정",
            "현장",
            "시체",
            "알고"
        ],

        "solution": """
탐정이 범인이었다.

경찰에게 아직 공개되지 않은
피해자의 오른손과 반지에 대한 정보를
탐정이 알고 있었기 때문이다.

탐정은 자신이 범행 현장에 있었기 때문에
그 정보를 알고 있었던 것이다.
"""
    },


    {
        "id": 6,
        "title": "눈이 오지 않았는데 발자국",
        "difficulty": "⭐⭐⭐⭐",
        "category": "발자국 / 함정",
        "questions": 20,

        "story": """
겨울 밤,
한 별장에서 살인 사건이 발생했다.

눈이 많이 내린 날이었다.

별장 주변에는 발자국이 하나뿐이었다.

그 발자국은 별장 안에서
현관까지 이어져 있었다.

밖으로 나간 발자국은 없었다.

경찰은 범인이 아직 집 안에 있다고 생각했다.

하지만 형사는 발자국을 보더니
범인은 이미 도망갔다고 말했다.

왜일까?
""",

        "suspects": [
            {
                "name": "준호",
                "role": "별장 주인",
                "info": "사건 당시 집 안에 있었다고 주장한다."
            },
            {
                "name": "수아",
                "role": "친구",
                "info": "사건 직전에 별장을 방문했다."
            },
            {
                "name": "민석",
                "role": "택배기사",
                "info": "사건 당일 물건을 배달했다."
            }
        ],

        "timeline": [
            ("18:00", "폭설 시작"),
            ("19:20", "피해자가 별장에 도착"),
            ("20:10", "택배 배달"),
            ("21:00", "사건 발생 추정"),
            ("22:00", "경찰 도착")
        ],

        "rules": {
            "발자국": "YES",
            "눈": "YES",
            "실내": "YES",
            "현관": "YES",
            "나간": "YES",
            "밖": "YES",
            "신발": "YES",
            "거꾸로": "YES",
            "뒤로": "YES",
            "범인": "YES",
            "택배": "NO",
            "창문": "NO"
        },

        "clues": [
            "발자국의 방향을 자세히 확인해야 한다.",
            "발자국은 들어온 흔적처럼 보이지만 실제 방향이 반대일 수 있다.",
            "신발 자국의 앞뒤가 중요한 단서다.",
            "범인은 발자국을 이용해 경찰을 속였다."
        ],

        "keywords": [
            "발자국",
            "눈",
            "신발",
            "거꾸로",
            "뒤로",
            "방향"
        ],

        "solution": """
범인은 신발을 거꾸로 신고 걸었다.

실제로는 별장에서 밖으로 나갔지만
발자국의 모양은 안으로 들어온 것처럼 보였다.

경찰이 발자국의 방향을 그대로 믿도록 만든
간단하지만 효과적인 함정이었다.
"""
    },


    {
        "id": 7,
        "title": "사라진 유언장",
        "difficulty": "⭐⭐⭐⭐",
        "category": "상속 / 문서",
        "questions": 20,

        "story": """
한 부자가 갑자기 사망했다.

가족들은 오래된 유언장을 찾았다.

유언장에는 대부분의 재산을
장남에게 준다고 적혀 있었다.

그런데 이상한 점이 있었다.

유언장에 적힌 날짜가
부자가 병원에 입원하기 전이었다.

가족들은 모두 장남을 의심했다.

하지만 진짜 문제는
유언장의 내용이 아니었다.

무엇이 문제였을까?
""",

        "suspects": [
            {
                "name": "장남",
                "role": "상속 후보",
                "info": "유언장의 최대 수혜자다."
            },
            {
                "name": "변호사",
                "role": "법률 담당",
                "info": "유언장 작성에 관여했다."
            },
            {
                "name": "막내",
                "role": "상속 후보",
                "info": "유언장에 거의 아무것도 받지 못했다."
            }
        ],

        "timeline": [
            ("3월 2일", "부자가 유언장을 작성했다고 알려짐"),
            ("3월 5일", "부자가 병원 입원"),
            ("3월 8일", "가족들이 유언장을 확인"),
            ("3월 9일", "유언장 원본이 사라짐"),
            ("3월 10일", "경찰 수사 시작")
        ],

        "rules": {
            "날짜": "YES",
            "시간": "YES",
            "문서": "YES",
            "원본": "YES",
            "서명": "YES",
            "유언장": "YES",
            "장남": "UNKNOWN",
            "변호사": "UNKNOWN",
            "병원": "YES",
            "돈": "NO",
            "살인": "NO",
            "위조": "YES",
            "조작": "YES"
        },

        "clues": [
            "유언장의 날짜가 중요하다.",
            "문서의 원본과 사본을 비교해야 한다.",
            "서명 자체보다 작성 시점이 의심스럽다.",
            "유언장은 위조되었을 가능성이 있다."
        ],

        "keywords": [
            "날짜",
            "유언장",
            "문서",
            "원본",
            "서명",
            "위조",
            "조작"
        ],

        "solution": """
문제는 유언장의 내용이 아니라
작성 날짜와 원본의 진위였다.

누군가 기존 문서를 바꾸거나
새로운 유언장을 만들어
상속 결과를 바꾸려고 했다.

따라서 가족 중 한 명을 바로 범인으로 지목하기보다
문서의 작성 과정부터 조사해야 했다.
"""
    },


    {
        "id": 8,
        "title": "죽은 사람이 보낸 문자",
        "difficulty": "⭐⭐⭐⭐",
        "category": "문자 / 자동화",
        "questions": 20,

        "story": """
한 남자가 밤 11시에 사망했다.

그런데 다음 날 아침,
친구들에게 문자 메시지가 도착했다.

"나 괜찮아. 걱정하지 마."

메시지를 받은 친구들은
피해자가 살아 있다고 생각했다.

하지만 경찰은 이 문자가
살인 사건의 중요한 단서라고 말했다.

왜일까?
""",

        "suspects": [
            {
                "name": "피해자",
                "role": "사망자",
                "info": "밤 11시경 사망한 것으로 추정된다."
            },
            {
                "name": "친구",
                "role": "문자 수신자",
                "info": "아침에 메시지를 받았다."
            },
            {
                "name": "동료",
                "role": "직장 동료",
                "info": "피해자의 휴대폰을 알고 있었다."
            }
        ],

        "timeline": [
            ("22:30", "피해자가 마지막으로 온라인 상태"),
            ("23:00", "피해자 사망 추정"),
            ("23:10", "휴대폰에서 예약 메시지 설정"),
            ("07:00", "문자 메시지 발송"),
            ("08:30", "친구가 경찰에 신고")
        ],

        "rules": {
            "문자": "YES",
            "예약": "YES",
            "자동": "YES",
            "휴대폰": "YES",
            "사망": "YES",
            "죽은": "YES",
            "미리": "YES",
            "녹음": "NO",
            "친구": "NO",
            "살아": "NO",
            "인터넷": "YES"
        },

        "clues": [
            "문자는 사람이 직접 보낸 것이 아닐 수 있다.",
            "예약 메시지 기능을 조사해야 한다.",
            "문자 발송 시간이 사망 시간보다 훨씬 늦다.",
            "피해자가 미리 메시지를 예약했을 가능성이 있다."
        ],

        "keywords": [
            "문자",
            "예약",
            "자동",
            "휴대폰",
            "미리",
            "사망"
        ],

        "solution": """
피해자는 사망하기 전에
예약 문자 기능을 이용해 메시지를 설정했다.

따라서 다음 날 도착한 문자는
피해자가 살아 있었다는 증거가 아니었다.

오히려 피해자가 자신의 죽음을
예상하고 있었을 가능성을 보여주는 단서였다.
"""
    },


    {
        "id": 9,
        "title": "없는 방",
        "difficulty": "⭐⭐⭐⭐⭐",
        "category": "건축 / 착각",
        "questions": 20,

        "story": """
한 호텔에서 사건이 발생했다.

목격자는 범인이
호텔 307호에서 나오는 것을 봤다고 말했다.

경찰이 307호를 확인했지만
그 방은 존재하지 않았다.

호텔의 방 번호는
305 다음이 306,
그 다음이 308이었다.

목격자는 거짓말을 한 것일까?

형사는 오히려
목격자의 말이 정확하다고 판단했다.
""",

        "suspects": [
            {
                "name": "목격자",
                "role": "호텔 투숙객",
                "info": "복도에서 범인을 봤다고 주장한다."
            },
            {
                "name": "관리인",
                "role": "호텔 직원",
                "info": "호텔 구조를 잘 알고 있다."
            },
            {
                "name": "범인",
                "role": "불명",
                "info": "307호에서 나왔다고 알려졌다."
            }
        ],

        "timeline": [
            ("20:00", "목격자가 호텔 체크인"),
            ("21:10", "복도에서 이상한 소리를 들음"),
            ("21:12", "307호에서 사람이 나오는 것을 봄"),
            ("21:20", "경찰 도착"),
            ("21:30", "307호가 존재하지 않는다는 사실 확인")
        ],

        "rules": {
            "307": "YES",
            "방": "YES",
            "호텔": "YES",
            "구조": "YES",
            "번호": "YES",
            "복도": "YES",
            "거울": "YES",
            "반사": "YES",
            "착각": "YES",
            "비밀": "YES",
            "지하": "NO",
            "옥상": "NO"
        },

        "clues": [
            "호텔의 방 번호가 일반적인 순서와 다르다.",
            "목격자는 '307호'라는 숫자를 실제 방 번호라고 말한 것이 아닐 수 있다.",
            "거울이나 반사에 의해 숫자가 뒤집혀 보였을 가능성이 있다.",
            "목격자의 말 자체가 완전히 거짓은 아니다."
        ],

        "keywords": [
            "307",
            "방",
            "호텔",
            "번호",
            "거울",
            "반사",
            "착각",
            "구조"
        ],

        "solution": """
목격자는 실제로 존재하지 않는 307호를 본 것이 아니다.

복도 반대편의 표지판이
거울에 반사되어 숫자가 다르게 보였던 것이다.

목격자가 본 장소는 실제로 다른 방이었지만
그가 본 '307'이라는 숫자는
거울에 비친 숫자였다.

따라서 목격자의 말은 거짓말이 아니었다.
"""
    },


    {
        "id": 10,
        "title": "마지막 사건",
        "difficulty": "⭐⭐⭐⭐⭐",
        "category": "메타 / 탐정",
        "questions": 20,

        "story": """
당신은 마지막 사건을 맡았다.

사건 파일에는 이상한 문장이 적혀 있다.

"이 사건을 해결하는 사람은
다음 사건의 범인이 된다."

피해자는 발견되지 않았다.

흉기도 없다.

용의자도 없다.

오직 책상 위에
탐정의 이름이 적힌 메모 한 장만 있다.

그리고 그 이름은...

당신의 이름이었다.

사건을 조사할수록
새로운 기록이 나타난다.

이 사건의 범인은 누구일까?
""",

        "suspects": [
            {
                "name": "당신",
                "role": "탐정",
                "info": "현재 사건을 조사하고 있다."
            },
            {
                "name": "기록자",
                "role": "정체불명",
                "info": "사건 파일을 작성한 사람."
            },
            {
                "name": "미지의 인물",
                "role": "정체불명",
                "info": "어떤 기록에도 등장하지 않는다."
            }
        ],

        "timeline": [
            ("00:00", "사건 파일 생성"),
            ("00:05", "탐정의 이름이 기록됨"),
            ("00:10", "첫 번째 단서 발견"),
            ("00:20", "새로운 기록 생성"),
            ("현재", "탐정이 사건을 조사 중")
        ],

        "rules": {
            "탐정": "YES",
            "당신": "YES",
            "이름": "YES",
            "기록": "YES",
            "파일": "YES",
            "기록자": "YES",
            "메모": "YES",
            "범인": "UNKNOWN",
            "피해자": "UNKNOWN",
            "미래": "YES",
            "다음": "YES",
            "게임": "YES",
            "플레이어": "YES"
        },

        "clues": [
            "사건 파일은 탐정이 조사할 때마다 새로운 기록을 만든다.",
            "탐정의 행동 자체가 사건의 일부가 된다.",
            "처음부터 탐정의 이름이 사건 파일에 존재했다.",
            "범인은 특정 인물이 아니라 사건을 만들어낸 구조일 가능성이 있다.",
            "당신이 사건을 조사하는 행동 자체가 마지막 단서다."
        ],

        "keywords": [
            "탐정",
            "당신",
            "기록",
            "파일",
            "이름",
            "플레이어",
            "조사",
            "행동",
            "게임"
        ],

        "solution": """
이 사건의 핵심은 '범인이 누구인가'가 아니었다.

당신이 사건을 조사할 때마다
사건 파일에는 새로운 기록이 추가되었다.

즉, 탐정은 단순히 사건을 조사한 것이 아니라
사건의 기록을 직접 만들어내고 있었다.

마지막 사건의 범인은 특정 사람이 아니라
'사건을 완성시키는 탐정의 행동' 그 자체였다.

그리고 마지막 기록에는 이렇게 적혀 있다.

"당신이 이 문장을 읽었다면
사건은 이미 완성되었다."
"""
    }
]


# ============================================================
# 🏅 업적
# ============================================================

ACHIEVEMENTS = {
    "first_case": {
        "name": "첫 사건",
        "description": "첫 사건을 해결했습니다."
    },
    "three_cases": {
        "name": "견습 탐정",
        "description": "3개의 사건을 해결했습니다."
    },
    "five_cases": {
        "name": "명탐정",
        "description": "5개의 사건을 해결했습니다."
    },
    "all_cases": {
        "name": "전설의 탐정",
        "description": "모든 사건을 해결했습니다."
    },
    "no_hint": {
        "name": "독심술사",
        "description": "힌트를 한 번도 사용하지 않고 사건을 해결했습니다."
    },
    "fast_solver": {
        "name": "번개 추리",
        "description": "10번 이하의 질문으로 사건을 해결했습니다."
    }
}


# ============================================================
# 🧠 세션 상태 초기화
# ============================================================

DEFAULTS = {
    "started": False,
    "case_index": 0,
    "questions_left": 20,
    "question_history": [],
    "clues": [],
    "case_finished": False,
    "case_won": False,
    "score": 0,
    "total_score": 0,
    "hint_used": 0,
    "completed_cases": [],
    "achievements": [],
    "final_answer": "",
    "game_complete": False,
    "last_answer": None,
    "session_started": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "streak": 0
}

for key, value in DEFAULTS.items():

    if key not in st.session_state:
        st.session_state[key] = value


case = CASES[st.session_state.case_index]


# ============================================================
# 🔧 함수
# ============================================================

def normalize(text):

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        "",
        text
    )

    text = re.sub(
        r"[.,!?~'\"(){}\[\]<>:;]",
        "",
        text
    )

    return text


def get_answer(question):

    q = normalize(question)

    # 정확한 키워드 우선
    for keyword, answer in case["rules"].items():

        if normalize(keyword) in q:

            return answer

    return "UNKNOWN"


def add_clue():

    index = len(
        st.session_state.clues
    )

    if index < len(case["clues"]):

        clue = case["clues"][index]

        if clue not in st.session_state.clues:

            st.session_state.clues.append(clue)


def reset_case():

    st.session_state.questions_left = case["questions"]

    st.session_state.question_history = []

    st.session_state.clues = []

    st.session_state.case_finished = False

    st.session_state.case_won = False

    st.session_state.hint_used = 0

    st.session_state.final_answer = ""

    st.session_state.last_answer = None


def unlock_achievement(key):

    if key not in st.session_state.achievements:

        st.session_state.achievements.append(key)


def calculate_rank(score):

    if score >= 900:
        return "S"

    if score >= 700:
        return "A"

    if score >= 500:
        return "B"

    if score >= 300:
        return "C"

    return "D"


def next_case():

    if st.session_state.case_index < len(CASES) - 1:

        st.session_state.case_index += 1

        reset_case()

    else:

        st.session_state.game_complete = True


def check_achievements():

    completed = len(
        st.session_state.completed_cases
    )

    if completed >= 1:
        unlock_achievement("first_case")

    if completed >= 3:
        unlock_achievement("three_cases")

    if completed >= 5:
        unlock_achievement("five_cases")

    if completed >= len(CASES):
        unlock_achievement("all_cases")

    if (
        st.session_state.case_won
        and st.session_state.hint_used == 0
    ):
        unlock_achievement("no_hint")

    if (
        st.session_state.case_won
        and len(st.session_state.question_history) <= 10
    ):
        unlock_achievement("fast_solver")


# ============================================================
# 🎮 전체 종료 화면
# ============================================================

if st.session_state.game_complete:

    st.markdown("""
    <div class="success-box">

    <div style="font-size:60px;">🏆</div>

    <h1>모든 사건 해결</h1>

    <h2>당신은 전설의 탐정입니다.</h2>

    <p>
    모든 사건의 진실을 밝혀냈습니다.
    </p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="rank">
        {calculate_rank(st.session_state.total_score)} 등급
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="stat-number">
        {st.session_state.total_score}점
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "해결 사건",
            f"{len(st.session_state.completed_cases)} / {len(CASES)}"
        )

    with col2:
        st.metric(
            "획득 업적",
            len(st.session_state.achievements)
        )

    with col3:
        st.metric(
            "최종 연속 해결",
            st.session_state.streak
        )

    st.divider()

    st.subheader("🏅 획득한 업적")

    for key in st.session_state.achievements:

        achievement = ACHIEVEMENTS[key]

        st.markdown(
            f"""
            <div class="clue">
            🏅 <b>{achievement['name']}</b><br>
            <span class="small">
            {achievement['description']}
            </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    if st.button(
        "🔄 처음부터 다시 플레이",
        use_container_width=True
    ):

        for key in DEFAULTS:

            if key in st.session_state:
                del st.session_state[key]

        st.rerun()

    st.stop()


# ============================================================
# 🕵️ 헤더
# ============================================================

st.markdown("""
<div class="title-wrap">

<h1>🕵️ 예스노탐정</h1>

<div class="subtitle">
질문으로 진실을 밝혀라.
</div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# 🚪 시작 화면
# ============================================================

if not st.session_state.started:

    st.markdown("""
    <div class="case-card">

    <div class="case-id">
    DETECTIVE ACADEMY // CASE SYSTEM
    </div>

    <div class="case-title">
    당신은 오늘부터 탐정입니다.
    </div>

    <div class="story">

    사건에는 항상 진실이 존재합니다.

    하지만 처음부터 모든 것을 알 수는 없습니다.

    당신에게 주어진 무기는 단 하나.

    <strong>질문.</strong>

    사건에 대해 무엇이든 물어보세요.

    단,
    답변은 YES,
    NO,
    또는 알 수 없음.

    질문을 통해 단서를 모으고,
    마지막에는 당신의 언어로 사건을 설명해야 합니다.

    총 10개의 사건이 기다리고 있습니다.

    쉬운 사건부터 시작해서
    점점 더 복잡한 사건으로 넘어갑니다.

    진짜 탐정이라면
    단순히 답을 맞히는 것이 아니라

    <strong>
    왜 그런 일이 일어났는지 설명해야 합니다.
    </strong>

    </div>

    </div>
    """, unsafe_allow_html=True)

    st.subheader("🎮 게임 규칙")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown("### 🔎")
        st.write("질문하기")
        st.caption("사건에 대해 자유롭게 질문하세요.")

    with c2:
        st.markdown("### 🧠")
        st.write("추리하기")
        st.caption("YES와 NO를 연결하세요.")

    with c3:
        st.markdown("### 📓")
        st.write("단서 모으기")
        st.caption("탐정 수첩에 단서가 기록됩니다.")

    with c4:
        st.markdown("### 🏆")
        st.write("해결하기")
        st.caption("마지막에 직접 사건을 설명하세요.")

    st.divider()

    st.subheader("📚 사건 목록")

    for item in CASES:

        st.markdown(
            f"""
            <div class="panel">

            <span class="badge">
            CASE {item['id']:02d}
            </span>

            <span class="badge">
            {item['difficulty']}
            </span>

            <span class="badge">
            {item['category']}
            </span>

            <h3>{item['title']}</h3>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.divider()

    if st.button(
        "🚨 첫 번째 사건 시작",
        use_container_width=True
    ):

        st.session_state.started = True

        st.rerun()

    st.stop()


# ============================================================
# 📌 사이드바
# ============================================================

with st.sidebar:

    st.markdown("## 🕵️ 탐정 수첩")

    st.divider()

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

    st.metric(
        "총 점수",
        st.session_state.total_score
    )

    st.divider()

    st.markdown("### 📊 조사 상태")

    st.progress(
        min(
            len(st.session_state.question_history)
            / case["questions"],
            1.0
        )
    )

    st.caption(
        f"질문 {len(st.session_state.question_history)} / {case['questions']}"
    )

    st.divider()

    st.markdown("### 💡 힌트")

    if st.session_state.hint_used < 3:

        if st.button(
            f"힌트 사용 ({st.session_state.hint_used}/3)",
            use_container_width=True
        ):

            st.session_state.hint_used += 1

            clue_index = min(
                st.session_state.hint_used - 1,
                len(case["clues"]) - 1
            )

            clue = case["clues"][clue_index]

            if clue not in st.session_state.clues:

                st.session_state.clues.append(clue)

            # 힌트 사용시 점수 차감
            st.session_state.score = max(
                0,
                st.session_state.score - 10
            )

            st.rerun()

    else:

        st.caption(
            "이번 사건의 힌트를 모두 사용했습니다."
        )

    st.divider()

    st.markdown("### 🏅 업적")

    st.write(
        f"{len(st.session_state.achievements)} / {len(ACHIEVEMENTS)}"
    )

    for key in st.session_state.achievements:

        st.write(
            f"🏅 {ACHIEVEMENTS[key]['name']}"
        )


# ============================================================
# 📁 사건 카드
# ============================================================

st.markdown(
    f"""
    <div class="case-card">

    <div class="case-id">
    CASE #{case['id']:03d}
    &nbsp; // &nbsp;
    {case['category']}
    </div>

    <div class="case-title">
    {case['title']}
    </div>

    <div>
    <span class="badge">
    난이도 {case['difficulty']}
    </span>

    <span class="badge">
    질문 {case['questions']}회
    </span>
    </div>

    <br>

    <div class="story">
    {case['story']}
    </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 📊 현재 사건 정보
# ============================================================

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.metric(
        "남은 질문",
        st.session_state.questions_left
    )

with c2:

    st.metric(
        "발견한 단서",
        len(st.session_state.clues)
    )

with c3:

    st.metric(
        "질문 점수",
        st.session_state.score
    )

with c4:

    st.metric(
        "힌트 사용",
        f"{st.session_state.hint_used}/3"
    )


# ============================================================
# 👤 용의자
# ============================================================

with st.expander("👤 용의자 / 관련 인물 보기"):

    cols = st.columns(
        len(case["suspects"])
    )

    for col, suspect in zip(
        cols,
        case["suspects"]
    ):

        with col:

            st.markdown(
                f"""
                <div class="suspect">

                <div class="suspect-name">
                {suspect['name']}
                </div>

                <div class="suspect-role">
                {suspect['role']}
                </div>

                <br>

                <div>
                {suspect['info']}
                </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# 🕰️ 타임라인
# ============================================================

with st.expander("🕰️ 사건 타임라인 보기"):

    for time, text in case["timeline"]:

        st.markdown(
            f"""
            <div class="timeline-item">

            <div class="timeline-time">
            {time}
            </div>

            <div class="timeline-text">
            {text}
            </div>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 🔎 질문
# ============================================================

st.divider()

st.subheader("🔎 질문하기")

st.markdown("""
<div class="question-panel">

<b>탐정의 질문</b>

<br><br>

사건에 대해 궁금한 것을 자유롭게 질문하세요.

<br><br>

예를 들어:

<br>

• 범인은 가족입니까?<br>
• 시계가 중요한 단서입니까?<br>
• 피해자는 혼자였습니까?<br>
• 범인은 사건 현장에 있었습니까?<br>
• CCTV가 사건과 관련 있습니까?<br>

<br>

<b>좋은 질문일수록 사건의 진실에 가까워집니다.</b>

</div>
""", unsafe_allow_html=True)

st.write("")

question = st.text_input(
    "질문",
    placeholder="예: 범인은 가족입니까?",
    key="question_input"
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

    st.session_state.last_answer = answer

    if answer == "YES":

        st.session_state.score += 5

        add_clue()

    elif answer == "NO":

        st.session_state.score += 3

    else:

        st.session_state.score += 1

    st.rerun()


# ============================================================
# 💬 최근 답변
# ============================================================

if st.session_state.last_answer:

    answer = st.session_state.last_answer

    if answer == "YES":

        st.success(
            "🟢 YES — 그렇습니다."
        )

    elif answer == "NO":

        st.error(
            "🔴 NO — 아닙니다."
        )

    else:

        st.warning(
            "🟡 알 수 없음 — 그 질문만으로는 판단할 수 없습니다."
        )


# ============================================================
# 📜 질문 기록
# ============================================================

if st.session_state.question_history:

    with st.expander(
        f"💬 질문 기록 ({len(st.session_state.question_history)})",
        expanded=True
    ):

        for index, item in enumerate(
            reversed(
                st.session_state.question_history
            ),
            1
        ):

            answer = item["answer"]

            if answer == "YES":

                st.markdown(
                    f"""
                    <div class="answer-yes">

                    <b>Q.</b> {item['question']}

                    <br><br>

                    <b>🟢 YES</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            elif answer == "NO":

                st.markdown(
                    f"""
                    <div class="answer-no">

                    <b>Q.</b> {item['question']}

                    <br><br>

                    <b>🔴 NO</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.markdown(
                    f"""
                    <div class="answer-unknown">

                    <b>Q.</b> {item['question']}

                    <br><br>

                    <b>🟡 알 수 없음</b>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# 📓 탐정 수첩
# ============================================================

st.divider()

st.subheader("📓 탐정 수첩")

if not st.session_state.clues:

    st.info(
        "아직 특별한 단서가 없습니다. "
        "질문을 통해 단서를 찾아보세요."
    )

else:

    for index, clue in enumerate(
        st.session_state.clues,
        1
    ):

        st.markdown(
            f"""
            <div class="clue">

            🔎 <b>단서 #{index}</b>

            <br>

            {clue}

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# 🧠 최종 추리
# ============================================================

st.divider()

st.subheader("🧠 최종 추리")

st.markdown("""
<div class="hint-box">

<strong>탐정의 마지막 임무</strong>

<br><br>

지금까지 모은 단서를 이용해서
사건의 진실을 직접 설명하세요.

<br><br>

단순히

"범인이 누구다."

라고 쓰는 것보다

<strong>
왜 그런 일이 일어났는지,
어떻게 범행이 가능했는지
</strong>

설명할수록 높은 점수를 받을 수 있습니다.

</div>
""", unsafe_allow_html=True)

st.write("")

final_answer = st.text_area(
    "당신의 최종 추리",
    placeholder=(
        "예:\n"
        "범인은 시계를 조작했습니다.\n"
        "실제 사망 시간과 다른 시간이 보이도록 만들어\n"
        "자신의 알리바이를 만들려고 했습니다."
    ),
    value=st.session_state.final_answer,
    height=180
)

st.session_state.final_answer = final_answer


# ============================================================
# 🚨 최종 제출
# ============================================================

if st.button(
    "🚨 최종 추리 제출",
    use_container_width=True
):

    if len(final_answer.strip()) < 15:

        st.error(
            "조금 더 자세하게 설명해주세요."
        )

    else:

        answer_text = normalize(
            final_answer
        )

        matched_keywords = []

        for keyword in case["keywords"]:

            if normalize(keyword) in answer_text:

                matched_keywords.append(keyword)

        matched = len(
            matched_keywords
        )

        # 질문을 많이 했을수록 조사 보너스
        question_count = len(
            st.session_state.question_history
        )

        investigation_bonus = max(
            0,
            20 - question_count
        )

        # 핵심 단서 보너스
        clue_bonus = len(
            st.session_state.clues
        ) * 5

        # 정답 판정
        if matched >= 3:

            st.session_state.case_won = True

            st.session_state.score += (
                50
                + investigation_bonus
                + clue_bonus
            )

        elif matched >= 2:

            st.session_state.case_won = True

            st.session_state.score += (
                35
                + clue_bonus
            )

        else:

            st.session_state.case_won = False

        st.session_state.case_finished = True

        # 성공 처리
        if st.session_state.case_won:

            if case["id"] not in st.session_state.completed_cases:

                st.session_state.completed_cases.append(
                    case["id"]
                )

            st.session_state.total_score += (
                st.session_state.score
            )

            st.session_state.streak += 1

            check_achievements()

        else:

            st.session_state.streak = 0

        st.rerun()


# ============================================================
# 🏁 사건 결과
# ============================================================

if st.session_state.case_finished:

    st.divider()

    if st.session_state.case_won:

        st.markdown("""
        <div class="success-box">

        <div style="font-size:58px;">
        🟢
        </div>

        <h1>CASE CLOSED</h1>

        <h2>사건 해결 성공!</h2>

        <p>
        당신은 사건의 핵심을 찾아냈습니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="rank">
            +{st.session_state.score}점
            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("📖 사건의 진실")

        st.markdown(
            f"""
            <div class="panel">

            {case['solution']}

            </div>
            """,
            unsafe_allow_html=True
        )

        st.subheader("🔎 당신이 찾은 핵심 단서")

        for clue in case["clues"]:

            st.markdown(
                f"""
                <div class="clue">
                {clue}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.divider()

        if case["id"] < len(CASES):

            if st.button(
                "➡️ 다음 사건으로",
                use_container_width=True
            ):

                next_case()

                st.rerun()

        else:

            if st.button(
                "🏆 최종 결과 보기",
                use_container_width=True
            ):

                st.session_state.game_complete = True

                st.rerun()

    else:

        st.markdown("""
        <div class="fail-box">

        <div style="font-size:58px;">
        🔴
        </div>

        <h1>CASE FAILED</h1>

        <h2>아직 진실에 도달하지 못했습니다.</h2>

        <p>
        하지만 사건의 정답은 공개됩니다.
        </p>

        </div>
        """, unsafe_allow_html=True)

        st.subheader("📖 사건의 진실")

        st.markdown(
            f"""
            <div class="panel">

            {case['solution']}

            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "🔄 이 사건 다시 조사",
            use_container_width=True
        ):

            reset_case()

            st.rerun()


# ============================================================
# 📊 진행률
# ============================================================

st.divider()

st.subheader("📊 전체 탐정 진행률")

completed_count = len(
    st.session_state.completed_cases
)

st.progress(
    completed_count / len(CASES)
)

st.caption(
    f"{completed_count} / {len(CASES)} 사건 해결"
)


# ============================================================
# 🏅 업적
# ============================================================

with st.expander("🏅 탐정 업적"):

    for key, achievement in ACHIEVEMENTS.items():

        unlocked = (
            key in st.session_state.achievements
        )

        if unlocked:

            st.success(
                f"🏅 {achievement['name']} — "
                f"{achievement['description']}"
            )

        else:

            st.caption(
                f"🔒 {achievement['name']} — "
                f"{achievement['description']}"
            )


# ============================================================
# 📜 게임 기록
# ============================================================

with st.expander("📋 현재 세션 기록"):

    st.write(
        f"게임 시작: {st.session_state.session_started}"
    )

    st.write(
        f"현재 사건: CASE #{case['id']:03d}"
    )

    st.write(
        f"해결한 사건: {completed_count}개"
    )

    st.write(
        f"총 점수: {st.session_state.total_score}"
    )

    st.write(
        f"현재 연속 해결: {st.session_state.streak}"
    )


# ============================================================
# 🔄 리셋
# ============================================================

st.divider()

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "🔄 현재 사건 초기화",
        use_container_width=True
    ):

        reset_case()

        st.rerun()

with col2:

    if st.button(
        "🎲 랜덤 사건",
        use_container_width=True
    ):

        st.session_state.case_index = random.randint(
            0,
            len(CASES) - 1
        )

        reset_case()

        st.rerun()


# ============================================================
# 푸터
# ============================================================

st.markdown("""
<div class="footer">

🕵️ 예스노탐정

<br><br>

질문은 많아도 된다.
하지만 진실은 하나다.

<br>

YES / NO DETECTIVE

</div>
""", unsafe_allow_html=True)
