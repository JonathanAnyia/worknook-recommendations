from surprise import Dataset, Reader, KNNBasic
from surprise.model_selection import cross_validate
import pandas as pd
import joblib
import os
import json

def train_and_save_knn_model():
    reader = Reader(rating_scale=(1, 5))
    df = pd.read_csv("data/dataset.csv")
    data = Dataset.load_from_df(df[['user_id', 'worker_id', 'rating']], reader)

    trainset = data.build_full_trainset()

    sim_options = {
        "name": "cosine",
        "user_based": True,
    }

    algo = KNNBasic(sim_options=sim_options)
    algo.fit(trainset)

    joblib.dump(algo, "models/knn_model.joblib")
    print("Model saved to models/knn_model.joblib")

def load_knn_model_and_recommend(top_n=5):
    import json
    df = pd.read_csv("data/dataset.csv")
    algo = joblib.load("models/knn_model.joblib")

    all_users = df["user_id"].unique()
    all_workers = df["worker_id"].unique()

    seen_pairs = set(zip(df["user_id"], df["worker_id"]))

    unseen_pairs = [
        (user, worker)
        for user in all_users
        for worker in all_workers
        if (user, worker) not in seen_pairs
    ]

    predictions = []
    for user_id, worker_id in unseen_pairs:
        try:
            pred = algo.predict(uid=int(user_id), iid=int(worker_id))

            service_match = df[df["worker_id"] == worker_id]
            service_type = (
                str(service_match["service_type"].mode().iloc[0])
                if not service_match.empty
                else "Unknown"
            )

            predictions.append({
                "user_id": int(user_id),
                "worker_id": int(worker_id),
                "predicted_rating": float(round(pred.est, 2)),
                "service_type": service_type
            })
        except Exception:
            continue

    sorted_preds = sorted(predictions, key=lambda x: x["predicted_rating"], reverse=True)
    top_recommendations = sorted_preds[:top_n]

    # Save top recommendations to a JSON file
    if not os.path.exists("sample_data"):
        os.makedirs("sample_data")

    with open("sample_data/sample_knn_recommendations.json", "w") as f:
        json.dump(top_recommendations, f, indent=4)

    print(f"Top {top_n} KNN recommendations saved to sample_data/sample_knn_recommendations.json")

    return top_recommendations
