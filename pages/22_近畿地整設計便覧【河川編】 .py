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
    "[Source Code](https://github.com/dicechick373/chatbot-himeji)"
    "[OpenAI API](https://platform.openai.com)"

# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/chiseibinran/kasen"

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
