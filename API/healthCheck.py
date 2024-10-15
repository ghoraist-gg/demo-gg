import os
import gg_helpers
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv("GITGUARDIAN_API_KEY")

# Set the headers for authentication
headers = {
    "Authorization": f"Token {API_KEY}",
    "Content-Type": "application/json"
}

def getHealthCheck():
    url = "v1/health"
    response = gg_helpers.GG_API_GET_RESPONSE(url, headers)
    print(f"Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    getHealthCheck()
