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
- ✅ Check Python 3.12+ compatibility
- ✅ Create virtual environment
- ✅ Install dependencies (`mcp`, `httpx`, `msal`)
- ✅ Verify setup with `validate_workshop.py`

### Step 3: Configure Environment (Optional - for Business Central)

Create `.env` file for Business Central integration:

```bash
# Copy the template
cp .env.example .env

# Edit with your Business Central credentials
# BC_TENANT_ID=your-azure-ad-tenant-id
# BC_CLIENT_ID=your-app-registration-client-id
# BC_CLIENT_SECRET=your-app-registration-secret
# BC_ENVIRONMENT=your-bc-environment-name
# BC_COMPANY_ID=your-company-id
```

> 🧪 **Skip this step** to use mock data mode (not recommended for learning)

### Step 4: Validate Your Setup

```bash
# Activate virtual environment (if not already active)
.\workshop-env\Scripts\activate  # Windows
source workshop-env/bin/activate  # macOS/Linux

# Run validation
python validate_workshop.py
```

**Expected output**: ✅ All checks should pass

### Step 5: Test the MCP Server

```bash
# Run the server directly (test mode)
python server_workshop.py
```

**Expected**: Server starts and waits for stdin/stdout communication

### Step 6: Configure Claude Desktop

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

### Step 7: Test in Claude Desktop

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

## 🎓 Practical Exercises

### Part A: Testing Existing Tools with Business Central APIs

#### Exercise 1: Test Customer Tools (Standard BC API)

**Business Central API**: `GET /api/v2.0/companies({id})/customers` ✅

**Test commands in Claude Desktop:**

```text
"Show me the top 5 customers from Business Central"
"Analyze customer data from our BC system" 
"List all customers with their balances"
```

**What you'll see**:
- ✅ Real customer data from your Business Central environment
- Customer names, IDs, balances, and contact information
- OAuth 2.0 authentication working with Azure AD

**Learning points**:
- How MCP tools call Business Central Standard APIs
- OAuth 2.0 authentication flow
- Parameter handling (`top` parameter)

---

#### Exercise 2: Test Currency Exchange Rates (Standard BC API)

**Business Central API**: `GET /api/v2.0/companies({id})/currencies` ✅

**Test commands in Claude Desktop:**

```text
"What are the current currency exchange rates from Business Central?"
"Show me all available currencies from our BC system"
"What's the exchange rate for EUR in Business Central?"
```

**What you'll see**:
- ✅ Real currency data from Business Central
- Exchange rates, currency codes, and rate effective dates
- Standard API response structure from BC

**Learning points**:
- Standard Business Central API endpoints
- Read-only operations
- API response structure

---

### Part B: Implementing New Tools with Business Central APIs

#### Exercise 3: Implement `get_employees` Tool

**Goal**: Add a new tool that connects to Business Central's employees API

**Business Central API**: `GET /api/v2.0/companies({id})/employees` ✅

> 🔧 **This tool needs to be implemented** - follow these steps:

**Verify the implementation**:

1. **Add method to `src/client.py`**:
   ```python
   async def get_employees(self, top: int = 20) -> List[Dict]:
   ```

2. **Register in `server_workshop.py`**:
   - Add to tools list: `get_employees`
   - Add to tool handler

3. **Test in Claude Desktop**:
   ```text
   "Show me the employees from Business Central"
   "Get the top 5 employees"
   "List all employees in our BC system"
   ```

**Expected results**:
- ✅ Real employee data from Business Central
- Names, job titles, contact information, and employment details
- Standard Business Central API v2.0 response format

---

#### Exercise 4: Implement `get_payment_terms` Tool (Hands-on)

**Goal**: Add a new tool for Business Central payment terms

**Business Central API**: `GET /api/v2.0/companies({id})/paymentTerms` ✅

> 🔧 **This tool needs to be implemented** - follow these steps:

##### Step 4.1: Verify mock data exists

Check that `data/payment_terms.csv` exists with this structure:

