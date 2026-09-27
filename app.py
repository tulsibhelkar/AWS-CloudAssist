import sys
import time
from pathlib import Path

import requests
import streamlit as st


# ============================================================
# 1. PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

st.set_page_config(
    page_title="AWS CloudAssist | AI Technical Support",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. PROFESSIONAL CSS
# ============================================================

st.markdown(
    """
<style>

/* ---------- GLOBAL ---------- */

.stApp {
    background-color: #F4F7FB;
    color: #172033;
}

.main .block-container,
[data-testid="stMainBlockContainer"] {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 6rem;
}

[data-testid="stMain"] {
    background-color: #F4F7FB;
}

[data-testid="stMain"] p,
[data-testid="stMain"] h1,
[data-testid="stMain"] h2,
[data-testid="stMain"] h3,
[data-testid="stMain"] label {
    color: #172033;
}


/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"] {
    background: #151D2B;
    border-right: 1px solid #263244;
}

section[data-testid="stSidebar"] * {
    color: #E5E7EB;
}

section[data-testid="stSidebar"] .stCaption {
    color: #A8B4C6;
}

section[data-testid="stSidebar"] hr {
    border-color: #344154;
}

section[data-testid="stSidebar"] button {
    background: #263449;
    color: #FFFFFF !important;
    border: 1px solid #40516B;
    border-radius: 10px;
}

section[data-testid="stSidebar"] button:hover {
    background: #354760;
    color: #FFFFFF !important;
    border-color: #FF9900;
}

section[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background: #202B3C;
    border-color: #40516B;
}

section[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #FFFFFF;
}


/* ---------- HERO ---------- */

.hero {
    background: linear-gradient(
        120deg,
        #111827 0%,
        #192A43 60%,
        #243C59 100%
    );
    border: 1px solid #334155;
    border-radius: 20px;
    padding: 36px 40px;
    margin-bottom: 25px;
    box-shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
}

.hero-label {
    color: #FFB84D;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 2px;
    margin-bottom: 12px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 38px;
    font-weight: 800;
    letter-spacing: -1px;
    margin-bottom: 12px;
}

.hero-description {
    color: #D0DBE8;
    font-size: 15px;
    line-height: 1.8;
    max-width: 760px;
}


/* ---------- SECTION TITLES ---------- */

.section-heading {
    color: #172033;
    font-size: 19px;
    font-weight: 750;
    margin-top: 18px;
    margin-bottom: 12px;
}


/* ---------- METRIC CARDS ---------- */

div[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #DFE7F0;
    border-radius: 15px;
    padding: 18px 20px;
    box-shadow: 0 4px 15px rgba(15, 23, 42, 0.04);
}

div[data-testid="stMetric"] * {
    color: #172033 !important;
}

div[data-testid="stMetricLabel"] p {
    color: #64748B !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

div[data-testid="stMetricValue"] {
    color: #172033 !important;
    font-weight: 800 !important;
}


/* ---------- MAIN BUTTONS ---------- */

[data-testid="stMain"] .stButton button {
    background: #FFFFFF;
    color: #172033 !important;
    border: 1px solid #D9E2EE;
    border-radius: 11px;
    min-height: 48px;
    font-weight: 650;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.03);
}

[data-testid="stMain"] .stButton button * {
    color: #172033 !important;
}

[data-testid="stMain"] .stButton button:hover {
    background: #FFF4DF;
    color: #172033 !important;
    border-color: #FF9900;
}

[data-testid="stMain"] .stButton button:hover * {
    color: #172033 !important;
}


/* ---------- CHAT MESSAGES ---------- */

div[data-testid="stChatMessage"] {
    background: #FFFFFF;
    border: 1px solid #E1E8F0;
    border-radius: 15px;
    padding: 16px 20px;
    margin-bottom: 14px;
    box-shadow: 0 3px 12px rgba(15, 23, 42, 0.035);
}

div[data-testid="stChatMessage"] p,
div[data-testid="stChatMessage"] li {
    color: #172033 !important;
    line-height: 1.7;
}

div[data-testid="stChatMessage"] a {
    color: #2563EB !important;
}


/* ---------- CHAT INPUT ---------- */

div[data-testid="stChatInput"] {
    background: #FFFFFF;
    border: 1px solid #D9E2EE;
    border-radius: 14px;
}

div[data-testid="stChatInput"] textarea {
    color: #172033 !important;
    background: #FFFFFF !important;
}

div[data-testid="stChatInput"] textarea::placeholder {
    color: #64748B !important;
}

div[data-testid="stChatInput"] button {
    color: #172033 !important;
}


/* ---------- EXPANDERS ---------- */

[data-testid="stMain"] [data-testid="stExpander"] {
    background: #F8FAFC;
    border: 1px solid #E2E8F0;
    border-radius: 10px;
}

[data-testid="stMain"] [data-testid="stExpander"] * {
    color: #172033;
}


/* ---------- FOOTER ---------- */

.custom-footer {
    text-align: center;
    color: #64748B;
    font-size: 12px;
    line-height: 1.8;
    padding-top: 35px;
}

footer {
    visibility: hidden;
}


/* ---------- RESPONSIVE ---------- */

@media (max-width: 768px) {

    .hero {
        padding: 24px;
    }

    .hero-title {
        font-size: 29px;
    }

    .hero-description {
        font-size: 14px;
    }

    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem;
    }

}

</style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 3. LOAD RAG SYSTEM
# ============================================================

@st.cache_resource(show_spinner="Loading AWS knowledge base...")
def load_rag_system():
    from generate_answer import generate_answer
    return generate_answer


@st.cache_resource(show_spinner=False)
def get_collection():
    import chromadb

    client = chromadb.PersistentClient(
        path=str(BASE_DIR / "data" / "chroma_db")
    )

    return client.get_collection(
        name="aws_cloudassist"
    )


def get_chunk_count():
    try:
        return get_collection().count()
    except Exception:
        return 0


def check_ollama():
    try:
        response = requests.get(
            "http://localhost:11434/api/tags",
            timeout=3,
        )

        return response.status_code == 200

    except requests.RequestException:
        return False


# ============================================================
# 4. SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "total_questions" not in st.session_state:
    st.session_state.total_questions = 0

if "last_response_time" not in st.session_state:
    st.session_state.last_response_time = None

if "pending_question" not in st.session_state:
    st.session_state.pending_question = None


# ============================================================
# 5. SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## ☁️ AWS CloudAssist")

    st.caption("AI TECHNICAL SUPPORT PLATFORM")

    st.divider()

    st.markdown("### Workspace")

    st.markdown("**💬 AI Assistant**")

    st.caption(
        "Documentation-grounded answers "
        "for supported AWS services."
    )

    st.divider()

    st.markdown("### Supported Services")

    st.markdown("☁️ Amazon EC2")
    st.markdown("🪣 Amazon S3")
    st.markdown("🔐 AWS IAM")

    st.divider()

    st.markdown("### System Status")

    ollama_online = check_ollama()

    if ollama_online:
        st.success("Ollama service online")
    else:
        st.error("Ollama service offline")

    st.caption("Language model: Llama 3.2 3B")
    st.caption("Vector database: ChromaDB")
    st.caption("Embedding model: MiniLM-L6-v2")

    st.divider()

    if st.button(
        "Clear Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.total_questions = 0
        st.session_state.last_response_time = None
        st.session_state.pending_question = None
        st.rerun()

    st.divider()

    st.caption(
        "AWS CloudAssist | Local RAG Application"
    )


# ============================================================
# 6. HERO HEADER
# ============================================================

# IMPORTANT:
# HTML is left-aligned to prevent Markdown from
# displaying the tags as a code block.

st.markdown(
    """
<div class="hero">
<div class="hero-label">INTELLIGENT CLOUD SUPPORT</div>
<div class="hero-title">AWS CloudAssist</div>
<div class="hero-description">
Your AI-powered technical assistant for Amazon EC2,
Amazon S3, and AWS Identity and Access Management.
Ask questions, explore cloud concepts, and receive
documentation-grounded answers with source references.
</div>
</div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 7. DASHBOARD METRICS
# ============================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Knowledge Base",
        value=f"{get_chunk_count()} Chunks",
    )

with col2:
    st.metric(
        label="Questions Asked",
        value=st.session_state.total_questions,
    )

with col3:

    response_time = st.session_state.last_response_time

    st.metric(
        label="Last Response",
        value=(
            f"{response_time:.1f}s"
            if response_time is not None
            else "—"
        ),
    )


# ============================================================
# 8. EXAMPLE QUESTIONS
# ============================================================

if not st.session_state.messages:

    st.markdown(
        '<div class="section-heading">Explore AWS CloudAssist</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Select a suggested question or enter your own below."
    )

    examples = [
        (
            "EC2 Basics",
            "What is an EC2 instance?"
        ),
        (
            "S3 Storage",
            "What is Amazon S3?"
        ),
        (
            "IAM Security",
            "What is AWS IAM?"
        ),
        (
            "EC2 Features",
            "What are the features of Amazon EC2?"
        ),
    ]

    example_cols = st.columns(2)

    for index, (label, example_question) in enumerate(examples):

        with example_cols[index % 2]:

            if st.button(
                label,
                key=f"example_{index}",
                use_container_width=True,
            ):

                st.session_state.pending_question = (
                    example_question
                )

                st.rerun()


# ============================================================
# 9. SOURCE RENDERING
# ============================================================

def render_sources(sources):

    if not sources:
        return

    with st.expander(
        f"AWS Documentation Sources ({len(sources)})"
    ):

        for index, source in enumerate(
            sources,
            start=1
        ):

            st.markdown(
                f"**{index}. {source['title']}**"
            )

            st.markdown(
                f"[Open official AWS documentation]({source['url']})"
            )

            if index < len(sources):
                st.divider()


# ============================================================
# 10. CHAT HISTORY
# ============================================================

st.markdown(
    '<div class="section-heading">AI Assistant</div>',
    unsafe_allow_html=True,
)

for message in st.session_state.messages:

    avatar = (
        "👤"
        if message["role"] == "user"
        else "☁️"
    )

    with st.chat_message(
        message["role"],
        avatar=avatar,
    ):

        st.markdown(message["content"])

        if message.get("response_time") is not None:

            st.caption(
                f"Response time: "
                f"{message['response_time']:.1f} seconds"
            )

        render_sources(
            message.get("sources", [])
        )


# ============================================================
# 11. QUESTION INPUT
# ============================================================

typed_question = st.chat_input(
    "Ask a question about EC2, S3, or IAM..."
)

if typed_question:

    st.session_state.pending_question = (
        typed_question
    )


question = st.session_state.pending_question


# ============================================================
# 12. GENERATE ANSWER
# ============================================================

if question:

    st.session_state.pending_question = None

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    st.session_state.total_questions += 1

    with st.chat_message(
        "user",
        avatar="👤"
    ):
        st.markdown(question)

    with st.chat_message(
        "assistant",
        avatar="☁️"
    ):

        if not ollama_online:

            answer = (
                "Ollama is currently unavailable. "
                "Please start Ollama and try again."
            )

            st.error(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                    "sources": [],
                    "response_time": None,
                }
            )

        else:

            start_time = time.perf_counter()

            try:

                with st.spinner(
                    "Searching AWS documentation and generating answer..."
                ):

                    generate_answer = load_rag_system()

                    answer, results = generate_answer(
                        question
                    )

                elapsed = (
                    time.perf_counter() - start_time
                )

                st.session_state.last_response_time = elapsed

                sources = []
                seen_urls = set()

                for result in results:

                    metadata = result["metadata"]

                    url = metadata["source_url"]

                    if url in seen_urls:
                        continue

                    seen_urls.add(url)

                    sources.append(
                        {
                            "title": metadata["title"],
                            "url": url,
                            "service": metadata["service"],
                        }
                    )

                st.markdown(answer)

                st.caption(
                    f"Response generated in "
                    f"{elapsed:.1f} seconds"
                )

                render_sources(sources)

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": answer,
                        "sources": sources,
                        "response_time": elapsed,
                    }
                )

            except Exception as error:

                st.error(
                    "An error occurred while "
                    "processing your question."
                )

                st.code(str(error))

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": (
                            "An error occurred while "
                            "processing your question."
                        ),
                        "sources": [],
                        "response_time": None,
                    }
                )


# ============================================================
# 13. FOOTER
# ============================================================

st.markdown(
    """
<div class="custom-footer">
AWS CloudAssist | Documentation-Grounded AI Assistant
<br>
Built with Python · Streamlit · ChromaDB · Ollama
<br>
Independent student project. Not affiliated with AWS.
</div>
    """,
    unsafe_allow_html=True,
)
