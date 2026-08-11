import pandas as pd
import mlflow
from sklearn.metrics import accuracy_score, f1_score


def compare():
    # Load test data
    test_df = pd.read_csv("data/processed/test.csv")
    X_test = test_df.drop("target", axis=1)
    y_test = test_df["target"]

    # Load both models
    champion = mlflow.sklearn.load_model("models:/WineClassifier@champion")
    challenger = mlflow.sklearn.load_model("models:/WineClassifier@challenger")

    # Predict with both
    champion_preds = champion.predict(X_test)
    challenger_preds = challenger.predict(X_test)

    # Compare
    results = {
        "Model": ["Champion", "Challenger"],
        "Type": [type(champion).__name__, type(challenger).__name__],
        "Accuracy": [
            accuracy_score(y_test, champion_preds),
            accuracy_score(y_test, challenger_preds),
        ],
        "F1 Score": [
            f1_score(y_test, champion_preds, average="weighted"),
            f1_score(y_test, challenger_preds, average="weighted"),
        ],
    }

    df = pd.DataFrame(results)
    print("Champion vs Challenger Comparison:")
    print(df.to_string(index=False))

    # Determine winner
    if results["F1 Score"][1] > results["F1 Score"][0]:
        print("\nChallenger outperforms Champion! Consider promoting.")
    else:
        print("\nChampion still holds. Challenger needs more work.")


if __name__ == "__main__":
    compare()
