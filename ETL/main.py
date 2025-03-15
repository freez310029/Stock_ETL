import yfinance as yf
import pandas as pd
import configparser
from google.oauth2 import service_account
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import bigquery
from pandas_gbq import to_gbq
from Env import STOCKS


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


# 抓取股票數據
def fetch_stock_data():
    all_data = []
    for stock, stock_id in STOCKS.items():
        try:
            # 嘗試下載股價資料
            data = yf.download(stock, period="1d")  # 只抓取當日資料

            if data.empty:
                print(f"警告: {stock} 無資料")
                continue  # 如果資料為空，跳過這筆數據

            last_row = data.iloc[-1]

            all_data.append({
                "date": last_row.name.strftime("%Y-%m-%d"),
                "stock_id": stock_id,
                "closing_price": last_row["Close"]
            })

        except Exception as e:
            # 捕獲並處理所有可能的異常
            print(f"錯誤: 無法抓取 {stock} 的資料. 錯誤原因: {str(e)}")

        if all_data:
            return pd.DataFrame(all_data)
        else:
            return pd.DataFrame(columns=["date", "stock_id", "closing_price"])


# 上傳到 BigQuery
def upload_to_bigquery(df):
    if df.empty:
        print("No data to upload.")
        return

    try:
        # 嘗試將資料上傳到 BigQuery
        to_gbq(df, destination_table=BQ_TABLE,
               project_id=PROJECT_ID,
               credentials=credentials,
               if_exists="append")  # append 避免覆蓋歷史數據
        print(f"資料成功上傳到 BigQuery: {BQ_TABLE}")

    except DefaultCredentialsError:
        print("錯誤: 無法找到有效的 GCP 認證。請確認您的 GCP 認證配置。")

    except bigquery.exceptions.GoogleCloudError as e:
        # 其他 Google Cloud 相關錯誤
        print(f"錯誤: Google Cloud 錯誤 - {str(e)}")

    except Exception as e:
        # 捕獲所有其他異常
        print(f"錯誤: 無法上傳資料到 BigQuery. 錯誤原因: {str(e)}")


if __name__ == "__main__":
    df = fetch_stock_data()
    print(df)
    upload_to_bigquery(df)
    print("Data uploaded successfully!")
