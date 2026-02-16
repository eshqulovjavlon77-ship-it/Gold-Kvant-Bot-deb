import requests
import pandas as pd
import pandas_ta as ta
import time

TOKEN = "8521739464:AAHM_ZwfT7wxYGH8hbJ2..." # O'zingizni tokenni qoldiring
CHAT_ID = "6737326135"

def get_data():
    url = "https://api.binance.com/api/3/klines?symbol=BTCUSDT&interval=5m&limit=100"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=['ts', 'o', 'h', 'l', 'c', 'v', 'ct', 'q', 'n', 'tbb', 'tbq', 'i'])
    df['close'] = df['close'].astype(float)
    return df

def check_signal():
    df = get_data()
    df['rsi'] = ta.rsi(df['close'], length=14)
    last_rsi = df['rsi'].iloc[-1]
    
    # Sezgirlik: 30 o'rniga 35, 70 o'rniga 65
    if last_rsi < 35:
        msg = f"🟢 SATIB OLISH (RSI: {last_rsi:.2f})"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")
    elif last_rsi > 65:
        msg = f"🔴 SOTISH (RSI: {last_rsi:.2f})"
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}")

while True:
    try:
        check_signal()
    except:
        pass
    time.sleep(60)
