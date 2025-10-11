#!/usr/bin/env python3
"""
MCP Workshop Server - STDIO Transport Version for Claude Desktop
This is a standalone version that uses STDIO transport instead of HTTP.
"""
import asyncio
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types
from pydantic import AnyUrl
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(name)s: %(message)s',
    handlers=[logging.StreamHandler(sys.stderr)]
)
logger = logging.getLogger(__name__)

# Import Business Central client
from client import BusinessCentralClient

# Initialize Business Central client
bc_client = BusinessCentralClient()

# Create MCP server instance
mcp_server = Server("bc-workshop-server")

@mcp_server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """📋 List all available tools"""
    return [
        types.Tool(
            name="get_customers",
            description="🏢 Get customer list from Business Central",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "integer",
                        "description": "Maximum number of customers to return (default: 20)"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_items",
            description="📦 Get items list from Business Central",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "integer", 
                        "description": "Maximum number of items to return (default: 20)"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_sales_orders",
            description="🛒 Get sales orders from Business Central",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "integer",
                        "description": "Maximum number of orders to return (default: 10)"
                    }
                },
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_customer_details",
            description="🔍 Get detailed information about a specific customer",
            inputSchema={
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string",
                        "description": "Customer unique ID"
                    }
                },
                "required": ["customer_id"],
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_item_details",
            description="🔍 Get detailed information about a specific item",
            inputSchema={
                "type": "object",
                "properties": {
                    "item_no": {
                        "type": "string",
                        "description": "Item number"
                    }
                },
                "required": ["item_no"],
                "additionalProperties": False
            }
        ),
        types.Tool(
            name="get_currency_exchange_rates",
            description="💱 Get currency exchange rates from Business Central",
            inputSchema={
                "type": "object",
                "properties": {
                    "top": {
                        "type": "integer",
                        "description": "Maximum number of rates to return (default: 20)"
                    }
                },
                "additionalProperties": False
            }
        ),
    ]

@mcp_server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """🔧 Execute a tool"""
    
    if arguments is None:
        arguments = {}
    
    try:
        logger.info(f"📞 Calling tool: {name} with arguments: {arguments}")
        
        if name == "get_customers":
            top = arguments.get("top", 20)
            customers = await bc_client.get_customers(top=top)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"🏢 **Business Central Customers** (Showing {len(customers)} results)\n\n" +
                         "\n".join([
                             f"• **{customer.get('displayName', 'N/A')}** (ID: {customer.get('id', 'N/A')})\n"
                             f"  📍 {customer.get('address', {}).get('city', 'N/A')}\n"
                             f"  📞 {customer.get('phoneNumber', 'N/A')}\n"
                             for customer in customers
                         ])
                )
            ]
        
        elif name == "get_items":
            top = arguments.get("top", 20)
            items = await bc_client.get_items(top=top)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"📦 **Business Central Items** (Showing {len(items)} results)\n\n" +
                         "\n".join([
                             f"• **{item.get('displayName', 'N/A')}** (No: {item.get('number', 'N/A')})\n"
                             f"  💰 Price: {item.get('unitPrice', 0)}\n"
                             f"  📊 Stock: {item.get('inventory', 0)}\n"
                             for item in items
                         ])
                )
            ]
        
        elif name == "get_sales_orders":
            top = arguments.get("top", 10)
            orders = await bc_client.get_orders(top=top)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"🛒 **Sales Orders** (Showing {len(orders)} results)\n\n" +
                         "\n".join([
                             f"• **Order {order.get('number', 'N/A')}** - Customer: {order.get('customerName', 'N/A')}\n"
                             f"  💰 Total: {order.get('totalAmountIncludingTax', 0)}\n"
                             f"  📅 Date: {order.get('orderDate', 'N/A')}\n"
                             for order in orders
                         ])
                )
            ]
        
        elif name == "get_customer_details":
            customer_id = arguments.get("customer_id")
            if not customer_id:
                return [types.TextContent(type="text", text="❌ Error: customer_id is required")]
            
            customer = await bc_client.get_customer_by_id(customer_id)
            if not customer:
                return [types.TextContent(type="text", text=f"❌ Customer not found: {customer_id}")]
            
            return [
                types.TextContent(
                    type="text",
                    text=f"🏢 **Customer Details**\n\n"
                         f"**Name:** {customer.get('displayName', 'N/A')}\n"
                         f"**ID:** {customer.get('id', 'N/A')}\n"
                         f"**Phone:** {customer.get('phoneNumber', 'N/A')}\n"
                         f"**Email:** {customer.get('email', 'N/A')}\n"
                         f"**Address:** {customer.get('address', {}).get('street', 'N/A')}, "
                         f"{customer.get('address', {}).get('city', 'N/A')}\n"
                         f"**Country:** {customer.get('address', {}).get('countryLetterCode', 'N/A')}\n"
                )
            ]
        
        elif name == "get_item_details":
            item_no = arguments.get("item_no")
            if not item_no:
                return [types.TextContent(type="text", text="❌ Error: item_no is required")]
            
            item = await bc_client.get_item_by_number(item_no)
            if not item:
                return [types.TextContent(type="text", text=f"❌ Item not found: {item_no}")]
            
            return [
                types.TextContent(
                    type="text",
                    text=f"📦 **Item Details**\n\n"
                         f"**Name:** {item.get('displayName', 'N/A')}\n"
                         f"**Number:** {item.get('number', 'N/A')}\n"
                         f"**Price:** {item.get('unitPrice', 0)}\n"
                         f"**Stock:** {item.get('inventory', 0)}\n"
                         f"**Category:** {item.get('itemCategoryCode', 'N/A')}\n"
                         f"**Unit of measure:** {item.get('baseUnitOfMeasure', 'N/A')}\n"
                )
            ]
        
        elif name == "get_currency_exchange_rates":
            top = arguments.get("top", 20)
            rates = await bc_client.get_currency_exchange_rates(top=top)
            
            return [
                types.TextContent(
                    type="text",
                    text=f"💱 **Currency Exchange Rates** (Showing {len(rates)} results)\n\n" +
                         "\n".join([
                             f"• **{rate.get('currencyCode', 'N/A')}** - Rate: {rate.get('relationalExchangeRateAmount', rate.get('exchangeRateAmount', 'N/A'))}\n"
                             f"  📅 Start date: {rate.get('startingDate', 'N/A')}\n"
                             for rate in rates
                         ])
                )
            ]
        
        else:
            return [
                types.TextContent(
                    type="text",
                    text=f"❌ Unknown tool: {name}"
                )
            ]
    
    except Exception as e:
        logger.error(f"Error executing {name}: {e}", exc_info=True)
        return [
            types.TextContent(
                type="text",
                text=f"❌ Error executing {name}: {str(e)}"
            )
        ]

