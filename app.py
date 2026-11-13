from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
from collaborative import load_svd_model_and_recommend
from content_based import load_content_model_and_recommend
from knn import load_knn_model_and_recommend

app = Flask(__name__)
CORS(app)

# Load dataset once
df = pd.read_csv("data/dataset.csv")

@app.route('/')
def home():
    return "Welcome to the Recommendation API!"

# === Main routes under /recommend ===

@app.route('/recommend/content', methods=['GET'])
def recommend_content():
    user_input = request.args.get('input', '')
    if not user_input:
        return jsonify({'error': 'Missing input parameter'}), 400

    recommendations = load_content_model_and_recommend(user_input)
    return jsonify(recommendations)

@app.route('/recommend/svd', methods=['GET'])
def recommend_svd():
    recommendations = load_svd_model_and_recommend()
    return jsonify(recommendations)

@app.route('/recommend/knn', methods=['GET'])
def recommend_knn():
    recommendations = load_knn_model_and_recommend()
    return jsonify(recommendations)

# === Alias routes for easier access ===

@app.route('/content', methods=['GET'])
def content_alias():
    return recommend_content()

@app.route('/collaborative', methods=['GET'])
def collaborative_alias():
    return recommend_svd()

@app.route('/knn', methods=['GET'])
def knn_alias():
    return recommend_knn()

if __name__ == '__main__':
    app.run(debug=True)
