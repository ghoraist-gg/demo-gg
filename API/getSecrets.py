import requests
import os
import json
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GITGUARDIAN_API_KEY")

# Set the base URL for the API
BASE_URL = "https://api.gitguardian.com"

# Set the headers for authentication
headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

# Function to list existing secrets
def list_secrets():
    url = f"{BASE_URL}/v1/incidents/secrets"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        API_Data = response.json()
        print(f"Number of incidents: {len(API_Data)}")
        
        for index, incident in enumerate(API_Data):
            print(f"Incident #{index+1} :")
            print(f"-----------")
            incidentData = json.dumps(incident, indent=4)
            print(incidentData)
            print(f"-----------")
            
if __name__ == "__main__":
    list_secrets()
