import schedule
import time
import datetime
import yfinance as yf
import pymssql

def job():
    now = datetime.datetime.now()
    current_time = now.time()
    start = datetime.time(9, 30)
    end = datetime.time(14, 0)

    if start <= current_time <= end:
        ticker = yf.Ticker("2330.TW")
        df = ticker.history(period="1d", interval="15m")
        if not df.empty:
            latest = df.iloc[-1]
            trade_date = now.date().strftime("%Y-%m-%d")
            trade_time = now.strftime("%H:%M")   # 加上小時和分鐘
            open_price = float(latest["Open"])
            high_price = float(latest["High"])
            low_price = float(latest["Low"])
            close_price = float(latest["Close"])
            volume = int(latest["Volume"])

            connect = pymssql.connect("ericdb01.database.windows.net","ericsa","Giball100","free-sql-db-4608316")
            cursor = connect.cursor()
            cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tsmc_stock' AND xtype='U')
            CREATE TABLE dbo.tsmc_stock (
                trade_date DATE,
                trade_time VARCHAR(5),   -- 新增時間欄位
                open_price FLOAT,
                high_price FLOAT,
                low_price FLOAT,
                close_price FLOAT,
                volume BIGINT
            )
            """)
            connect.commit()

            cursor.execute("""
            INSERT INTO dbo.tsmc_stock(trade_date, trade_time, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (trade_date, trade_time, open_price, high_price, low_price, close_price, volume))
            connect.commit()
            cursor.close()
            connect.close()
            print(f"{trade_date} {trade_time} 已寫入: 開 {open_price}, 高 {high_price}, 低 {low_price}, 收 {close_price}, 量 {volume}")

        # 如果已經到下午 14:00，就結束程式
        if current_time >= end:
            print("已到下午兩點，抓取完成，程式結束。")
            exit(0)

# 每 15 分鐘執行一次
schedule.every(15).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
