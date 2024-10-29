import os
import gg_helpers
from dotenv import load_dotenv

# -----------------------
# AUTHENT part
# -----------------------

# Load API key from .env file
load_dotenv()
global API_KEY
API_KEY = os.getenv("GITGUARDIAN_API_KEY")

Hello World!

# Set the headers for authentication
global HEADERS
HEADERS = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json; charset=UTF-8"
}

# -----------------------
# run part
# -----------------------

def getHealthCheck():
    url = "v1/health"
    
    try:
        response = gg_helpers.GG_API_GET_RESPONSE(url, HEADERS)
        print(f"Response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error Detected: {e}")
    
if __name__ == "__main__":
    getHealthCheck()
