from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100


def pdf_loader(pdf_file: str):
    """PDFをLangChainのDocumentに変換する関数"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    loader = PyMuPDFLoader(pdf_file)
    docs = loader.load_and_split(text_splitter)

    return docs
