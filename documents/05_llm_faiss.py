import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import ConversationalRetrievalChain
import os

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"


def load_faiss():

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # load vectorstore
    vectorstore = FAISS.load_local(VECTORSTORE_DIR, embeddings)

    return vectorstore


def run_llm(query):
    '''ベクトルDBの検索結果を踏まえて回答する関数'''
    vectorstore = load_faiss()

    # set chat-model
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        verbose=True,
        temperature=0,
        model_name="gpt-3.5-turbo-0613"
    )

    # set chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True)

    return chain({"question": query, "chat_history": []})


if __name__ == "__main__":

    db = load_faiss()

    query = 'アスファルト舗装の最小厚さは？'

    results = run_llm(query)
    print("質問：", results["question"])
    print("回答：", results["answer"])
