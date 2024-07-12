# Parkinson-Disease---MLOps Pipeline

This repository contains a simplified MLOps platform (including training, serving and monitoring).
The goal of this project was to show what MLOps tool do and how they work together.

This project was inspired by the [MLOps Zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp) course provided by [DataTalks.Club](https://datatalks.club/).

# Context

Parkinson Disease is a brain neurological disorder. It leads to shaking of the body, hands and provides stiffness to the body. No proper cure or treatment is available yet at the advanced stage. Treatment is possible only when done at the early or onset of the disease. These will not only reduce the cost of the disease but will also possibly save a life. Most methods available can detect Parkinson in an advanced stage; which means loss of approx.. 60% dopamine in basal ganglia and is responsible for controlling the movement of the body with a small amount of dopamine. More than 145,000 people have been found alone suffering in the U.K and in India, almost one million population suffers from this disease and it’s spreading fast in the entire world.

The main objective of this project is to understand what is Parkinson’s disease and to detect the early onset of the disease and to apply what has been learned during the MLOps Zoomcamp course to build a MLOps pipeline for Parkinson-Disease Prediction.

# Dataset

This dataset comprises comprehensive health information for 2,105 patients diagnosed with Parkinson's Disease, each uniquely identified with IDs ranging from 3058 to 5162. The dataset includes demographic details, lifestyle factors, medical history, clinical measurements, cognitive and functional assessments, symptoms, and a diagnosis indicator. This dataset is valuable for researchers and data scientists aiming to explore factors associated with Parkinson's Disease, develop predictive models, and conduct statistical analyses.

The original dataset is available at [here](https://www.kaggle.com/datasets/rabieelkharoua/parkinsons-disease-dataset-analysis/data)

### Dataset Overview

Demographic Details

1. PatientID: A unique identifier assigned to each patient (3058 to 5162).
2. Age: The age of the patients ranges from 50 to 90 years.
3. Gender: Gender of the patients, where 0 represents Male and 1 represents Female.
4. Ethnicity: The ethnicity of the patients, coded as follows:
   A. Caucasian
   B. African American
   C. Asian
   D. Other
5. EducationLevel: The education level of the patients, coded as follows:
   A. None
   B: High School
   C. Bachelor's
   D. Higher

Lifestyle Factors

1. BMI: Body Mass Index of the patients, ranging from 15 to 40.
2. Smoking: Smoking status, where 0 indicates No and 1 indicates Yes.
3. AlcoholConsumption: Weekly alcohol consumption in units, ranging from 0 to 20.
4. PhysicalActivity: Weekly physical activity in hours, ranging from 0 to 10.
5. DietQuality: Diet quality score, ranging from 0 to 10.
6. SleepQuality: Sleep quality score, ranging from 4 to 10.

Medical History

1. FamilyHistoryParkinsons: Family history of Parkinson's Disease, where 0 indicates No and 1 indicates Yes.
2. TraumaticBrainInjury: History of traumatic brain injury, where 0 indicates No and 1 indicates Yes.
3. Hypertension: Presence of hypertension, where 0 indicates No and 1 indicates Yes.
4. Diabetes: Presence of diabetes, where 0 indicates No and 1 indicates Yes.
5. Depression: Presence of depression, where 0 indicates No and 1 indicates Yes.
6. Stroke: History of stroke, where 0 indicates No and 1 indicates Yes.

Clinical Measurements

1. SystolicBP: Systolic blood pressure, ranging from 90 to 180 mmHg.
2. DiastolicBP: Diastolic blood pressure, ranging from 60 to 120 mmHg.
3. CholesterolTotal: Total cholesterol levels, ranging from 150 to 300 mg/dL.
4. CholesterolLDL: Low-density lipoprotein cholesterol levels, ranging from 50 to 200 mg/dL.
5. CholesterolHDL: High-density lipoprotein cholesterol levels, ranging from 20 to 100 mg/dL.
6. CholesterolTriglycerides: Triglycerides levels, ranging from 50 to 400 mg/dL.

Cognitive and Functional Assessments

1. UPDRS: Unified Parkinson's Disease Rating Scale score, ranging from 0 to 199. Higher scores indicate greater severity of the disease.
2. MoCA: Montreal Cognitive Assessment score, ranging from 0 to 30. Lower scores indicate cognitive impairment.
3. FunctionalAssessment: Functional assessment score, ranging from 0 to 10. Lower scores indicate greater impairment.

Symptoms

1. Tremor: Presence of tremor, where 0 indicates No and 1 indicates Yes.
2. Rigidity: Presence of muscle rigidity, where 0 indicates No and 1 indicates Yes.
3. Bradykinesia: Presence of bradykinesia (slowness of movement), where 0 indicates No and 1 indicates Yes.
4. PosturalInstability: Presence of postural instability, where 0 indicates No and 1 indicates Yes.
5. SpeechProblems: Presence of speech problems, where 0 indicates No and 1 indicates Yes.
6. SleepDisorders: Presence of sleep disorders, where 0 indicates No and 1 indicates Yes.
7. Constipation: Presence of constipation, where 0 indicates No and 1 indicates Yes.
8. Diagnosis: Diagnosis status for Parkinson's Disease, where 0 indicates No and 1 indicates Yes.
9. DoctorInCharge: This column contains confidential information about the doctor in charge, with "DrXXXConfid" as the value for all patients.

# MLOps pipeline

to be continued...

# How to use

Prerequisite: Install Docker (Windows: Docker Desktop)

Download repository from GitHub

´´´bash
git clone https://github.com/sanghvirajit/Parkinson-Disease---MLOps-Pipeline.git
cd Parkinson-Disease---MLOps-Pipeline
pip install -r requirements.txt
´´´

Best Practices are used for linting and formatting. 
All the dependencies are written in the requirements.ci.txt. Lint section is also added in the Makefile

Run the following code to use it

´´´bash
pip install -r requirements.ci.txt
Make lint
´´´

# AWS Cloud for streaming. 

AWS credentials can be set as Enviromental Variables as follow

´´´bash
export AWS_ACCESS_KEY_ID="AWS_ACCESS_KEY_ID"
export AWS_SECRET_ACCESS_KEY="AWS_SECRET_ACCESS_KEY"
export AWS_DEFAULT_REGION="AWS_DEFAULT_REGION"
´´´

# MLFlow for Experiemental Tracking

MLFlow experiment name can be set as enviromental variable as follow:

export EXPERIMENT_NAME="parkinson-disease-prediction-experiment"

## Running the Docker Compose

To start the docker compose run the following commands in terminal

´´´bash
./scripts/start.sh
´´´

The command will start the docker compose.

### Access individual services

´´´bash
mage: http://localhost:6789
mlflow: http://localhost:5000
´´´

# Mage as Orchestration

Mage is employed for the orchestration. Mage can be access at ´´´bash http://localhost:5000 ´´´. Under the Pipelines, 4 Pipelines for the training of Linear Regression, Logistic Regression, XGBoost and CatBoost are implemented.


# MLFlow expriements

Linear Regression, Logistic Regression, XGBoost and CatBoost models were tested. The main focus of the project was not to find the best model but to work on the best MLOps technologies so the best model amoung the 4 was choosen. CatBoost was not anyway giving bad results. The Accuracy of the CatBoost Model is 96% with RMSE of 0.20.

All the experiements were logged in the MLFLOW which can be access at ´´´bash http://localhost:5000 ´´´. The Best Models among the XGBoost and CatBoost were registred with the MLFLow model registry. 

CatBoost Model can be find under "Production" tag and XGBoost Model can be find under "Staging".


### Save the Artifacts of the best model from the MLFlow Registry to S3 Bucket on AWS

The artifacts of the best model (CatBoost) was then loaded and save to the S3 Bucket of the AWS, from where it will be loaded later.

save the RUN_ID of the best model as an enviroment variable

´´´bash
export RUN_ID="6f4c13e86ae94d7a958349c35af3fbb1"
´´´

## Putting everything to Docker

### Configuring AWS CLI to run in Docker

´´´´bash
export AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY"
export AWS_DEFAULT_REGION="YOUR_REGION"
´´´

### Build and Run Docker with all enviromental variables

´´´´bash
docker build -t parkinson-disease-prediction:latest .

docker run -it --rm \
    -p 9696:9696 \
    -e RUN_ID="${RUN_ID}" \
    -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    parkinson-disease-prediction:latest
´´´