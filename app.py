import streamlit as st
from streamlit_extras.stoggle import stoggle


from orchestrator import Orchestrator
from task import Task

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="llm_api_key", type="password")
    "[Gen an OpenAI API Key](https://platform.openai.com/account/api-keys)"

    model = st.selectbox(
        "Which model do you want to use ?",
        ("gpt-3.5-turbo", "gpt-4o"),
    )

    "[View the source code](https://github.com/Chengheri/blogpost_app)"

st.title("📑 Write a blog post")
st.caption(" A streamlit blog post writer powered by OpenAI and AutoGen")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi, we are a team of multi agents who can write blog posts."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if "response" not in st.session_state:
    st.session_state["response"] = None

if "submitted" not in st.session_state:
    st.session_state["submitted"] = False

with st.form(key="blog_post"):
    topic = st.text_area("What is the topic of your blog post ?", "", key="topic")
    num_words = st.number_input(
        "Which is the expected number of words of your blog post ?", key="num_words", value=100, placeholder="Type a number..."
    )
    submitted = st.form_submit_button("Submit")
    st.session_state["submitted"] = submitted
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        task = Task(topic, num_words).get_task()
        llm_config = {"model": model, "api_key": openai_api_key}
        orchestrator = Orchestrator(llm_config)
        response = orchestrator.generate_response(task)
        writer_responses = orchestrator.get_writer_responses(response)
        initial_version = writer_responses[0]
        refined_version = writer_responses[1]
        st.write("### Initial version:")
        st.write(initial_version)
        st.write("### Refined version:")
        st.write(refined_version)
        
        cost = orchestrator.get_cost(response)
        st.session_state["cost"] = cost
        
        meta_feedback = orchestrator.get_meta_feedback(response)
        stoggle(
            "🖍️Show Feedback",
            meta_feedback,
        )
        
if st.session_state["submitted"]:
    show_cost = st.button("Show Cost")
    if show_cost:
        st.write(st.session_state["cost"])
       

