from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    root_mean_squared_error,
)
import mlflow

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("parkinson-disease-prediction-experiment")


if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def get_metrics(y_val, y_pred):
    accuracy = accuracy_score(y_val, y_pred)
    precision = precision_score(y_val, y_pred)
    recall = recall_score(y_val, y_pred)
    f1 = f1_score(y_val, y_pred)
    rmse = root_mean_squared_error(y_val, y_pred)

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "rmse": rmse,
    }


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    with mlflow.start_run():
        mlflow.sklearn.autolog()
        mlflow.set_tag("Developer", "sanghvirajit")
        mlflow.set_tag("model", "LinearRegression")

        X_train, X_val, y_train, y_val = data

        # Dicts
        train_dicts = X_train.to_dict(orient="records")
        val_dicts = X_val.to_dict(orient="records")

        # DictVextorizer
        dv = DictVectorizer()
        X_train = dv.fit_transform(train_dicts)
        X_val = dv.transform(val_dicts)

        # Loading the model
        model = LinearRegression()

        # fit and train
        model.fit(X_train, y_train)

        # Predict
        y_pred_continuous = model.predict(X_val)
        # Threshold 0f 0.5, if probablity is greater than 0.5 --> 1 else 0
        y_pred = [1 if value > 0.5 else 0 for value in y_pred_continuous]

        metrics = get_metrics(y_val, y_pred)

        mlflow.log_metric("accuracy", metrics["accuracy"])
        mlflow.log_metric("precision", metrics["precision"])
        mlflow.log_metric("recall", metrics["recall"])
        mlflow.log_metric("f1", metrics["f1"])
        mlflow.log_metric("rmse", metrics["rmse"])

    return {
        "accuracy": metrics["accuracy"],
        "precision": metrics["precision"],
        "recall": metrics["recall"],
        "f1": metrics["f1"],
        "rmse": metrics["rmse"],
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
