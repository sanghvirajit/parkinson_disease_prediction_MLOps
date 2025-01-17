FROM python:3.9.7-slim

RUN pip install -U pip

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY [ "app/api/local_api.py", "./" ]

EXPOSE 9696

# Set environment variables
ENV MLFLOW_TRACKING_URI=http://mlflow:5000
ENV MODEL_NAME="parkinson-disease-models"
ENV EXPERIMENT_NAME="parkinson-disease-prediction-experiment"

ENTRYPOINT [ "gunicorn", "--bind=0.0.0.0:9696", "local_api:app", "--timeout", "90", "--workers", "3"]
