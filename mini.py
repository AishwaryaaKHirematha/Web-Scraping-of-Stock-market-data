import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import io

def get_nse_stock_data(symbol,start_date,end_date):
    
    start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    
    url = f"https://www.nseindia.com/api/historical/cm/equity?symbol={symbol}&series=[%22EQ%22]&from={start_date}&to={end_date}&csv=true"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",

        "Accept-Language": "en-US,en;q=0.5",
        "Referer": "https://www.nseindia.com/"
    }
    
    with requests.Session() as s:
        
        s.get("https://www.nseindia.com", headers=headers)
        response = s.get(url, headers=headers)
    
    data = response.content.decode('utf-8')
    
    df = pd.read_csv(io.StringIO(data))
    
   
    df.columns = df.columns.str.strip()
    
    
    print("Columns:", df.columns)
    print(df.head())
    
    if 'Date' not in df.columns:
        raise KeyError("Expected column 'Date' not found in the downloaded data.")
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    
    return df


def plot_stock_data(df, symbol):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['OPEN'], label='OPEN Price')
    plt.title(f'Stock Prices of {symbol}')
    plt.xlabel(' Date')
    plt.ylabel('Open Price')
    plt.legend()
    plt.grid()
    plt.xticks(rotation=45)
    plt.tight_layout()  
    plt.show()

symbol = 'HAL'
start_date = '2024-06-23'
end_date = '2024-07-23'
df = get_nse_stock_data(symbol,start_date,end_date)
plot_stock_data(df, symbol)

df.to_excel('nse_stock_data.xlsx', index=False)



