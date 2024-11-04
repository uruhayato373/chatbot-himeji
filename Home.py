import json
import openai
from backend.llm_faiss import run_llm
import streamlit as st

# OpenAI　APIキー設定
openai.api_key = st.secrets["OPENAI_API_KEY"]

# JSONファイルから設定を読み込む
with open("config.json", "r") as f:
    config = json.load(f)


def get_vectorstore_dir(stock):
    return config["stock_dir_map"].get(stock, "")


def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state["messages"] = [
            {"role": "assistant", "content": "質問を入力してください"}
        ]
    if "chat_history" not in st.session_state:
        st.session_state["chat_history"] = []


def display_chat_history():
    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])


def process_user_input(prompt, vectorstore_dir):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = run_llm(
        query=prompt,
        vectordir=vectorstore_dir,
        chat_history=st.session_state["chat_history"],
    )
    msg = response["answer"]
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.session_state.chat_history.append((prompt, response["answer"]))
    st.chat_message("assistant").write(msg)


def main():
    st.header("LangChain🦜🔗 himeji-model")

    with st.sidebar:
        stock = st.radio(
            label="対象図書を選択してください",
            options=config["stock_options"],
            index=0,
        )

        st.subheader("Link")
        "[OpenAI API](https://platform.openai.com)"

    vectorstore_dir = get_vectorstore_dir(stock)

    initialize_session_state()
    display_chat_history()

    if prompt := st.chat_input():
        process_user_input(prompt, vectorstore_dir)


if __name__ == "__main__":
    main()
