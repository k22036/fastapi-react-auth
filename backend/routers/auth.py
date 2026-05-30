from datetime import datetime, timezone
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from repositories.blacklisted_token import (
    BlacklistedTokenRepository,
    get_blacklisted_token_repository,
)
from repositories.user import UserRepository, get_user_repository
from schemas import MessageResponse, SignInRequest, SignUpRequest, TokenResponse
from security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)

router = APIRouter(prefix="/auth", tags=["auth"])
_bearer_scheme = HTTPBearer()

# 型エイリアス: リポジトリの依存注入
_UserRepo = Annotated[UserRepository, Depends(get_user_repository)]
_TokenRepo = Annotated[
    BlacklistedTokenRepository, Depends(get_blacklisted_token_repository)
]


# ---------------------------------------------------------------------------
# Dependencies
# ---------------------------------------------------------------------------


def _get_validated_token(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme),
) -> tuple[str, dict]:
    """JWT を検証し、トークン文字列とペイロードを返す FastAPI 依存関数。
    期限切れ・不正なトークンの場合は HTTPException (401) を送出する。
    """
    token = credentials.credentials
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token, payload


# 型エイリアス: 検証済みトークン (raw_token, payload)
_ValidatedToken = Annotated[tuple[str, dict], Depends(_get_validated_token)]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


@router.post(
    "/signup",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="新規ユーザー登録",
)
def signup(request: SignUpRequest, user_repo: _UserRepo):
    if user_repo.find_by_email(request.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user_repo.create(request.email, get_password_hash(request.password))
    return MessageResponse(message="User created successfully")


@router.post(
    "/signin",
    response_model=TokenResponse,
    summary="サインイン（JWTトークン取得）",
)
def signin(request: SignInRequest, user_repo: _UserRepo):
    user = user_repo.find_by_email(request.email)

    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive",
        )

    return TokenResponse(access_token=create_access_token(subject=user.email))


@router.post(
    "/signout",
    response_model=MessageResponse,
    summary="サインアウト（トークン無効化）",
)
def signout(token_data: _ValidatedToken, token_repo: _TokenRepo):
    token, payload = token_data

    if token_repo.is_blacklisted(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has already been invalidated",
        )

    token_repo.add(token, datetime.fromtimestamp(payload["exp"], tz=timezone.utc))
    return MessageResponse(message="Successfully signed out")
