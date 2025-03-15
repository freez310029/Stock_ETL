FROM python:3.9

# 設定工作目錄
WORKDIR /

# 複製專案檔案到容器內
COPY ..

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "ETL/main.py"]
