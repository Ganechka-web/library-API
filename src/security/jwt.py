from datetime import datetime, timedelta
from typing import Any

from jose import jwt

from core.settings import SECRET_KEY, ALGORITHM


def get_signed_jwt(user_id: int) -> str:
    payload = {
        'user_id': user_id,
        'exp': datetime.now() + timedelta(hours=1)
    }
    encrypted_payload = jwt.encode(payload, 
                                   SECRET_KEY, 
                                   algorithm=ALGORITHM)
    return encrypted_payload


def get_jwt_payload(token: str) -> dict[str, Any]:
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=ALGORITHM
    )
    return payload
