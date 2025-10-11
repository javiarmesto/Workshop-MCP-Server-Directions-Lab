"""
azure_auth.py

Objective:
---------
Manage OAuth2 authentication with Azure AD (Entra ID) using the Client Credentials flow,
including token cache and async helpers to obtain and renew the access token.

This module centralizes token acquisition to access the Business Central API from Python,
following security and efficiency best practices.

References:
- https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-client-creds-grant-flow
- https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/azure-active-directory
"""

# =============================
# IMPORTS AND DEPENDENCIES
# =============================
import asyncio
import httpx
from datetime import datetime, timedelta
from typing import Optional
from config import config


# =============================
# MAIN TOKEN MANAGEMENT CLASS
# =============================
class AzureTokenManager:
    def __init__(self):
        # Current token and expiration
        self._token: Optional[str] = None
        self._expires: Optional[datetime] = None
        # Access scope for Business Central
        self._scope = "https://api.businesscentral.dynamics.com/.default"


    # =============================
    # PRIVATE METHOD: Token valid?
    # =============================
    def _valid(self) -> bool:
        return (
            self._token is not None
            and self._expires is not None
            and datetime.utcnow() < self._expires
        )


    # =============================
    # GET TOKEN (public, preferred)
    # =============================
    async def get_token(self) -> Optional[str]:
        """
        Returns a valid token, renewing if necessary.
        Returns None if Azure AD credentials are not configured.
        """
        # Check if we have Azure AD credentials configured
        if not config.azure_ad.client_id or not config.azure_ad.client_secret or not config.azure_ad.tenant_id:
            return None
        
        if self._valid():
            return self._token
        return await self._fetch()


    # =============================
    # PRIVATE METHOD: Request new token from Azure AD
    # =============================
    async def _fetch(self) -> Optional[str]:
        url = f"{config.azure_ad.authority}/oauth2/v2.0/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": config.azure_ad.client_id,
            "client_secret": config.azure_ad.client_secret,
            "scope": self._scope
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        async with httpx.AsyncClient() as cli:
            resp = await cli.post(url, data=data, headers=headers, timeout=30)
        if resp.status_code == 200:
            j = resp.json()
            self._token = j["access_token"]
            self._expires = datetime.utcnow() + timedelta(seconds=j.get("expires_in", 3600))
            return self._token
        print(f"[ERROR] Azure AD Token: {resp.status_code}")
        return None


    # =============================
    # ALTERNATIVE METHOD: Request token (simulates Postman)
    # =============================
    async def _acquire_new_token(self) -> Optional[str]:
        """
        Acquires a new token from Azure AD using a URL-encoded body (useful for advanced debugging).
        """
        token_url = f"{config.azure_ad.authority}/oauth2/v2.0/token"
        # Build the body as URL-encoded
        form = {
            "grant_type":    "client_credentials",
            "client_id":     config.azure_ad.client_id,
            "client_secret": config.azure_ad.client_secret,
            "scope":         self._scope
        }
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                # USE content= and urllib.parse.urlencode to simulate Postman exactly
                import urllib.parse
                payload = urllib.parse.urlencode(form)
                response = await client.post(
                    token_url,
                    content=payload,
                    headers=headers
                )
                # DEBUG: if it fails, see full body
                if response.status_code != 200:
                    print(f"[DEBUG] Token request failed ({response.status_code}): {response.text}")
                    return None
                data = response.json()
                access_token = data["access_token"]
                expires_in   = data.get("expires_in", 3600)
                # cache
                self._token_cache   = access_token
                self._token_expires = datetime.now() + timedelta(seconds=expires_in - 300)
                return access_token
        except Exception as e:
            print(f"[ERROR] Exception acquiring token: {e}")
            return None


# =============================
# GLOBAL SINGLETON FOR USE ACROSS THE PROJECT
# =============================
token_manager = AzureTokenManager()