from google.auth.exceptions import DefaultCredentialsError
from google.cloud import bigquery
from pandas_gbq import to_gbq
from get_data import fetch_stock_data


# 上傳到 BigQuery
def upload_to_bigquery(df, table_name, project_id, credentials):
    if df.empty:
        print("No data to upload.")
        return

    try:
        # 嘗試將資料上傳到 BigQuery
        to_gbq(df, destination_table=table_name,
               project_id=project_id,
               credentials=credentials,
               if_exists="append")  # append 避免覆蓋歷史數據
        print(f"資料成功上傳到 BigQuery: {table_name}")

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