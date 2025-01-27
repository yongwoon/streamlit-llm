"""_summary_

INPUT Message:

Returns:
    _type_: _description_
"""
from dotenv import load_dotenv
from langchain_core.output_parsers import PydanticOutputParser

import streamlit as st
from langchain_core.messages.chat import ChatMessage
from langchain_core.prompts import PromptTemplate, load_prompt
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_community.utilities import SerpAPIWrapper

# Constants
MODEL_NAME = "gpt-4-turbo"
SEARCH_PARAMS = {"engine": "google", "gl": "kr", "hl": "ko", "num": "3"}

# API KEY 정보로드
load_dotenv()

# .streamlit/secrets.toml 에 정의되어 있음
# 검색을 위한 API KEY 설정
# os.environ["SERPAPI_API_KEY"] =

class EmailSummary(BaseModel):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "person": "테디",
                    "company": "테디노트",
                    "email": "teddy@teddynote.com",
                    "subject": "RAG 솔루션 시연 관련 미팅 제안",
                    "summary": "테디노트의 RAG 솔루션 시연을 위한 미팅 제안",
                    "date": "7월 18일 오전 10시"
                }
            ]
        }
    }

    person: str = Field(description="메일을 보낸 사람")
    company: str = Field(description="메일을 보낸 사람의 회사 정보")
    email: str = Field(description="메일을 보낸 사람의 이메일 주소")
    subject: str = Field(description="메일 제목")
    summary: str = Field(description="메일 본문을 요약한 텍스트")
    date: str = Field(description="메일 본문에 언급된 미팅 날짜와 시간")

class ChatState:
    @staticmethod
    def initialize_chat() -> None:
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

    @staticmethod
    def print_messages() -> None:
        for chat_message in st.session_state["messages"]:
            st.chat_message(chat_message.role).write(chat_message.content)

    @staticmethod
    def add_message(role: str, message: str) -> None:
        st.session_state["messages"].append(ChatMessage(role=role, content=message))

    @staticmethod
    def clear_messages() -> None:
        st.session_state["messages"] = []

class EmailChains:
    @staticmethod
    def create_email_parsing_chain():
        output_parser = PydanticOutputParser(pydantic_object=EmailSummary)
        prompt = PromptTemplate.from_template(
            """
            You are a helpful assistant. Please answer the following questions in KOREAN.

            #QUESTION:
            다음의 이메일 내용 중에서 주요 내용을 추출해 주세요.

            #EMAIL CONVERSATION:
            {email_conversation}

            #FORMAT:
            {format}
            """
        )
        prompt = prompt.partial(format=output_parser.get_format_instructions())
        return prompt | ChatOpenAI(model=MODEL_NAME) | output_parser

    @staticmethod
    def create_report_chain():
        prompt = load_prompt("prompts/email/kr/email.yaml")
        return prompt | ChatOpenAI(model=MODEL_NAME) | StrOutputParser()

def process_email(user_input: str) -> None:
    # 1) Parse email
    email_chain = EmailChains.create_email_parsing_chain()
    answer = email_chain.invoke({"email_conversation": user_input})

    # 2) Search additional information
    search = SerpAPIWrapper(params=SEARCH_PARAMS)
    search_query = f"{answer.person} {answer.company} {answer.email}"
    search_result = eval(search.run(search_query))
    search_result_string = "\n".join(search_result)

    # 3) Generate email summary report
    report_chain = EmailChains.create_report_chain()
    report_input = {
        "sender": answer.person,
        "additional_information": search_result_string,
        "company": answer.company,
        "email": answer.email,
        "subject": answer.subject,
        "summary": answer.summary,
        "date": answer.date,
    }

    # Stream response
    response = report_chain.stream(report_input)
    with st.chat_message("assistant"):
        container = st.empty()
        ai_answer = ""
        for token in response:
            ai_answer += token
            container.markdown(ai_answer)

    # Save chat history
    ChatState.add_message("user", user_input)
    ChatState.add_message("assistant", ai_answer)

def main():
    st.title("Email 요약기 💬")

    # Initialize chat state
    ChatState.initialize_chat()

    # Sidebar
    with st.sidebar:
        if st.button("대화 초기화"):
            ChatState.clear_messages()

    # Display chat history
    ChatState.print_messages()

    # Handle user input
    user_input = st.chat_input("궁금한 내용을 물어보세요!")
    if user_input:
        st.chat_message("user").write(user_input)
        process_email(user_input)

if __name__ == "__main__":
    main()
