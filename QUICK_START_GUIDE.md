# 🚀 Quick Start Guide: MCP Server Workshop

> **Quick access to setup instructions and hands-on exercises**  
> Build an MCP Server with Business Central Integration in 30 minutes

📖 **[Complete Workshop Guide →](WORKSHOP_GUIDE_EN.md)** | 📊 **[Presentation Slides →](data/MCP_Server_Custom%20Directions.pptx)**

---

## 📝 Step-by-Step Instructions

### Step 1: Download the Repository 📥

1. Go to: **https://github.com/javiarmesto/Workshop-MCP-Server-Directions-Lab**
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Open a terminal and navigate to the extracted folder:
   ```bash
   cd Workshop-MCP-Server-Directions-Lab-main
   ```

### Step 2: Automated Setup (Recommended) ⚡

**For Windows:**
```powershell
.\setup.ps1
```

**For macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

The script will automatically:
- [OK] Auto-detect Python installation (no PATH configuration needed)
- [OK] Check Python 3.12+ compatibility
- [OK] Create virtual environment
- [OK] Install dependencies (`mcp`, `fastmcp`, `httpx`, `pydantic`)
- [OK] Verify setup with `validate_workshop.py`

**Note**: The setup script automatically finds Python in common installation locations. You don't need Python in your system PATH.

### Step 3: Configure Environment (Optional - for Business Central)

Create `.env` file for Business Central integration:

```bash
# Copy the template
cp .env.example .env

# Edit with your Business Central & Azure credentials
# AZURE_TENANT_ID=your-azure-ad-tenant-id
# AZURE_CLIENT_ID=your-app-registration-client-id
# AZURE_CLIENT_SECRET=your-app-registration-secret
# BC_ENVIRONMENT=your-bc-environment-name
# BC_COMPANY_ID=your-company-id
```

> 🧩 The server reads AZURE_* for AAD and BC_* for Business Central context, matching the Workshop Guide.

> 🧪 **Skip this step** to use mock data mode (not recommended for learning)

### Step 4: Validate Your Setup

```bash
# Activate virtual environment (if not already active)
.\workshop-env\Scripts\activate  # Windows
source workshop-env/bin/activate  # macOS/Linux

# Run validation
python validate_workshop.py
```

**Expected output**: All checks should pass (6/6)

```
[PASS] Python Version
[PASS] Dependencies  
[PASS] Files
[PASS] Configuration
[PASS] Data Files
[PASS] Server Import

[STATS] RESULT: 6/6 checks passed
[SUCCESS] WORKSHOP READY! You can run: python server_workshop.py
```

### Step 5: Test the MCP Server

**Quick test** (lists available tools):

```bash
python test_server.py
```

**Expected output**:
```
============================================================
AVAILABLE TOOLS:
============================================================

1. get_customers
   Description: Get customer list from Business Central

2. get_items
   Description: Get items list from Business Central

3. get_sales_orders
   Description: Get sales orders from Business Central

4. get_projects
   Description: Get projects from Business Central

5. get_customer_details
   Description: Get a customer by ID or name

6. get_currency_exchange_rates
   Description: Get currency exchange rates

[INFO] Total tools available: 6
[SUCCESS] Test completed successfully!
```

**Alternative**: Run the server directly (waits for STDIO communication):

```bash
python server_workshop.py
```

**Note**: The server uses STDIO transport and will wait for JSON-RPC messages. Use `test_server.py` for a quick validation, or configure Claude Desktop for real usage.

### Step 6: Get Configuration Paths

Before configuring any tool, get your paths in the correct format:

```powershell
# Run the configuration paths script
.\ConfigurationPaths.ps1
```

