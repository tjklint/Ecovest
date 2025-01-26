from flask import Flask, send_from_directory, jsonify
import os
import pickle
import numpy as np
import pandas as pd
import requests
import time
import json
import io

app = Flask(__name__, static_folder='dist', static_url_path='/dist')

models_dir = './models'

@app.route('/api/pipeline/<ticker>', methods=['GET'])
def pipeline_endpoint(ticker):
    try:
        output = run_pipeline(ticker)
        if output is None:
            return jsonify({"error": "Pipeline failed to return output"}), 500
        return jsonify(output), 200
    except Exception as e:
        print(f"Error in pipeline endpoint: {str(e)}")
        return jsonify({"error": f"Internal Server Error: {str(e)}"}), 500

def start_pipeline(ticker: str):
    try:
        url = "https://api.gumloop.com/api/v1/start_pipeline"
        payload = {
            "user_id": "hI4Nlc2KB2Y7M9knwyq9I1bV0A73",
            "saved_item_id": "6Y1atyi7zBSGMMxw9FR9h7",
            "pipeline_inputs": [
                {"input_name": "input", "value": f"https://www.google.ca/search?q=stock+ticker+{ticker}"}
            ]
        }
        headers = {"Authorization": "Bearer 9bd8e50e969e4392bcd40105cb404640", "Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print(f"start_pipeline response: {data}")
            return data.get("run_id")
        else:
            print(f"Failed start_pipeline: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"Error in start_pipeline: {str(e)}")
        return None


def get_output(run_id: str):
    url = "https://api.gumloop.com/api/v1/get_pl_run"
    params = {
        "run_id": run_id,
        "user_id": "hI4Nlc2KB2Y7M9knwyq9I1bV0A73"
    }
    headers = {
        "Authorization": "Bearer 9bd8e50e969e4392bcd40105cb404640"
    }
    response = requests.get(url, params=params, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data.get("outputs", {}).get("output", None)
    return None

def run_pipeline(ticker: str):
    try:
        run_id = start_pipeline(ticker)
        if not run_id:
            print("Failed to start pipeline.")
            return None

        output = None
        while output is None:
            print(f"Waiting for pipeline to finish for run_id: {run_id}...")
            time.sleep(5)
            output = get_output(run_id)

        # Convert output string to JSON
        output_data = json.loads(output)
        
        # Extract 'text' and 'data'
        text_output = output_data.get("text")
        data_output = output_data.get("data")

        if text_output is None or data_output is None:
            print("Incomplete output. Missing 'text' or 'data'.")
            return None

        print(f"Pipeline completed. Text output: {text_output}, Data output: {data_output}")
        return {"text": text_output, "data": data_output}
    except Exception as e:
        print(f"Error in run_pipeline: {str(e)}")
        return None

@app.route('/api/predict/<ticker>', methods=['GET'])
def predict(ticker):
    try:
        csv_file_url = 'http://localhost:5173/data/sp500_price_data.csv'

        print(f"Starting prediction for ticker: {ticker}")

        # Fetch the CSV from the web server
        print(f"Fetching stock price data from {csv_file_url}")
        response = requests.get(csv_file_url)
        
        if response.status_code != 200:
            print(f"Failed to fetch stock data. Status code: {response.status_code}")
            return jsonify({"error": f"Failed to fetch stock data from {csv_file_url}"}), 404

        # Load the stock price data
        stocks_data = pd.read_csv(io.StringIO(response.text))
        print(f"Data loaded. Columns: {stocks_data.columns}")

        stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])

        if ticker not in stocks_data.columns:
            print(f"No data found for ticker {ticker}")
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404

        ticker_data = stocks_data[['Date', ticker]].rename(columns={ticker: 'StockPrice'}).dropna()
        print(f"Processed {len(ticker_data)} rows of data for ticker {ticker}")

        ticker_data['days_since_start'] = (ticker_data['Date'] - ticker_data['Date'].min()).dt.days

        # Check if the pre-trained model exists for the specified ticker
        model_path = os.path.join(models_dir, f"{ticker}_model.pkl")
        if not os.path.exists(model_path):
            print(f"No pre-trained model found for ticker {ticker}. Model path: {model_path}")
            return jsonify({"error": f"No pre-trained model found for ticker {ticker}. Please train the model first."}), 404

        # Load the pretrained model
        print(f"Loading pre-trained model from {model_path}")
        with open(model_path, 'rb') as f:
            rf = pickle.load(f)
        print(f"Model loaded successfully for ticker {ticker}")

        # Predict the next 30 days
        last_day = ticker_data['days_since_start'].max()
        print(f"Last day in historical data: {last_day}")
        future_days = np.arange(last_day + 1, last_day + 31).reshape(-1, 1)
        future_prices = rf.predict(future_days)
        future_dates = [ticker_data['Date'].max() + pd.Timedelta(days=i) for i in range(1, 31)]

        # Prepare response data for Chart.js
        response_data = {
            "ticker": ticker,
            "historical": {
                "dates": ticker_data['Date'].dt.strftime('%Y-%m-%d').tolist(),
                "prices": ticker_data['StockPrice'].tolist()
            },
            "predicted": {
                "dates": [date.strftime('%Y-%m-%d') for date in future_dates],
                "prices": future_prices.tolist()
            }
        }

        print(f"Prediction complete for ticker {ticker}. Returning response.")
        return jsonify(response_data)

    except Exception as e:
        print(f"Error during prediction for ticker {ticker}: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Example API route
@app.route('/api/hello')
def hello():
    return jsonify({"message": "Hello from Flask!"})

# Serve the main page at '/'
@app.route('/')
def serve_main():
    return send_from_directory('dist', 'index.html')

# Serve the analytics page at '/analytics'
@app.route('/analytics')
def serve_analytics():
    return send_from_directory('dist', 'analytics.html')

# OPTIONAL: If you have additional static files in dist/assets, you can add:
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    return send_from_directory('dist/assets', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
