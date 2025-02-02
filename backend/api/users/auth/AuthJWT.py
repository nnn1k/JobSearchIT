from datetime import timedelta, datetime
from pathlib import Path
from typing import Optional, Tuple

import jwt
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'

class AuthJWT:
    private_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "auth" / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 60_000
    refresh_token_expire_days: int = 7
    TOKEN_TYPE_FIELD = 'type'
    ACCESS_TOKEN_TYPE = 'access'
    REFRESH_TOKEN_TYPE = 'refresh'

    def encode_jwt(
            self,
            payload: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        private_key = self.private_key_path.read_text()
        to_encode = payload.copy()
        now = datetime.utcnow()
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=self.access_token_expire_minutes)
        to_encode.update(exp=expire, iat=now)
        encoded = jwt.encode(to_encode, private_key, algorithm=self.algorithm)
        return encoded

    def decode_jwt(
            self,
            token: str | bytes,
    ):
        public_key: str = self.public_key_path.read_text()
        decoded = jwt.decode(token, public_key, algorithms=[self.algorithm])
        return decoded

    def create_jwt(
            self,
            token_type: str,
            token_data: dict,
            expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {self.TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(token_data)
        return self.encode_jwt(
            payload=jwt_payload,
            expire_timedelta=expire_timedelta
        )

    def create_access_token(self, id: int, user_type: str) -> str:
        jwt_payload = {
            'sub': str(id),
            'type': user_type
        }
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload
        )

    def create_refresh_token(self, id: int, user_type: str) -> str:
        jwt_payload = {
            'sub': str(id),
            'type': user_type
        }
        return self.create_jwt(
            token_type=self.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=self.refresh_token_expire_days)
        )

    def token_refresh(self, refresh_token: str) -> tuple[str, str] | tuple[None, None]:
        try:
            decoded_refresh_token = self.decode_jwt(refresh_token)
            id = decoded_refresh_token.get("sub")
            user_type = decoded_refresh_token.get("type")
            access_token = self.create_access_token(id=id, user_type=user_type)
            refresh_token = self.create_refresh_token(id=id, user_type=user_type)
            return access_token, refresh_token
        except Exception as e:
            print(f'error:{e}')
            return None, None


jwt_token = AuthJWT()
