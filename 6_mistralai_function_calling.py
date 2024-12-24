import pandas as pd
import requests
import json
import os
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from mistralai import Mistral, UserMessage
from mistralai.models import UserMessage
#from mistralai.models.chatCompletion import ChatMessage
from mistralai.client import MistralClient
#from mistralai.models import ChatMessage
import functools
import time



# Set the environment variable
os.environ["MISTRALAI_API_KEY"] = "aTLH3ol0C106cwFLymbSWjFIvb02Ktcd"

# Access the environment variable
api_key = os.environ["MISTRALAI_API_KEY"] 

apikey="ELJXSS2821PSF8D0"

model = "mistral-large-latest"
client = Mistral(api_key=api_key)



# Function to get stock data using Mistral AI
def fetch_stock_data(symbols, apikey, function='TIME_SERIES_DAILY',outputsize='full'):
    stock_data = {}
    for symbol in symbols:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&outputsize={outputsize}&apikey={apikey}'

        
        
        # Create a user query to fetch stock data
        user_query = f"Fetch stock data for {symbol} from Alpha Vantage"
        messages = [
        {
            "role": "user",
            "content": user_query,
        },
    ]

        # Define the tool for fetching stock data
        tools = [
            {
                "type": "function",
                "function": {
                    "name": "fetch_stock_data",
                    "description": "Fetch stock data from Alpha Vantage",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "url": {
                                "type": "string",
                                "description": "The URL to fetch stock data.",
                            }
                        },
                        "required": ["url"],
                    },
                },
            }
        ]

        # Send the request to Mistral AI
        response = client.chat.complete(
            model=model,
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        messages.append(response.choices[0].message)

        # Execute the function call
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_params = json.loads(tool_call.function.arguments)

        # Make the API call using the function parameters
        function_result = requests.get(function_params['url']).json()
        messages.append({"role":"tool", "name":function_name, "content":json.dumps(function_result),"tool_call_id":tool_call.id})

        # Get the final response from Mistral AI
        response = client.chat.complete(
            model=model,
            messages=messages
        )
        
        # Debugging: Print the response content
        print(f"Response content for {symbol}: {response.choices[0].message.content}")

        # Attempt to parse the response content as JSON
        try:
            data = json.dumps(response.choices[0].message.content)
        except json.JSONDecodeError as e:
            print(f"JSONDecodeError for {symbol}: {e}")
            continue

        if "Error Message" in data or "Note" in data:
            print(f"Error in data fetching for {symbol}: {data}")

        stock_data[symbol] = data

        # Add a delay to avoid rate limiting
        time.sleep(1)

    return stock_data

    #     # Debugging: Print the response content
    #     print(f"Response content for {symbol}: {response.choices[0].message.content}")
        
    #     # Attempt to parse the response content as JSON
    #     try:
    #         data = json.loads(response.choices[0].message.content)
    #     except json.JSONDecodeError as e:
    #         print(f"JSONDecodeError for {symbol}: {e}")
    #         continue

    #     if "Error Message" in data or "Note" in data:
    #         print(f"Error in data fetching for {symbol}: {data}")

    #     stock_data[symbol] = data
    # return stock_data

    #     data = json.loads(response.choices[0].message.content)
    #     if "Error Message" in data or "Note" in data:
    #         print(f"Error in data fetching for {symbol}: {data}")

    #     stock_data[symbol] = data
    # return stock_data

# Example usage
apikey = apikey

symbols = ['IBM', 'MSFT', 'TSLA']
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
        output_path = f'{symbol}_stock_graph_6.png'
        plt.savefig(output_path)
        plt.close()
        if not os.path.exists(output_path):
            print(f"Failed to save graph for {symbol} at {output_path}")

def create_pdf(graph_paths, pdf_path):
    c = canvas.Canvas(pdf_path, pagesize=letter)
    c.drawString(100, 750, 'Stock Analysis Report')
    y_position = 700
    for graph_path in graph_paths:
        if not os.path.exists(graph_path):
            print(f"Warning: {graph_path} does not exist. Skipping.")
            continue
        c.drawImage(graph_path, 100, y_position, width=400, height=300)
        y_position -= 350
        if y_position < 50:
            c.showPage()
            y_position = 700
    c.save()

# Example usage
graph_paths = [f'{symbol}_stock_graph_6.png' for symbol in symbols]
create_pdf(graph_paths, '6_stock_analysis_report.pdf')

def stock_analysis_agent(symbols, apikey):
    # Fetch stock data for multiple symbols
    stock_data = fetch_stock_data(symbols, apikey)
    print(stock_data)

    # Analyze stock data for multiple symbols
    analyzed_data = analyze_stock_data(stock_data)

    # Generate graphs for multiple symbols
    generate_graphs(analyzed_data)

    # Create PDF for multiple symbols
    graph_paths = [f'{symbol}_stock_graph_6.png' for symbol in symbols]
    create_pdf(graph_paths, '6_stock_analysis_report.pdf')

    print('PDF report generated: 6_stock_analysis_report.pdf')

# Example usage
stock_analysis_agent(['IBM', 'MSFT', 'TSLA'], apikey)
