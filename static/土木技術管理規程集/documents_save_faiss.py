import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from  langchain.schema import Document
import json
from typing import Iterable
import glob
import openai
import time

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# 作業ディレクトリの設定
WORK_DIR = "static/土木技術管理規程集"

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu"

# LangchainのDocumentクラスを保存したjsonLファイルを読み込む関数
def load_docs_from_jsonl(file_path)->Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

# Documentクラスをvectorstore(FAISS)に保存する関数
def save_local_faiss(docs):
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    try:
      db = FAISS.from_documents(docs, embeddings)
      db.save_local(VECTORSTORE_DIR)
      print(f'{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。')
      return 
    except openai.error.RateLimitError as e:
      # 指定された期間待機してから再試行
      wait_time = 10
      time.sleep(wait_time)
      return save_local_faiss(docs)

if __name__ == "__main__":
    
    # ディレクトリ内のjsonLファイルを取得
    files = glob.glob(f'{WORK_DIR}/**/*.jsonl', recursive=True)

    result = []
    for file in files :
        print(file)
        docs = load_docs_from_jsonl(file)
        result.extend(docs)

    # ベクトルDBに保存
    save_local_faiss(result)