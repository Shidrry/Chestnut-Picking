import pandas as pd
import random
import datetime
import time
import yfinance as yf

from common_func import get_data_from_yfinance, add_moving_averages, calculate_atr, plot_candlestick

url = 'https://raw.githubusercontent.com/Shidrry/Chestnut-Picking/refs/heads/main/nikkei%2B.csv'
nikkei_plus = pd.read_csv(url, header=None, names=['code'])
code_list = nikkei_plus['code'].tolist()

def run_prediction_cycle_prod(code):
    end_date = datetime.datetime.now() + datetime.timedelta(days=1)
    start_date = end_date - datetime.timedelta(days=365)

    data = get_data_from_yfinance(code, start_date, end_date)
    
    trading_value_threshold = 20000*10^6 # 20億以上はほしい
    resent_trading_value = data['Close'].iloc[-1] * data['Volume'].iloc[-1]
    if resent_trading_value <= trading_value_threshold:
        print(f"スキップ {code}: 最近の売買代金が {trading_value_threshold} 以下です。")

    data = add_moving_averages(data)
    atr = calculate_atr(data)  # ATRを計算

    if len(data) > 80:
        data_last_three_months = data.iloc[-80:]  # ランダムに選ばれた期間

        plot_candlestick(data_last_three_months, include_atr=True, atr_series=atr)
        time.sleep(0.5)

        # 最新の終値とATRの表示
        current_close = data_last_three_months['Close'].iloc[-1]
        current_atr = atr.iloc[-1]
        print(f"現在の終値: {current_close:.2f}, 現在のATR値: {current_atr:.2f}")
        
        name = yf.Ticker(code+'.T').info.get('longName')
        print(f"証券コード: {code}, 会社名: {name}")

        print("Enterで次のチャート")
        input()

    else:
        print(f"スキップ {code}: データ不足")

for code in random.sample(nikkei_plus['code'].tolist(), len(nikkei_plus['code'])):
    run_prediction_cycle_prod(code)