import requests
import os
import json
from dotenv import load_dotenv

# -----------------------
# INIT part
# -----------------------

# Set the base URL for the API
BASE_URL = "https://api.gitguardian.com/v1/"


# -----------------------
# AUTHENT part
# -----------------------

# Load API key from .env file
load_dotenv()
global API_KEY
API_KEY = os.getenv("GITGUARDIAN_API_KEY")

# Set the headers for authentication
global HEADERS
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

# -----------------------
# Function to list existing secrets
# https://api.gitguardian.com/docs#tag/Secret-Incidents
# -----------------------
def list_secrets():
    target = "incidents/secrets"
    allMySecrets = GG_API_GET(target)            
    
    print(f"Number of incidents: {len(allMySecrets)}")
        
    for index, incident in enumerate(allMySecrets):
        print(f"Incident #{index+1} :")
        print(f"-----------")
        incidentData = json.dumps(incident, indent=4)
        print(incidentData)
        print(f"-----------")

# -----------------------
# Generic function to query the API and manage pagination
# https://docs.gitguardian.com/api-docs/pagination
# -----------------------
def GG_API_GET(_endpoint ):
    _url = f"{BASE_URL}{_endpoint}"
    _headers = HEADERS
    API_Data = []    
    while True:
        response = requests.get(_url, headers=_headers)
        assert response.status_code == 200
        API_Data += response.json()
        if "next" not in response.links:
            break
        _url = response.links["next"]["url"]  
    return API_Data

# -----------------------            
# MAIN function
# -----------------------
if __name__ == "__main__":
    list_secrets()
