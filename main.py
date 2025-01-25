"""
브라우저에서 어떠한 액션(값을 입력, slider 값을 변경)이 있을 때마다,
모든 코드가 갱신（refresh）된다.
"""

import streamlit as st

st.set_page_config(
    page_title="FullstackGPT Home",
    page_icon="🤖",
)

st.markdown(
"""
# Hello!

Welcome to my llm app!

Here are the apps I made:
"""
)