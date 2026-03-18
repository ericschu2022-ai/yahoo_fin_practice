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
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='tsmc_history' AND xtype='U')
CREATE TABLE dbo.tsmc_history (
    trade_date DATE,
    open_price FLOAT,
    high_price FLOAT,
    low_price FLOAT,
    close_price FLOAT,
    volume BIGINT,
    dividend FLOAT NULL
)
"""

# 插入資料的 SQL
INS_SQL = """
INSERT INTO dbo.tsmc_history(trade_date, open_price, high_price, low_price, close_price, volume, dividend)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

try:
    connect = pymssql.connect(server, user, password, database)
    cursor = connect.cursor()

    # 建立 table
    cursor.execute(CREATE_TABLE_SQL)
    connect.commit()

    # 使用 yfinance 抓取 TSMC 從 2025-01-01 到今天的股價
    start_date = "2025-01-01"
    # ✅ end_date 設成今天 +1 天，確保包含今天
    end_date = (datetime.date.today() + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    ticker = yf.Ticker("2330.TW")
    df = ticker.history(start=start_date, end=end_date)

    # 抓取除息資訊
    dividends = ticker.dividends

    if not df.empty:
        for idx, row in df.iterrows():
            trade_date = idx.strftime("%Y-%m-%d")   # ✅ 轉成字串
            open_price = float(row["Open"])
            high_price = float(row["High"])
            low_price = float(row["Low"])
            close_price = float(row["Close"])
            volume = int(row["Volume"])

            # 檢查當日是否有除息紀錄
            dividend = None
            if idx in dividends.index:
                dividend = float(dividends.loc[idx])

            # 寫入資料庫
            cursor.execute(INS_SQL, (trade_date, open_price, high_price, low_price, close_price, volume, dividend))

        connect.commit()
        print(f"✅ 已成功寫入 TSMC 從 {start_date} 到 {end_date} 的股價與除息資料，共 {len(df)} 筆")
    else:
        print("查無股價資料")

    cursor.close()
    connect.close()

except Exception as e:
    print(f"連線失敗: 原因 {e}")
