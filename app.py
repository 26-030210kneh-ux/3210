import os
import hashlib
from datetime import datetime

import requests
import streamlit as st


# =========================================================
# 기본 설정
# =========================================================

st.set_page_config(
    page_title="GHOST COMMIT",
    page_icon="👻",
    layout="wide"
)


# =========================================================
# 화면 디자인
# =========================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'JetBrains Mono', monospace;
}

.stApp {
    background:
        radial-gradient(circle at 80% 10%, rgba(0,255,140,.07), transparent 28%),
        #030806;
    color: #d9ffe9;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
}

.hero {
    border: 1px solid #1d6040;
    border-radius: 16px;
    padding: 30px;
    background: linear-gradient(
        135deg,
        rgba(10,35,22,.96),
        rgba(3,12,8,.98)
    );
}

.hero .tag {
    color: #54ff9b;
    font-size: 13px;
    font-weight: bold;
}

.hero h1 {
    font-size: 46px;
    margin: 8px 0;
}

.hero p {
    color: #91ad9c;
}

.tutorial {
    border: 1px solid #286c48;
    border-radius: 14px;
    padding: 22px;
    background: rgba(7,28,17,.8);
    margin: 20px 0;
}

.step {
    padding: 10px 0;
    border-bottom: 1px solid rgba(100,255,170,.1);
}

.step:last-child {
    border-bottom: none;
}

.evidence {
    border: 1px solid #17452f;
    border-radius: 12px;
    padding: 18px;
    background: rgba(5,18,11,.7);
    margin-bottom: 12px;
}

.alert {
    border-left: 4px solid #ff4747;
    padding: 15px 18px;
    background: rgba(80,10,10,.2);
    border-radius: 8px;
}

.success {
    border-left: 4px solid #45ff9b;
    padding: 15px 18px;
    background: rgba(10,80,45,.18);
    border-radius: 8px;
}

.hint {
    border-left: 4px solid #4db8ff;
    padding: 15px 18px;
    background: rgba(20,70,100,.15);
    border-radius: 8px;
}

.small {
    color: #799083;
    font-size: 12px;
}

div[data-testid="stSidebar"] {
    background: #07100b;
    border-right: 1px solid #123522;
}

.stButton button {
    border: 1px solid #1d6040;
    background: #08170e;
    color: #baffd5;
}

