import mlflow

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    root_mean_squared_error,
)

import xgboost as xgb
from sklearn.preprocessing import StandardScaler

from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
from hyperopt.pyll import scope

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("parkinson-disease-prediction-experiment")

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    pass


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
        "max_depth": scope.int(hp.uniform("max_depth", 1, 20)),
        "learning_rate": hp.uniform("learning_rate", 0.01, 0.2),
        "reg_alpha": hp.loguniform("reg_alpha", -5, -1),
        "reg_lambda": hp.loguniform("reg_lambda", -6, -1),
        "min_child_weight": hp.loguniform("min_child_weight", -1, 3),
        "objective": "reg:squarederror",
        "seed": 42,
    }

    def objective(params):
        with mlflow.start_run():
            mlflow.xgboost.autolog()
            mlflow.set_tag("Developer", "sanghvirajit")
            mlflow.set_tag("model", "XGBoostClassifier")
            mlflow.log_params(params)

            # Train and evaluate XGBoost
            xgb_model = xgb.XGBClassifier(**params)
            xgb_model.fit(X_train, y_train)
            y_pred_xgboost = xgb_model.predict(X_val)

            metrics = get_metrics(y_val, y_pred_xgboost)

            mlflow.log_metric("accuracy", metrics["accuracy"])
            mlflow.log_metric("precision", metrics["precision"])
            mlflow.log_metric("recall", metrics["recall"])
            mlflow.log_metric("f1", metrics["f1"])
            mlflow.log_metric("rmse", metrics["rmse"])

        return {"loss": metrics["accuracy"], "status": STATUS_OK}

    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=32,
        trials=Trials(),
    )

    return
