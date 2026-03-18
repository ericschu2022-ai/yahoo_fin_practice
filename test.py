import pymssql
import yfinance as yf
import datetime

print("模組已成功匯入")

# 資料庫連線設定
server = "ericdb01.database.windows.net"
user = "ericsa"
password = "Giball100"
database = "free-sql-db-4608316"

# 建立 table 的 SQL (只需執行一次)
CREATE_TABLE_SQL = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tsmc_stock' AND xtype='U')
CREATE TABLE dbo.tsmc_stock (
    trade_date DATE,
    trade_time VARCHAR(5),   -- 新增時間欄位
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT
)
"""

# 插入資料的 SQL
INS_SQL = """
INSERT INTO dbo.tsmc_stock(trade_date, trade_time, open_price, high_price, low_price, close_price)
VALUES (%s, %s, %s, %s, %s, %s)
"""

try:
    connect = pymssql.connect(server, user, password, database)
    cursor = connect.cursor()

    # 建立 table
    cursor.execute(CREATE_TABLE_SQL)
    connect.commit()

    # 使用 yfinance 抓取 TSMC 當日股價
    ticker = yf.Ticker("2330.TW")  # TSMC 在 Yahoo Finance 的代碼
    today = datetime.date.today().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M")  # 取得當下時間
    df = ticker.history(period="1d")

    if not df.empty:
        open_price = float(df["Open"].iloc[0])
        high_price = float(df["High"].iloc[0])
        low_price = float(df["Low"].iloc[0])
        close_price = float(df["Close"].iloc[0])

        # 寫入資料庫
        cursor.execute(INS_SQL, (today, current_time, open_price, high_price, low_price, close_price))
        connect.commit()
        print(f"已寫入 {today} {current_time} TSMC 股價: 開 {open_price}, 高 {high_price}, 低 {low_price}, 收 {close_price}")
    else:
        print("今日尚無交易資料")

    cursor.close()
    connect.close()

except Exception as e:
    print(f"連線失敗: 原因 {e}")
