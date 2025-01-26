from flask import Flask, send_from_directory, jsonify
import os
import pickle
import numpy as np
import pandas as pd
import requests
import time
import json


app = Flask(__name__, static_folder='dist', static_url_path='/dist')

models_dir = './models'
csv_file = 'http://localhost:5173/data/sp500_esg_data.csv'

@app.route('/api/pipeline/<ticker>', methods=['GET'])
def pipeline_endpoint(ticker):
    try:
        output = run_pipeline(ticker)
        if output is None:
            return jsonify({"error": "Pipeline failed to return output"}), 500
        return jsonify({"output": output}), 200
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
        
        # Return the value of the 'text' key
        text_output = output_data.get("text")
        if text_output is None:
            print("No 'text' found in the output.")
            return None

        print(f"Pipeline completed. Text output: {text_output}")
        return text_output
    except Exception as e:
        print(f"Error in run_pipeline: {str(e)}")
        return None

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
