import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

your_alpha_vantage_api_key="7PG776Z4SYL0BKB"



def fetch_stock_data(symbols, apikey, function='TIME_SERIES_DAILY'):
    stock_data = {}
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'
        response = requests.get(url)
        data = response.json()
        stock_data[symbol] = data
    return stock_data

# Example usage
apikey = 'your_alpha_vantage_api_key'
symbols = ['AAPL', 'MSFT', 'GOOGL']
stock_data = fetch_stock_data(symbols, apikey)


def analyze_stock_data(stock_data):
    analyzed_data = {}
    for symbol, data in stock_data.items():
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })
        df = df.astype({
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64'
        })
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA50'] = df['close'].rolling(window=50).mean()
        analyzed_data[symbol] = df
    return analyzed_data











def analyze_stock_data(stock_data):
    analyzed_data = {}
    for symbol, data in stock_data.items():
        df = pd.DataFrame.from_dict(data['Time Series (Daily)'], orient='index')
        df = df.rename(columns={
            '1. open': 'open',
            '2. high': 'high',
            '3. low': 'low',
            '4. close': 'close',
            '5. volume': 'volume'
        })
        df = df.astype({
            'open': 'float64',
            'high': 'float64',
            'low': 'float64',
            'close': 'float64',
            'volume': 'int64'
        })
        df['MA20'] = df['close'].rolling(window=20).mean()
        df['MA50'] = df['close'].rolling(window=50).mean()
        analyzed_data[symbol] = df
    return analyzed_data



def generate_graphs(analyzed_data):
    for symbol, df in analyzed_data.items():
        plt.figure(figsize=(14, 7))
        plt.plot(df.index, df['close'], label='Close Price')
        plt.plot(df.index, df['MA20'], label='20-Day MA')
        plt.plot(df.index, df['MA50'], label='50-Day MA')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title(f'{symbol} Stock Price and Moving Averages')
        plt.legend()
        plt.savefig(f'{symbol}_stock_graph.png')
        plt.close()




def create_pdf(graph_paths, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, 'Stock Analysis Report')
    y_position = 700
    for graph_path in graph_paths:
        c.drawImage(graph_path, 100, y_position, width=400, height=300)
        y_position -= 350
        if y_position < 50:
            c.showPage()
            y_position = 700
    c.save()

# Example usage
graph_paths = [f'{symbol}_stock_graph.png' for symbol in symbols]
create_pdf(graph_paths, 'stock_analysis_report.pdf')


def stock_analysis_agent(symbols, apikey):
    # Fetch stock data for multiple symbols
    stock_data = fetch_stock_data(symbols, apikey)

    # Analyze stock data for multiple symbols
    analyzed_data = analyze_stock_data(stock_data)

    # Generate graphs for multiple symbols
    generate_graphs(analyzed_data)

    # Create PDF for multiple symbols
    graph_paths = [f'{symbol}_stock_graph.png' for symbol in symbols]
    create_pdf(graph_paths, 'stock_analysis_report.pdf')

    print('PDF report generated: stock_analysis_report.pdf')

# Example usage
stock_analysis_agent(['AAPL', 'MSFT', 'GOOGL'], 'your_alpha_vantage_api_key')






