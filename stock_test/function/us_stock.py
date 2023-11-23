import yfinance as yf
import os
import time
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from function.translations import translation_dict

def get_intraDay_data_today(stock_symbol='AAPL'):
    """
    取得特定股票的今日盤中資料。

    Parameters:
    - stock_symbol (str): 股票代碼。預設值為 'AAPL'。

    Returns:
    - DataFrame: 包含盤中資料的 Pandas DataFrame。
    """
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, interval='1m')
    return stock_data

def get_intraDay_data_7day(stock_symbol='AAPL'):
    """
    取得特定股票的過去 7 天盤中資料。

    Parameters:
    - stock_symbol (str): 股票代碼。預設值為 'AAPL'。

    Returns:
    - DataFrame: 包含盤中資料的 Pandas DataFrame。
    """
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, interval='1m')
    return stock_data

def get_intraDay_data_6month(stock_symbol='AAPL'):
    """
    取得特定股票的過去 6 個月盤中資料。

    Parameters:
    - stock_symbol (str): 股票代碼。預設值為 'AAPL'。

    Returns:
    - DataFrame: 包含盤中資料的 Pandas DataFrame。
    """
    end_date = datetime.today().strftime('%Y-%m-%d')
    start_date = (datetime.today() - timedelta(days=180)).strftime('%Y-%m-%d')
    stock_data = yf.download(stock_symbol, start=start_date, end=end_date, interval='1m')
    return stock_data

def download_stock_data(stk_list):
    """
    下載一組股票的價量資料，並儲存在以當天日期為名的資料夾中。

    Parameters:
    - stk_list (list): 包含股票代碼的列表。

    Returns:
    - list: 失敗的股票代碼列表。
    """
    # 創立一個紀錄失敗股票的 list
    failed_list = []
    today_date = datetime.today().strftime('%Y%m%d')
    base_folder = os.path.join(os.getcwd(),'Data', today_date)
    os.makedirs(base_folder, exist_ok=True)

    # 開始迴圈抓資料囉！
    for i in stk_list:
        try: 
            # 打印出目前進度
            print('抓取資料: ' + i)
            # 填入股票代碼後直接下載成 csv 格式
            stock = yf.Ticker(i)
            stock_data = stock.history(period='max')
            
            # 修改日期格式
            stock_data.index = stock_data.index.strftime('%Y-%m-%d')
            
            file_path = os.path.join(base_folder, f'日成交資料_{i}.csv')
            stock_data.to_csv(file_path)
            
            # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
            time.sleep(1)
        except:
            failed_list.append(i)
            continue
    
    return failed_list

def download_financial_data(stk_list):
    """
    下載一組股票的損益表、資產負債表、現金流量表。

    Parameters:
    - stk_list (list): 包含股票代碼的列表。
    
    Returns:
    - failed_list (list): 下載失敗的股票列表。
    """

    # 創建一個紀錄失敗股票的 list
    failed_list = []

    # 創建以今天日期為名的資料夾，如果不存在的話
    base_folder = os.path.join(os.getcwd(),'Data', '財報資料')

    os.makedirs(base_folder, exist_ok=True)

    # 開始迴圈抓資料囉！
    for i in stk_list:
        try:
            # 打印出目前進度
            print('processing: ' + i)

            # 創建股票名稱的資料夾，如果不存在的話
            stock_folder = os.path.join(base_folder, i)
            os.makedirs(stock_folder, exist_ok=True)

            # 填入股票代碼後直接下載損益表、資產負債表和現金流量表成 CSV 格式
            stock = yf.Ticker(i)
            stock.financials.to_csv(os.path.join(stock_folder, f'損益表.csv'))
            stock.balance_sheet.to_csv(os.path.join(stock_folder, f'資產負債表.csv'))
            stock.cashflow.to_csv(os.path.join(stock_folder, f'現金流量表.csv'))

            # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
            time.sleep(1)
        except Exception as e:
            print(f"Failed to process {i}: {e}")
            failed_list.append(i)
            continue
    
    return failed_list

def plot_stock_chart(stock_symbol='AAPL', days=90):
    """
    繪製股票走勢圖。

    Parameters:
    - stock_code (str): 股票代碼。
    - days (int): 要顯示的天數，預設為 90 天。
    """
    try:
        # 讀取 CSV 時指定 'DATE' 欄位為索引並轉換為 DatetimeIndex
        file_path = f'./Data/20231123/日成交資料_{stock_symbol}.csv'
        df = pd.read_csv(file_path, index_col='Date', parse_dates=True)
        df = df.drop(['Dividends', 'Stock Splits'], axis=1)

        # 檢查資料是否足夠長
        if len(df) < days:
            raise ValueError(f"股票 {stock_code} 的歷史資料不足 {days} 天")

        # 選擇最近的指定天數資料
        df_last_days = df.iloc[-days:]

        print(df_last_days)

        # 圖表參數
        mc = mpf.make_marketcolors(up='r', down='g', inherit=True)
        s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)
        kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, figratio=(10, 8), figscale=0.75,figsize=(23, 8), title=stock_symbol, style=s)

        # 繪製股票走勢圖
        mpf.plot(df_last_days, **kwargs)
        plt.show()
    except FileNotFoundError:
        print(f"找不到股票 {stock_symbol} 的檔案")
    except Exception as e:
        print(f"繪製股票 {stock_symbol} 時發生錯誤: {str(e)}")

def translate_and_save(csv_path='/', output_suffix='_tw'):

    """
    翻譯 CSV 文件的第一列並保存。

    Parameters:
    - csv_path (str): 要翻譯的 CSV 文件路径。
    - output_path (str): 輸出 CSV 文件的路径後綴。

    Returns:
    - None
    """

    # 讀取 CSV 文件
    df = pd.read_csv(csv_path)
    # 修改所有行的第一列
    df.iloc[:, 0] = df.iloc[:, 0].map(translation_dict.get)

    # 將修改後的 DataFrame 寫入 CSV 文件
    base_path, file_name = os.path.split(csv_path)
    file_name, extension = os.path.splitext(file_name)
    output_path = os.path.join(base_path, f'{file_name}_{output_suffix}{extension}')

    # 將修改後的 DataFrame 寫入 CSV 文件
    df.to_csv(output_path, index=False, encoding='utf-8')


def main2():
    return True