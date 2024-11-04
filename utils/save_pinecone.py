import streamlit as st
import copy

from langchain_community.vectorstores import PineconeStore
from langchain_openai import OpenAIEmbeddings  # 新しいインポート方法
from pinecone import Pinecone, PodSpec

# OpenAIとPineconeのAPIキーを設定
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]

# インデックス名の設定
PINECONE_INDEX_NAME = "doboku"


def format_docs(org_docs, page_prefix: int):
    """Documentのmetadataを加工する関数"""
    docs = copy.deepcopy(org_docs)
    for doc in docs:
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs


def save_to_pinecone(docs):
    """DocumentをPineconeに保存する関数"""
    # Pineconeクライアントの初期化
    pc = Pinecone(api_key=PINECONE_API_KEY)

    # インデックスが存在しない場合は作成
    if PINECONE_INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=PINECONE_INDEX_NAME,
            dimension=1536,  # OpenAI embeddings の次元数
            metric="cosine",
            spec=PodSpec(environment="gcp-starter"),
        )

    # Embeddingsの設定
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

    # インデックスを取得
    index = pc.Index(PINECONE_INDEX_NAME)

    # PineconeStoreを使用してドキュメントを保存
    vectorstore = PineconeStore.from_documents(
        docs,
        embeddings,
        index_name=PINECONE_INDEX_NAME,
        pinecone_api_key=PINECONE_API_KEY,
    )

    print(f"{len(docs)}個のドキュメントをPineconeに保存しました。")
    return vectorstore


if __name__ == "__main__":
    # ディレクトリ内のPDFを単一のリストに格納
    result = []

    pdf_file = "static/土木技術管理規程集/道路１編/第１章_道路一般.pdf"

    docs = pdf_loader(pdf_file)
    result.extend(docs)

    # Pineconeに保存
    save_to_pinecone(result)
