import streamlit as st

from orchestrator import Orchestrator
from task import Task

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="llm_api_key", type="password")
    "[Gen an OpenAI API Key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/)"
    "[![Open in Github Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/)"

st.title("📑 Write a blog post")
st.caption(" A streamlit blog post writer powered by OpenAI and AutoGen")

with st.form("topic"):
    topic = st.text_area("Enter text:", "What is the topic of your blog post?")
    submitted = st.form_submit_button("Submit")
    num_words = st.number_input(
        "Number of words of your blog post", value=100, placeholder="Type a number..."
    )
    st.write("The current number is ", num_words)
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        task = Task(topic, num_words)
        Orchestrator().generate_response(task)
