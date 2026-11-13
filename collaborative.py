from surprise import SVD, Dataset, Reader
from surprise.model_selection import cross_validate
import pandas as pd
import joblib
import os
import json

def train_and_save_svd_model():
    if not os.path.exists("models"):
        os.makedirs("models")

    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("data/dataset.csv")
    data = Dataset.load_from_df(df[["user_id", "worker_id", "rating"]], reader)
    trainset = data.build_full_trainset()

    algo = SVD()
    algo.fit(trainset)

    joblib.dump(algo, "models/svd_model.joblib")
    print("SVD model saved to models/svd_model.joblib")

def load_svd_model_and_recommend(top_n=5):
    df = pd.read_csv("data/dataset.csv")
    algo = joblib.load("models/svd_model.joblib")

    all_users = df["user_id"].unique()
    all_workers = df["worker_id"].unique()

    user_worker_seen = set(zip(df["user_id"], df["worker_id"]))
    unseen_pairs = [
        (user, worker)
        for user in all_users
        for worker in all_workers
        if (user, worker) not in user_worker_seen
    ]

    recommendations = []
    for user_id, worker_id in unseen_pairs:
        pred = algo.predict(uid=int(user_id), iid=int(worker_id))
        recommendations.append({
            "user_id": int(user_id),
            "worker_id": int(worker_id),
            "predicted_rating": float(round(pred.est, 2))
        })

    # Sort by predicted rating and return top_n
    sorted_recommendations = sorted(recommendations, key=lambda x: x["predicted_rating"], reverse=True)
    top_recommendations = sorted_recommendations[:top_n]

    if not os.path.exists("sample_data"):
        os.makedirs("sample_data")

    with open("sample_data/sample_svd_recommendations.json", "w") as f:
        json.dump(top_recommendations, f, indent=4)

    print("Sample recommendations saved to sample_data/sample_svd_recommendations.json")

    return top_recommendations

def evaluate_svd_model():
    df = pd.read_csv("data/dataset.csv")
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df[["user_id", "worker_id", "rating"]], reader)

    algo = SVD()
    print("Evaluating SVD model using cross-validation...")
    results = cross_validate(algo, data, measures=["RMSE", "MAE"], cv=5, verbose=True)

    return results  # Return the dictionary of cross-validation scores