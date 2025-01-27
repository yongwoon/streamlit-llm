"""
브라우저에서 어떠한 액션(값을 입력, slider 값을 변경)이 있을 때마다,
모든 코드가 갱신（refresh）된다.
"""

import streamlit as st

import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth

# config.yaml ファイルの内容を読み込む
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ログインウィジェットの表示
try:
    authenticator.login()
except Exception as e:
    st.error(e)

st.markdown(
"""
# Hello!

Welcome to my llm app!

Here are the apps I made:
"""
)