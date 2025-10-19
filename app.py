from openai import OpenAI
import streamlit as st

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage  # ✅ Correct import

# Load OpenAI API key from Streamlit secrets
api_key = st.secrets["OPENAI_API_KEY"]

st.markdown("# ChatGPT-like clone")
st.write("Title")

# Initialize the LangChain ChatOpenAI model
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-3.5-turbo",
    streaming=True,
    temperature=0.7
)

# Store the selected model in session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

# Store chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant"):
        # Convert messages to LangChain message format
        langchain_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                langchain_messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                langchain_messages.append(AIMessage(content=m["content"]))
            elif m["role"] == "system":
                langchain_messages.append(SystemMessage(content=m["content"]))

        # ✅ Proper way to stream chunks of text
        def stream_response():
            for chunk in llm.stream(langchain_messages):
                yield chunk.content  # Yield only the text, not the object

        response = st.write_stream(stream_response())

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Extra UI elements (optional)
    st.markdown("ChatGPT like clone")

    if st.button("Click me"):
        st.markdown("Hello")

    agree = st.checkbox("I agree")
    if agree:
        st.write('Great!')

    st.markdown("Title")
