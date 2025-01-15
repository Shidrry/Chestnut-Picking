import pandas as pd
import random
import datetime
import time

from common_func import get_data_from_yfinance, add_moving_averages, calculate_atr, plot_candlestick

url = 'https://raw.githubusercontent.com/Shidrry/Chestnut-Picking/refs/heads/main/nikkei%2B.csv'
nikkei_plus = pd.read_csv(url, header=None, names=['code'])
code_list = nikkei_plus['code'].tolist()

def run_prediction_cycle_prod(code):
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=365)

    data = get_data_from_yfinance(code, start_date, end_date)
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
        
        print(f"証券コード: {code}")

        print("Enterで次のチャート")
        input()

    else:
        print("データ不足")

for code in random.shuffle(nikkei_plus['code'].tolist()):
    run_prediction_cycle_prod(code)