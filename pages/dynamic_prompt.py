from typing import Dict

from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import  load_prompt
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

import streamlit as st
from dotenv import load_dotenv
from utils.prompt_loader import PromptLoader

# 정수 설정
MODEL_NAME = "gpt-4"
DEFAULT_TEMPERATURE = 0

class ChatHistory:
    def __init__(self):
        # 처음 1 번만 실행하기 위한 코드
        if "messages" not in st.session_state:
            # session: 대화 내용을 저장하기 위한 용도로 생성
            # @see https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state
            st.session_state["messages"] = []

    def add_message(self, role: str, content: str) -> None:
        st.session_state["messages"].append(ChatMessage(role=role, content=content))

    def clear(self) -> None:
        st.session_state["messages"] = []

    def print_messages(self) -> None:
        for chat_message in st.session_state["messages"]:
            st.chat_message(chat_message.role).write(chat_message.content)

class DynamicPromptApp:
    def __init__(self):
        load_dotenv()
        self.chat_history = ChatHistory()
        self.prompt_loader = PromptLoader(
            base_folder="prompts/dynamic-prompts",
            languages=['kr', 'en']
        )

    def setup_sidebar(self) -> tuple[bool, str, str]:
        with st.sidebar:
            clear_btn = st.button("Reset Chat")
            display_names = self.prompt_loader.get_prompt_files()
            selected_display_name = st.selectbox(
                "Please select prompt type",
                display_names,
                index=0,
            )
            task_input = st.text_input("Input Task", value="")
            selected_prompt = self.prompt_loader.get_file_path(selected_display_name)

        return clear_btn, selected_prompt, task_input

    def create_chain(self, prompt_file_path: str):
        try:
            prompt = load_prompt(prompt_file_path)
            llm = ChatOpenAI(model=MODEL_NAME, temperature=DEFAULT_TEMPERATURE)
            return prompt | llm | StrOutputParser()
        except Exception as e:
            st.error(f"Error creating chain: {str(e)}")
            return None

    def build_input_variables(self, user_input: str, task_input: str) -> Dict[str, str]:
        return {"question": user_input, "task": task_input} if task_input else {"question": user_input}

    def handle_user_input(self, user_input: str, selected_prompt: str, task_input: str) -> None:
        # Print User Input
        st.chat_message("user").write(user_input)

        chain = self.create_chain(selected_prompt)
        if chain:
            response = chain.stream(self.build_input_variables(user_input, task_input))
            with st.chat_message("assistant"):
                container = st.empty()
                ai_answer = ""
                for token in response:
                    ai_answer += token
                    container.write(ai_answer)

            # Add User Input to Session
            self.chat_history.add_message("user", user_input)
            self.chat_history.add_message("assistant", ai_answer)

    def run(self):
        st.title("Dynamic prompt")

        clear_btn, selected_prompt, task_input = self.setup_sidebar()

        # ========= Clear chat history =========
        if clear_btn:
            self.chat_history.clear()

        # ========= Print history ==============
        self.chat_history.print_messages()

        # ========= User Input =================
        user_input = st.chat_input("Ask something")
        if user_input:
            self.handle_user_input(user_input, selected_prompt, task_input)

if __name__ == "__main__":
    app = DynamicPromptApp()
    app.run()
