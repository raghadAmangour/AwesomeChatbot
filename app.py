
from openai import OpenAI
import streamlit as st

api_key = st.secrets["Open_API_KEY "]
import streamlit as st
from langchain_openai import ChatOpenAI
# from langchain.schema import HumanMessage, AIMessage, SystemMessage
from langchain_core.messages import HumanMessage, SystemMessage

st.markdown("# ChatGPT-like clone")

st.write("Title")

# Initialize LangChain ChatOpenAI instead of OpenAI client
llm = ChatOpenAI(
    api_key=api_key,
    model_name="gpt-3.5-turbo",
    streaming=True,
    temperature=0.7
)

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle new user input
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Convert messages to LangChain format
        langchain_messages = []
        for m in st.session_state.messages:
            if m["role"] == "user":
                langchain_messages.append(HumanMessage(content=m["content"]))
            elif m["role"] == "assistant":
                langchain_messages.append(AIMessage(content=m["content"]))
            elif m["role"] == "system":
                langchain_messages.append(SystemMessage(content=m["content"]))
        
        # Stream the response
        response = st.write_stream(llm.stream(langchain_messages))
    
    st.session_state.messages.append({"role": "assistant", "content": response})


    st.markdown("ChatGPT like clone")

    if st.button("Click me"):
        st.markdown("Hello")

    # options= st.multiselect("What is you color" , ["Green", "Black"])

    # st.write('You selectd', options)
    
    agree =st.checkbox("I agree")

    if agree:
        st.write('Great!')

    st.markdown("Title")

    # st.button("Reset", type="primary")
    # if st.button("Say hello"):
    #     st.write("Whys hello there")
    # else:
    #     st.write("Goodbye")

    # if st.button("Aloha", type="tertiary"):
    #     st.write("Ciao")

