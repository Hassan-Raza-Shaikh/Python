from mlflow import MlflowClient


def register():
    client = MlflowClient()

    # Set alias 'champion' to version 2
    client.set_registered_model_alias(
        name="WineClassifier",
        alias="champion",
        version=2,
    )

    # Set alias 'challenger' to version 3
    client.set_registered_model_alias(
        name="WineClassifier",
        alias="challenger",
        version=3,
    )

    # Verify
    champion = client.get_model_version_by_alias("WineClassifier", "champion")
    challenger = client.get_model_version_by_alias("WineClassifier", "challenger")

    print(f"Champion: Version {champion.version}")
    print(f"Challenger: Version {challenger.version}")


if __name__ == "__main__":
    register()
