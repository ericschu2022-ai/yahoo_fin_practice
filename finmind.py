"""
透過 FinMind 擷取台灣股市資料
"""
from FinMind.data import DataLoader

dl = DataLoader()
#dl.login_by_token()  註冊會員的登入動作
# 回傳 pandas 的 dataframe 格式資料
df = dl.taiwan_stock_daily(stock_id="2330", start_date="2026-03-17", end_date="2026-03-19")
print(df)