```csv
id,code,displayName,dueDateCalculation,discountDateCalculation,discountPercent
PT001,NET30,Net 30 Days,30D,0D,0
PT002,NET15,Net 15 Days,15D,0D,0
PT003,COD,Cash on Delivery,0D,0D,0
PT004,210NET30,2/10 Net 30,30D,10D,2
PT005,NET60,Net 60 Days,60D,0D,0
```

##### Step 4.2: Add method to `src/client.py`

Add this method after `get_sales_orders()`:

```python
async def get_payment_terms(self, top: int = 20) -> List[Dict]:
    """
    Gets payment terms from Business Central.
    Parameters:
        top (int): Maximum number of terms to return (default 20).
    Returns:
        List of dictionaries with payment terms.
    """
    res = await self._request("GET", "paymentTerms", params={"$top": top})
    return res.get("value", []) if res else []
```

##### Step 4.3: Register tool in `server_workshop.py`

1. **Add to tools list** in `handle_list_tools()`:

```python
types.Tool(
    name="get_payment_terms",
    description="💳 Get payment terms from Business Central",
    inputSchema={
        "type": "object",
        "properties": {
            "top": {
                "type": "number",
                "description": "Maximum number of terms to return (default: 20)",
                "default": 20
            }
        }
    }
),
```

2. **Add to tool handler** in `handle_call_tool()`:

```python
elif tool_name == "get_payment_terms":
    top = arguments.get("top", 20)
    logger.info(f"📞 Calling tool: {tool_name} with top={top}")
    
    result = await bc_client.get_payment_terms(top=top)
    
    return types.CallToolResult(content=[
        types.TextContent(
            type="text",
            text=json.dumps(result, indent=2, ensure_ascii=False)
        )
    ])
```

##### Step 4.4: Test your implementation

1. **Restart Claude Desktop**
2. **Verify new tool appears**: Should now see 7 tools total
3. **Test the tool**:

```text
"Show me the payment terms from Business Central"
"List all available payment terms"
"What payment terms do we have?"
```

**Expected results**:
- ✅ Real payment terms data from Business Central
- Payment codes, descriptions, due date calculations, and discount terms
- Standard Business Central API v2.0 structure

---

## 🎯 What You've Learned

### Part A (Testing):
- How to test existing MCP tools with Claude Desktop
- Business Central Standard API integration patterns
- OAuth 2.0 authentication with Azure AD
- Difference between real API calls and mock data fallbacks

### Part B (Implementation):
- How to add new MCP tools to an existing server
- Business Central API client patterns
- Tool registration and parameter handling
- End-to-end testing workflow

### Key Concepts:
- **Standard APIs**: All tools use Business Central Standard API v2.0 (no custom extensions)
- **Authentication**: OAuth 2.0 with Azure AD for secure API access
- **Fallback Strategy**: Mock data available when BC credentials unavailable
- **MCP Protocol**: Tools, prompts, and resources working together
- **STDIO Transport**: Direct process communication with Claude Desktop

---

## 🆘 Troubleshooting

### Server not appearing in Claude Desktop?
- Verify **absolute paths** in `claude_desktop_config.json`
- Restart Claude Desktop completely
- Check that `validate_workshop.py` passes

### Tools not working?
- Test server directly: `python server_workshop.py`
- Check logs for authentication errors
- Verify `.env` file configuration (if using Business Central)

### Mock data not loading?
- Ensure CSV files exist in `data/` folder
- Check file permissions and encoding (UTF-8)
- Verify CSV structure matches expected format

### Need help?
- 📖 **[Complete Workshop Guide](WORKSHOP_GUIDE_EN.md)** - Full documentation
- 🔧 **[Troubleshooting Section](WORKSHOP_GUIDE_EN.md#-troubleshooting)** - Detailed solutions
- 📊 **[Presentation Slides](data/MCP_Server_Custom%20Directions.pptx)** - Visual walkthrough

---

**🎉 Congratulations!** You've successfully built an MCP server with Business Central integration!