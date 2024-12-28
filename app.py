import streamlit as st

from orchestrator import Orchestrator
from task import Task

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="llm_api_key", type="password")
    "[Gen an OpenAI API Key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/Chengheri/blogpost_app)"

st.title("📑 Write a blog post")
st.caption(" A streamlit blog post writer powered by OpenAI and AutoGen")

with st.form("blog post"):
    topic = st.text_area("What is the topic of your blog post ?", "")
    num_words = st.number_input(
        "The number of words of your blog post :", value=100, placeholder="Type a number..."
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        task = Task(topic, num_words).get_task()
        llm_config = {"model": "gpt-3.5-turbo", "api_key": openai_api_key}
        orchestrator = Orchestrator(llm_config)
        response = orchestrator.generate_response(task)
        writer_responses = orchestrator.get_writer_responses(response)
        initial_version = writer_responses[0]
        refined_version = writer_responses[1]
        st.write("### Initial version:")
        st.write(initial_version)
        st.write("### Refined version:")
        st.write(refined_version)
        
with st.form("feedback"):
    show_feedback = st.form_submit_button("Show feedback")
    if show_feedback and response:
        meta_feedback = orchestrator.get_meta_feedback(response)
        st.write("### Feedback")
        st.write(meta_feedback)
       

