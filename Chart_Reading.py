import sys
import pandas as pd
import random
import datetime
import time
import yfinance as yf

from common_func import get_data_from_yfinance, add_moving_averages, calculate_atr, plot_candlestick

url = 'https://raw.githubusercontent.com/Shidrry/Chestnut-Picking/refs/heads/main/nikkei%2B.csv'
nikkei_plus = pd.read_csv(url, header=None, names=['code'])
code_list = nikkei_plus['code'].tolist()

def run_prediction_cycle():
    random_stock = random.choice(code_list)
    end_date = datetime.datetime.now() - datetime.timedelta(days=75)
    start_date = end_date - datetime.timedelta(days=5*365 + 100)

    data = get_data_from_yfinance(random_stock, start_date, end_date)
    data = add_moving_averages(data)
    atr = calculate_atr(data)  # ATRを計算

    if len(data) > 125:  # データが120日以上ある場合に実行
        # ランダムな期間を選ぶ
        max_index = len(data) - 25  # 次月のデータ分を確保
        random_start = random.randint(0, max_index - 100)  # 最低100日分確保
        random_end = random_start + 100  # ランダム期間（100日分）

        data_last_three_months = data.iloc[random_start:random_end]  # ランダムに選ばれた期間
        next_month_data = data.iloc[random_end:random_end + 25]  # ランダム選択の次月データ
        combined_data = data.iloc[random_start:random_end + 25]

        plot_candlestick(data_last_three_months, include_atr=True, atr_series=atr)
        time.sleep(0.5)

        # 最新の終値とATRの表示
        current_close = data_last_three_months['Close'].iloc[-1]
        current_atr = atr.iloc[random_end - 1]
        name = yf.Ticker(random_stock+'.T').info.get('longName')
        print(f"現在の終値: {current_close:.2f}, 現在のATR値: {current_atr:.2f}, 証券コード: {random_stock}, 会社名: {name}")

        prediction = input("予想を入力してください: ")

        initial_price = next_month_data['Open'].iloc[0]
        high_price = next_month_data['High'].max()
        low_price = next_month_data['Low'].min()

        # 初期値と高値・安値の差分を表示
        high_diff = high_price - initial_price
        low_diff = initial_price - low_price
        color = 'blue' if low_diff > high_diff else 'red'
        plot_candlestick(combined_data, include_atr=True, atr_series=atr, highlight_start=next_month_data.index[0], highlight_end=next_month_data.index[-1], color=color)
        
        print(f"初期値: {initial_price:.2f}円, 高値: {high_price:.2f}円, 安値: {low_price:.2f}円")
        print(f"高値差分: {high_diff:.2f}円, 安値差分: {low_diff:.2f}円")

        user_feedback = input("結果を受けてのコメントを入力してください: ")

    else:
        print("データ不足")

if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 5

for _ in range(n):
    run_prediction_cycle()