import requests
import time

# List of functions:
# def GG_API_GET_RESPONSE(_endpoint, _headers): http_response
# def GG_API_GET_OBJECT(_endpoint, _headers): API_DATA []
# def GG_API_POST(_endpoint,_body, _headers): http_response

# -----------------------
# INIT part
# -----------------------

# Set the base URL for the API
BASE_URL = "https://api.gitguardian.com/v1" # US based environment
#BASE_URL = "https://api.eu1.gitguardian.com/v1" # EU based environment

debug = True

PARAMETER = {
    "per_page": 100,
}

HTTP_OK = 200
HTTP_CREATED = 201
HTTP_REQUEST_OK = 204
HTTP_TOO_MANY_REQUESTS = 429
HTTP_BAD_GATEWAY = 502

DEFAULT_RETRY_DELAY = 10 #by default, retry after 10 sec in case of a 429

# -----------------------
# Generic function to query the API w/o pagination on GET request & return the response object
# https://docs.gitguardian.com/api-docs/pagination
# -----------------------
def GG_API_GET_RESPONSE(_endpoint, _headers):
    _url = build_url(BASE_URL,_endpoint)
    if debug: print(f"[DEBUG][GET_OBJECT] _url= {_url}")
    while True:
        response = requests.get(_url, headers=_headers, params=PARAMETER)
        if debug: print(f"[DEBUG][GET_RESPONSE] response.status_code= {response.status_code}")
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
    firstIteration = True
    while True:
        if debug: print(f"[DEBUG][GET_OBJECT] _url= {_url}")
        if firstIteration : response = requests.get(_url, headers=_headers, params=PARAMETER)
        else : response = requests.get(_url, headers=_headers)
        firstIteration = False
        if debug: print(f"[DEBUG][GET_OBJECT] response.status_code= {response.status_code}")
        if response.status_code == HTTP_OK:
            API_Data += response.json()
            if "next" not in response.links:
                break
            else :
                _url = response.links["next"]["url"]              
        elif response.status_code == HTTP_TOO_MANY_REQUESTS or (not firstIteration and response.status_code == HTTP_BAD_GATEWAY) :
            retry_after = response.headers.get("Retry-After")
            if retry_after:
                time_to_wait = int(retry_after)
            else:
                time_to_wait = DEFAULT_RETRY_DELAY

            print(f"Error {response.status_code} from the API. Waiting {time_to_wait} seconds before retrying...")
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
        print(f"[DEBUG][API_POST] _url = {_url} -----")
        print(f"[DEBUG][API_POST] _body = {_body} -----")
        
    while True:
        response = requests.post(_url,_body,headers=_headers)

        if response.status_code == HTTP_OK or response.status_code == HTTP_CREATED or response.status_code == HTTP_REQUEST_OK:
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