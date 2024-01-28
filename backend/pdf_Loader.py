import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# openAIのAPIキーを設定
# OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集/道路１編"

# チャンクサイズとオーバーラップの設定
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


def pdf_loader(pdf_file: str):
    '''PDFをLangChainのDocumentに変換する関数'''

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs
