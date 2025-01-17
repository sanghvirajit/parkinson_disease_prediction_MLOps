from mlflow.tracking import MlflowClient
from mlflow.entities import ViewType
import mlflow

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    pass

mlflow.set_tracking_uri("http://mlflow:5000")
mlflow.set_experiment("parkinson-disease-prediction-experiment")


@transformer
def transform(*args, **kwargs):
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

    EXPERIMENT_NAME = "parkinson-disease-prediction-experiment"
    MODEL_NAME = "parkinson-disease-models"

    client = MlflowClient()
    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.rmse asc"],
    )[0]

    # register the best model
    run_id = best_run.info.run_id
    model_uri = f"runs:/{run_id}/model"
    model_accuracy = round(best_run.data.metrics["accuracy"] * 100)
    model_details = mlflow.register_model(model_uri=model_uri, name=MODEL_NAME)
    client.update_registered_model(
        name=model_details.name, description=f"Current accuracy: {model_accuracy}%"
    )
