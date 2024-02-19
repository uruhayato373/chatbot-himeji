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

def vectorstore_dir(stock):
    if stock == '土木工事共通仕様書':
        return "vectorstore/faiss/kyoutsuu_shiyousyo"
    elif stock == '土木請負工事必携':
        return "vectorstore/faiss/hikkei"
    elif stock == '規程集【道路Ⅰ編】':
        return "vectorstore/faiss/kiteisyuu/douro1"
    elif stock == '規程集【道路Ⅱ編】':
        return "vectorstore/faiss/kiteisyuu/douro2"
    elif stock == '規程集【河川編】':
        return "vectorstore/faiss/kiteisyuu/kasen"
    elif stock == '規程集【砂防編_砂防】':
        return "vectorstore/faiss/kiteisyuu/sabou"
    elif stock == '規程集【砂防編_急傾斜】':
        return "vectorstore/faiss/kiteisyuu/kyuukeisya"
    elif stock == '規程集【砂防編_地すべり】 ':
        return "vectorstore/faiss/kiteisyuu/jisuberi"
    elif stock == '地整便覧【土木工事共通編】':
        return "vectorstore/faiss/chiseibinran/kyoutsuu"
    elif stock == '地整便覧【道路編】 ':
        return "vectorstore/faiss/chiseibinran/douro"
    elif stock == '地整便覧【河川編】 ':
        return "vectorstore/faiss/chiseibinran/kasen"
    elif stock == '道路構造令':
        return "vectorstore/faiss/douro_kouzourei"
    elif stock == '河川管理施設等構造令':
        return "vectorstore/faiss/kasen_kouzourei"

# header
st.header("LangChain🦜🔗 himeji-model")

# sidebar
with st.sidebar:

    stock = st.radio(
        label='対象図書を選択してください',
        options=('土木工事共通仕様書', '土木請負工事必携', '規程集【道路Ⅰ編】',
                 '規程集【道路Ⅱ編】', '規程集【河川編】','規程集【砂防編_砂防】',
                 '規程集【砂防編_急傾斜】', '規程集【砂防編_地すべり】',
                 '地整便覧【土木工事共通編】', '地整便覧【道路編】', '地整便覧【河川編】'),
        index=0,
        # horizontal=True,
        )

    st.subheader('Link')
    "[OpenAI API](https://platform.openai.com)"

    
VECTORSTORE_DIR = vectorstore_dir(stock)

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