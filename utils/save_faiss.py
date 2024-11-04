import glob
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import OpenAIEmbeddings
from .pdf_loader import pdf_loader
from .format_docs import format_docs

# OpenAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"

# vectorstoreを保存するディレクトリの設定（日本語のディレクトリ名はエラーになる）
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"


def save_local_faiss(docs):
    """DocumentをFAISSに保存する関数"""
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY, verify=False)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_DIR)
    print(f"{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。")


def process_pdfs():
    """ディレクトリ内のPDFファイルを処理してベクトルDBに保存する関数"""
    pdf_files = glob.glob(f"{WORK_DIR}/*.pdf")
    result = []

    for i, file in enumerate(pdf_files, 1):
        print(f"{file}を処理中・・・")
        docs = pdf_loader(file)
        format = format_docs(docs, i)
        result.extend(format)
        print(f"{len(format)}個のドキュメントを格納しました")
        print(f"ドキュメントの総数は{len(result)}個になりました。")

    save_local_faiss(result)


if __name__ == "__main__":
    print(OPENAI_API_KEY)
    process_pdfs()
