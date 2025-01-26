import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import ChatPromptTemplate, load_prompt
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain import hub
from dotenv import load_dotenv

load_dotenv()
st.title("My LLM(Large Language Models) App")

# 처음 1 번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # session: 대화 내용을 저장하기 위한 용도로 생성
    # @see https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    st.session_state["messages"] = []

with st.sidebar:
    clear_btn = st.button("Init chat")
    selected_prompt = st.selectbox(
        "Please select prompt type",
        ("Default", "SNS", "Summary"),
        index=0,
    )

# ========= Methods =========
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role: str, message: str):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

def create_chain(prompt_type: str):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 AI 어시스턴트 입니다. 사용자의 요청사항에 따라 적절한 답변을 작성해 주세요."),
        ("user", "#Question: \n{question}"),
    ])

    if prompt_type == "SNS":
        # SNS 게시글 작성 prompt
        prompt = load_prompt("prompts/kr/sns.yaml")
    elif prompt_type == "Summary":
        # 요악 prompt
        # prompt = hub.pull("teddynote/chain-of-density-map-korean")
        prompt = load_prompt("prompts/kr/summary.yaml")

    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    chain = prompt | llm | StrOutputParser()

    return chain

# ========= Clear chat history =========
if clear_btn:
    st.session_state["messages"] = []

print_messages()

# ========= User Input =========
user_input = st.chat_input("Ask something")
if user_input:
    # Print User Input
    st.chat_message("user").write(user_input)

    chain = create_chain(selected_prompt)
    response = chain.stream({"question": user_input})
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.write(ai_answer)

    # Add User Input to Session
    add_message("user", user_input)
    add_message("assistant", ai_answer)

