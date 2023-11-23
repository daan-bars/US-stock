import yfinance as yf
import os
import time
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

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
    # 先測試一檔試看看
    stock = yf.Ticker('AAPL')

    # 取得價量資料＋股利發放資料＋股票分割資料
    stock.history(period='max')

    # 創立一個紀錄失敗股票的 list
    failed_list = []

    today_date = datetime.today().strftime('%Y%m%d')
    folder_name = today_date
    os.makedirs(folder_name, exist_ok=True)

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
            
            file_path = os.path.join(folder_name, f'價量資料_{i}.csv')
            stock_data.to_csv(file_path)
            
            # 停一秒，再抓下一檔，避免對伺服器造成負擔而被鎖住
            time.sleep(1)
        except:
            failed_list.append(i)
            continue
    
    return failed_list

def download_financial_data(stk_list):
    """
    繪製股票走勢圖。

    Parameters:
    - stock_code (str): 股票代碼。
    - days (int): 要顯示的天數，預設為 90 天。
    """
    # 取得今天的日期
    today_date = datetime.today().strftime('%Y%m%d')

    # 創建一個紀錄失敗股票的 list
    failed_list = []

    # 創建以今天日期為名的資料夾，如果不存在的話
    base_folder = os.path.join(os.getcwd(), today_date)
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
            stock.financials.to_csv(os.path.join(stock_folder, f'損益表_{i}.csv'))
            stock.balance_sheet.to_csv(os.path.join(stock_folder, f'資產負債表_{i}.csv'))
            stock.cashflow.to_csv(os.path.join(stock_folder, f'現金流量表_{i}.csv'))

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
        file_path = f'./20231122/價量資料_{stock_symbol}.csv'
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
        kwargs = dict(type='candle', mav=(5, 20, 60), volume=True, figratio=(10, 8), figscale=0.75,figsize=(23, 8),dpi=80, title=stock_symbol, style=s)

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

    translation_dict={
    'Beginning Cash Position': '期初現金餘額',
    'Capital Expenditure': '資本支出',
    'Cash Dividends Paid': '支付現金股利',
    'Cash Flow From Continuing Financing Activities': '來自持續融資活動的現金流量',
    'Cash Flow From Continuing Investing Activities': '來自持續投資活動的現金流量',
    'Cash Flow From Continuing Operating Activities': '來自持續營運活動的現金流量',
    'Change In Account Payable': '應付賬款的變動',
    'Change In Inventory': '存貨的變動',
    'Change In Other Current Assets': '其他流動資產的變動',
    'Change In Other Current Liabilities': '其他流動負債的變動',
    'Change In Other Working Capital': '其他營運資本的變動',
    'Change In Payable': '應付款項的變動',
    'Change In Payables And Accrued Expense': '應付款項及應計費用的變動',
    'Change In Receivables': '應收款項的變動',
    'Change In Working Capital': '營運資本的變動',
    'Changes In Account Receivables': '應收賬款的變動',
    'Changes In Cash': '現金變動',
    'Common Stock Dividend Paid': '支付普通股股息',
    'Common Stock Issuance': '發行普通股',
    'Common Stock Payments': '支付普通股款',
    'Deferred Income Tax': '递延所得税',
    'Deferred Tax': '递延税款',
    'Depreciation Amortization Depletion': '折舊、攤銷和減值',
    'Depreciation And Amortization': '折舊和攤銷',
    'End Cash Position': '期末現金餘額',
    'Financing Cash Flow': '融資現金流',
    'Free Cash Flow': '自由現金流',
    'Income Tax Paid Supplemental Data': '所得税支付（附加数据）',
    'Interest Paid Supplemental Data': '支付利息（附加数据）',
    'Investing Cash Flow': '投資現金流',
    'Issuance Of Capital Stock': '發行股本',
    'Issuance Of Debt': '發行債務',
    'Long Term Debt Issuance': '長期債務發行',
    'Long Term Debt Payments': '長期債務支付',
    'Net Business Purchase And Sale': '淨業務購買和銷售',
    'Net Common Stock Issuance': '淨普通股發行',
    'Net Income From Continuing Operations': '持續營運的淨收入',
    'Net Investment Purchase And Sale': '淨投資購買和銷售',
    'Net Issuance Payments Of Debt': '債務的淨發行和支付',
    'Net Long Term Debt Issuance': '淨長期債務發行',
    'Net Other Financing Charges': '融資的其他淨費用',
    'Net Other Investing Changes': '投資的其他淨變動',
    'Net PPE Purchase And Sale': '固定資產和無形資產的淨購買和銷售',
    'Net Short Term Debt Issuance': '淨短期債務發行',
    'Operating Cash Flow': '營運現金流',
    'Other Non Cash Items': '其他非現金項目',
    'Purchase Of Business': '購併企業',
    'Purchase Of Investment': '購買投資',
    'Purchase Of PPE': '購買固定資產和無形資產',
    'Repayment Of Debt': '債務的還款',
    'Repurchase Of Capital Stock': '回購股',
    'Sale Of Investment' : '投資賣出',
    'Short Term Debt Issuance' : '短期債務的發行',
    'Short Term Debt Payments' : '短期債務的支付',
    'Stock Based Compensation' : '股票基於報酬',
    }

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

def test():
    return True
