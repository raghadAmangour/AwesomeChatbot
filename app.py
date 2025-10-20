import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

# Load API key from secrets
api_key = st.secrets["OPENAI_API_KEY"]

st.markdown("# ChatGPT-like Clone")

# Initialize model
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-3.5-turbo",
    streaming=True,
    temperature=0.7
)

# Session state
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert to LangChain format
    langchain_messages = []
    for m in st.session_state.messages:
        if m["role"] == "user":
            langchain_messages.append(HumanMessage(content=m["content"]))
        elif m["role"] == "assistant":
            langchain_messages.append(AIMessage(content=m["content"]))
        elif m["role"] == "system":
            langchain_messages.append(SystemMessage(content=m["content"]))

    # Stream response
    response_text = ""
    with st.chat_message("assistant"):
        for chunk in llm.stream(langchain_messages):
            response_text += chunk.content
            st.write(chunk.content)

    st.session_state.messages.append({"role": "assistant", "content": response_text})

# Optional UI
if st.button("Click me"):
    st.markdown("Hello")

if st.checkbox("I agree"):
    st.write("Great!")
