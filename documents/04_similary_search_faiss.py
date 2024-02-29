import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
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


if __name__ == "__main__":

    db = load_faiss()

    query = 'アスファルト舗装の最小厚さは？'

    docs_and_scores = db.similarity_search_with_score(query)

    for doc in docs_and_scores:
        print("source:", doc[0].metadata["source"])
        print("page:", doc[0].metadata["page"])
        print("スコア:", doc[1])
