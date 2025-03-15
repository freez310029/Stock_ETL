import yfinance as yf
import pandas as pd
from Env import STOCKS


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


if __name__ == "__main__":
    df = fetch_stock_data()
    print(df)
    print("Data uploaded successfully!")
