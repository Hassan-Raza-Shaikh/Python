import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
import yaml
import os


def load_params():
    with open("params.yaml", "r") as f:
        params = yaml.safe_load(f)
    return params


def preprocess():
    params = load_params()

    # Load wine dataset
    wine = load_wine()
    df = pd.DataFrame(wine.data, columns=wine.feature_names)
    df["target"] = wine.target

    # Save raw data
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv("data/raw/wine.csv", index=False)

    # Split data
    train_df, test_df = train_test_split(
        df,
        test_size=params["data"]["test_size"],
        random_state=params["data"]["random_state"],
    )

    # Save processed data
    os.makedirs("data/processed", exist_ok=True)
    train_df.to_csv("data/processed/train.csv", index=False)
    test_df.to_csv("data/processed/test.csv", index=False)

    print(f"Data preprocessed: train={len(train_df)}, test={len(test_df)}")


if __name__ == "__main__":
    preprocess()
