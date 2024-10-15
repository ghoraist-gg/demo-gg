import os
import json
import gg_helpers
from dotenv import load_dotenv

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
    target = "v1/incidents/secrets"
    
    try:
        allMySecrets = gg_helpers.GG_API_GET_OBJECT(target, HEADERS)                    
        print(f"Number of incidents: {len(allMySecrets)}")            
        for index, incident in enumerate(allMySecrets):
            print(f"Incident #{index+1} :")
            print(f"-----------")
            incidentData = json.dumps(incident, indent=4)
            print(incidentData)
            print(f"-----------")
    except Exception as e:
        print(f"Error Detected: {e}")

# -----------------------            
# MAIN function
# -----------------------
if __name__ == "__main__":
    list_secrets()
