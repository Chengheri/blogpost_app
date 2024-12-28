import streamlit as st

from orchestrator import Orchestrator
from task import Task

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="llm_api_key", type="password")
    "[Gen an OpenAI API Key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/Chengheri/blogpost_app)"

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
        task = Task(topic, num_words).get_task()
        llm_config = {"model": "gpt-3.5-turbo", "api_key": openai_api_key}
        Orchestrator(llm_config).generate_response(task)

