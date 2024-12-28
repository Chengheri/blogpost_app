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
        {"role": "assistant", "content": "Hi, I'm an AI agent who can write blog posts."}
    ]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

with st.form("blog post"):
    topic = st.text_area("What is the topic of your blog post ?", "")
    st.session_state.messages.append({"role": "user", "content": topic})
    num_words = st.number_input(
        "Which is the expected number of words of your blog post ?", value=100, placeholder="Type a number..."
    )
    submitted = st.form_submit_button("Submit")
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
    elif submitted:
        task = Task(topic, num_words).get_task()
        llm_config = {"model": model, "api_key": openai_api_key}
        orchestrator = Orchestrator(llm_config)
        response = orchestrator.generate_response(task)
        st.session_state.messages.append({"role": "assistant", "content": response})
        writer_responses = orchestrator.get_writer_responses(response)
        initial_version = writer_responses[0]
        refined_version = writer_responses[1]
        st.write("### Initial version:")
        st.write(initial_version)
        st.write("### Refined version:")
        st.write(refined_version)
        

        meta_feedback = orchestrator.get_meta_feedback(response)
        stoggle(
            "Show Feedback🖍️",
            meta_feedback,
        )

        show_cost = st.checkbox("Show Cost")

        if show_cost:
            cost = orchestrator.get_cost(response)
            st.write(cost)
       

