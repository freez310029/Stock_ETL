# Stock_ETL

## 專案介紹

`Stock_ETL` 是一個自動化的 ETL (Extract, Transform, Load) 專案，專門用來抓取台灣股市的股票數據，並將其儲存到 GCP (Google Cloud Platform) 的 BigQuery 中。該專案通過 Docker 容器化，並將其部署到 GKE (Google Kubernetes Engine)，使用 CronJob 定期執行 ETL 任務，實現數據的自動化處理和上傳。

## 專案流程

1. **ETL 流程 (ETL/main.py)**：
   - 使用 Python 編寫的爬蟲程式，從 Yahoo Finance 等來源抓取台灣股市的每日收盤價 (ETL/get_data.py)。
   - 使用 Google Cloud BigQuery 儲存抓取的股市數據。
   - 每天定時抓取數據並進行處理，並將結果儲存於 BigQuery (ETL/upload.py)。
   - 可在Env.py中新增標的。

2. **Docker 建置與部署 (Dockerfile, dep.sh)**：
   - 使用 Docker 打包爬蟲程式，使其可以輕鬆部署和運行於 GCP。
   - 使用 `docker build`、`docker tag`、`docker push` 命令將容器上傳到 GCP 的 Container Registry。

3. **GKE 排程任務 (gke/cronjob.yaml)**：
   - 使用 GKE 配置 CronJob，自動化運行 ETL 任務，抓取股市數據並將其推送到 BigQuery。
   - 每天定時執行 ETL 任務。

4. **私鑰管理**：
   - 使用本地儲存的 Google Cloud 私鑰來進行身份驗證，並安全地將數據上傳至 GCP。

