"""
client.py

Asynchronous and resilient HTTP client for the Microsoft Dynamics 365 Business Central API.

Main features:
  - Automatically obtains and refreshes Azure AD tokens (OAuth2/Entra ID).
  - Implements exponential retry logic and robust HTTP error handling (401, 5xx).
  - Exposes async methods for key operations:
      * get_customers(top): List customers
      * get_customer(id): Customer detail
      * get_items(top): List items
      * get_orders(top): List sales orders
      * create_customer(data): Create a new customer

Quick onboarding:
  1. Ensure the `.env` file is correctly configured (see README).
  2. Use the client methods to interact with the BC API from MCP tools.
  3. Consult each method's docstrings for examples and usage details.

Useful references:
  - Business Central REST APIs: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/webservices/api-overview
  - Security and authentication: https://learn.microsoft.com/en-us/dynamics365/business-central/dev-itpro/administration/enable-apis-using-azure-active-directory
  - TechSphereDynamics Blog: https://techspheredynamics.com
"""
import asyncio
import httpx
import logging
import os
from typing import Any, Dict, List, Optional
from config import config
# Make sure azure_auth.py is in the same directory or adjust the import based on your project structure
try:
    from azure_auth import token_manager
except ModuleNotFoundError:
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from azure_auth import token_manager

# Global logging configuration
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)
logger = logging.getLogger("bc_client")


class APIEndpointBuilder:
    """
    Dynamic URL builder for Business Central standard and custom APIs.
    """
    def __init__(self, base_url: str, company_id: str):
        self.base_url = base_url
        self.company_id = company_id
        
    def build_standard_url(self, endpoint: str) -> str:
        """Builds URL for standard API: /api/v2.0/companies({company})/endpoint"""
        return f"{self.base_url}/companies({self.company_id})/{endpoint}"
        
    def build_custom_url(self, publisher: str, app_group: str, version: str, endpoint: str, use_company: bool = False) -> str:
        """
        Builds URL for custom API.
        Format: /api/{publisher}/{app_group}/{version}/{endpoint}
        If use_company=True: /api/{publisher}/{app_group}/{version}/companies({company})/{endpoint}
        """
        # Extract the base up to tenant/environment, without /api/v2.0
        base_parts = self.base_url.split('/api/v2.0')
        base_without_version = base_parts[0]
        custom_path = f"{base_without_version}/api/{publisher}/{app_group}/{version}"
        
        if use_company:
            return f"{custom_path}/companies({self.company_id})/{endpoint}"
        else:
            return f"{custom_path}/{endpoint}"


