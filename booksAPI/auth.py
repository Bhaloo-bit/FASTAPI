from fastapi import Header, HTTPException

# in  production u add this in env
API_KEY = "m_secred_api_key"

def verify_api_key(x_api_key : str= Header()):
    "verify the API key from the request header."
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail = "Invalid API Key")
    