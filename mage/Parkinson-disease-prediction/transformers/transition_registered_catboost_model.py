from mlflow.tracking import MlflowClient
from datetime import datetime
import mlflow

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    pass


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

    mlflow.set_tracking_uri("http://mlflow:5000")
    mlflow.set_experiment("parkinson-disease-prediction-experiment")

    model_name = "parkinson-disease-models"

    client = MlflowClient()
    latest_versions = client.get_latest_versions(model_name, stages=["None"])

    for version in latest_versions:
        model_version = version.version

    # Move the registered model to stage
    new_stage = "Production"
    client.transition_model_version_stage(
        name=model_name,
        version=model_version,
        stage=new_stage,
        archive_existing_versions=False,
    )

    date = datetime.today().date()
    client.update_model_version(
        name=model_name,
        version=model_version,
        description=f"The model version {model_version} was transitioned to {new_stage} on {date}.",
    )
