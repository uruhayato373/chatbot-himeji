import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# openAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# proxy設定
# HYOGOドメイン内で実行しない場合はコメントアウト
os.environ["http_proxy"] = st.secrets["PROXY"]
os.environ["https_proxy"] = st.secrets["PROXY"]

# ベクトルDBの指定
VECTORSTORE_DIR = "vectorstore/faiss/kiteisyuu/douro1"


# ベクトルDBの検索結果を踏まえて回答する関数
def run_llm(query,):

    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY )
    
    # load vectorstore
    vectorstore = FAISS.load_local(VECTORSTORE_DIR,embeddings)
    
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
    
    return chain({"question": query, "chat_history": []})

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
    print("回答：", format_answer(results))

if __name__ == "__main__":

    # query = "暫定時の車線運用についてどのようにすべきか？"
    # test(query)

    # query = "道路の横断勾配は標準で何％？"
    # test(query)

    # query = "路面などの流出係数はどこに規定されている？"
    # test(query)

    # query = "排水施設の最小勾配と最大勾配は？"
    # test(query)

    # query = "下水汚泥溶融スラグの使用について教えて"
    # test(query)

    query = "アスファルト舗装の最小厚さは？"
    test(query)