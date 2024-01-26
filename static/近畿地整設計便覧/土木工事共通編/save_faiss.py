# import os
import glob
import streamlit as st
import copy
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
# import json
# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# 作業ディレクトリの設定
WORK_DIR = "static/近畿地整設計便覧/土木工事共通編"

# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/chiseibinran/kyoutsuu"


def pdf_loader(pdf_file: str):
    '''PDFをOCR処理してLangChainのDocumentに変換する関数'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs


def format_metadata(org_docs, page_prefix: int):
    '''DocumentのmetaDataを加工する関数'''

    docs = copy.deepcopy(org_docs)
    for doc in docs:
        # sourceを「近畿地整設計便覧_土木工事共通編」のフォーマットに修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を「1-1」のフォーマットに修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs


def save_local_faiss(docs):
    '''DocumentをFAISSに保存する関数'''
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

        # Documentクラスのメタデータ（出典・ページ番号）を加工
        formatted_docs = format_metadata(docs, i+1)
        print(formatted_docs[0])

        result.extend(formatted_docs)
        print(f'{len(formatted_docs)}個のドキュメントを格納しました')
        print(f'ドキュメントの総数は{len(result)}個になりました。')

    # ベクトルDBに保存
    save_local_faiss(result)
