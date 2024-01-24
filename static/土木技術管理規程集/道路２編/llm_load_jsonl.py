import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from  langchain.schema import Document
import json
from typing import Iterable

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# LangChainのDocumentクラスを保存したファイル名の設定
DOCUMENT_PATH = "documents/土木技術管理規程集/道路２編.jsonl"

# LangchainのDocumentクラスを保存したjsonLファイルを読み込む関数
def load_docs_from_jsonl(file_path)->Iterable[Document]:
    array = []
    with open(file_path, 'r') as jsonl_file:
        for line in jsonl_file:
            data = json.loads(line)
            obj = Document(**data)
            array.append(obj)
    return array

# ベクトルDBの検索結果を踏まえて回答する関数
def run_llm(query, chat_history = []):

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY )
    
    # load jsonL
    docs = load_docs_from_jsonl(DOCUMENT_PATH)

    # load vectorstore
    vectorstore = FAISS.from_documents(docs, embeddings)

    # set chat-model
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY ,
        verbose=True,
        temperature=0,
        model_name="gpt-3.5-turbo-0613"
    )

    # set chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat,
        retriever=vectorstore.as_retriever(), 
        return_source_documents=True)
    
    return chain({"question": query, "chat_history": chat_history})

# 回答に出典を付与する関数
def format_answer(response):
    sources = []
    for r in response["source_documents"]:
        source = r.metadata["source"]
        page = r.metadata["page"]
        sources.append(source + 'P:'+ page)
    
    return  f"{response['answer']} \n\n 出典「{sources}」"


# 出力テスト
def test(query):
    results = run_llm(query,[])
    print("質問：", results["question"])
    print("質問：", format_answer(results))

if __name__ == "__main__":

    query = "歩道乗入れ部の勾配は何％にすべきか？"
    test(query)