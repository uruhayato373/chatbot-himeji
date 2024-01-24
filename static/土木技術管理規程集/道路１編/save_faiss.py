import os
import glob
import streamlit as st
import copy
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
import json
# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"

# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNL_OVERLAP = 100

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"

# PDFをOCR処理してLangChainのDocumentクラスに変換する関数
def pdf_loader(pdf_file: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNL_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs

# DocumentクラスのMetaDataを加工する関数
def format_docs(org_docs, page_prefix: int):
    docs = copy.deepcopy(org_docs)
    for doc in docs:
        # sourceを「土木技術管理規程集_道路１編」のフォーマットに修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を「1-1」のフォーマットに修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs

# Documentクラスをvectorstore(FAISS)に保存する関数
def save_local_faiss(docs):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(VECTORSTORE_DIR)
    print(f'{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。')
    return 


if __name__ == "__main__":
    # ディレクトリ内のPDFファイルを取得
    pdf_files = glob.glob(f"{WORK_DIR}/*.pdf")

    # ディレクトリ内のPDFを単一のリストに格納
    result = []

    # 全PDFファイルを処理
    for i, file in enumerate(pdf_files):
        print(f'{file}を処理中・・・')
        
        # PDFをOCR処理してDocumentクラスに格納
        docs = pdf_loader(file)
        print(docs[0])

        # Documentクラスのメタデータ（出典・ページ番号）を加工        
        format = format_docs(docs, i+1)

        result.extend(format)
        print(f'{len(format)}個のドキュメントを格納しました')
        print(f'ドキュメントの総数は{len(result)}個になりました。')


        
    # ベクトルDBに保存
    save_local_faiss(result)
