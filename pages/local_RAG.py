import os
import streamlit as st
import httpx
import httpcore

from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI
from utils.langsmith_config import setup_langsmith


if "chain" not in st.session_state:
    # file upload 전에 chain 을 생성하지 않음을 의마
    st.session_state["chain"] = None

# Setup LangSmith
setup_langsmith(project_name="local-rag", enable_tracing=True)

try:
    from langchain_ollama import ChatOllama
except ImportError:
    pass

from utils.retriever import create_retriever

# 定数定義
CACHE_DIR = ".cache"
FILES_DIR = f"{CACHE_DIR}/files"
EMBEDDINGS_DIR = f"{CACHE_DIR}/embeddings"
SUPPORTED_MODELS = {
    "xionic": {
        "prompt_file": "prompts/local-lag/en/pdf-rag-xionic.yaml",
        "model_config": {
            "model_name": "xionic-1-72b-20240610",
            "base_url": "https://sionic.chat/v1/",
            "api_key": "934c4bbc-c384-4bea-af82-1450d7f8128d",
        }
    },
    # ollama list 에서 model name 확인 가능
    "ollama": {
        "prompt_file": "prompts/local-lag/en/pdf-rag-ollama.yaml",
        "model_name": "EEVE-Korean-Instruct-10.8B-v1.0-Q8_0.gguf:latest"
        # "model_name": "EEVE-Korean-10.8B:latest"
    }
}

def initialize_directories():
    """キャッシュディレクトリの初期化"""
    for directory in [CACHE_DIR, FILES_DIR, EMBEDDINGS_DIR]:
        if not os.path.exists(directory):
            os.mkdir(directory)

def initialize_session_state():
    """セッション状態の初期化"""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    if "chain" not in st.session_state:
        st.session_state["chain"] = None

def setup_sidebar():
    """サイドバーの設定"""
    with st.sidebar:
        clear_btn = st.button("대화 초기화")
        uploaded_file = st.file_uploader("파일 업로드", type=["pdf"])
        selected_model = st.selectbox("LLM 선택", list(SUPPORTED_MODELS.keys()), index=0)
    return clear_btn, uploaded_file, selected_model

def get_llm(model_name):
    """LLMインスタンスの取得"""
    if model_name == "xionic":
        return ChatOpenAI(**SUPPORTED_MODELS[model_name]["model_config"])
    elif model_name == "ollama":
        return ChatOllama(
            model=SUPPORTED_MODELS[model_name]["model_name"],
            temperature=0
        )
    raise ValueError(f"Unsupported model: {model_name}")

def create_chain(retriever, model_name):
    """チェーンの作成"""
    prompt = load_prompt(SUPPORTED_MODELS[model_name]["prompt_file"])
    llm = get_llm(model_name)

    return (
        {"context": retriever | format_doc, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

def handle_user_input(user_input, warning_msg):
    """ユーザー入力の処理"""
    chain = st.session_state["chain"]
    if chain is None:
        warning_msg.error("파일을 업로드 해주세요.")
        return

    st.chat_message("user").write(user_input)
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""

        try:
            for token in chain.stream(user_input):
                ai_answer += token
                container.markdown(ai_answer)
        except (httpcore.ConnectError, httpx.NetworkError) as e:
            error_msg = f"Network Error: {str(e)}"
            warning_msg.error(f"네트워크 연결 오류: {error_msg}")
        except (httpx.TimeoutException) as e:
            error_msg = f"Timeout Error: {str(e)}"
            warning_msg.error(f"시간 초과 오류: {error_msg}")
        except Exception as e:
            error_msg = f"Unexpected Error: {str(e)}"
            warning_msg.error(f"예상치 못한 오류가 발생했습니다: {error_msg}")
            return

    add_message("user", user_input)
    add_message("assistant", ai_answer)



# 이전 대화를 출력
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message.role).write(chat_message.content)


# 새로운 메시지를 추가
def add_message(role, message):
    st.session_state["messages"].append(ChatMessage(role=role, content=message))


# 파일을 캐시 저장(시간이 오래 걸리는 작업을 처리할 예정)
@st.cache_resource(show_spinner="업로드한 파일을 처리 중입니다...")
def embed_file(file):
    # 업로드한 파일을 캐시 디렉토리에 저장합니다.
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    with open(file_path, "wb") as f:
        f.write(file_content)

    return create_retriever(file_path)


def format_doc(document_list):
    return "\n\n".join([doc.page_content for doc in document_list])

# メイン処理
def main():
    initialize_directories()
    initialize_session_state()

    st.title("Local 모델 기반 RAG 💬")

    clear_btn, uploaded_file, selected_model = setup_sidebar()

    if uploaded_file:
        retriever = embed_file(uploaded_file)
        st.session_state["chain"] = create_chain(retriever, selected_model)

    if clear_btn:
        st.session_state["messages"] = []

    print_messages()

    user_input = st.chat_input("궁금한 내용을 물어보세요!")
    warning_msg = st.empty()

    if user_input:
        handle_user_input(user_input, warning_msg)

if __name__ == "__main__":
    main()
