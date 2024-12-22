import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

your_alpha_vantage_api_key="7PG776Z4SYL0BKB"

def fetch_stock_data(symbol, apikey, function='TIME_SERIES_DAILY'):
    url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'
    response = requests.get(url)
    data = response.json()
    return data

# Example usage
apikey = 'your_alpha_vantage_api_key'
symbol = 'AAPL'
stock_data = fetch_stock_data(symbol, apikey)




def analyze_stock_data(stock_data):
    # Convert data to DataFrame
    df = pd.DataFrame.from_dict(stock_data['Time Series (Daily)'], orient='index')
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

    # Perform analysis (e.g., Moving Average)
    df['MA20'] = df['close'].rolling(window=20).mean()
    df['MA50'] = df['close'].rolling(window=50).mean()

    return df

# Example usage
analyzed_data = analyze_stock_data(stock_data)


def generate_graphs(analyzed_data):
    plt.figure(figsize=(14, 7))
    plt.plot(analyzed_data.index, analyzed_data['close'], label='Close Price')
    plt.plot(analyzed_data.index, analyzed_data['MA20'], label='20-Day MA')
    plt.plot(analyzed_data.index, analyzed_data['MA50'], label='50-Day MA')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Stock Price and Moving Averages')
    plt.legend()
    plt.savefig('stock_graph.png')
    plt.close()

# Example usage
generate_graphs(analyzed_data)



def create_pdf(graph_path, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, 'Stock Analysis Report')
    c.drawImage(graph_path, 100, 400, width=400, height=300)
    c.save()

# Example usage
create_pdf('stock_graph.png', 'stock_analysis_report.pdf')



def stock_analysis_agent(symbol, apikey):
    # Fetch stock data
    stock_data = fetch_stock_data(symbol, apikey)

    # Analyze stock data
    analyzed_data = analyze_stock_data(stock_data)

    # Generate graphs
    generate_graphs(analyzed_data)

    # Create PDF
    create_pdf('stock_graph.png', 'stock_analysis_report.pdf')

    print('PDF report generated: stock_analysis_report.pdf')

# Example usage
stock_analysis_agent('AAPL', 'your_alpha_vantage_api_key')






