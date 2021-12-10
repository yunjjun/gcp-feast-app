from feast import FeatureStore
import os

cur_path = os.path.dirname(os.path.abspath(__file__))
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(cur_path, "env/mlops-feast-project-03527d1a5442.json")
store = FeatureStore(repo_path=cur_path)
entity_rows = [{"user_id": "v5zlw0"}]

feature_vector = store.get_online_features(
    features=[
    "user_transaction_count_7d:transaction_count_7d",
    "user_account_features:credit_score",
    "user_account_features:account_age_days",
    "user_account_features:user_has_2fa_installed",
    "user_has_fraudulent_transactions:user_has_fraudulent_transactions_7d"
],
    entity_rows=entity_rows
).to_dict()

print(feature_vector)