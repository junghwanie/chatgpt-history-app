import streamlit as st
import os

from utils import print_messages, StreamHandler
from langchain_core.messages import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

st.set_page_config(page_title="ChatGPT", page_icon="🦜")
st.title("🦜 ChatGPT")
st.markdown('''
- Refer to [@TeddyNote](https://www.youtube.com/c/@teddynote)
- [`Github 💻 streamlit-tutorial`](https://github.com/happy-jihye/Streamlit-Tutorial)
''')

# API KEY settings
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

# Record data as session state to accumulate conversation content
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Store session state variable that stores chat conversation history
if "store" not in st.session_state:
    st.session_state["store"] = dict()

with st.sidebar:
    session_id = st.text_input("Session ID", value="abc123")

# Print previous conversation history but visualize only
print_messages()

# Systematically remembers previous conversations
# Every time we enter a conversation, it is rerun and the variables are initialized,
# so the conversation contents cannot be accumulated.
# It needs to be modified so that it can be cached by putting it in the session state.
# store = {} 

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in st.session_state["store"]: # If the session ID is not in the store
        # Create a new ChatMessageHistory object and save it to the store
        st.session_state["store"][session_id] = ChatMessageHistory()
    return st.session_state["store"][session_id] # Return session record for that session ID


if user_input := st.chat_input("메시지를 입력해주세요."):
    # What the user entered
    st.chat_message("user").write(f"{user_input}")
    # st.session_state["messages"].append(("user", user_input))
    st.session_state["messages"].append(ChatMessage(role="user", content=user_input))

    # AI's answer
    with st.chat_message("assistant"):
        # Stream results without waiting for a response
        # Print tokens one by one in real time
        stream_handler = StreamHandler(st.empty()) 

        # Generate AI answers using LLM
        # 1. Model definition
        llm = ChatOpenAI(streaming=True, callbacks=[stream_handler])

        # 2. Create prompt
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "질문에 짧고 간결하게 답변해주세요",
                ),
                # Use conversation history as a variable, history becomes the key of MessageHistory
                MessagesPlaceholder(variable_name="history"),
                ("human", "{question}"), # Enter user's question
            ]
        )
        chain = prompt | llm

        chain_with_memory = RunnableWithMessageHistory(
            chain,
            get_session_history, # Retrieve session history
            input_messages_key="question", # Key to User Question
            history_messages_key="history", # Key to the recorded message
        )

        #msg = chain.invoke({"question": user_input})
        #msg = response.content
        response = chain_with_memory.invoke(
            {"question": user_input},
            config={"configurable": {"session_id": session_id}},
        )
        msg = response.content
        # msg = f"당신이 입력한 내용: {user_input}"
        # st.write(msg)
        st.session_state["messages"].append(ChatMessage(role="assistant", content=msg))