import copy


def format_docs(org_docs, page_prefix: int):
    """Documentのmetadataを加工する関数"""
    docs = copy.deepcopy(org_docs)
    for doc in docs:
        # sourceを「土木技術管理規程集_道路１編」のフォーマットに修正
        source = doc.metadata["source"].split("/")
        new_source = source[1] + "_" + source[2].split("\\")[0]
        doc.metadata.update({"source": new_source})

        # ページ番号を「1-1」のフォーマットに修正
        new_page = f'{str(page_prefix)}-{str(doc.metadata["page"]+1)}'
        doc.metadata.update({"page": new_page})

    return docs
