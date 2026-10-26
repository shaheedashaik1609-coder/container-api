import os
import secrets
from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_key(key: str | None = Security(api_key_header)):
    expected_key = os.getenv("API_KEY","")
    if not expected_key or key != expected_key or not secrets.compare_digest(key, expected_key):
        raise HTTPException(status_code=401, detail="Invalid API Key")
