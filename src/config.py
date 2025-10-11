"""
config.py

Centralized configuration module for the Microsoft Dynamics 365 Business Central MCP application.

Main features:
  - Automatic loading of environment variables from `.env` (security and portability).
  - Validates the presence of Azure AD credentials (tenant_id, client_id, client_secret).
  - Gets and validates Business Central parameters (environment, company_id, tenant_id).
  - Exposes Pydantic models for typing and validation:
      * AzureADConfig: Azure AD authentication configuration.
      * BusinessCentralConfig: BC API configuration.
  - Creates a global `config` instance with validated values accessible throughout the app.

Quick onboarding:
  1. Configure the `.env` file with the required variables (see README).
  2. Use `config.azure_ad` and `config.bc` to access configuration in any module.
  3. Call `config.validate()` to check validity before launching critical operations.

Useful references:
  - Authentication configuration: https://learn.microsoft.com/en-us/azure/active-directory/develop/howto-add-app-roles-in-azure-ad-apps
  - Business Central REST APIs: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/webservices/api-overview
  - TechSphereDynamics Blog: https://techspheredynamics.com
"""
import os
import logging
from dotenv import load_dotenv, find_dotenv
from typing import Optional
from pydantic import BaseModel, Field, model_validator

# Load .env automatically if it exists, even during Uvicorn reload processes
env_path = find_dotenv()
if env_path:
    load_dotenv(env_path, override=True)

# Global logging configuration (if not already configured)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("config")


class AzureADConfig(BaseModel):
    """
    Configuration model for Azure AD authentication.
    Includes tenant_id, client_id, client_secret and authority (calculated if not provided).
    All fields are optional to support mock data mode.
    """
    tenant_id: Optional[str] = Field(default=None, description="Azure AD Tenant ID")
    client_id: Optional[str] = Field(default=None, description="Azure AD Application ID")
    client_secret: Optional[str] = Field(default=None, description="Azure AD Client Secret")
    authority: Optional[str] = None

    @model_validator(mode="after")
    def set_authority(self):
        # Set authority if not provided and tenant_id is available
        if not self.authority and self.tenant_id:
            self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        return self


class BusinessCentralConfig(BaseModel):
    """
    Configuration model for the Business Central API.
    Includes environment, company_id, tenant_id and base_url (calculated if not provided).
    All fields are optional to support mock data mode.
    """
    environment: str = Field(default="production", description="BC Environment")
    company_id: Optional[str] = Field(default=None, description="Business Central Company ID")
    tenant_id: Optional[str] = Field(default=None, description="Azure AD Tenant ID for BC API path")
    base_url: Optional[str] = None

    @model_validator(mode="after")
    def set_base_url(self):
        if not self.base_url and self.tenant_id:
            # Build the base URL including tenant_id and environment
            self.base_url = (
                f"https://api.businesscentral.dynamics.com/v2.0/"
                f"{self.tenant_id}/{self.environment}/api/v2.0"
            )
        return self


class AppConfig:
    """
    Main configuration class for the MCP app.
    Exposes azure_ad and bc sections, and validation methods.
    """
    def __init__(self):
        self.azure_ad = self._load_azure()
        self.bc = self._load_bc()

    def _load_azure(self) -> AzureADConfig:
        """
        Loads Azure AD configuration from environment variables.
        Returns AzureADConfig with None values if credentials are not provided (for mock data mode).
        """
        t = os.getenv("AZURE_TENANT_ID")
        c = os.getenv("AZURE_CLIENT_ID")
        s = os.getenv("AZURE_CLIENT_SECRET")

        # If any Azure AD variables are missing, log a warning and return config with None values
        if not all([t, c, s]):
            missing = [v for v, val in (
                ("AZURE_TENANT_ID", t),
                ("AZURE_CLIENT_ID", c),
                ("AZURE_CLIENT_SECRET", s),
            ) if not val]
            logger.warning(f"Azure AD credentials not configured: {', '.join(missing)}. Running in mock data mode.")
            return AzureADConfig(tenant_id=t, client_id=c, client_secret=s)
        
        # All credentials are present
        return AzureADConfig(tenant_id=t, client_id=c, client_secret=s)

    def _load_bc(self) -> BusinessCentralConfig:
        """
        Loads Business Central configuration from environment variables.
        Returns config with None values if not provided (for mock data mode).
        """
        env = os.getenv("BC_ENVIRONMENT", "production")
        cid = os.getenv("BC_COMPANY_ID")
        # TEMPORARILY ignore BC_BASE_URL to force using /api/v2.0
        # base_url = os.getenv("BC_BASE_URL")  # Use BC_BASE_URL if present
        base_url = None  # Force automatic construction with /api/v2.0
        
        # Include tenant_id to correctly build the Business Central path (if available)
        tenant = self.azure_ad.tenant_id if self.azure_ad.tenant_id else None
        
        if not cid:
            logger.warning("BC_COMPANY_ID not configured. Running in mock data mode.")
        
        bc = BusinessCentralConfig(environment=env, company_id=cid, tenant_id=tenant, base_url=base_url)
        return bc

    def validate(self) -> bool:
        """
        Validates that the loaded configuration is consistent and complete.
        Returns True if valid, False if any critical field is missing.
        This method checks if Azure AD and BC credentials are configured.
        """
        try:
            # Check if we have Azure AD credentials
            has_azure = (
                self.azure_ad.tenant_id is not None and
                self.azure_ad.client_id is not None and
                self.azure_ad.client_secret is not None
            )
            
            # Check if we have BC configuration
            has_bc = self.bc.company_id is not None
            
            if has_azure and has_bc:
                logger.info("Configuration valid: Azure AD and Business Central configured")
                return True
            elif not has_azure and not has_bc:
                logger.warning("Configuration: Running in mock data mode (no Azure AD or BC credentials)")
                return False
            else:
                logger.warning("Configuration: Partial credentials provided. May run in mixed mode.")
                return False
        except Exception as e:
            logger.error(f"Invalid configuration: {e}")
            return False


# Shared instance for global use
config = AppConfig()
