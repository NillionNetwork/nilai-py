import enum
from typing import Optional
from pydantic import BaseModel
from secp256k1 import PrivateKey as NilAuthPrivateKey, PublicKey as NilAuthPublicKey


class NilAuthInstance(enum.Enum):
    SANDBOX = "https://nilauth.sandbox.app-cluster.sandbox.nilogy.xyz"
    PRODUCTION = "https://nilauth-cf7f.nillion.network/"


class AuthType(enum.Enum):
    API_KEY = "API_KEY"
    DELEGATION_TOKEN = "DELEGATION_TOKEN"


class DelegationServerConfig(BaseModel):
    nilauth_url: str = NilAuthInstance.SANDBOX.value
    expiration_time: Optional[int] = 60
    token_max_uses: Optional[int] = 1


class RequestType(enum.Enum):
    DELEGATION_TOKEN_REQUEST = "DELEGATION_TOKEN_REQUEST"
    DELEGATION_TOKEN_RESPONSE = "DELEGATION_TOKEN_RESPONSE"


class DelegationTokenRequest(BaseModel):
    type: RequestType = RequestType.DELEGATION_TOKEN_REQUEST
    public_key: str


class DelegationTokenResponse(BaseModel):
    type: RequestType = RequestType.DELEGATION_TOKEN_RESPONSE
    delegation_token: str


DefaultDelegationTokenServerConfig = DelegationServerConfig(
    nilauth_url=NilAuthInstance.SANDBOX.value,
    expiration_time=60,
    token_max_uses=1,
)

__all__ = [
    "NilAuthPrivateKey",
    "NilAuthPublicKey",
    "NilAuthInstance",
    "AuthType",
    "DelegationTokenRequest",
    "DelegationTokenResponse",
    "DefaultDelegationTokenServerConfig",
]