@mcp_server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    """📝 List all available prompts"""
    return [
        types.Prompt(
            name="customer_analysis",
            description="🏢 Detailed customer analysis with Business Central insights",
            arguments=[
                types.PromptArgument(
                    name="customer_id",
                    description="Customer ID to analyze",
                    required=True
                )
            ]
        ),
        types.Prompt(
            name="vendor_analysis",
            description="🏭 Detailed vendor analysis",
            arguments=[
                types.PromptArgument(
                    name="vendor_id",
                    description="Vendor ID to analyze",
                    required=True
                )
            ]
        )
    ]

@mcp_server.get_prompt()
async def handle_get_prompt(name: str, arguments: dict | None) -> types.GetPromptResult:
    """🎯 Get a specific prompt with its messages"""
    
    if arguments is None:
        arguments = {}
    
    if name == "customer_analysis":
        customer_id = arguments.get("customer_id", "")
        message_text = f"""Analyze customer {customer_id} from Business Central:

1. Use the get_customer_details tool to retrieve customer information
2. Analyze the customer's purchase history and patterns  
3. Identify trends and opportunities
4. Provide actionable insights for account management

Focus on data-driven insights and specific recommendations."""
        
    elif name == "vendor_analysis":
        vendor_id = arguments.get("vendor_id", "")
        message_text = f"""Analyze vendor {vendor_id} from Business Central:

1. Use the get_vendor_details tool to retrieve vendor information
2. Analyze the vendor's performance and reliability
3. Identify trends in purchasing and delivery
4. Provide actionable insights for procurement optimization

Focus on data-driven insights and specific recommendations."""
        
    else:
        message_text = f"Prompt '{name}' is not available."
    
    return types.GetPromptResult(
        description=f"Prompt for {name}",
        messages=[
            types.PromptMessage(
                role="user",
                content=types.TextContent(
                    type="text",
                    text=message_text
                )
            )
        ]
    )

@mcp_server.list_resources()
async def handle_list_resources() -> list[types.Resource]:
    """📂 List available resources (data files)"""
    return [
        types.Resource(
            uri=AnyUrl("file://data/customers.csv"),
            name="Customer Data",
            description="📊 Customer data in CSV format",
            mimeType="text/csv"
        ),
        types.Resource(
            uri=AnyUrl("file://data/items.csv"),
            name="Item Data",
            description="📦 Item/product data in CSV format",
            mimeType="text/csv"
        ),
        types.Resource(
            uri=AnyUrl("file://data/prices.csv"),
            name="Item Prices",
            description="💰 Item price data in CSV format",
            mimeType="text/csv"
        ),
        types.Resource(
            uri=AnyUrl("file://data/vendors.csv"),
            name="Vendor Data",
            description="🏭 Vendor data in CSV format",
            mimeType="text/csv"
        )
    ]

@mcp_server.read_resource()
async def handle_read_resource(uri: AnyUrl) -> str:
    """📖 Read a specific resource"""
    from pathlib import Path
    
    # Extract path from URI
    path_str = str(uri).replace("file://", "")
    file_path = Path(path_str)
    
    try:
        if file_path.exists():
            content = file_path.read_text(encoding='utf-8')
            logger.info(f"📄 Read resource: {path_str}")
            return content
        else:
            logger.warning(f"⚠️ Resource not found: {path_str}")
            return f"Resource not found: {path_str}"
    except Exception as e:
        logger.error(f"❌ Error reading resource {path_str}: {e}")
        return f"Error reading resource: {str(e)}"

async def main():
    """Run the MCP server using STDIO transport"""
    logger.info("🌟 Starting MCP Workshop Server with STDIO transport")
    logger.info("📡 Ready for Claude Desktop connection")
    
    # Run the server with STDIO transport
    async with stdio_server() as (read_stream, write_stream):
        await mcp_server.run(
            read_stream,
            write_stream,
            mcp_server.create_initialization_options()
        )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}", exc_info=True)
        sys.exit(1)

