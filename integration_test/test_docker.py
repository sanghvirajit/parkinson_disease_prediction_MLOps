import requests
import json

from deepdiff import DeepDiff

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49653921083489861581538707770444738268127167767589683202",
                "data": "ewogICAgICAgICAgICAiZGF0YSI6IHsKICAgICAgICAgICAgICAgICAgIkFnZSI6IDY3LAogICAgICAgICAgICAgICAgICAiR2VuZGVyIjogIjEiLAogICAgICAgICAgICAgICAgICAiRXRobmljaXR5IjogIjIiLAogICAgICAgICAgICAgICAgICAiRWR1Y2F0aW9uTGV2ZWwiOiAiMSIsCiAgICAgICAgICAgICAgICAgICJCTUkiOiAyNC43NzI1OTQwMzQ1NzcyOCwKICAgICAgICAgICAgICAgICAgIlNtb2tpbmciOiAiMCIsCiAgICAgICAgICAgICAgICAgICJBbGNvaG9sQ29uc3VtcHRpb24iOiAxMy45NDEzODU3NDAzOTEwMDQsCiAgICAgICAgICAgICAgICAgICJQaHlzaWNhbEFjdGl2aXR5IjogMi40NzI1MzQzMjIzNTczOTksCiAgICAgICAgICAgICAgICAgICJEaWV0UXVhbGl0eSI6IDkuNTkzMzA5NzM5MTI4MzY5LAogICAgICAgICAgICAgICAgICAiU2xlZXBRdWFsaXR5IjogNi4wNjA5OTIxMjA1Nzc3MjUsCiAgICAgICAgICAgICAgICAgICJGYW1pbHlIaXN0b3J5UGFya2luc29ucyI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlRyYXVtYXRpY0JyYWluSW5qdXJ5IjogIjAiLAogICAgICAgICAgICAgICAgICAiSHlwZXJ0ZW5zaW9uIjogIjEiLAogICAgICAgICAgICAgICAgICAiRGlhYmV0ZXMiOiAiMCIsCiAgICAgICAgICAgICAgICAgICJEZXByZXNzaW9uIjogIjAiLAogICAgICAgICAgICAgICAgICAiU3Ryb2tlIjogIjAiLAogICAgICAgICAgICAgICAgICAiU3lzdG9saWNCUCI6IDkyLAogICAgICAgICAgICAgICAgICAiRGlhc3RvbGljQlAiOiA2MCwKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sVG90YWwiOiAxOTMuMTM4MTg2ODEwNjI5NiwKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sTERMIjogMTM3LjUxNzU1MDM3NjIxMjgsCiAgICAgICAgICAgICAgICAgICJDaG9sZXN0ZXJvbEhETCI6IDI1LjQ4MjQ2NzAzNTgwNjgxMywKICAgICAgICAgICAgICAgICAgIkNob2xlc3Rlcm9sVHJpZ2x5Y2VyaWRlcyI6IDMxMy42NjY3NDg3NjkyNjk1MywKICAgICAgICAgICAgICAgICAgIlVQRFJTIjogNTguOTkwOTIwOTYzMzM3OTQsCiAgICAgICAgICAgICAgICAgICJNb0NBIjogMTkuOTAyMjMzNjE1NzE4MTQ2LAogICAgICAgICAgICAgICAgICAiRnVuY3Rpb25hbEFzc2Vzc21lbnQiOiA1LjEwNDkxNDQ4NDAyMDkwNSwKICAgICAgICAgICAgICAgICAgIlRyZW1vciI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlJpZ2lkaXR5IjogIjEiLAogICAgICAgICAgICAgICAgICAiQnJhZHlraW5lc2lhIjogIjEiLAogICAgICAgICAgICAgICAgICAiUG9zdHVyYWxJbnN0YWJpbGl0eSI6ICIwIiwKICAgICAgICAgICAgICAgICAgIlNwZWVjaFByb2JsZW1zIjogIjAiLAogICAgICAgICAgICAgICAgICAiU2xlZXBEaXNvcmRlcnMiOiAiMSIsCiAgICAgICAgICAgICAgICAgICJDb25zdGlwYXRpb24iOiAiMCIKICAgICAgICAgICAgICAgfSwKICAgICAgICAgICAgInBhdGllbnRfaWQiOiAiOWZhOTc4MjUtYTM0NS00MDY4LWE1ZDktM2ZkYTYwN2ZjOWIwIgogICAgICAgICB9",
                "approximateArrivalTimestamp": 1720978801.315,
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49653921083489861581538707770444738268127167767589683202",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::058264402883:role/lambda-kinesis-role",
            "awsRegion": "eu-central-1",
            "eventSourceARN": "arn:aws:kinesis:eu-central-1:058264402883:stream/parkinson-input-stream",
        }
    ]
}


url = "http://localhost:8080/2015-03-31/functions/function/invocations"
actual_response = requests.post(url, json=event).json()
print(f"Actual response: {json.dumps(actual_response, indent=2)}")

expected_response = {
                        'predictions': [
                                    {'model': 'parkinson_disease_prediction_model', 
                                        'version': 'integration_test', 
                                        'prediction': {
                                                        'parkinson_diseases_prediction': 'Yes', 
                                                        'patient_id': '9fa97825-a345-4068-a5d9-3fda607fc9b0'
                                                    }
                                    }
                                ]
                    }
print(f"Expected response: {json.dumps(expected_response, indent=2)}")

diff = DeepDiff(actual_response, expected_response)

assert 'values_changed' not in diff
assert 'type_changes' not in diff