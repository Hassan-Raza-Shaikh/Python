import pandas as pd
import pickle
import json
import os
import mlflow
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score


def evaluate():
    # Load test data
    test_df = pd.read_csv("data/processed/test.csv")
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]

    # Load model
    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)

    # Predict
    y_pred = model.predict(X_test)

    # Calculate metrics
    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "f1_score": float(f1_score(y_test, y_pred, average="weighted")),
        "precision": float(precision_score(y_test, y_pred, average="weighted")),
        "recall": float(recall_score(y_test, y_pred, average="weighted")),
    }

    # Save metrics locally (for DVC)
    os.makedirs("models", exist_ok=True)
    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # Log metrics & artifact to MLflow run
    experiment = mlflow.get_experiment_by_name("wine-classification")
    if experiment:
        runs = mlflow.search_runs(
            experiment_ids=[experiment.experiment_id],
            order_by=["start_time DESC"],
            max_results=1,
        )
        if not runs.empty:
            run_id = runs.iloc[0]["run_id"]
            with mlflow.start_run(run_id=run_id):
                mlflow.log_metrics(metrics)
                mlflow.log_artifact("models/metrics.json")

    print("Evaluation metrics:")
    for metric, value in metrics.items():
        print(f"  {metric}: {value:.4f}")


if __name__ == "__main__":
    evaluate()
