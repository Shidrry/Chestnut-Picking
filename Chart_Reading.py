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
    end_date = datetime.datetime.now() - datetime.timedelta(days=60)
    start_date = end_date - datetime.timedelta(days=5*365 + 100)

    data = get_data_from_yfinance(random_stock, start_date, end_date)
    data = add_moving_averages(data)
    atr = calculate_atr(data)  # ATRを計算

    if len(data) > 120:  # データが120日以上ある場合に実行
        # ランダムな期間を選ぶ
        max_index = len(data) - 20  # 次月のデータ分を確保
        random_start = random.randint(0, max_index - 100)  # 最低100日分確保
        random_end = random_start + 80  # ランダム期間（80日分）

        data_last_three_months = data.iloc[random_start:random_end]  # ランダムに選ばれた期間
        next_month_data = data.iloc[random_end:random_end + 20]  # ランダム選択の次月データ
        combined_data = data.iloc[random_start:random_end + 20]

        plot_candlestick(data_last_three_months, include_atr=True, atr_series=atr)
        time.sleep(0.5)

        # 最新の終値とATRの表示
        current_close = data_last_three_months['Close'].iloc[-1]
        current_atr = atr.iloc[random_end - 1]
        name = yf.Ticker(code+'.T').info.get('longName')
        print(f"現在の終値: {current_close:.2f}, 現在のATR値: {current_atr:.2f}, 会社名: {name}")

        print("Enterもしくはラベル入力で正解表示")
        answer = input()

        initial_price = next_month_data['Open'].iloc[0]
        high_price = next_month_data['High'].max()
        low_price = next_month_data['Low'].min()

        # 初期値と高値・安値の差分を表示
        high_diff = high_price - initial_price
        low_diff = initial_price - low_price
        color = 'blue' if low_diff > high_diff else 'red'
        plot_candlestick(combined_data, include_atr=True, atr_series=atr, highlight_start=next_month_data.index[0], highlight_end=next_month_data.index[-1], color=color)
        
        print(f"証券コード: {random_stock}")
        print(f"初期値: {initial_price:.2f}円, 高値: {high_price:.2f}円, 安値: {low_price:.2f}円")
        print(f"高値差分: {high_diff:.2f}円, 安値差分: {low_diff:.2f}円, 閾値: {current_atr * 1.5:.2f}円")

        print("正解のラベル")
        correct = input()
        
        if answer != '' and correct != '':
            score = 1 if answer == correct else 0
            return score, False
        else:
            return None, True

    else:
        print("データ不足")
        return None, False

if len(sys.argv) > 1:
    n = int(sys.argv[1])
else:
    n = 5

scores = []
skips = 0
for _ in range(n):
    result, skip = run_prediction_cycle()
    if result is not None:
        scores.append(result)
    if skip:
        skips += 1

if scores:
    correct_answers = scores.count(1)
    incorrect_answers = scores.count(0)
    accuracy = correct_answers / len(scores) * 100
    print(f"総回答数: {len(scores)}, 正解: {correct_answers}, 誤答: {incorrect_answers}, 正答率: {accuracy:.2f}%, スキップ数: {skips}")
else:
    print("有効なスコアがありません。")