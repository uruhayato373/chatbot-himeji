import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.schema import Document
from typing import Iterable

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
# os.environ["http_proxy"] = st.secrets["PROXY"]
# os.environ["https_proxy"] = st.secrets["PROXY"]

# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"

# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100

def pdf_loader(pdf_file: str) -> Iterable[Document]:
    '''PDFをLangChainのDocumentに変換する関数'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs

def format_metadata(docs: Iterable[Document], page_prefix: int)-> Iterable[Document]:
    '''Documentのmetadataを加工する関数'''
    for doc in docs:
        # sourceを修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs


if __name__ == "__main__":

    # PDFファイルを指定
    pdf_file = 'static/土木技術管理規程集/道路１編/第１章_道路一般.pdf'

    # Documentリストに変換
    docs = pdf_loader(pdf_file)

    # metadataを加工
    formatted_docs = format_metadata(docs, 1)

    print(docs[0].page_content)
    print("-----------------------------------------------------------")
    print("source:", docs[0].metadata['source'])
    print("-----------------------------------------------------------")
    print("page:", docs[0].metadata['page'])
