from datetime import timedelta, datetime
from pathlib import Path

import jwt
from pydantic import BaseModel

from backend.core.config.settings import settings


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class AuthJWT:
    private_key_path: Path = settings.jwt.private_key
    public_key_path: Path = settings.jwt.public_key
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 30
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

    def create_access_token(self, user_id: int, user_type: str) -> str:
        jwt_payload = {
            'sub': str(user_id),
            'type': user_type
        }
        return self.create_jwt(
            token_type=self.ACCESS_TOKEN_TYPE,
            token_data=jwt_payload
        )

    def create_refresh_token(self, user_id: int, user_type: str) -> str:
        jwt_payload = {
            'sub': str(user_id),
            'type': user_type
        }
        return self.create_jwt(
            token_type=self.REFRESH_TOKEN_TYPE,
            token_data=jwt_payload,
            expire_timedelta=timedelta(days=self.refresh_token_expire_days)
        )


jwt_token = AuthJWT()
