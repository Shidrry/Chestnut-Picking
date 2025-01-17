import pandas as pd
import numpy as np
import yfinance as yf
import mplfinance as mpf

def get_data_from_yfinance(ticker, start_date, end_date):
    data = yf.download(ticker+'.T', start=start_date, end=end_date, progress=False)
    data.columns = data.columns.get_level_values(0)
    data = data[['Open', 'High', 'Low', 'Close', 'Volume']]  # 必要な列を選択
    return data

def calculate_atr(data, period=14):
    high_low = data['High'] - data['Low']
    high_close = np.abs(data['High'] - data['Close'].shift())
    low_close = np.abs(data['Low'] - data['Close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = np.max(ranges, axis=1)
    atr = true_range.rolling(window=period).mean()
    return atr

def add_moving_averages(data):
    data['MA5'] = data['Close'].rolling(window=5).mean()
    data['MA25'] = data['Close'].rolling(window=25).mean()
    data['MA75'] = data['Close'].rolling(window=75).mean()
    return data

def plot_candlestick(data, include_atr=False, atr_series=None, highlight_start=None, highlight_end=None, color=None):
    apds = []
    if include_atr and atr_series is not None:
        atr_plot = atr_series.loc[data.index]  # ATRデータの範囲を調整
        apds.append(mpf.make_addplot(atr_plot, type='line', color='fuchsia', ylabel='ATR', linestyle='-', width=0.75))

    # 移動平均線の追加
    apds.append(mpf.make_addplot(data['MA5'], color='yellow', linestyle='solid', width=0.75))
    apds.append(mpf.make_addplot(data['MA25'], color='orange', linestyle='solid', width=0.75))
    apds.append(mpf.make_addplot(data['MA75'], color='green', linestyle='solid', width=0.75))

    if highlight_start and highlight_end and color:
        where_values = (data.index >= highlight_start) & (data.index <= highlight_end)
        y1_value = data['High'].max()
        y2_value = data['Low'].min()
        kwargs = {'fill_between': dict(y1=y1_value, y2=y2_value, where=where_values, color=color, alpha=0.3)}
    else:
        kwargs = {}

    # 日付フォーマットを設定
    datetime_format = '%Y%m%d'

    # プロット実行
    marketcolors = mpf.make_marketcolors(
        up='#DC143C', # 上昇時のろうそくの塗りつぶし色
        down='#00BFFF', # 下降時のろうそくの塗りつぶし色
        edge='black',
        wick={
            # 辞書形式で、ろうそく足の真の色を指定
            'up':'#DC143C', # 上昇時のろうそくの芯の色
            'down':'#00BFFF' # 下降時のろうそくの芯の色
        }
    )
    my_style = mpf.make_mpf_style(
        marketcolors=marketcolors,
        gridcolor='gray',
        facecolor='black', # チャートの背景の色
        edgecolor='gray', # チャートの外枠の色
        figcolor='black', # チャートの外側の色
        gridstyle='-.', # チャートのグリッドの種類 "--":実線, "--":破線, ":":点線, "-.":破線と点線の組み合わせ
        gridaxis='both',
        rc = {
            'xtick.color': 'white', # X軸の色
            'xtick.labelsize': 8, # X軸の文字サイズ
            'ytick.color': 'white', # Y軸の色
            'ytick.labelsize': 8, # Y軸の文字サイズ
            'axes.labelsize': 10, # 軸ラベルの文字サイズ
            'axes.labelcolor': 'white', # 軸ラベルの色
        }
    )
    mpf.plot(data, type='candle', figscale=1.5, figratio=(20, 10), style=my_style, volume=True, addplot=apds, datetime_format=datetime_format, show_nontrading=False, **kwargs)