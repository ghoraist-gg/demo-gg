# Save data to an AWS bucket 
import boto3
import pymongo
from typing import Dict
 
def aws_upload(data: Dict):
    database = boto3.resource(
        service_name='s3',
        region_name='us-east-2',
        aws_access_key_id='AKIAF6BAFJKR45SAWSZ5',
        aws_secret_access_key="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" #comment 
    )
    database.push(data) 
 
MONGO_URI = "mongodb+srv://testuser:hub24aoeu@gg-is-awesome-gg273.mongodb.net/test?retryWrites=true&w=majority"

def pull_data_from_mongo(query: Dict): 
    return pymongo.connect(MONGO_URI).fetch(query)
