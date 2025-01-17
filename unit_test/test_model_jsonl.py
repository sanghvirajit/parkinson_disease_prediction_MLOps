from pathlib import Path
import pickle
import pandas as pd
import json
from app import model

assets_path = Path(__file__).parent / "assets"
model_path = Path(__file__).parent / "../model/catboost_model.pkl"

test_cases = assets_path.glob("*.txt")

# Load model from the local dir to test the functions
with open(model_path, "rb") as file:
    logged_model = pickle.load(file)


# Read text files
def read_txt(file_path):
    with open(file_path, "r") as file:
        # Read the contents of the file
        content = file.read()
    return content


def test_jsonl_cases():
    # Loop over all test cases
    for test_case in test_cases:
        test_data = read_txt(test_case)
        test_case_name = test_case.stem.split("__")[0]
        ground_truth = test_case.stem.split("__")[1]
        test_data = test_data.replace("'", '"')

        # Convert to JSON object
        data_json = json.loads(test_data)

        # Predict
        model_service = model.ModelService(logged_model)

        processed_data = model_service.prepare_features(data_json)
        y_pred = logged_model.predict(processed_data)

        assert (
            int(ground_truth) == y_pred[0]
        ), f"Expected ground_truth {int(ground_truth)} but got {y_pred[0]} for test case {test_case_name}"


def test_base64_decode():
    data = "ewogICAgICAgICAgICAiZGF0YSI6IHsKICAgICAgICAgICAgICAgICAgIkFnZSI6IDY3LAogICAgICAgICAgICAgICAgICAiR2VuZGVyIjogIjEiLAogICAgICAgICAgICAgICAgICAiRXRobmljaXR5IjogIjIiLAogICAgICAgICAgICAgICAgICAiRWR1Y2F0aW9uTGV2ZWwiOiAiMSIsCiAgICAgICAgICAgICAgICAgICJCTUkiOiAyNC43NzI1OTQwMzQ1NzcyOCwKICAgICAgICAgICAgICAgICAgIlNtb2tpbmciOiAiMCIsCiAgICAgICAgICAgICAgICAgICJBbGNvaG9sQ29uc3VtcHRpb24iOiAxMy45NDEzODU3NDAzOTEwMDQsCiAgICAgICAgICAgICAgICAgICJQaHlzaWNhbEFjdGl2aXR5IjogMi40NzI1MzQzMjIzNTczOTksCiAgICAgICAgICAgICAgICAgICJEaWV0UXVhbGl0eSI6IDkuNTkzMzA5NzM5MTI4MzY5LAogICAgICAgICAgICAgICAgICAiU2xlZXBRdWFsaXR5IjogNi4wNjA5OTIxMjA1Nzc3MjUsCiAgICAgICAgICAgICAgICAgICJGYW1pbHlIaXN0b3J5UGFya2luc29ucyI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlRyYXVtYXRpY0JyYWluSW5qdXJ5IjogIjAiLAogICAgICAgICAgICAgICAgICAiSHlwZXJ0ZW5zaW9uIjogIjEiLAogICAgICAgICAgICAgICAgICAiRGlhYmV0ZXMiOiAiMCIsCiAgICAgICAgICAgICAgICAgICJEZXByZXNzaW9uIjogIjAiLAogICAgICAgICAgICAgICAgICAiU3Ryb2tlIjogIjAiLAogICAgICAgICAgICAgICAgICAiU3lzdG9saWNCUCI6IDkyLAogICAgICAgICAgICAgICAgICAiRGlhc3RvbGljQlAiOiA2MCwKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sVG90YWwiOiAxOTMuMTM4MTg2ODEwNjI5NiwKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sTERMIjogMTM3LjUxNzU1MDM3NjIxMjgsCiAgICAgICAgICAgICAgICAgICJDaG9sZXN0ZXJvbEhETCI6IDI1LjQ4MjQ2NzAzNTgwNjgxMywKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sVHJpZ2x5Y2VyaWRlcyI6IDMxMy42NjY3NDg3NjkyNjk1MywKICAgICAgICAgICAgICAgICAgIlVQRFJTIjogNTguOTkwOTIwOTYzMzM3OTQsCiAgICAgICAgICAgICAgICAgICJNb0NBIjogMTkuOTAyMjMzNjE1NzE4MTQ2LAogICAgICAgICAgICAgICAgICAiRnVuY3Rpb25hbEFzc2Vzc21lbnQiOiA1LjEwNDkxNDQ4NDAyMDkwNSwKICAgICAgICAgICAgICAgICAgIlRyZW1vciI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlJpZ2lkaXR5IjogIjEiLAogICAgICAgICAgICAgICAgICAiQnJhZHlraW5lc2lhIjogIjEiLAogICAgICAgICAgICAgICAgICAiUG9zdHVyYWxJbnN0YWJpbGl0eSI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlNwZWVjaFByb2JsZW1zIjogIjAiLAogICAgICAgICAgICAgICAgICAiU2xlZXBEaXNvcmRlcnMiOiAiMSIsCiAgICAgICAgICAgICAgICAgICJDb25zdGlwYXRpb24iOiAiMCIKICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgInBhdGllbnRfaWQiOiAiOWZhOTc4MjUtYTM0NS00MDY4LWE1ZDktM2ZkYTYwN2ZjOWIwIgogICAgICAgICB9"

    actual_output = model.base64_decode(data)

    expected_output = {
        "data": {
            "Age": 67,
            "Gender": "1",
            "Ethnicity": "2",
            "EducationLevel": "1",
            "BMI": 24.77259403457728,
            "Smoking": "0",
            "AlcoholConsumption": 13.941385740391004,
            "PhysicalActivity": 2.472534322357399,
            "DietQuality": 9.593309739128369,
            "SleepQuality": 6.060992120577725,
            "FamilyHistoryParkinsons": "0",
            "TraumaticBrainInjury": "0",
            "Hypertension": "1",
            "Diabetes": "0",
            "Depression": "0",
            "Stroke": "0",
            "SystolicBP": 92,
            "DiastolicBP": 60,
            "CholesterolTotal": 193.1381868106296,
            "CholesterolLDL": 137.5175503762128,
            "CholesterolHDL": 25.482467035806813,
            "CholesterolTriglycerides": 313.66674876926953,
            "UPDRS": 58.99092096333794,
            "MoCA": 19.902233615718146,
            "FunctionalAssessment": 5.104914484020905,
            "Tremor": "0",
            "Rigidity": "1",
            "Bradykinesia": "1",
            "PosturalInstability": "0",
            "SpeechProblems": "0",
            "SleepDisorders": "1",
            "Constipation": "0",
        },
        "patient_id": "9fa97825-a345-4068-a5d9-3fda607fc9b0",
    }

    assert actual_output == expected_output


