import os
import hashlib
import requests
import streamlit as st

# =========================================================
# GHOST COMMIT
# The repository remembers everything.
# =========================================================

st.set_page_config(
    page_title="GHOST COMMIT",
    page_icon="👻",
    layout="wide",
)

# -----------------------------
# STYLE
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600&family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] {
    font-family: "Space Grotesk", sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at top right, #0b2115 0%, #050807 38%),
        #050807;
    color: #d8f7e3;
}

h1, h2, h3, code, .mono {
    font-family: "IBM Plex Mono", monospace;
}

.hero {
    padding: 35px;
    border: 1px solid #245b39;
    border-radius: 16px;
    background: linear-gradient(135deg, #07120c, #0a1710);
    margin-bottom: 22px;
}

.glitch {
    color: #8dffb2;
    text-shadow:
        2px 0 #174b2b,
        -2px 0 #0c6b35;
}

.card {
    padding: 20px;
    border: 1px solid #1d4931;
    border-radius: 13px;
    background: #08100c;
    margin: 8px 0;
}

.small {
    color: #8fa99a;
    font-size: 0.85rem;
}

.evidence {
    border-left: 3px solid #63ff91;
    padding: 14px 18px;
    background: #07100b;
    margin: 10px 0;
    border-radius: 5px;
}

.warning {
    border-left: 3px solid #ffcc66;
    padding: 14px 18px;
    background: #151107;
    margin: 10px 0;
}

.terminal {
    background: #020503;
    border: 1px solid #21492f;
    padding: 18px;
    border-radius: 10px;
    font-family: "IBM Plex Mono", monospace;
    color: #8dffb2;
}
</style>
""", unsafe_allow_html=True)


# -----------------------------
# SESSION
# -----------------------------
defaults = {
    "repo": "",
    "actions": [],
    "opened": [],
    "ending": None,
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


def record(action):
    if action not in st.session_state.actions:
        st.session_state.actions.append(action)


# -----------------------------
# GITHUB API
# -----------------------------
API = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json"
}

token = os.getenv("GITHUB_TOKEN", "").strip()

if token:
    HEADERS["Authorization"] = f"Bearer {token}"


@st.cache_data(ttl=45, show_spinner=False)
def github_get(endpoint):

    try:
        response = requests.get(
            API + endpoint,
            headers=HEADERS,
            timeout=12
        )

        if response.status_code == 200:
            return response.json()

        return {
            "error": response.status_code,
            "message": response.text[:300]
        }

    except requests.RequestException as error:

        return {
            "error": "NETWORK",
            "message": str(error)
        }


def normalize_repo(value):

    value = value.strip()

    value = value.replace(
        "https://github.com/",
        ""
    )

    value = value.replace(
        "http://github.com/",
        ""
    )

    value = value.strip("/")

    if value.endswith(".git"):
        value = value[:-4]

    if value.count("/") != 1:
        return ""

    return value


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="hero">

<div class="small">
CASE FILE 13 // FORENSIC REPOSITORY INVESTIGATION
</div>

<h1 class="glitch">
👻 GHOST COMMIT
</h1>

<h3>
The repository remembers everything.
</h3>

<p>
A developer vanished.<br>
The project didn't.<br>
Someone rewrote the story.
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("ACCESS TERMINAL")

    repo_input = st.text_input(
        "GitHub repository",
        value=st.session_state.repo,
        placeholder="username/ghost-commit"
    )

    if st.button(
        "⟳ SYNC GITHUB",
        use_container_width=True
    ):

        st.session_state.repo = repo_input.strip()

        github_get.clear()

        record("GITHUB_SYNC")

        st.rerun()

    st.divider()

    st.caption("OBJECTIVE")

    st.write(
        "Recover the truth without trusting "
        "the story around the repository."
    )

    st.divider()

    st.caption("INVESTIGATOR STATUS")

    st.write(
        f"Evidence opened: "
        f"**{len(st.session_state.opened)}**"
    )

    st.write(
        f"Actions recorded: "
        f"**{len(st.session_state.actions)}**"
    )


repo = normalize_repo(repo_input)

if repo:
    st.session_state.repo = repo


# =========================================================
# LIVE DATA
# =========================================================

live = {
    "commits": [],
    "branches": [],
    "issues": [],
    "error": None
}

if repo:

    live["commits"] = github_get(
        f"/repos/{repo}/commits?per_page=50"
    )

    live["branches"] = github_get(
        f"/repos/{repo}/branches?per_page=50"
    )

    live["issues"] = github_get(
        f"/repos/{repo}/issues?state=all&per_page=50"
    )

    for key in [
        "commits",
        "branches",
        "issues"
    ]:

        if isinstance(
            live[key],
            dict
        ) and "error" in live[key]:

            live["error"] = live[key]
            break


# =========================================================
# TABS
# =========================================================

tabs = st.tabs([
    "🗂 EVIDENCE",
    "⌁ GITHUB",
    "🧩 DEDUCTION",
    "☠ ENDING"
])


# =========================================================
# EVIDENCE
# =========================================================

with tabs[0]:

    st.subheader("Evidence Locker")

    evidence = [

        (
            "HISTORY",
            "README / RECOVERY WARNING",
            "If the history contradicts the files, "
            "trust neither. Find the commit that "
            "changed the rules."
        ),

        (
            "CONTROL",
            "ISSUE #13 / BACKUP WARNING",
            "The backup is not a backup if one person "
            "controls it."
        ),

        (
            "MOTIVE",
            "CLEANUP DIFF / OWNERSHIP",
            "Recovery code was removed while ownership "
            "metadata changed."
        ),

        (
            "SURVIVAL",
            "BRANCH: still-here",
            "I didn't delete the project. "
            "I made sure nobody could restore it."
        ),
    ]

    for tag, title, text in evidence:

        with st.expander(
            f"{tag} // {title}"
        ):

            st.markdown(
                f"""
                <div class="evidence">
                {text}
                </div>
                """,
                unsafe_allow_html=True
            )

            record(tag)

            if tag not in st.session_state.opened:
                st.session_state.opened.append(tag)

    st.markdown("### Suspects")

    columns = st.columns(3)

    suspects = [
        ("MIRA", "Maintainer"),
        ("NOAH", "Archivist"),
        ("YOU", "Investigator"),
    ]

    for column, (name, role) in zip(
        columns,
        suspects
    ):

        with column:

            st.markdown(
                f"""
                <div class="card">
                <h3>{name}</h3>
                <span class="small">{role}</span>
                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# GITHUB
# =========================================================

with tabs[1]:

    st.subheader(
        "Live Repository Forensics"
    )

    if not repo:

        st.info(
            "왼쪽에 GitHub 저장소를 입력하고 "
            "SYNC GITHUB를 눌러줘."
        )

        st.markdown("""
        <div class="terminal">
        WAITING FOR REPOSITORY...
        </div>
        """, unsafe_allow_html=True)

    elif live["error"]:

        error = live["error"]

        st.error(
            f"GitHub API error: "
            f"{error.get('message', 'unknown')}"
        )

    else:

        commits = (
            live["commits"]
            if isinstance(
                live["commits"],
                list
            )
            else []
        )

        branches = (
            live["branches"]
            if isinstance(
                live["branches"],
                list
            )
            else []
        )

        issues_raw = (
            live["issues"]
            if isinstance(
                live["issues"],
                list
            )
            else []
        )

        issues = [
            issue
            for issue in issues_raw
            if isinstance(issue, dict)
            and "pull_request" not in issue
        ]

        branch_names = [
            branch.get(
                "name",
                ""
            )
            for branch in branches
        ]

        commit_messages = []

        for commit in commits:

            message = (
                commit
                .get("commit", {})
                .get("message", "")
                .splitlines()[0]
            )

            commit_messages.append(
                message
            )

        has_ghost_branch = any(
            name.lower() == "still-here"
            for name in branch_names
        )

        has_issue_13 = any(
            issue.get("number") == 13
            for issue in issues
        )

        expected = [
            "initial case file",
            "recovery warning",
            "backup warning",
            "remove obsolete recovery path",
            "archive old files",
        ]

        commit_score = sum(
            any(
                expected_text in message.lower()
                for message in commit_messages
            )
            for expected_text in expected
        )

        integrity = (
            commit_score * 12
            + (20 if has_ghost_branch else 0)
            + (20 if has_issue_13 else 0)
        )

        integrity = min(
            integrity,
            100
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "CASE INTEGRITY",
            f"{integrity}%"
        )

        col2.metric(
            "COMMITS",
            len(commits)
        )

        col3.metric(
            "BRANCHES",
            len(branches)
        )

        st.markdown(
            "### Commit Fingerprint"
        )

        if commit_messages:

            for message in commit_messages[:15]:

                st.code(
                    message,
                    language="text"
                )

        else:

            st.warning(
                "커밋을 찾지 못했어."
            )

        st.markdown(
            "### Branches"
        )

        for name in branch_names:

            if name.lower() == "still-here":

                st.write(
                    "👻 " + name
                )

            else:

                st.write(
                    "· " + name
                )

        st.markdown(
            "### Issues"
        )

        if issues:

            for issue in issues[:10]:

                st.write(
                    f"#{issue.get('number')} "
                    f"— {issue.get('title', '')}"
                )

        else:

            st.write(
                "No issues found."
            )

        if (
            has_ghost_branch
            and has_issue_13
        ):

            st.success(
                "HIDDEN ARTIFACTS DETECTED — "
                "the repository is telling a second story."
            )

        record(
            "LIVE_FORENSICS"
        )


# =========================================================
# DEDUCTION
# =========================================================

with tabs[2]:

    st.subheader(
        "Reconstruct the Incident"
    )

    st.write(
        "Choose carefully. "
        "The second question is the real key."
    )

    suspect = st.radio(
        "WHO BENEFITED?",
        [
            "MIRA — Maintainer",
            "NOAH — Archivist",
            "YOU — Investigator",
        ]
    )

    mechanism = st.radio(
        "WHAT ACTUALLY HAPPENED?",
        [
            "Mira destroyed recovery to seize control.",

            "Noah accidentally buried the recovery path.",

            "Someone used the investigator's actions "
            "to legitimize the cover-up.",
        ]
    )

    if st.button(
        "SUBMIT DEDUCTION",
        type="primary"
    ):

        record("DEDUCTION")

        if (
            suspect.startswith("YOU")
            and mechanism.startswith("Someone")
        ):

            st.session_state.ending = "TRUE"

        elif (
            suspect.startswith("MIRA")
            and mechanism.startswith("Mira")
        ):

            st.session_state.ending = "PARTIAL"

        else:

            st.session_state.ending = "BAD"

        st.rerun()

    st.divider()

    st.markdown(
        "### Investigation Log"
    )

    for action in st.session_state.actions:

        st.write(
            f"▸ {action}"
        )


# =========================================================
# ENDING
# =========================================================

with tabs[3]:

    st.subheader(
        "Final Audit"
    )

    ending = st.session_state.ending

    if ending == "TRUE":

        st.markdown("""
        <div class="hero">

        <div class="small">
        CASE CLOSED // TRUE ENDING
        </div>

        <h2 class="glitch">
        GHOST COMMIT
        </h2>

        <h3>
        THE REPOSITORY DIDN'T LIE.
        <br>
        THE STORY AROUND IT DID.
        </h3>

        <p>
        The cover-up needed an investigator.
        </p>

        <p>
        Your investigation became the final
        piece of evidence that made the false
        history look legitimate.
        </p>

        <h3>
        AUDIT SIGNATURE: YOU
        </h3>

        </div>
        """, unsafe_allow_html=True)

    elif ending == "PARTIAL":

        st.warning("""
        PARTIAL ENDING

        You found the destruction,
        but not who weaponized the investigation.
        """)

    elif ending == "BAD":

        st.error("""
        BAD ENDING

        You trusted the most convenient story.
        """)

    else:

        st.info(
            "No verdict yet."
        )

    st.markdown(
        "### CASE PRINCIPLE"
    )

    st.code(
        "GitHub isn't the platform hosting the game.\n"
        "GitHub IS the game world.",
        language="text"
    )

    if repo:

        fingerprint = hashlib.sha256(
            (
                repo
                + "|"
                + "|".join(
                    st.session_state.actions
                )
            ).encode()
        ).hexdigest()[:16].upper()

        st.caption(
            "SESSION FINGERPRINT // "
            + fingerprint
        )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "GHOST COMMIT // Competition Edition // "
    "Fictional case + public GitHub metadata"
)
