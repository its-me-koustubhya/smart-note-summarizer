import streamlit as st
from summarizer import generate_summary

st.set_page_config(
    page_title="Smart Note Summarizer",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Smart Note Summarizer")
st.markdown(
    """
    🔐 Your OpenAI API key is <b>never stored or shared</b>.
    It’s used only in your current session to connect directly with OpenAI’s servers.
    """,
    unsafe_allow_html=True,
)

api_key = st.text_input("🔑 Enter your OpenAI API key", type="password")
st.write("Paste your text or article below and let AI summarize it for you.")

SAMPLE_TEXT = """Prompt engineering is a relatively new discipline for developing and optimizing prompts to efficiently use language models (LMs) for a wide variety of applications and research topics. Prompt engineering skills help to better understand the capabilities and limitations of large language models (LLMs).
Researchers use prompt engineering to improve the capacity of LLMs on a wide range of common and complex tasks such as question answering and arithmetic reasoning. Developers use prompt engineering to design robust and effective prompting techniques that interface with LLMs and other tools.
Prompt engineering is not just about designing and developing prompts. It encompasses a wide range of skills and techniques that are useful for interacting and developing with LLMs. It's an important skill to interface, build with, and understand capabilities of LLMs. You can use prompt engineering to improve safety of LLMs and build new capabilities like augmenting LLMs with domain knowledge and external tools.
Motivated by the high interest in developing with LLMs, we have created this new prompt engineering guide that contains all the latest papers, advanced prompting techniques, learning guides, model-specific prompting guides, lectures, references, new LLM capabilities, and tools related to prompt engineering.
"""

# Initialize session state for text
if 'user_text' not in st.session_state:
    st.session_state.user_text = ""


# Button to load sample text
if st.button("📋 Load Sample Text"):
    st.session_state.user_text = SAMPLE_TEXT

# Multi-line text box for input
user_text = st.text_area(
    "📝 Enter your text here:", 
    value=st.session_state.user_text,
    height=300
)

# Update session state when text changes
if user_text != st.session_state.user_text:
    st.session_state.user_text = user_text

PLAN_LIMITS = {
    "Free": 400,    # words
    "Basic": 2000,
    "Pro": 5000
}

plan = st.sidebar.selectbox(
    "Select your usage plan",
    ["Free", "Basic", "Pro"],
    index=0
)

max_words = PLAN_LIMITS[plan]
st.sidebar.caption(f"💡 Max {max_words} words per request for {plan} users.")

st.sidebar.title("About This App")
st.sidebar.info(
    """
    This app uses **OpenAI's GPT-4o-mini** to:
    - Summarize large text passages  
    - Create TL;DR summaries  
    - Generate quiz questions  
    - Estimate API cost  
    """
)

st.caption(f"🧾 Word count: {len(user_text.split())}/{max_words}")

# Button to trigger summarization
if st.button("Summarize Now"):
    if not user_text.strip():
        st.warning("Please enter some text to summarize.")
    elif len(user_text.split()) < 50: 
        st.warning("Text too short! Please enter at least 50 words.") 
    else:
        word_count = len(user_text.split())
        if word_count > max_words:
            st.error(f"🚫 Text too long! You entered {word_count} words, "
                     f"but the {plan} plan allows only {max_words}.")
        else:
            st.info("⚙️ Using Mock Mode" if not api_key else "🔗 Using your OpenAI API key")
            with st.spinner("Generating summary..."):
                summary, cost = generate_summary(user_text,api_key if api_key else None)
                st.subheader("📄 Summary + Quiz")
                st.write(summary)
                if cost > 0:
                    st.success(f"✅ Summary generated! Cost: ${cost:.6f}")
                else:
                    st.info("📝 Mock summary generated (no API key provided)")

