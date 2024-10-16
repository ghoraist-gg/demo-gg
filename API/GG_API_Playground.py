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
    "Content-Type": "application/json; charset=UTF-8"
}


# -----------------------            
# List members
# -----------------------
def list_members():
    print(f"---- list_members -----")
    target = "v1/members"
    
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
    target = f"v1/incidents/secrets/{_incident_id}/assign"
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
# MAIN function
# -----------------------
if __name__ == "__main__":
    #list_secrets()
    #list_members()
    assignIncident("13780368",837753)
    
    
#13780368
#13780367

#837753
#851088
