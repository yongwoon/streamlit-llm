import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from dotenv import load_dotenv
from utils.prompt_loader import PromptLoader

load_dotenv()
st.title("Dynamic prompt")

# 처음 1 번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # session: 대화 내용을 저장하기 위한 용도로 생성
    # @see https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    st.session_state["messages"] = []

with st.sidebar:
    clear_btn = st.button("Reset Chat")

    loader = PromptLoader(base_folder="prompts/dynamic-prompts", languages=['kr', 'en'])
    display_names = loader.get_prompt_files()
    selected_display_name = st.selectbox(
        "Please select prompt type",
        display_names,
        index=0,
    )

    task_input = st.text_input("Input Task", value="")
    selected_prompt = loader.get_file_path(selected_display_name)

# ========= Methods =========
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role: str, message: str):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def create_chain(prompt_file_path: str):
    prompt = load_prompt(prompt_file_path)
    llm = ChatOpenAI(model="gpt-4", temperature=0)
    chain = prompt | llm | StrOutputParser()

    return chain

def build_input_variables():
    if task_input:
        return { "question": user_input, "task": task_input}
    else:
        return { "question": user_input }

# ========= Clear chat history =========
if clear_btn:
    st.session_state["messages"] = []

# ========= Print history ==============
print_messages()

# ========= User Input =================
user_input = st.chat_input("Ask something")
if user_input:
    # Print User Input
    st.chat_message("user").write(user_input)

    chain = create_chain(selected_prompt)
    response = chain.stream(build_input_variables())
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.write(ai_answer)

    # Add User Input to Session
    add_message("user", user_input)
    add_message("assistant", ai_answer)

