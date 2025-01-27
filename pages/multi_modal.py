import streamlit as st
import os
from langchain_core.messages.chat import ChatMessage
from langchain_openai import ChatOpenAI
from utils.langsmith_config import setup_langsmith
from utils.models import MultiModal

# Constants
CACHE_DIR = ".cache"
FILES_DIR = f"{CACHE_DIR}/files"
EMBEDDINGS_DIR = f"{CACHE_DIR}/embeddings"
DEFAULT_SYSTEM_PROMPT = """당신은 표(재무제표) 를 해석하는 금융 AI 어시스턴트 입니다.
당신의 임무는 주어진 테이블 형식의 재무제표를 바탕으로 흥미로운 사실을 정리하여 친절하게 답변하는 것입니다."""

# Setup LangSmith
setup_langsmith(project_name="multi-modal", enable_tracing=True)

def init_directories():
    """Initialize required directories"""
    for directory in [CACHE_DIR, FILES_DIR, EMBEDDINGS_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)

def init_session_state():
    """Initialize session state variables"""
    if "messages" not in st.session_state:
        st.session_state["messages"] = []

def create_sidebar():
    """Create and handle sidebar elements"""
    with st.sidebar:
        clear_btn = st.button("대화 초기화")
        uploaded_file = st.file_uploader("이미지 업로드", type=["jpg", "jpeg", "png"])
        selected_model = st.selectbox("LLM 선택", ["gpt-4o", "gpt-4o-mini"], index=0)
        system_prompt = st.text_area(
            "시스템 프롬프트",
            DEFAULT_SYSTEM_PROMPT,
            height=200,
        )
    return clear_btn, uploaded_file, selected_model, system_prompt

def print_messages(tab):
    """Print previous messages in the specified tab"""
    for chat_message in st.session_state["messages"]:
        tab.chat_message(chat_message.role).write(chat_message.content)

def add_message(role, message):
    """Add a new message to the session state"""
    st.session_state["messages"].append(ChatMessage(role=role, content=message))

@st.cache_resource(show_spinner="업로드한 이미지를 처리 중입니다...")
def process_imagefile(file):
    """Process and save uploaded image file"""
    file_path = os.path.join(FILES_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())
    return file_path

def generate_answer(image_filepath, system_prompt, user_prompt, model_name="gpt-4o"):
    """Generate answer using the multimodal model"""
    llm = ChatOpenAI(
        temperature=0,
        model_name=model_name,
    )
    multimodal = MultiModal(llm, system_prompt=system_prompt, user_prompt=user_prompt)
    return multimodal.stream(image_filepath)

def handle_user_input(user_input, uploaded_file, system_prompt, selected_model, tabs):
    """Handle user input and generate response"""
    main_tab1, main_tab2 = tabs
    warning_msg = main_tab2.empty()

    if not uploaded_file:
        warning_msg.error("이미지를 업로드 해주세요.")
        return

    image_filepath = process_imagefile(uploaded_file)
    response = generate_answer(
        image_filepath, system_prompt, user_input, selected_model
    )

    main_tab2.chat_message("user").write(user_input)

    with main_tab2.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token.content
            container.markdown(ai_answer)

    add_message("user", user_input)
    add_message("assistant", ai_answer)

def main():
    """Main application function"""
    init_directories()
    init_session_state()

    st.title("이미지 인식 기반 챗봇 💬")

    # Create tabs
    tabs = st.tabs(["이미지", "대화내용"])
    main_tab1, main_tab2 = tabs

    # Setup sidebar
    clear_btn, uploaded_file, selected_model, system_prompt = create_sidebar()

    if clear_btn:
        st.session_state["messages"] = []

    print_messages(main_tab2)

    if uploaded_file:
        image_filepath = process_imagefile(uploaded_file)
        main_tab1.image(image_filepath)

    user_input = st.chat_input("궁금한 내용을 물어보세요!")
    if user_input:
        handle_user_input(user_input, uploaded_file, system_prompt, selected_model, tabs)

if __name__ == "__main__":
    main()
