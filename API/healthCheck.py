import requests
import os
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
def getHealthCheck():
    url = f"{BASE_URL}/v1/health"
    response = requests.get(url, headers=headers)
    print(f"Response: {response.status_code} - {response.text}")

if __name__ == "__main__":
    getHealthCheck()