.stButton button:hover {
    border-color: #49ff9b;
    color: white;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# 게임 상태
# =========================================================

if "tutorial_done" not in st.session_state:
    st.session_state.tutorial_done = False

if "opened" not in st.session_state:
    st.session_state.opened = []

if "actions" not in st.session_state:
    st.session_state.actions = []

if "repo_data" not in st.session_state:
    st.session_state.repo_data = None

if "ending" not in st.session_state:
    st.session_state.ending = None


# =========================================================
# 함수
# =========================================================

def log_action(action):
    st.session_state.actions.append(
        f"{datetime.now().strftime('%H:%M:%S')} // {action}"
    )


def open_evidence(name):
    if name not in st.session_state.opened:
        st.session_state.opened.append(name)
        log_action(f"증거 확인: {name}")


def progress():
    return len(st.session_state.opened)


# =========================================================
# 사건 증거
# =========================================================

evidence = {

    "기록 // README // 복구 경고": """
README 마지막 문장

"기록이 파일과 모순된다면 둘 다 믿지 마라.
규칙을 바꾼 커밋을 찾아라."

분석:

누군가 단순히 파일을 삭제한 것이 아니다.

프로젝트의 '복구 규칙' 자체가 바뀌었다.
""",

    "통제 // Issue #13 // 백업 경고": """
ISSUE #13

제목:
백업은 백업이 아니다.

내용:

"한 사람이 백업을 통제한다면
그것은 백업이 아니라
단일 실패 지점이다."

작성자:
NOAH

상태:
CLOSED

이슈가 닫힌 시점은
복구 경로가 사라진 시점과 매우 가깝다.
""",

    "동기 // cleanup.diff // 소유권": """
CLEANUP DIFF

삭제된 것:

- recovery/restore.py
- recovery/manifest.json

변경된 것:

owner = "team"

↓

owner = "maintainer"

결론:

복구 기능이 사라졌을 뿐만 아니라
소유권의 규칙도 바뀌었다.
""",

    "생존 // branch: still-here": """
BRANCH: still-here

숨겨진 브랜치에서 발견된 문장:

"I didn't delete the project.
I made sure nobody could restore it."

번역:

"나는 프로젝트를 지우지 않았다.
아무도 복구할 수 없도록 만들었다."

작성자의 이름은 남아 있지 않다.
"""
}


# =========================================================
# 용의자
# =========================================================

suspects = {
    "MIRA": "메인테이너 — 저장소의 최종 관리자",
    "NOAH": "아카이비스트 — 백업과 기록 담당",
    "YOU": "조사관 — 사건을 조사하는 사람"
}


# =========================================================
# 사이드바
# =========================================================

with st.sidebar:

    st.markdown("## 🔐 조사 터미널")

    st.caption("GHOST COMMIT // 사건번호 GC-013")

    st.divider()

    st.markdown("### 🎯 현재 진행도")

    st.write(
        f"증거 조사: **{len(st.session_state.opened)}/4**"
    )

    st.write(
        f"행동 기록: **{len(st.session_state.actions)}**"
    )

    st.divider()

    st.markdown("### 🕹️ 게임 순서")

    st.write("① 튜토리얼 읽기")
    st.write("② 증거 4개 조사")
    st.write("③ 용의자 추리")
    st.write("④ 결말 확인")

    st.divider()

    st.markdown("### 🔗 GitHub")

    repo = st.text_input(
        "저장소 주소",
        placeholder="username/ghost-commit"
    )

    if st.button(
        "⟳ GitHub 동기화",
        use_container_width=True
    ):

        if "/" not in repo:

            st.error(
                "예: username/ghost-commit"
            )

        else:

            try:

                owner, name = repo.strip().split("/", 1)

                headers = {}

                token = os.getenv("GITHUB_TOKEN")

                if token:
                    headers["Authorization"] = (
                        f"Bearer {token}"
                    )

                commits = requests.get(
                    f"https://api.github.com/repos/{owner}/{name}/commits",
                    headers=headers,
                    timeout=8
                ).json()

                branches = requests.get(
                    f"https://api.github.com/repos/{owner}/{name}/branches",
                    headers=headers,
                    timeout=8
                ).json()

                issues = requests.get(
                    f"https://api.github.com/repos/{owner}/{name}/issues?state=all",
                    headers=headers,
                    timeout=8
                ).json()

                st.session_state.repo_data = {
                    "repo": repo,
                    "commits": commits
                    if isinstance(commits, list)
                    else [],
                    "branches": branches
                    if isinstance(branches, list)
                    else [],
                    "issues": issues
                    if isinstance(issues, list)
                    else []
                }

                log_action(
                    f"GitHub 동기화: {repo}"
                )

                st.success("동기화 성공!")

            except Exception as e:

                st.error(
                    f"GitHub 연결 실패: {e}"
                )


# =========================================================
# 메인 제목
# =========================================================

st.markdown("""
<div class="hero">

<div class="tag">
CASE FILE // GC-013 // CLASSIFIED
</div>

<h1>👻 GHOST COMMIT</h1>

<p>
저장소는 모든 것을 기억한다.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# 첫 방문 튜토리얼
# =========================================================

if not st.session_state.tutorial_done:

    st.markdown("""
    <div class="tutorial">

    <h2>🎮 게임 방법</h2>

    <p>
    걱정하지 마세요. 어렵지 않습니다.
    아래 순서대로 하면 됩니다.
    </p>

    <div class="step">
    <b>STEP 1 — 📁 증거</b><br>
    아래의 증거 4개를 하나씩 열어보세요.
    </div>

    <div class="step">
    <b>STEP 2 — 🔍 단서 찾기</b><br>
    누가 복구 경로를 없앴는지,
    누가 저장소를 통제했는지 생각해보세요.
    </div>

    <div class="step">
    <b>STEP 3 — 🧩 추리</b><br>
    가장 의심되는 인물을 선택하세요.
    </div>

    <div class="step">
    <b>STEP 4 — ☠️ 결말</b><br>
    추리를 확정하고 결과를 확인하세요.
    </div>

    <div class="step">
    <b>💡 초보자 팁</b><br>
    GitHub를 연결하지 않아도
    기본 사건은 플레이할 수 있습니다.
    </div>

    </div>
    """, unsafe_allow_html=True)

    if st.button(
        "🚨 사건 조사 시작",
        use_container_width=True
    ):

        st.session_state.tutorial_done = True

        log_action("튜토리얼 종료")

        st.rerun()


# =========================================================
# 탭
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📁 증거 조사",
    "⌘ GitHub",
    "🧩 추리",
    "☠️ 결말"
])


# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.header("📁 증거 보관함")

    st.write(
        f"현재 **{progress()}/4개**의 증거를 확인했습니다."
    )

    if progress() < 4:

        st.markdown("""
        <div class="hint">
        💡 <b>힌트</b><br>
        아래 증거를 전부 열어보세요.
        모든 증거를 봐야 사건의 전체 그림이 보입니다.
        </div>
        """, unsafe_allow_html=True)

    st.write("")

    for title, content in evidence.items():

        with st.expander(
            "› " + title
        ):

            open_evidence(title)

            st.code(
                content,
                language="text"
            )

    st.divider()

    st.subheader("👤 용의자")

    cols = st.columns(3)

    for col, (name, role) in zip(
        cols,
        suspects.items()
    ):

        with col:

            st.markdown(
                f"""
                <div class="evidence">

                <h3>{name}</h3>

                <span class="small">
                {role}
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )

    if progress() == 4:

        st.success(
            "✅ 모든 증거를 확인했습니다! "
            "이제 「🧩 추리」 탭으로 이동하세요."
        )


# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.header("⌘ GitHub 포렌식")

    st.markdown("""
    <div class="hint">

    <b>이 메뉴는 선택사항입니다.</b><br><br>

    처음 플레이하는 경우 그냥 넘어가도 됩니다.<br>
    실제 GitHub 저장소를 연결하면
    추가 정보를 조사할 수 있습니다.

    </div>
    """, unsafe_allow_html=True)

    data = st.session_state.repo_data

    if not data:

        st.info(
            "아직 GitHub 저장소를 연결하지 않았습니다."
        )

    else:

        st.subheader(
            f"🔎 {data['repo']}"
        )

        commits = data["commits"]
        branches = data["branches"]
        issues = data["issues"]

        ghost_branch = any(
            b.get("name") == "still-here"
            for b in branches
        )

        issue_13 = any(
            i.get("number") == 13
            for i in issues
        )

        c1, c2, c3 = st.columns(3)

        c1.metric(
            "커밋",
            len(commits)
        )

        c2.metric(
            "still-here",
            "발견" if ghost_branch else "없음"
        )

        c3.metric(
            "Issue #13",
            "발견" if issue_13 else "없음"
        )

        st.divider()

        st.subheader(
            "최근 커밋"
        )

        for commit in commits[:10]:

            message = (
                commit
                .get("commit", {})
                .get("message", "")
                .split("\n")[0]
            )

            sha = commit.get(
                "sha",
                ""
            )[:7]

            st.write(
                f"`{sha}` — {message}"
            )


# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.header("🧩 추리 보드")

    if progress() < 4:

        st.markdown("""
        <div class="alert">

        ⚠️ 아직 증거를 전부 확인하지 않았습니다.

        <br><br>

        먼저 <b>「📁 증거 조사」</b>에서
        4개의 증거를 모두 확인하세요.

        </div>
        """, unsafe_allow_html=True)

    else:

        st.success(
            "증거 조사 완료! 이제 범인을 추리하세요."
        )

        st.markdown("""
        <div class="hint">

        <b>🧠 핵심 질문</b><br><br>

        단순히 누가 파일을 삭제했는지를 찾는 것이 아닙니다.<br><br>

        <b>
        누가 이 사건이 정상적인 작업처럼 보이도록 만들었을까요?
        </b>

        </div>
        """, unsafe_allow_html=True)

        st.write("")

        suspect = st.radio(
            "① 가장 의심되는 인물은?",
            list(suspects.keys()),
            horizontal=True
        )

        st.write("")

        reason = st.radio(
            "② 가장 중요한 단서는?",
            [
                "미라가 복구 경로를 없애 저장소를 장악했다.",
                "노아가 백업을 숨기고 기록을 조작했다.",
                "누군가 조사관의 행동을 이용해 은폐를 정당화했다."
            ]
        )

        st.write("")

        if st.button(
            "🔎 추리 확정",
            use_container_width=True
        ):

            st.session_state.ending = (
                suspect,
                reason
            )

            log_action(
                f"최종 추리: {suspect}"
            )

            st.success(
                "추리가 기록되었습니다!"
            )

            st.info(
                "이제 「☠️ 결말」 탭으로 이동하세요."
            )


# =========================================================
# TAB 4
# =========================================================

with tab4:

    st.header("☠️ 최종 결말")

    if not st.session_state.ending:

        st.markdown("""
        <div class="hint">

        아직 결말이 나오지 않았습니다.

        <br><br>

        <b>📁 증거 조사 → 🧩 추리 → ☠️ 결말</b>

        순서대로 진행해주세요.

        </div>
        """, unsafe_allow_html=True)

    else:

        suspect, reason = (
            st.session_state.ending
        )

        # TRUE ENDING
        if (
            suspect == "YOU"
            and
            "조사관의 행동" in reason
        ):

            st.markdown("""
            <div class="hero">

            <div class="tag">
            TRUE ENDING // GHOST COMMIT
            </div>

            <h1>
            👻 진실을 밝혀냈다
            </h1>

            <p>
            저장소는 거짓말하지 않았다.
            </p>

            <p>
            거짓말을 한 것은
            저장소 주변의 이야기였다.
            </p>

            </div>
            """, unsafe_allow_html=True)

            st.success("""
            누군가는 조사관의 행동을
            증거의 일부로 만들었습니다.

            그리고 마지막 흔적은
            당신에게 연결되어 있습니다.
            """)

        # PARTIAL ENDING
        elif suspect == "MIRA":

            st.markdown("""
            <div class="alert">

            <h2>
            ⚠️ PARTIAL ENDING
            </h2>

            <p>
            미라가 복구 경로를 제거하고
            저장소를 장악한 것처럼 보입니다.
            </p>

            <p>
            하지만 아직 설명되지 않는
            흔적이 남아 있습니다.
            </p>

            </div>
            """, unsafe_allow_html=True)

        # BAD ENDING
        else:

            st.markdown("""
            <div class="alert">

            <h2>
            ☠️ BAD ENDING
            </h2>

            <p>
            당신은 저장소가 보여준
            첫 번째 이야기를 믿었습니다.
            </p>

            <p>
            그리고 누군가는
            그 틈을 이용했습니다.
            </p>

            </div>
            """, unsafe_allow_html=True)

        # 감사 로그
        st.divider()

        st.subheader(
            "🧾 조사 기록"
        )

        if st.session_state.actions:

            for action in st.session_state.actions:

                st.code(
                    action,
                    language="text"
                )

        fingerprint = hashlib.sha256(
            "|".join(
                st.session_state.actions
            ).encode()
        ).hexdigest()[:12].upper()

        st.write(
            f"**SESSION FINGERPRINT:** `{fingerprint}`"
        )


# =========================================================
# 하단
# =========================================================

st.divider()

st.caption(
    "GHOST COMMIT // 한국어 에디션 // "
    "저장소는 모든 것을 기억한다."
)
