import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from  langchain.schema import Document
import json
from typing import Iterable
import glob

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# vectorstoreを保存するディレクトリの設定
# 日本語のディレクトリ名はエラーになる
VECTORSTORE_DIR = "vectorstore/faiss"

# LangchainのDocumentクラスを保存したjsonLファイルを読み込む関数
def load_docs_from_jsonl(file_path)->Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

# LangchainのDocumentクラスを保存したjsonLファイルを読み込む関数
def load_docs_from_jsonl(file_path)->Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

if __name__ == "__main__":
    
    # ディレクトリ内のjsonLファイルを取得
    files = glob.glob(f'documents/**/*.jsonl', recursive=True)

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY )

    # 最初のdbを作成
    first_doc = load_docs_from_jsonl(files[0])
    db = FAISS.from_documents(first_doc, embeddings)

    del files[0]
    for file in files :

        docs = load_docs_from_jsonl(file)
        db.merge_from(FAISS.from_documents(docs, embeddings))
        
    # ローカルに保存
    db.save_local(VECTORSTORE_DIR)
    print(f'{len(docs)}個のドキュメントを{VECTORSTORE_DIR}に保存しました。')
