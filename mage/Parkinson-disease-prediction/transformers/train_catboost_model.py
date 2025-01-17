import mlflow

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    root_mean_squared_error,
)

from catboost import CatBoostClassifier
from sklearn.preprocessing import StandardScaler

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    pass

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("parkinson-disease-prediction-experiment")


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

    X_train, X_val, y_train, y_val = data

    # Standardize the data
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_val = scaler.transform(X_val)

    # Define the hyperparameter space
    search_space = {
        "iterations": hp.choice("max_depth", [500, 1000, 1500]),
        "learning_rate": hp.choice("learning_rate", [0.01, 0.05, 0.1]),
        "depth": hp.choice("depth", [4, 6, 8, 10]),
        "l2_leaf_reg": hp.choice("l2_leaf_reg", [1, 3, 5, 7, 9]),
        "border_count": hp.choice("border_count", [32, 50, 100]),
        "bagging_temperature": hp.choice("bagging_temperature", [0.5, 1, 2, 5]),
        "random_strength": hp.choice("random_strength", [0.5, 1, 2]),
        "scale_pos_weight": hp.choice("scale_pos_weight", [1, 2, 3, 5]),
    }

    def objective(params):
        with mlflow.start_run():
            mlflow.log_params(params)

            # Train and evaluate CatBoost
            mlflow.set_tag("Developer", "sanghvirajit")
            mlflow.set_tag("model", "CatBoostClassifier")
            catboost = CatBoostClassifier(verbose=0, **params)
            catboost.fit(X_train, y_train)
            y_pred_catboost = catboost.predict(X_val)

            metrics = get_metrics(y_val, y_pred_catboost)

            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_metric("precision", metrics["precision"])
            mlflow.log_metric("recall", metrics["recall"])
            mlflow.log_metric("f1", metrics["f1"])
            mlflow.log_metric("rmse", metrics["rmse"])

            # Log the model manually
            mlflow.catboost.log_model(
                catboost,
                artifact_path="model",
            )

        return {"loss": metrics["accuracy"], "status": STATUS_OK}

    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=10,
        trials=Trials(),
    )

    return
