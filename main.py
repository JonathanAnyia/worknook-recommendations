
import pandas as pd
from collaborative import train_and_save_svd_model, load_svd_model_and_recommend
from content_based import train_and_save_content_model, load_content_model_and_recommend
from knn import train_and_save_knn_model, load_knn_model_and_recommend

train_and_save_svd_model()
train_and_save_content_model()

#load_content_model_and_recommend(user_input="Cleaning", top_n=5)

df = pd.read_csv("data/dataset.csv")
train_and_save_knn_model()

print("CSV Columns:", df.columns)

print("\n=== Recommendations from Saved Models ===")

print("\nSVD Collaborative Filtering Recommendations:", load_svd_model_and_recommend())

print("\nContent-Based Recommendations:", load_content_model_and_recommend("Plumbing and maintenance"))

print("\nKNN Recommendations:")
recommendations = load_knn_model_and_recommend()
for rec in recommendations:
    print(f"Recommend worker {rec['worker_id']} ({rec['service_type']}) to user {rec['user_id']} with predicted rating {rec['predicted_rating']}")
