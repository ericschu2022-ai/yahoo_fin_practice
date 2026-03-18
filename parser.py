import yfinance as yf
import mplfinance as mpf

def stock_info(id):
    tick = yf.Ticker(id)
    info = tick.fast_info
    print(f'最高價 {info.get("dayHigh")}')
    print(f'最低價 {info.get("dayLow")}')
    print(f'最新價 {info.get("lastPrice")}')
    print(f'開盤價 {info.get("open")}')
    print(f'前一日收盤價 {info.get("previousClose")}')

stock_info("2330.TW")
stock_info("2345.TW")

import yfinance as yf; tick = yf.Ticker('2330.TW'); print(dir(tick.fast_info))
