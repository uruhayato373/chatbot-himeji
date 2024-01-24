import os
import openai
from backend.llm_faiss import run_llm
import streamlit as st
from streamlit_chat import message

# OpenAI　APIキー設定
openai.api_key = st.secrets["OPENAI_API_KEY"]

# proxy設定 
# デプロイ時はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# header
st.header("LangChain🦜🔗 himeji-model")

# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "質問を入力してください"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
  
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
            query=prompt,vectordir = VECTORSTORE_DIR
        )
    msg = response['answer']
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)

