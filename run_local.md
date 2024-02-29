# ローカルPCで起動する方法

## python3.10のインストール

[python公式サイト](https://www.python.org/downloads/windows/)からWindowsインストーラーをダウンロードして実行する。

- [Python 3.10.11 - April 5, 2023 Windows installer (64-bit)](https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe)

インストールする際に、「Add python.exr to PATH」にチェックを入れておくこと。

![pythonインストール画面](img/python_install.PNG)

## VSCodeのインストール

[公式サイト](https://code.visualstudio.com/download)からWindows版をダウンロードして実行。

日本語化については[この記事](https://www.javadrive.jp/vscode/install/index4.html)を参照。

拡張機能（extention）もインストールしておく

- python
- Pylance

## proxy環境の確認

「スタートメニュー」＞「設定」＞「ネットワークとインターネット」＞「プロキシ」をクリック。

プロキシ設定の画面内に「スクリプトのアドレス」があるので、そのアドレスをコピーしてブラウザに張り付けると、proxypacのファイルがダウンロードされる。

![スクリプトのアドレス](img/proxy_01.PNG)

メモ帳でファイルを開き、最下段に記載されているIPアドレスとポート番号を確認

```
return "PROXY 202.221.175.116:3128 ; PROXY 210.130.236.140:3128";
```

この場合、IPアドレスは「202.221.175.116」、ポート番号が「3128」

IPアドレスはおそらく２種類記載されているが、どちらか一方でよい。

## pipの設定

pythonのパッケージ管理ツール「pip」は、python3.10をインストールすれば自動的にインストールされるが、HYOGOドメインに参加しているPC（つまり職場PC）で利用するためには、SSLの設定とプロキシ設定が必要。

### フォルダオプションの設定変更

エクスプローラーを起動し、「表示」＞「オプション」をクリックするとフォルダーオプションが起動するので、「表示」タブを開いて、下記の設定をしてから「OK」で保存。

1. 『隠しファイル、隠しフォルダー、および隠しドライブを表示する』を選択。
2. 『登録されている拡張子は表示しない』のチェックを外す。

### pip.iniファイルの作成

下記の場所にpip.iniファイルを作成する。m000000は職員番号。AppDataは隠しフォルダなので薄く表示される。

おそらくRomingフォルダまでは存在するので、その下にpipフォルダを作成する。

```
“C:\Users\m000000\AppData\Roaming\pip\pip.ini”
```

pip.iniファイルは、pipフォルダ内で「右クリック」＞「新規作成」＞「テキストドキュメント」を開き、ファイル名をpip.iniに変更して保存。

※基本的なことだが、フォルダオプションで拡張子を表示する設定にしていないと、pip.iniは作成できない。（pip.ini.txtになってしまう）

pip.iniに下記を張り付ける。

```bash
[global]
trusted-host = pypi.python.org
               pypi.org
               files.pythonhosted.org
proxy = http://<ユーザー名>:<パスワード>@<IPアドレス>:<ポート番号>
```
trusted-hostは信頼済みサイトを登録する。このままコピペでよい。

proxyは各PCやユーザ情報を登録する。

例えば

- 職員番号「m000000」
- パスワード「password」
- IPアドレス「202.221.175.116」
- ポート番号が「3128」

の場合は、下記のとおりとなる。

```bash
proxy = http://m000000:password@202.221.175.116:3128
```

なお、ここでいうパスワードは、HYOGOドメイン（職場PC）にログインする際のパスワードを指す。

参考サイト
- https://qiita.com/kekosh/items/e96e822bf9cb6ca1aff8
- https://zero-cheese.com/10710/


# ローカル環境での実行

## リポジトリのクローン

コマンドプロンプトで下記を実行

```
git clone https://github.com/dicechick373/chatbot-himeji.git
```

VSCodeを起動して、「フォルダを開く」でフォルダを開く。

## ライブラリのインストール

アプリに必要なライブラリをインストールする

```python
pip install -r requirements.txt
```


## 環境変数の設定

プロジェクト直下に.streamlit/secrets.tomlを作成

```toml
OPENAI_API_KEY=''
PROXY='http://<ユーザー名>:<パスワード>@<IPアドレス>:<ポート番号>'

```

## streamlitの起動

VSCode内のターミナルで下記を実行

```bash
streamlit run Home.py
```

# PDFの読込等

下記参照

[道路Ⅰ編](https://github.com/dicechick373/chatbot-himeji/blob/main/static/%E5%9C%9F%E6%9C%A8%E6%8A%80%E8%A1%93%E7%AE%A1%E7%90%86%E8%A6%8F%E7%A8%8B%E9%9B%86/%E9%81%93%E8%B7%AF%EF%BC%91%E7%B7%A8/README.md)

