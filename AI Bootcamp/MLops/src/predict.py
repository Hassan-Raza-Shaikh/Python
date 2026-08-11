import pandas as pd
import mlflow


def predict():
    # Load the champion model from the registry
    model_uri = "models:/WineClassifier@champion"
    model = mlflow.sklearn.load_model(model_uri)

    print(f"Loaded model from: {model_uri}")
    print(f"Model type: {type(model).__name__}")

    # Load test data for demonstration
    test_df = pd.read_csv("data/processed/test.csv")
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]

    # Make predictions
    predictions = model.predict(X_test)

    # Show results
    results = pd.DataFrame({
        "actual": y_test.values,
        "predicted": predictions,
    })
    results["correct"] = results["actual"] == results["predicted"]

    print(f"\nPredictions on test set:")
    print(results.head(10))
    print(f"\nAccuracy: {results['correct'].mean():.4f}")
    print(f"Total samples: {len(results)}")


if __name__ == "__main__":
    predict()
