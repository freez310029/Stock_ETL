# Stock_ETL

## 專案介紹

`Stock_ETL` 是一個自動化的 ETL (Extract, Transform, Load) 專案，專門用來抓取台灣股市的股票數據，並將其儲存到 GCP (Google Cloud Platform) 的 BigQuery 中。該專案通過 Docker 容器化，並將其部署到 GKE (Google Kubernetes Engine)，使用 CronJob 定期執行 ETL 任務，實現數據的自動化處理和上傳。

## 專案流程

1. **ETL 流程**：
   - 使用 Python 編寫的爬蟲程式，從 Yahoo Finance 等來源抓取台灣股市的每日收盤價（例如 2330 和 0050 兩檔股票）。
   - 使用 Google Cloud BigQuery 儲存抓取的股市數據。
   - 每天定時抓取數據並進行處理，並將結果儲存於 BigQuery。

2. **Docker 容器化**：
   - 使用 Docker 打包爬蟲程式，使其可以輕鬆部署和運行於 GCP。
   - 使用 `docker build`、`docker tag`、`docker push` 命令將容器上傳到 GCP 的 Container Registry。

3. **自動化 CronJob**：
   - 使用 GKE 配置 CronJob，自動化運行 ETL 任務，抓取股市數據並將其推送到 BigQuery。
   - 每天定時執行 ETL 任務。

4. **私鑰管理**：
   - 使用本地儲存的 Google Cloud 私鑰來進行身份驗證，並安全地將數據上傳至 GCP。

## 環境要求

- Python 3.9+
- Docker
- Google Cloud Platform (GCP) 帳戶
- GKE (Google Kubernetes Engine)
- BigQuery

## 安裝步驟

1. **安裝必要套件**

   在專案根目錄下執行以下命令，安裝所需的 Python 套件：

   ```bash
   pip install -r requirements.txt
