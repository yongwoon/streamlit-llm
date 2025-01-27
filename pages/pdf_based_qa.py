from dataclasses import dataclass
from typing import List

import os
import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import load_prompt
from langchain_core.runnables import RunnablePassthrough
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_openai import ChatOpenAI
from utils.langsmith_config import setup_langsmith
from utils.retriever import create_retriever


if "chain" not in st.session_state:
    # file upload 전에 chain 을 생성하지 않음을 의마
    st.session_state["chain"] = None

# Setup LangSmith
setup_langsmith(
    project_name="trace-PDF",
    enable_tracing=True
)

st.title("pdf based QA")

# Create cache directory
if not os.path.exists(".cache"):
    os.mkdir(".cache")
if not os.path.exists(".cache/files"):
    os.mkdir(".cache/files")


# 처음 1 번만 실행하기 위한 코드
if "messages" not in st.session_state:
    # session: 대화 내용을 저장하기 위한 용도로 생성
    # @see https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
    st.session_state["messages"] = []

if "chain" not in st.session_state:
    # file upload 전에 chain 을 생성하지 않음을 의마
    st.session_state["chain"] = None

    # Setup LangSmith
    setup_langsmith(
        project_name="pdf-based-qa",
        enable_tracing=True
    )

@dataclass
class AppConfig:
    AVAILABLE_MODELS: List[str] = ("gpt-4o", "gpt-4-turbo", "gpt-4o-mini")
    DEFAULT_MODEL: str = "gpt-4o"

with st.sidebar:
    clear_btn = st.button("Reset Chat")
    uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
    selected_model = st.selectbox(
        "Select gpt Model",
        AppConfig.AVAILABLE_MODELS,
        index=0)

def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)

def add_message(role: str, message: str):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

# Caching uploaded file (시간이 오래 걸리는 작업을 처리할 예정)
# 한번 Upload 를 하면, 다음에 Upload 할때는 Cache 를 사용함
@st.cache_resource(show_spinner="Processing uploaded file...")
def embed_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장합니다.
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    return create_retriever(file_path)

# 해당 코드에서 create_chain() 함수가 if uploaded_file 블록보다 위에 있어야 하는 이유는 다음과 같습니다:
#
# 함수 정의 순서:
# Python에서는 함수를 사용하기 전에 먼저 정의되어 있어야 합니다.
# 만약 create_chain() 함수가 if uploaded_file 블록 아래에 있다면,
# 해당 함수를 호출할 때 NameError: name 'create_chain' is not defined 에러가 발생할 수 있습니다.
#
# 코드 실행 흐름:
# 이 Streamlit 앱에서는:
# 사용자가 파일을 업로드하면 if uploaded_file 블록이 실행됩니다
# 그 후 사용자가 입력을 하면 create_chain() 함수가 호출됩니다
# 따라서 create_chain() 함수는 실제로 사용되기 전에 정의되어 있어야 정상적으로 작동합니다.
# 이는 Python의 기본적인 스코프 규칙을 따르는 것으로, 코드의 안정성과 가독성을 위해 함수는 사용되기 전에 정의되어야 합니다.
def create_chain(retriever: VectorStoreRetriever, model_name=AppConfig.DEFAULT_MODEL):
    # ========== RAG process =============
    # 単階 6: Create Prompt
    prompt = load_prompt("prompts/pdf/en/pdf-rag.yaml")

    # 단계 7: LLM 생성
    llm = ChatOpenAI(model_name=model_name, temperature=0)

    # 단계 8: Chain 생성
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return chain

# ========== file uploader =============
if uploaded_file:
    # ファイル Upload 後, retriver 生成 (process time が 長く かかる 作業)
    retriever = embed_file(uploaded_file)
    chain = create_chain(retriever, model_name=selected_model)
    st.session_state["chain"] = chain

# ========= Clear chat history =========
if clear_btn:
    st.session_state["messages"] = []

# ========= Print history ==============
print_messages()

# ========= User Input =================
user_input = st.chat_input("Ask something")
warning_msg = st.empty()

if user_input:
    chain = st.session_state["chain"]

    if chain is not None:
        # Print User Input
        st.chat_message("user").write(user_input)
        response = chain.stream(user_input)
        with st.chat_message("assistant"):
            container = st.empty()
            ai_answer = ""
            for token in response:
                ai_answer += token
                container.write(ai_answer)

        # Add User Input to Session
        add_message("user", user_input)
        add_message("assistant", ai_answer)
    else:
        warning_msg.write("Please upload a PDF file first.")
