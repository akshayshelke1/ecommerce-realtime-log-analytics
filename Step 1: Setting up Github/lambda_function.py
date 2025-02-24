import boto3
import csv
from opensearchpy import OpenSearch

s3 = boto3.client('s3')

# OpenSearch Configuration
OPENSEARCH_HOST = "https://your-opensearch-domain.com"
INDEX_NAME = "logs-index"
auth = ('admin', 'YourPassword')  # Use SigV4 in production

client = OpenSearch(OPENSEARCH_HOST, http_auth=auth)

def lambda_handler(event, context):
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']
    
    # Read file from S3
    file_obj = s3.get_object(Bucket=bucket_name, Key=object_key)
    data = file_obj['Body'].read().decode('utf-8').splitlines()
    
    # Process CSV logs
    reader = csv.DictReader(data)
    for row in reader:
        log_entry = {
            "timestamp": row["timestamp"],
            "user_id": row["user_id"],
            "action": row["action"],
            "page": row["page"],
            "status_code": int(row["status_code"]),
            "amount_spent": float(row["amount_spent"])
        }
        client.index(index=INDEX_NAME, body=log_entry)

    return {"status": "Success"}