def test_prepare_feature():
    model_service = model.ModelService(logged_model)

    test_data = {
        "Age": 67,
        "Gender": "1",
        "Ethnicity": "2",
        "EducationLevel": "1",
        "BMI": 24.77259403457728,
        "Smoking": "0",
        "AlcoholConsumption": 13.941385740391004,
        "PhysicalActivity": 2.472534322357399,
        "DietQuality": 9.593309739128369,
        "SleepQuality": 6.060992120577725,
        "FamilyHistoryParkinsons": "0",
        "TraumaticBrainInjury": "0",
        "Hypertension": "1",
        "Diabetes": "0",
        "Depression": "0",
        "Stroke": "0",
        "SystolicBP": 92,
        "DiastolicBP": 60,
        "CholesterolTotal": 193.1381868106296,
        "CholesterolLDL": 137.5175503762128,
        "CholesterolHDL": 25.482467035806813,
        "CholesterolTriglycerides": 313.66674876926953,
        "UPDRS": 58.99092096333794,
        "MoCA": 19.902233615718146,
        "FunctionalAssessment": 5.104914484020905,
        "Tremor": "0",
        "Rigidity": "1",
        "Bradykinesia": "1",
        "PosturalInstability": "0",
        "SpeechProblems": "0",
        "SleepDisorders": "1",
        "Constipation": "0",
    }

    preocessed_data = model_service.prepare_features(test_data)
    expected_output = pd.DataFrame

    assert expected_output == type(
        preocessed_data
    ), "Expected output should be pandas dataframe"
