import openai
import streamlit as st
from typing import Any, Dict, List
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI

# OpenAIのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]


def run_llm(query, vectordir, chat_history: List[Dict[str, Any]] = []):
    # set embeddings
    embeddings = OpenAIEmbeddings(openai_api_key=openai.api_key)

    # load vectorstore
    vectorstore = FAISS.load_local(vectordir, embeddings)

    # set chat-model
    chat = ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        verbose=True,
        temperature=0,
        model_name="gpt-3.5-turbo-0613",
    )

    # set chain
    chain = ConversationalRetrievalChain.from_llm(
        llm=chat, retriever=vectorstore.as_retriever(), return_source_documents=True
    )

    response = chain({"question": query, "chat_history": chat_history})

    return {"question": response["question"], "answer": format_answer(response)}

    # return chain({"question": query, "chat_history": []})


def format_answer(response):
    sources = []
    for r in response["source_documents"]:
        source = r.metadata["source"]
        page = r.metadata["page"]
        sources.append(source + "P:" + page)

    return f"{response['answer']} \n\n 出典:{sources}"
