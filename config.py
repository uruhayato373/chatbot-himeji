import os

# プロキシ設定
proxy = os.environ.get("PROXY")
if proxy:
    os.environ["http_proxy"] = proxy
    os.environ["https_proxy"] = proxy