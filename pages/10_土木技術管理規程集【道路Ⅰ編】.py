import os
import openai
from backend.llm_faiss import run_llm
import streamlit as st
from streamlit_chat import message

# OpenAI　APIキー設定
openai.api_key = st.secrets["OPENAI_API_KEY"]

# proxy設定
# デプロイ時はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# header
st.header("LangChain🦜🔗 himeji-model")

# sidebar
with st.sidebar:

    st.subheader('Link')
    "[第1章_道路一般](https://works-documentation.vercel.app/01_%E5%9C%9F%E6%9C%A8%E5%85%B1%E9%80%9A/02_%E8%AA%BF%E6%9F%BB%E3%83%BB%E8%A8%88%E7%94%BB%E3%83%BB%E8%A8%AD%E8%A8%88/01_%E5%9C%9F%E6%9C%A8%E6%8A%80%E8%A1%93%E7%AE%A1%E7%90%86%E8%A6%8F%E5%AE%9A%E9%9B%86/01_%E9%81%93%E8%B7%AF%E2%85%A0%E7%B7%A8/01_%E7%AC%AC%EF%BC%91%E7%AB%A0_%E9%81%93%E8%B7%AF%E4%B8%80%E8%88%AC/%E7%AC%AC%EF%BC%91%E7%AB%A0_%E9%81%93%E8%B7%AF%E4%B8%80%E8%88%AC.pdf)"
    "[OpenAI API](https://platform.openai.com)"

# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "質問を入力してください"}]

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
        query=prompt,
        vectordir=VECTORSTORE_DIR,
        chat_history=st.session_state["chat_history"]
    )
    msg = response['answer']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.session_state.chat_history.append((prompt, response["answer"]))
    st.chat_message("assistant").write(msg)
