import yfinance as yf
import pandas as pd
import configparser
from google.oauth2 import service_account
from pandas_gbq import to_gbq

# 讀取 config.ini
config = configparser.ConfigParser()
config.read("core/config.ini", encoding="utf-8")

# 設定 GCP 認證
CREDENTIALS_PATH = config["google_cloud"]["credentials_path"]
PROJECT_ID = config["google_cloud"]["project_id"]
DATASET_ID = config["bigquery"]["dataset_id"]
TABLE_ID = config["bigquery"]["table_id"]

BQ_TABLE = f"{DATASET_ID}.{TABLE_ID}"  # pandas-gbq 格式
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)

# 定義爬取股票代碼
STOCKS = {
    "2330.TW": "2330",
    "0050.TW": "0050"
}


# 抓取股票數據
def fetch_stock_data():
    all_data = []
    for stock, stock_id in STOCKS.items():
        data = yf.download(stock, period="1d")  # 只抓取當日資料
        if not data.empty:
            last_row = data.iloc[-1]
            all_data.append({
                "date": last_row.name.strftime("%Y-%m-%d"),
                "stock_id": stock_id,
                "closing_price": last_row["Close"]
            })

    return pd.DataFrame(all_data)


# 上傳到 BigQuery
def upload_to_bigquery(df):
    if df.empty:
        print("No data to upload.")
        return

    to_gbq(df, destination_table=BQ_TABLE,
           project_id=PROJECT_ID,
           credentials=credentials,
           if_exists="append")  # append 避免覆蓋歷史數據


if __name__ == "__main__":
    df = fetch_stock_data()
    print(df)
    upload_to_bigquery(df)
    print("Data uploaded successfully!")
