import requests
import time


# List of functions:
# def GG_API_GET_RESPONSE(_endpoint, _headers): http_response
# def GG_API_GET_OBJECT(_endpoint, _headers): API_DATA []


# -----------------------
# INIT part
# -----------------------

# Set the base URL for the API
BASE_URL = "https://api.gitguardian.com/" # US based environment
#BASE_URL = "https://api.eu1.gitguardian.com/" # EU based environment

global debug
debug = True

global PARAMETER
PARAMETER = {
    "per_page": 100,
}

global HTTP_OK
HTTP_OK = 200

global HTTP_CREATED
HTTP_CREATED = 201

global HTTP_TOO_MANY_REQUESTS
HTTP_TOO_MANY_REQUESTS = 429

global DEFAULT_RETRY_DELAY
DEFAULT_RETRY_DELAY = 60 #by default, retry after 60 sec

# -----------------------
# Generic function to query the API w/o pagination on GET request & return the response object
# https://docs.gitguardian.com/api-docs/pagination
# -----------------------
def GG_API_GET_RESPONSE(_endpoint, _headers):
    _url = build_url(BASE_URL,_endpoint)
    while True:
        response = requests.get(_url, headers=_headers)

        if response.status_code == HTTP_OK:
            break             
        elif response.status_code == HTTP_TOO_MANY_REQUESTS:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                time_to_wait = int(retry_after)
            else:
                time_to_wait = DEFAULT_RETRY_DELAY 

            print(f"Rate limit reached from the API. Waiting {time_to_wait} seconds before retrying...")
            time.sleep(time_to_wait)
        else:
            raise Exception(f"Error communicating with GG API: Received HTTP status code {response.status_code} - {response.text}")

    return response

# -----------------------
# Generic function to query the API and manage pagination on GET request that return an object
# https://docs.gitguardian.com/api-docs/pagination
# -----------------------
def GG_API_GET_OBJECT(_endpoint, _headers):
    _url = build_url(BASE_URL,_endpoint)
    API_Data = []
    while True:
        response = requests.get(_url, headers=_headers)

        if response.status_code == HTTP_OK:
            API_Data += response.json()
            if "next" not in response.links:
                break
            _url = response.links["next"]["url"]              
        elif response.status_code == HTTP_TOO_MANY_REQUESTS:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                time_to_wait = int(retry_after)
            else:
                time_to_wait = DEFAULT_RETRY_DELAY

            print(f"Rate limit reached from the API. Waiting {time_to_wait} seconds before retrying...")
            time.sleep(time_to_wait)
        else:
            raise Exception(f"Error communicating with GG API: Received HTTP status code {response.status_code} - {response.text}")

    return API_Data


# -----------------------
# Generic function to query the API on POST request & return the http response object
# https://docs.gitguardian.com/api-docs/pagination
# -----------------------
def GG_API_POST(_endpoint,_body, _headers):
    _url = build_url(BASE_URL,_endpoint)
    if debug:
        print(f"[DEBUG]---- GG_API_POST _url = {_url} -----")
        print(f"[DEBUG]---- GG_API_POST _body = {_body} -----")
        
    while True:
        response = requests.post(_url,_body,headers=_headers)

        if response.status_code == HTTP_OK or response.status_code == HTTP_CREATED :
            break             
        elif response.status_code == HTTP_TOO_MANY_REQUESTS:
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                time_to_wait = int(retry_after)
            else:
                time_to_wait = DEFAULT_RETRY_DELAY

            print(f"Rate limit reached from the API. Waiting {time_to_wait} seconds before retrying...")
            time.sleep(time_to_wait)
        else:
            raise Exception(f"Error communicating with GG API: Received HTTP status code {response.status_code} - {response.text}")

    return response

# -----------------------
# Generic function to merge 2 strings and build a URL w/o checking the "/" in the middle
# -----------------------
def build_url(_prefix,_suffix):
    # Remove trailing slash from prefix (if any) and leading slash from suffix (if any)
    _prefix = _prefix.rstrip('/')
    _suffix = _suffix.lstrip('/')
    _url = f"{_prefix}/{_suffix}"
    
    return _url