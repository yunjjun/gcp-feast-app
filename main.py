import os
from pathlib import Path
from fastapi import FastAPI, Response, HTTPException, status
from feast import FeatureStore
import googleapiclient.discovery

ROOT_DIR = Path(__file__).parent.parent
app = FastAPI()

cur_path = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(cur_path, "env/gcp-mlops-feast-project-7afb5fd3d3d6.json")
PROJECT_ID= "gcp-mlops-feast-project"
BUCKET_NAME= "gcp-mlops-feast-project-bucket"
BIGQUERY_DATASET_NAME="gcp_mlops_feast_dataset"
AI_PLATFORM_MODEL_NAME="gcp_mlops_feast_dataset"

store = FeatureStore(repo_path=cur_path)

@app.get("/")
def root():
    return "Fraud Detection !"

@app.post("/predict")
def predict(entity):
    entity_rows = [{"user_id":entity}]
    feature_vector = store.get_online_features(
        features=[
        "user_transaction_count_7d:transaction_count_7d",
        "user_account_features:credit_score",
        "user_account_features:account_age_days",
        "user_account_features:user_has_2fa_installed",
        "user_has_fraudulent_transactions:user_has_fraudulent_transactions_7d"
    ],
        entity_rows=[{"user_id":entity}]
    ).to_dict()
    
    del feature_vector["user_id"]

    print(feature_vector.values())
    instances = [
        [feature_values[i] for feature_values in feature_vector.values()]
        for i in range(len(entity_rows))
    ]
    
    service = googleapiclient.discovery.build('ml', 'v1')
    name = f'projects/{PROJECT_ID}/models/{AI_PLATFORM_MODEL_NAME}'
    
    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    return response

@app.get("/healthcheck")
def healthcheck():
    return {"status": "ok"}
