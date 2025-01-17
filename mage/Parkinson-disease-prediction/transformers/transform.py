from sklearn.model_selection import train_test_split

if "transformer" not in globals():
    from mage_ai.data_preparation.decorators import transformer
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(df, *args, **kwargs):
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

    numerical_columns = [
        "Age",
        "BMI",
        "AlcoholConsumption",
        "PhysicalActivity",
        "DietQuality",
        "SleepQuality",
        "SystolicBP",
        "DiastolicBP",
        "CholesterolTotal",
        "CholesterolLDL",
        "CholesterolHDL",
        "CholesterolTriglycerides",
        "UPDRS",
        "MoCA",
        "FunctionalAssessment",
    ]

    categorical_columns = [
        "Gender",
        "Ethnicity",
        "EducationLevel",
        "Smoking",
        "FamilyHistoryParkinsons",
        "TraumaticBrainInjury",
        "Hypertension",
        "Diabetes",
        "Depression",
        "Stroke",
        "Tremor",
        "Rigidity",
        "Bradykinesia",
        "PosturalInstability",
        "SpeechProblems",
        "SleepDisorders",
        "Constipation",
    ]

    # Changing the categorical column values dtype from int64 to str (object)
    df[categorical_columns] = df[categorical_columns].astype(str)

    X = df[numerical_columns + categorical_columns]

    # Target variable -> y
    target = "Diagnosis"
    y = df[target]

    # Split the data into training and validation sets
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    return X_train, X_val, y_train, y_val


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
