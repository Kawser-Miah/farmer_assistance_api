import requests
import os
from dotenv import load_dotenv
from fastapi import Header, HTTPException
from jose import jwt


load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
JWKS_URL = f"{SUPABASE_URL}/auth/v1/.well-known/jwks.json"

jwks = requests.get(JWKS_URL).json()


def decode_supabase_jwt(authorization: str = Header(...)) -> str:
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    token = authorization.split(" ")[1]

    try:
        # Read token header
        unverified_header = jwt.get_unverified_header(token)

        # Find matching public key
        key = next(
            k for k in jwks["keys"]
            if k["kid"] == unverified_header["kid"]
        )


        # Decode & VERIFY
        payload = jwt.decode(
            token,
            key,
            algorithms=["ES256"],
            audience="authenticated",
            issuer=f"{SUPABASE_URL}/auth/v1",
        )
       

        return payload["sub"]  # auth.users.id (UUID as string)

    except Exception as e:
        print(f"JWT decode error: {str(e)}")  # Debug log
        raise HTTPException(status_code=401, detail="Invalid or expired token")