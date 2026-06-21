from fastapi import Depends, HTTPException, Security
from fastapi.security import OAuth2AuthorizationCodeBearer
from keycloak import KeycloakOpenID
import os

# Конфигурация Keycloak (замените на реальные значения через переменные окружения)
KEYCLOAK_SERVER_URL = os.getenv("KEYCLOAK_SERVER_URL", "https://keycloak.example.com")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "lexicon")
KEYCLOAK_CLIENT_ID = os.getenv("KEYCLOAK_CLIENT_ID", "intake-gateway")
KEYCLOAK_CLIENT_SECRET = os.getenv("KEYCLOAK_CLIENT_SECRET", "")

keycloak_openid = KeycloakOpenID(
    server_url=KEYCLOAK_SERVER_URL,
    client_id=KEYCLOAK_CLIENT_ID,
    realm_name=KEYCLOAK_REALM,
    client_secret_key=KEYCLOAK_CLIENT_SECRET
)

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/auth",
    tokenUrl=f"{KEYCLOAK_SERVER_URL}/realms/{KEYCLOAK_REALM}/protocol/openid-connect/token",
)

async def get_current_user(token: str = Security(oauth2_scheme)):
    try:
        userinfo = keycloak_openid.userinfo(token)
        return userinfo
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")

def require_role(role: str):
    def role_checker(user: dict = Depends(get_current_user)):
        realm_roles = user.get("realm_access", {}).get("roles", [])
        if role not in realm_roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return role_checker
