import os
import json
import gg_helpers
import time
from datetime import datetime
from dotenv import load_dotenv

# -----------------------
# AUTHENT part
# -----------------------

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GITGUARDIAN_API_KEY")

# Set the headers for authentication
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json; charset=UTF-8"
}


# -----------------------            
# List members
# -----------------------
def list_members():
    print(f"---- list_members -----")
    target = "members"
    
    try:
        allMembers = gg_helpers.GG_API_GET_OBJECT(target, HEADERS)                    
        print(f"Number of members: {len(allMembers)}")            
        for index, member in enumerate(allMembers):
            print(f"-----------")
            print(f"member #{index+1} :")
            print(f"-----------")
            incidentData = json.dumps(member, indent=4)
            print(incidentData)
            print(f"-----------")
    except Exception as e:
        print(f"Error Detected: {e}")

# -----------------------
# Function to list existing secrets
# https://api.gitguardian.com/docs#tag/Secret-Incidents
# -----------------------
def list_secrets():
    print(f"---- list_secrets -----")    
    target = "incidents/secrets"
    
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
# Assign a secret incident
# https://api.gitguardian.com/docs#tag/Secret-Incidents/operation/assign-incident
# parameter is mutually exclusive
# {
#   "email": "eric@gitguardian.com",
#   "member_id": 4295
# }
# -----------------------
def assignIncident(_incident_id,_member_id):
    print(f"---- assignIncident -----")
    target = f"incidents/secrets/{_incident_id}/assign"
    body = {
        "member_id": _member_id
    }
    try:
        assignResponse = gg_helpers.GG_API_POST(target,json.dumps(body),HEADERS)                    
        print(f"-----------")
        incidentData = json.dumps(assignResponse.json(), indent=4)
        print(incidentData)
        print(f"-----------")
    except Exception as e:
        print(f"Error Detected: {e}")


# -----------------------   
def tprint(msg):
    timestamp=datetime.now().strftime('%M:%S.%f')[:-3]
    print(timestamp, msg)


# -----------------------            
# MAIN function
# -----------------------
if __name__ == "__main__":
    #list_secrets()
    list_members()
    