**What this script does:**
- Detects your workshop directory automatically
- Displays Python executable path
- Shows server script path
- Outputs **two formats**:
  - **FOR CLAUDE DESKTOP**: JSON format with forward slashes (`/`)
  - **FOR MCP INSPECTOR**: Windows format with backslashes (`\`)

**Example output:**
```
============================================================
 FOR CLAUDE DESKTOP (JSON format)
============================================================
Command:    C:/Users/.../workshop-env/Scripts/python.exe
Args:       C:/Users/.../server_workshop.py
PYTHONPATH: C:/Users/.../Workshop-MCP-Server-Directions-Lab

============================================================
 FOR MCP INSPECTOR (Windows format)
============================================================
Transport Type: STDIO
Command:        C:\Users\...\workshop-env\Scripts\python.exe
Arguments:      C:\Users\...\server_workshop.py
Env (optional): PYTHONPATH=C:\Users\...\Workshop-MCP-Server-Directions-Lab
```

> 💡 **Tip**: Keep this terminal window open while configuring tools, or run the script again anytime you need the paths.

### Step 7: Test with MCP Inspector (Optional)

**MCP Inspector** provides a visual interface to test your MCP server before configuring Claude Desktop.

#### Install MCP Inspector

```bash
# Quick start (no installation)
npx @modelcontextprotocol/inspector

# Or install globally
npm install -g @modelcontextprotocol/inspector
mcp-inspector
```

#### Configure MCP Inspector

MCP Inspector will open a web interface. Configure it with:

1. **Transport Type**: `STDIO`
2. **Command**: Your `python.exe` path from Step 6 (Windows format with `\`)
   ```
   C:\Users\...\Workshop-MCP-Server-Directions-Lab\workshop-env\Scripts\python.exe
   ```
3. **Arguments**: Your `server_workshop.py` path from Step 6 (Windows format)
   ```
   C:\Users\...\Workshop-MCP-Server-Directions-Lab\server_workshop.py
   ```
4. **Environment Variables** (optional but recommended):
   - Key: `PYTHONPATH`
   - Value: Your workshop path from Step 6

#### Test Your Server

1. Click **"Connect"** to start the server
2. Browse the **Tools** tab:
   - You should see 6 tools: `get_customers`, `get_items`, `get_sales_orders`, etc.
   - Click any tool to see its parameters
   - Fill in parameters and click "Execute" to test
3. Check the **Prompts** tab:
   - `customer_analysis` - Analyzes customer data
   - `pricing_analysis` - Analyzes pricing and stock
4. Inspect the **Resources** tab:
   - View available data files (CSV and JSON)

**Benefits of MCP Inspector:**
- ✅ Visual debugging interface
- ✅ Test tools easily without CLI
- ✅ Inspect input/output data structures
- ✅ Faster iteration during development

> 💡 **Tip**: Use MCP Inspector during development to test your tools before integrating with Claude Desktop

### Step 8: Configure Claude Desktop

**Location of config file:**
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Add this configuration** (use **absolute paths**):

```json
{
  "mcpServers": {
    "bc-workshop-server": {
      "command": "C:\\full\\path\\to\\workshop-env\\Scripts\\python.exe",
      "args": ["C:\\full\\path\\to\\server_workshop.py"]
    }
  }
}
```

### Step 9: Test in Claude Desktop

1. **Restart Claude Desktop**
2. **Verify tools are available**:
   ```
   Ask Claude: "What MCP tools do you have available?"
   ```
3. **Test a tool**:
   ```
   Ask Claude: "Show me the top 5 customers from Business Central"
   ```

**Expected**: Claude should show available tools and execute them successfully.

---

## 💡 Step 10: Practical Exercises

Welcome to the hands-on section! You'll learn by doing:
- **Part A (Exercises 1-2)**: Test existing MCP tools with **Business Central Standard APIs**
- **Part B (Exercises 3-4)**: Implement new tools using **Business Central Standard APIs**

> **Workshop Objective**: We connect directly to **Business Central Standard APIs v2.0** 
> **Focus**: Real API integration with `/companies`, `/customers`, `/employees`, `/jobs` 
> **Mock Data**: Only used as exceptional fallback when BC credentials are unavailable

---

## Part A: Testing Existing Tools with Business Central APIs

### Exercise 1: Test Customer Tools (Standard BC API)

**Goal**: Learn how to use MCP tools that connect to **Business Central Standard API**.

**Business Central API Used**: `GET /api/v2.0/companies({id})/customers` 

**Tools to test**:
1. `get_customers` - Calls Business Central Standard API
2. `customer_analysis` prompt - Analyzes real BC customer data

**Step-by-step testing**:

1. **Open Claude Desktop** (ensure your MCP server is configured from Step 10)

2. **Test get_customers tool with real BC API**:
 ```
 Ask Claude: "Show me the top 5 customers from Business Central"
 ```
 
 **Expected result**: Claude calls Business Central API and shows:

 ```text
 🏢 **Business Central Customers** (Showing X results)
 
 • **Customer Name** (ID: xxx)
   📍 City
   📞 Phone Number
 ```

3. **Test customer_analysis prompt with BC data**:
 ```
 Ask Claude: "Analyze customer data from Business Central"
 ```
 
 **Expected result**: Claude uses real Business Central customer data for analysis.

**Study the real API implementation**:
- Open `src/client.py`
- Find `get_customers()` method
- See how it calls: `f"{self.base_url}/customers"` **This is the standard BC API!**
- Notice the OAuth 2.0 authentication with `self.headers`

**API Endpoints this exercise uses**:
- `GET /api/v2.0/companies({companyId})/customers`
- Standard Business Central API v2.0 
- OAuth 2.0 authentication 

---

### Exercise 2: Test Currency Exchange Rates (Standard BC API)

**Goal**: Use a tool that calls Business Central's **standard `/currencies` API**.

**Business Central API Used**: `GET /api/v2.0/companies({id})/currencies` 

**Step-by-step testing**:

1. **Test the tool with Business Central API**:
 ```
 Ask Claude: "What are the current currency exchange rates from Business Central?"
 ```
 
 **Expected result**: Real currency data from your BC environment:

 ```text
 💱 **Currency Exchange Rates** (Showing X results)
 
 • **EUR** - Rate: 1.08
   📅 Start date: 2025-01-01
 
 • **GBP** - Rate: 0.85
   📅 Start date: 2025-01-01
 ```

2. **Study the standard API implementation**:
 - Open `src/client.py`
 - Find `get_currency_exchange_rates()` method
 - See how it calls: `f"{self.base_url}/currencies"` **Standard BC API endpoint!**
 - This is a **read-only** operation on a standard Business Central entity

**Try these with Business Central API**:
- "Show me all available currencies from Business Central"
- "What's the exchange rate for EUR in our BC system?"
- "List currency rates from Business Central"

**Key Learning**: This tool demonstrates calling a **standard Business Central API endpoint** with OAuth 2.0 authentication - no custom extensions needed.

---

## Part B: Implementing New Tools with Business Central Standard APIs

Now you'll add **2 new tools** that connect to **Business Central Standard APIs**. Each exercise shows you how to implement real API integration with Business Central.

> **Primary Objective**: Connect to Business Central Standard API v2.0 
> **Learning Goal**: Build MCP tools that call real BC endpoints 
> **Mock Data**: Only as exceptional fallback when BC credentials unavailable

### Exercise 3: Implement `get_employees` Tool (Hands-on Implementation)

**Goal**: Add a new tool that fetches employees using the **standard Business Central API**.

**Business Central API Used**: `GET /api/v2.0/companies({id})/employees` 

> **This tool needs to be implemented** - you'll build it from scratch!

**What you'll learn**:

- How to analyze existing MCP tool implementations
- Business Central API integration patterns in real code
- Parameter handling with filters and limits
- Adding new tools to an existing MCP server

---

#### Step 3.1: Add Tool to Client (src/client.py)

Open `src/client.py` and **add this method** after the `get_currency_exchange_rates()` method (around line 268):

```python
async def get_employees(self, top: int = 20) -> List[Dict]:
 """
 Gets employees from Business Central using Standard API v2.0
 
 Business Central API: GET /api/v2.0/companies({id})/employees
 Authentication: OAuth 2.0 with Azure AD
 
 Args:
 top: Maximum number of employees to return (default 20)
 
 Returns:
 List of employees from Business Central
 """
 res = await self._request("GET", "employees", params={"$top": top})
 if res:
 logger.info(f"Employees retrieved: {len(res.get('value', []))}")
 else:
 logger.error("Could not retrieve employees list.")
 return res.get("value", []) if res else []
```

**Key points about this implementation**:
- Uses the standard `employees` endpoint
- Follows the same pattern as existing tools (`get_customers`, `get_items`)
- Uses `_request()` method for consistent API handling and authentication
- Supports `$top` parameter for limiting results
- Returns the `value` array from Business Central API response

#### Step 3.2: Register Tool in Server (server_workshop.py)

**1. Add to tools list** in `handle_list_tools()` method (around line 110):

```python
# Employees Tool - Standard BC API
types.Tool(
 name="get_employees",
 description=" Get employees from Business Central using standard API",
 inputSchema={
 "type": "object",
 "properties": {
 "top": {
 "type": "number",
 "description": "Maximum number of employees to return (default: 20)",
 "default": 20
 }
 }
 }
),
```

**2. Add tool handler** in `handle_call_tool()` method (around line 200):

```python
elif tool_name == "get_employees":
 top = arguments.get("top", 20)
 logger.info(f" Calling tool: {tool_name} with top={top}")
 
 result = await bc_client.get_employees(top=top)
 
 return types.CallToolResult(content=[
 types.TextContent(
 type="text",
 text=json.dumps(result, indent=2, ensure_ascii=False)
 )
 ])
```

#### Step 3.3: Test Your New Employees Tool

**1. Restart Claude Desktop** to load the new tool

**2. Test the tool**:

```text
Ask Claude: "Show me the employees from Business Central"
Ask Claude: "Get the top 5 employees"
Ask Claude: "List all employees in our BC system"
```

**Expected Results**:
Claude calls the Business Central Standard API: `GET /api/v2.0/companies({id})/employees` and returns real employee data including names, job titles, contact information, and employment details.

** Congratulations!** You've implemented a new MCP tool that connects to **Business Central Employees API**.

---

### Exercise 4: Implement `get_projects` Tool

**Goal**: Add another tool using Business Central's standard `/jobs` API (projects are called "jobs" in BC).

**Business Central API Used**: `GET /api/v2.0/companies({id})/jobs` 

> **This tool also needs to be implemented** - follow these steps:

#### Step 4.1: Add Tool to Client (src/client.py)

Add this method after `get_employees()`:

```python
async def get_projects(self, top: int = 20) -> List[Dict]:
 """
 Gets projects (jobs) from Business Central using Standard API v2.0
 
 Business Central API: GET /api/v2.0/companies({id})/jobs
 Authentication: OAuth 2.0 with Azure AD
 
 Args:
 top: Maximum number of projects to return (default 20)
 
 Returns:
 List of projects from Business Central
 """
 res = await self._request("GET", "jobs", params={"$top": top})
 if res:
 logger.info(f"Projects retrieved: {len(res.get('value', []))}")
 else:
 logger.error("Could not retrieve projects list.")
 return res.get("value", []) if res else []
```

---

#### Step 4.2: Register Tool in Server (server_workshop.py)

**1. Add tool definition** in `handle_list_tools()`:

```python
# Projects Tool - Standard BC API
types.Tool(
 name="get_projects",
 description=" Get projects (jobs) from Business Central using standard API",
 inputSchema={
 "type": "object",
 "properties": {
 "top": {
 "type": "number",
 "description": "Maximum number of projects to return (default: 20)",
 "default": 20
 }
 }
 }
),
```

**2. Add tool handler** in `handle_call_tool()`:

```python
elif tool_name == "get_projects":
 top = arguments.get("top", 20)
 logger.info(f" Calling tool: {tool_name} with top={top}")
 
 result = await bc_client.get_projects(top=top)
 
 return types.CallToolResult(content=[
 types.TextContent(
 type="text",
 text=json.dumps(result, indent=2, ensure_ascii=False)
 )
 ])
```

---

#### Step 4.3: Test Your Projects Tool

**1. Restart Claude Desktop** to load the new tool

**2. Test the tool**:

```text
Ask Claude: "Show me the projects from Business Central"
Ask Claude: "Get the top 5 projects"
Ask Claude: "List all projects (jobs) in our BC system"
```

**Expected Results**:
Claude calls the Business Central Standard API: `GET /api/v2.0/companies({id})/jobs` and returns:
```
🎯 **Business Central Projects** (Showing X results)

• **Project Number** - Description
  👤 Customer: Customer Name
  📊 Status: In Progress
  💰 Budget: $XX,XXX
```

** Congratulations!** You've implemented a new MCP tool that connects to **Business Central Projects (Jobs) API**.

---

## 🎉 Congratulations!

You've completed the MCP Server Workshop! You now understand:

- MCP architecture and protocol
- How to configure and run an MCP server
- Business Central API integration
- Creating tools, prompts, and resources
- Testing with Claude Desktop

### 🚀 Next Steps

1. **Customize**: Add your own tools for specific Business Central operations
2. **Extend**: Integrate other data sources
3. **Deploy**: Deploy your server to production
4. **Learn More**: Study the MCP specification at [modelcontextprotocol.io](https://modelcontextprotocol.io)

### Resources

- **MCP Documentation**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- **Business Central API**: [Microsoft Docs](https://learn.microsoft.com/dynamics365/business-central/dev-itpro/api-reference/)
- **Repository**: [GitHub](https://github.com/javiarmesto/Workshop-MCP-Server-Directions-Lab)

---

**Congratulations on completing the MCP Server Workshop!** You've successfully learned how to build custom MCP tools that integrate with Business Central APIs. Keep building amazing AI-powered solutions.