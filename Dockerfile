# ベースイメージを指定
FROM python:3

# 環境変数を設定
ENV PYTHONUNBUFFERED 1

# 作業ディレクトリを作成
RUN mkdir /code

# 作業ディレクトリを設定
WORKDIR /code

# エイリアスファイルをコピーして設定
COPY ./.alias /root
RUN cat /root/.alias >> /root/.bashrc

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y cron

# プロジェクトの依存関係をコピーしてインストール
COPY requirements.txt /code/
RUN pip install --upgrade pip && pip install -r requirements.txt

# プロジェクトのソースコードをコピー
COPY . /code/

# cronジョブの設定ファイルをコピー
COPY mycron /etc/cron.d/mycron

# cronジョブのファイルに実行権限を付与
RUN chmod 0644 /etc/cron.d/mycron

# cronジョブを登録
RUN crontab /etc/cron.d/mycron

# cronサービスを起動し、Djangoアプリケーションを起動
CMD service cron start
