import pandas as pd
import pickle
import yaml
import os
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


def load_params():
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params


def train():
    params = load_params()
    train_params = params["train"]

    # Load processed training data
    train_df = pd.read_csv("data/processed/train.csv")
    X_train = train_df.drop("target", axis=1)
    y_train = train_df["target"]

    # Select model based on config
    if train_params["model_type"] == "RandomForest":
        model = RandomForestClassifier(
            n_estimators=train_params["n_estimators"],
            max_depth=train_params["max_depth"],
            random_state=train_params["random_state"],
        )
    elif train_params["model_type"] == "LogisticRegression":
        model = LogisticRegression(
            max_iter=1000,
            random_state=train_params["random_state"],
        )
    else:
        raise ValueError(f"Unknown model type: {train_params['model_type']}")

    # Set MLflow experiment
    mlflow.set_experiment("wine-classification")

    # Start an MLflow run
    with mlflow.start_run():
        # Log parameters to MLflow
        mlflow.log_params(train_params)
        mlflow.log_param("test_size", params["data"]["test_size"])

        # Train
        model.fit(X_train, y_train)

        # Save model pickle for DVC
        os.makedirs("models", exist_ok=True)
        with open("models/model.pkl", "wb") as f:
            pickle.dump(model, f)

        # Log model using MLflow's sklearn integration & register in registry
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="wine-model",
            input_example=X_train.iloc[:1],
            registered_model_name="WineClassifier",
        )

        print(f"Model trained: {train_params['model_type']}")
        print(f"MLflow Run ID: {mlflow.active_run().info.run_id}")


if __name__ == "__main__":
    train()
