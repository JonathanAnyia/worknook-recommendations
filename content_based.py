from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib
import os
import json

def train_and_save_content_model():
    if not os.path.exists("models"):
        os.makedirs("models")

    df = pd.read_csv("data/dataset.csv")
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['service_type'])

    joblib.dump(vectorizer, "models/tfidf_vectorizer.joblib")
    joblib.dump(tfidf_matrix, "models/tfidf_matrix.joblib")
    df.to_csv("models/content_df.csv", index=False)
    print("Content-based model components saved.")

def load_content_model_and_recommend(user_input, top_n=5):
    model_path = "models/tfidf_vectorizer.joblib"
    vectorizer = joblib.load(model_path)
    df = pd.read_csv("data/dataset.csv")

    tfidf_matrix = vectorizer.transform(df['service_type'])
    user_tfidf = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_tfidf, tfidf_matrix)

    top_indices = similarity.argsort()[0][-top_n:][::-1]
    recommendations = df.iloc[top_indices]

    top_recommendations = recommendations[['worker_id', 'service_type']].to_dict(orient='records')

    # Save to JSON
    if not os.path.exists("sample_data"):
        os.makedirs("sample_data")

    with open("sample_data/sample_content_recommendations.json", "w") as f:
        json.dump(top_recommendations, f, indent=4)

    print(f"Top {top_n} content-based recommendations saved to sample_data/sample_content_recommendations.json")

    return top_recommendations

