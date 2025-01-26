from flask import Flask, send_from_directory, jsonify
import os
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__, static_folder='dist', static_url_path='/dist')

models_dir = './models'
csv_file = './data/sp500_price_data.csv'

@app.route('/api/predict/<ticker>', methods=['GET'])
def predict(ticker):
    try:
        # Check if the CSV file exists
        if not os.path.exists(csv_file):
            return jsonify({"error": f"Stock data file not found at {csv_file}"}), 404

        # Load the stock price data
        stocks_data = pd.read_csv(csv_file)
        stocks_data['Date'] = pd.to_datetime(stocks_data['Date'])

        if ticker not in stocks_data.columns:
            return jsonify({"error": f"No data found for ticker {ticker}"}), 404

        ticker_data = stocks_data[['Date', ticker]].rename(columns={ticker: 'StockPrice'}).dropna()

        ticker_data['days_since_start'] = (ticker_data['Date'] - ticker_data['Date'].min()).dt.days

        # Check if the pre-trained model exists for the specified ticker
        model_path = os.path.join(models_dir, f"{ticker}_model.pkl")
        if not os.path.exists(model_path):
            return jsonify({"error": f"No pre-trained model found for ticker {ticker}. Please train the model first."}), 404

        # Load the pretrained model
        with open(model_path, 'rb') as f:
            rf = pickle.load(f)

        # Predict the next 30 days
        last_day = ticker_data['days_since_start'].max()
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

        return jsonify(response_data)

    except Exception as e:
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
