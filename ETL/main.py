import configparser
from google.oauth2 import service_account
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import bigquery
from pandas_gbq import to_gbq
from get_data import fetch_stock_data
from upload import upload_to_bigquery

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


if __name__ == "__main__":
    df = fetch_stock_data()
    upload_to_bigquery(df,
                       table_name=BQ_TABLE,
                       project_id=PROJECT_ID,
                       credentials=credentials)
    print("Data uploaded successfully!")