class BusinessCentralClient:
    """
    Asynchronous client for the Business Central API.
    Manages authentication, retries and exposes methods for standard and custom APIs.
    """
    def __init__(self):
        self.base = config.bc.base_url
        self.comp = config.bc.company_id
        self.url_builder = APIEndpointBuilder(self.base, self.comp)
        self._retries = 3  # Number of retries for transient errors
        self._timeout = 30  # Global timeout for HTTP requests (seconds)

    async def _request(
        self, method: str, path_or_url: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        is_full_url: bool = False
    ) -> Optional[Dict[str, Any]]:
        """
        Makes an authenticated HTTP request to the Business Central API.
        Handles automatic retries for 401/5xx errors and refreshes token if necessary.
        Parameters:
            method (str): HTTP method ('GET', 'POST', etc.)
            path_or_url (str): Relative path within BC company or full URL
            params (dict): Optional query parameters
            data (dict): JSON payload for POST/PUT
            is_full_url (bool): If True, path_or_url is a full URL
        Returns:
            Dictionary with JSON response or None if it fails.
        """
        if is_full_url:
            url = path_or_url
        else:
            url = self.url_builder.build_standard_url(path_or_url)
            
        resp = None
        for i in range(self._retries):
            logger.debug(f"BC Request #{i+1}: {method} {url} params={params} data={data}")
            token = await token_manager.get_token()
            if not token:
                logger.warning("Azure AD credentials not configured. Cannot connect to Business Central API. Running in mock data mode.")
                return None
            headers = {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json"
            }
            async with httpx.AsyncClient(timeout=self._timeout) as cli:
                resp = await cli.request(method, url, headers=headers, params=params, json=data)
            # DEBUG: show response
            logger.debug(f"BC Response {resp.status_code}: {resp.text[:200]}")
            if resp.status_code in (200, 201, 204):
                if resp.status_code == 204:  # No Content
                    return {"success": True}
                try:
                    return resp.json()
                except ValueError:
                    return {"success": True, "raw_response": resp.text}
            if resp.status_code == 401:
                token_manager._token = None
                logger.warning("Token expired or invalid. Retrying...")
                continue
            if resp.status_code >= 500:
                logger.warning(f"Error {resp.status_code} in Business Central. Retrying...")
                await asyncio.sleep(2 ** i)
                continue
            break
        if resp is not None:
            logger.error(f"BC API {method} {path_or_url}: {resp.status_code} - {resp.text[:200]}")
        else:
            logger.error(f"BC API {method} {path_or_url}: No response received from server.")
        return None


    async def get_customers(self, top: int = 20) -> List[Dict]:
        """
        Gets a list of customers from Business Central.
        Parameters:
            top (int): Maximum number of customers to return (default 20).
        Returns:
            List of dictionaries with customers.
        """
        res = await self._request("GET", "customers", params={"$top": top})
        if res:
            logger.info(f"Customers retrieved: {len(res.get('value', []))}")
        else:
            logger.error("Could not retrieve customer list.")
        return res.get("value", []) if res else []


    async def get_customer(self, cid: str) -> Optional[Dict]:
        """
        Gets the detail of a customer by their ID.
        Parameters:
            cid (str): Customer's unique ID in BC.
        Returns:
            Dictionary with customer data or None if doesn't exist.
        """
        return await self._request("GET", f"customers({cid})")

    async def get_customer_by_id(self, customer_id: str) -> Optional[Dict]:
        """
        Gets the detail of a customer by their ID (alias for get_customer).
        Parameters:
            customer_id (str): Customer's unique ID in BC.
        Returns:
            Dictionary with customer data or None if doesn't exist.
        """
        return await self.get_customer(customer_id)


    async def get_items(self, top: int = 20) -> List[Dict]:
        """
        Lists items from Business Central.
        Parameters:
            top (int): Maximum number of items to return (default 20).
        Returns:
            List of dictionaries with items.
        """
        res = await self._request("GET", "items", params={"$top": top})
        return res.get("value", []) if res else []

    async def get_item_by_number(self, item_no: str) -> Optional[Dict]:
        """
        Gets the detail of an item by its number.
        Parameters:
            item_no (str): Item number in BC.
        Returns:
            Dictionary with item data or None if doesn't exist.
        """
        # Try direct access first
        result = await self._request("GET", f"items({item_no})")
        if result:
            return result
        
        # If it fails, try with filter
        res = await self._request("GET", "items", params={"$filter": f"number eq '{item_no}'", "$top": 1})
        if res and 'value' in res and res['value']:
            return res['value'][0]
        return None


    async def get_orders(self, top: int = 10) -> List[Dict]:
        """
        Lists sales orders from Business Central.
        Parameters:
            top (int): Maximum number of orders to return (default 10).
        Returns:
            List of dictionaries with sales orders.
        """
        res = await self._request("GET", "salesOrders", params={"$top": top})
        return res.get("value", []) if res else []

    async def get_sales_orders(self, filter_query: str = "", top: int = 20) -> List[Dict]:
        """
        Lists sales orders from Business Central with filters.
        Parameters:
            filter_query (str): Optional filter to search for specific orders
            top (int): Maximum number of orders to return (default 20).
        Returns:
            List of dictionaries with sales orders.
        """
        params = {"$top": top}
        if filter_query:
            params["$filter"] = filter_query
        res = await self._request("GET", "salesOrders", params=params)
        return res.get("value", []) if res else []


    async def create_customer(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Creates a new customer in Business Central.
        Parameters:
            data (dict): Dictionary with new customer fields according to BC API.
        Returns:
            JSON response of the new customer or None on error.
        Notes:
            - Consult official documentation for the required data schema.
        """
        return await self._request("POST", "customers", data=data)

    async def get_currency_exchange_rates(self, currency_code: Optional[str] = None, top: int = 20) -> List[Dict]:
        """
        Gets currency exchange rates from Business Central.
        Parameters:
            currency_code (str): Specific currency code (optional, e.g.: 'USD', 'EUR')
            top (int): Maximum number of rates to return (default 20).
        Returns:
            List of dictionaries with exchange rates.
        """
        params = {"$top": top}
        if currency_code:
            params["$filter"] = f"currencyCode eq '{currency_code}'"
        
        res = await self._request("GET", "currencyExchangeRates", params=params)
        return res.get("value", []) if res else []

    # ========================================================================
    # METHODS FOR CUSTOM DELIVERY APIS
    # ========================================================================
    """
    These methods are for custom APIs in Business Central
    The dynamic endpoint creation must take into account this configuration:
     url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics",
            app_group="delivery", 
            version="v1.0",
            endpoint="deliveries",
            use_company=True
        )
    Important to document and explain this additional point in the step-by-step guide
    """

    async def get_deliveries(self, filters: Optional[Dict] = None, top: int = 20) -> List[Dict]:
        """
        Gets deliveries from TechSphereDynamics custom API.
        Parameters:
            filters (dict): Optional filters (customer_id, status, date_from, date_to)
            top (int): Maximum number of deliveries to return
        Returns:
            List of dictionaries with deliveries
        """
        params = {"$top": top}
        if filters:
            if filters.get("customer_id"):
                params["$filter"] = f"customerId eq '{filters['customer_id']}'"
            if filters.get("status"):
                filter_expr = params.get("$filter", "")
                if filter_expr:
                    filter_expr += f" and status eq '{filters['status']}'"
                else:
                    filter_expr = f"status eq '{filters['status']}'"
                params["$filter"] = filter_expr
            if filters.get("date_from") or filters.get("date_to"):
                date_filter = []
                if filters.get("date_from"):
                    date_filter.append(f"deliveryDate ge {filters['date_from']}")
                if filters.get("date_to"):
                    date_filter.append(f"deliveryDate le {filters['date_to']}")
                if date_filter:
                    filter_expr = params.get("$filter", "")
                    date_expr = " and ".join(date_filter)
                    if filter_expr:
                        filter_expr += f" and ({date_expr})"
                    else:
                        filter_expr = date_expr
                    params["$filter"] = filter_expr

        url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics", 
            app_group="delivery", 
            version="v1.0", 
            endpoint="deliveries",
            use_company=True
        )
        res = await self._request("GET", url, params=params, is_full_url=True)
        return res.get("value", []) if res else []

    async def get_delivery(self, delivery_id: str) -> Optional[Dict]:
        """
        Gets the detail of a specific delivery.
        Parameters:
            delivery_id (str): Unique delivery ID (GUID or No.)
        Returns:
            Dictionary with delivery data or None if doesn't exist
        """
        # If delivery_id looks like a GUID, use direct access WITHOUT quotes
        if len(delivery_id) > 20 and '-' in delivery_id:
            # It's a GUID (id field), use direct access WITHOUT quotes
            url = self.url_builder.build_custom_url(
                publisher="techSphereDynamics",
                app_group="delivery", 
                version="v1.0",
                endpoint=f"deliveries({delivery_id})",  # WITHOUT quotes for GUID
                use_company=True
            )
            return await self._request("GET", url, is_full_url=True)
        else:
            # It's a No. (number), use filter because direct access with quotes doesn't work
            url = self.url_builder.build_custom_url(
                publisher="techSphereDynamics",
                app_group="delivery", 
                version="v1.0",
                endpoint="deliveries",
                use_company=True
            )
            params = {"$filter": f"no eq '{delivery_id}'", "$top": 1}
            response = await self._request("GET", url, params=params, is_full_url=True)
            if response and 'value' in response and response['value']:
                return response['value'][0]
            return None

    async def update_delivery_status(self, delivery_id: str, status: str, notes: str = "") -> Optional[Dict]:
        """
        Updates the status of a delivery.
        Parameters:
            delivery_id (str): Unique delivery ID
            status (str): New status ('Pending', 'InTransit', 'Delivered', 'Cancelled')
            notes (str): Optional additional notes
        Returns:
            Dictionary with update response
        """
        data = {
            "status": status,
            "lastUpdateDate": None,  # BC will assign it automatically
        }
        if notes:
            data["notes"] = notes
            
        url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics",
            app_group="delivery",
            version="v1.0", 
            endpoint=f"deliveries('{delivery_id}')",
            use_company=True
        )
        return await self._request("PATCH", url, data=data, is_full_url=True)

    async def get_delivery_routes(self, date_from: str, date_to: str, driver_id: Optional[str] = None) -> List[Dict]:
        """
        Gets delivery routes for a date range.
        Parameters:
            date_from (str): Start date in YYYY-MM-DD format
            date_to (str): End date in YYYY-MM-DD format
            driver_id (str): Specific driver ID (optional)
        Returns:
            List of delivery routes
        """
        params = {
            "$filter": f"routeDate ge {date_from} and routeDate le {date_to}"
        }
        if driver_id:
            params["$filter"] += f" and driverId eq '{driver_id}'"
            
        url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics",
            app_group="delivery", 
            version="v1.0",
            endpoint="routes",
            use_company=True
        )
        res = await self._request("GET", url, params=params, is_full_url=True)
        return res.get("value", []) if res else []

    async def optimize_route(self, route_data: Dict[str, Any]) -> Optional[Dict]:
        """
        Requests route optimization.
        Parameters:
            route_data (dict): Route data to optimize (deliveries, constraints, etc.)
        Returns:
            Dictionary with optimized route
        """
        url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics",
            app_group="delivery",
            version="v1.0", 
            endpoint="routes/optimize",
            use_company=True
        )
        return await self._request("POST", url, data=route_data, is_full_url=True)

    async def get_inventory_status(self, warehouse_id: Optional[str] = None) -> List[Dict]:
        """
        Gets inventory status for deliveries.
        Parameters:
            warehouse_id (str): Specific warehouse ID (optional)
        Returns:
            List with inventory status
        """
        params = {}
        if warehouse_id:
            params["$filter"] = f"warehouseId eq '{warehouse_id}'"
            
        url = self.url_builder.build_custom_url(
            publisher="techSphereDynamics",
            app_group="delivery",
            version="v1.0", 
            endpoint="inventory",
            use_company=True
        )
        res = await self._request("GET", url, params=params, is_full_url=True)
        return res.get("value", []) if res else []


# Shared instance for global use
bc_client = BusinessCentralClient()
