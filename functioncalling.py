import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

ALPHA_VANTAGE_API_KEY ="7PG776Z4SYL0BKB"
MISTRAL_API_KEY = "aTLH3ol0C106cwFLymbSWjFIvb02Ktcd"



def fetch_stock_data(stock_symbol, interval="daily", output_size="compact"):
    url = f"https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_INTRADAY" if interval == "intraday" else "TIME_SERIES_DAILY",
        "symbol": stock_symbol,
        "apikey": ALPHA_VANTAGE_API_KEY,
        "interval": "5min" if interval == "intraday" else None,
        "outputsize": output_size,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error fetching data: {response.status_code}, {response.text}")
    



# def fetch_stock_data(symbol, apikey, function='TIME_SERIES_DAILY'):
#     url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={apikey}'
#     response = requests.get(url)
#     data = response.json()
#     return data



def mistral_call_function(function_name, arguments):
    url = "https://api.mistral.ai/v1/function-calling"
    headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}"}
    payload = {
        "function_name": function_name,
        "arguments": arguments,
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise ValueError(f"Error in Mistral function call: {response.status_code}, {response.text}")





CODESTRAL_API_KEY = "6E5UHsogwNblf0IH0pGzRnJsBRW8BIIN"
CODESTRAL_COMPLETION_ENDPOINT = "https://codestral.mistral.ai/v1/fim/completions"


def generate_graph(data, graph_type="line", title="Stock Trend", x_label="Date", y_label="Price"):
    payload ={
        "model": "codestral-2405",
        "temperature": 1.5,
        "top_p": 1,
        "max_tokens": 0,
        "stream": False,
        "stop": "string",
        "random_seed": 0,
        "prompt": "def",
        "suffix": "return a+b",
        "min_tokens": 0,
        
    }
    headers = {"Authorization": f"Bearer {CODESTRAL_API_KEY}"}
    response = requests.post(CODESTRAL_COMPLETION_ENDPOINT, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json().get("graph_url", "Graph URL not found in response.")
    else:
        print("Payload sent:", json.dumps(payload, indent=4))
        print("Response from API:", response.text)
        raise ValueError(f"Error generating graph: {response.status_code}, {response.text}")


# def generate_graph(data, graph_type="line", title="Stock Trend", x_label="Date", y_label="Price"):
#     payload = {
#         "model": "codestral-2405",
#         "prompt": json.dumps({
#             "data": data,
#             "type": graph_type,
#             "title": title,
#             "x_label": x_label,
#             "y_label": y_label,
#         }),
#     }
#     headers = {"Authorization": f"Bearer {CODESTRAL_API_KEY}"}
#     response = requests.post(CODESTRAL_COMPLETION_ENDPOINT, json=payload, headers=headers)
#     if response.status_code == 200:
#         return response.json()["graph_url"]
#     else:
#         raise ValueError(f"Error generating graph: {response.status_code}, {response.text}")
    



CODESTRAL_CHAT_ENDPOINT = "https://codestral.mistral.ai/v1/chat/completions"

# def generate_pdf(report_content, filename="report.pdf"):
#     from reportlab.lib.pagesizes import letter
#     from reportlab.pdfgen import canvas

#     try:
#         # Create a PDF locally if the API fails
#         pdf = canvas.Canvas(filename, pagesize=letter)
#         pdf.drawString(100, 750, report_content)
#         pdf.save()
#         print(f"PDF successfully created locally: {filename}")
#         return filename
#     except Exception as e:
#         raise ValueError(f"Failed to generate PDF locally: {e}")









def generate_pdf(report_content):
    payload = {
        "model": "codestral-2405",
        "temperature": 1.5,
        "top_p": 1,
        "max_tokens": 0,
        "stream": False,
        "stop": "string",
        "random_seed": 0,
        "prompt": "def",
        "suffix": "return a+b",
        "min_tokens": 0,
        "messages": [
            {"role": "system", "content": "Create a PDF report from the following data and graphs."},
            {"role": "user", "content": report_content},
        ],
    }
    headers = {"Authorization": f"Bearer {CODESTRAL_API_KEY}"}
    response = requests.post(CODESTRAL_CHAT_ENDPOINT, json=payload, headers=headers)
    if response.status_code == 200:
        return response.json()["pdf_url"]
    else:
        raise ValueError(f"Error generating PDF: {response.status_code}, {response.text}")
    


def main():
    stock_symbol = "AAPL"
    interval = "daily"
    
    # Step 1: Fetch stock data
    stock_data = fetch_stock_data(stock_symbol, interval=interval)

    # Step 2: Perform analysis (mock example)
    analysis_summary = f"Stock {stock_symbol} is trending upward. Suggest holding for now."

    # Step 3: Generate graph
    graph_url = generate_graph(stock_data["Time Series (Daily)"], title=f"{stock_symbol} Price Trends")

    # Step 4: Generate PDF
    report_content = f"Analysis for {stock_symbol}:\n{analysis_summary}\nGraph: {graph_url}"
    pdf_url = generate_pdf(report_content)

    # Output results
    print(f"Graph: {graph_url}")
    print(f"Downloadable PDF: {pdf_url}")

if __name__ == "__main__":
    main()






