# 🚀 MCP Server Workshop - Business Central Integration

Welcome to the **MCP Server Workshop**! This workshop teaches you to build a complete MCP (Model Context Protocol) server with STDIO transport for Claude Desktop, integrated with Microsoft Dynamics 365 Business Central.

> ⏱️ **Workshop Duration**: 20-30 minutes  
> 📖 **[Complete Workshop Guide →](WORKSHOP_GUIDE_EN.md)**  
> 🚀 **[Quick Start Guide →](QUICK_START_GUIDE.md)** (Setup + Exercises)  
> 📊 **Presentation Slides**: [MCP_Server_Custom Directions.pptx](data/MCP_Server_Custom%20Directions.pptx)

---

## 🎯 Workshop Objectives

Learn to build, extend, and customize MCP servers with:
- ✅ MCP Protocol fundamentals
- ✅ STDIO transport for Claude Desktop integration
- ✅ Business Central API integration
- ✅ Custom tools and prompts creation
- ✅ Practical exercises for hands-on learning

---

## 📋 Prerequisites

Before starting the workshop, ensure you have:

### Required:
- 🐍 **Python 3.12 or higher** installed ([Download here](https://www.python.org/downloads/))
- 💻 **Claude Desktop** app installed ([Download here](https://claude.ai/download))
- 📦 Basic command line knowledge (terminal/PowerShell)

### Required for Business Central Integration (Workshop Objective):
- 🏭 **Azure AD Tenant** with Business Central access
-  **Business Central Environment** with Standard API v2.0 enabled:
  - Sandbox or Production environment
  - API endpoints: `/api/v2.0/companies`, `/items`, `/customers`, `/salesOrders`, etc.
  - Company name and Environment name
- 🚀 **Azure AD App Registration** configured:
  - Client ID, Client Secret, Tenant ID
  - API permissions for Business Central (Dynamics 365 Business Central)
  - Redirect URI configured (if needed)

### Alternative (Only if BC access is not available):
- 🧪 **Mock Data Mode**: The workshop includes mock data as a fallback
  - Allows completing exercises without real BC connection
  - Limited to testing MCP protocol mechanics
  - Does not demonstrate real authentication or API integration
  - **Not recommended** for full workshop experience

### Good to Know:
- ✅ Virtual environment setup is automated via scripts
- ✅ All Python dependencies are listed in `requirements.txt`
- 🧪 Mock data available **only as fallback** if BC access unavailable

---

## 📚 Quick Start

### 📥 Step 1: Download the Repository

1. Go to: **https://github.com/javiarmesto/Workshop-MCP-Server-Directions-Lab**
2. Click the green **"Code"** button
3. Select **"Download ZIP"**
4. Extract the ZIP file to your desired location
5. Open a terminal and navigate to the extracted folder:
   ```bash
   cd Workshop-MCP-Server-Directions-Lab-main
   ```

### 🚀 Step 2: Automated Setup (Recommended - 2 minutes)

**For Windows PowerShell:**
```powershell
# Run the automated setup script
.\setup.ps1

# For help and options:
.\setup.ps1 -Help

# Force recreate virtual environment:
.\setup.ps1 -Force
```

**For macOS/Linux:**
```bash
# Make script executable and run
chmod +x setup.sh
./scripts/setup.sh
```

The automated scripts will:
- [OK] Auto-detect Python installation (no PATH required)
- [OK] Check Python version (3.12+ required)
- [OK] Create and activate virtual environment
- [OK] Install all dependencies automatically
- [OK] Verify the installation works
- [OK] Show you next steps

**Important**: The setup script automatically finds Python in common locations. You don't need to add Python to your system PATH.

### 📋 Manual Setup (5 minutes)

```bash
# 1. Download and extract
# Go to: https://github.com/javiarmesto/Workshop-MCP-Server-Directions-Lab
# Click "Code" → "Download ZIP"
# Extract the ZIP file
# Navigate to the extracted folder:
cd Workshop-MCP-Server-Directions-Lab-main

# 2. Install dependencies
python -m venv workshop-env

# Activate virtual environment
# Windows PowerShell:
.\workshop-env\Activate.ps1
# Windows CMD:
workshop-env\activate.bat
# macOS/Linux:
source workshop-env/bin/activate

# Install dependencies (ensure virtual environment is activated!)
pip install -r requirements.txt

# 3. Configure credentials (optional - works with mock data)
cp .env.example .env
# Edit .env with your Azure AD and Business Central credentials
# Example:
# AZURE_TENANT_ID=your-tenant-id-guid
# AZURE_CLIENT_ID=your-app-registration-client-id
# AZURE_CLIENT_SECRET=your-app-registration-secret
# BC_ENVIRONMENT=production
# BC_COMPANY_ID=your-company-guid

# 4. Test the server works
python ./test_server.py
```

**Expected output**: The test script will show all available MCP tools:
```
[SUCCESS] Server responded!

============================================================
AVAILABLE TOOLS:
============================================================

1. get_customers - Get customer list from Business Central
2. get_items - Get items list from Business Central
3. get_sales_orders - Get sales orders from Business Central
... (6 tools total)

[SUCCESS] Test completed successfully!
```

> 💡 **Quick test**: Use `python tests/test_server.py` to verify your server is working correctly

> 🚨 **Having setup issues?** See [SETUP_TROUBLESHOOTING.md](SETUP_TROUBLESHOOTING.md) for common solutions!

### Visual Testing with MCP Inspector (Optional)

Before configuring Claude Desktop, you can test your server visually with **MCP Inspector**:

**Install MCP Inspector:**
```bash
# Quick (no installation required)
npx @modelcontextprotocol/inspector

# Or install globally
npm install -g @modelcontextprotocol/inspector
mcp-inspector
```

**Get Configuration Paths:**
```powershell
# Run the configuration paths script
.\ConfigurationPaths.ps1
```

This script will display:
- Python executable path
- Server script path
- Workshop path
- **Claude Desktop format** (JSON with forward slashes `/`)
- **MCP Inspector format** (Windows with backslashes `\`)

**Configure in MCP Inspector UI:**
1. **Transport Type**: Select `STDIO`
2. **Command**: Paste the `python.exe` path (Windows format with backslashes)
3. **Arguments**: Paste the `server_workshop.py` path (Windows format)
4. **Environment Variables** (optional):
   - Key: `PYTHONPATH`
   - Value: Your workshop path

**Test Your Server:**
- Click "Connect" to start the server
- Browse the **Tools** tab to see all 6 available tools
- Click any tool and fill parameters to test it
- Check **Prompts** tab for `customer_analysis` and `pricing_analysis`
- Inspect **Resources** tab to view available data files

**Benefits:**
- ✅ Visual interface for debugging
- ✅ Test tools individually without Claude Desktop
- ✅ Inspect JSON request/response data
- ✅ Faster iteration during development

> 📖 **For detailed instructions**, see Step 6-7 in [WORKSHOP_GUIDE_EN.md](WORKSHOP_GUIDE_EN.md)

### Configure with Claude Desktop

**Option A: Automated Configuration (Recommended) ⚡**

```powershell
# Run the automated configuration script
.\configure_claude.ps1
```

This script will:
- ✅ Auto-detect all required paths
- ✅ Backup your existing configuration
- ✅ Create/update Claude Desktop config with correct paths and PYTHONPATH
- ✅ Validate the JSON configuration
- ✅ Open the config file for review
- ✅ Show you the next steps

Then restart Claude Desktop and start using your MCP tools!

---

**Option B: Manual Configuration**

**Get your paths first:**
```powershell
# Run the configuration paths script
.\ConfigurationPaths.ps1
```

Copy the paths from the "FOR CLAUDE DESKTOP (JSON format)" section.

**Edit your Claude Desktop configuration file:**

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`  
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Configuration template** (replace paths with yours):
```json
{
  "mcpServers": {
    "bc-workshop-server": {
      "command": "YOUR_PYTHON_PATH_HERE",
      "args": ["YOUR_SERVER_PATH_HERE"],
      "env": {
        "PYTHONPATH": "YOUR_WORKSHOP_PATH_HERE"
      }
    }
  }
}
```

> ⚠️ **Important**: Include the `"env"` field with `PYTHONPATH` to ensure proper module loading.
> 
> 💡 **Quick validation**: Run `Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json` to test your JSON.

Then restart Claude Desktop and start using your MCP tools!

---

## 📖 Documentation

- **[📘 Complete Workshop Guide](WORKSHOP_GUIDE_EN.md)** - Step-by-step instructions with architecture diagrams
- **[🎓 Presentation Slides](PRESENTATION_SLIDES_EN.md)** - For instructors teaching this workshop
- **[🔧 Troubleshooting](WORKSHOP_GUIDE_EN.md#-troubleshooting)** - Common issues and solutions

---

## 📁 Repository Structure

You should see this structure:

```
Workshop-MCP-Server-Directions-Lab/
├── 📄 server_workshop.py           # Main MCP server (STDIO transport)
├── 📄 validate_workshop.py         # Validation script
├── 📄 test_server.py               # Quick server test (lists tools)
├── 📄 test_workshop_exercise.py    # Exercise tests
├── 📄 requirements.txt             # Python dependencies
├── 📄 setup.ps1                    # Automated setup (Windows)
├── 📄 setup.sh                     # Automated setup (macOS/Linux)
├──  scripts/ConfigurationPaths.ps1       # Get paths for Claude Desktop & MCP Inspector
├── 🔒 .env.example                 # Environment template
├── 📖 README.md                    # This file
├── 📖 QUICK_START_GUIDE.md         # Quick start instructions
├── 📖 WORKSHOP_GUIDE_EN.md         # Complete step-by-step guide
│
├── 📁 src/                         # Source code modules
│   ├── azure_auth.py               # Azure AD authentication
│   ├── client.py                   # Business Central client
│   └── config.py                   # Configuration
│
└── 📁 data/                        # Sample data
    ├── README.md                   # Data files documentation
    ├── categories.csv              # Product categories
    ├── prices.csv                  # Price and stock data
    ├── substitutes.csv             # Product substitutions
    ├── sales_orders.csv            # Mock sales orders
    ├── payment_terms.csv           # Mock payment terms
    └── price-analysis.json         # Price analysis data
```

## 🔧 Prerequisites

### Software Requirements

- **Python 3.12+** (verify: `python --version`)
- **pip** (verify: `pip --version`)
- **Claude Desktop** - Download from [claude.ai](https://claude.ai/download)
- **Text editor** (VS Code, PyCharm, etc.)
- **Terminal/Command line** access

### Business Central Access (Optional)

**With Business Central access:**
- 🏢 **Azure AD Tenant** with Business Central access
- 🔑 **App Registration** in Azure AD (Client ID, Client Secret, Tenant ID)
- 🌍 **BC Environment** name (production or sandbox)
- 📋 **BC Company ID**

**Without Business Central access:**
- ✅ The workshop works with **mock data** included in the `data/` folder
- ✅ You can complete all exercises using sample CSV files
- ✅ Perfect for learning MCP concepts without external dependencies

### Knowledge Prerequisites

Beginner-friendly, but helpful to know:
- Basic Python programming
- JSON format
- Command line usage

---

## 🎓 What is STDIO Transport?

STDIO (Standard Input/Output) transport enables MCP servers to communicate with clients through stdin/stdout streams. This is the standard method for integrating MCP servers with Claude Desktop.

**Key Benefits:**
- ⚡ Fast local communication
- 🔒 No network exposure (secure by default)
- 🎯 Perfect for Claude Desktop integration
- ⚙️ Simple configuration - no ports or networking required

**How it works:**
1. Claude Desktop launches your MCP server as a subprocess
2. Communication happens via standard input/output streams
3. JSON-RPC messages are exchanged over these streams
4. The server provides tools, prompts, and resources to Claude

### STDIO vs HTTP Transport

While this workshop focuses on STDIO transport for Claude Desktop, MCP also supports HTTP-based transport for different use cases:

| Feature | **STDIO** (This Workshop) | **HTTP/SSE** (Alternative) |
|---------|---------------------------|----------------------------|
| **Transport** | stdin/stdout streams | HTTP + Server-Sent Events |
| **Use Case** | Claude Desktop integration | Web integrations, remote access |
| **Network** | Local only | Network-accessible |
| **Setup** | Simple | Requires port configuration |
| **Security** | Isolated by default | Needs HTTPS in production |
| **Best For** | Desktop apps, local tools | Cloud services, webhooks, APIs |

---

## 🛠️ Using This Template

This repository serves as a **complete, working template**. You can:

1. **Run immediately with Claude Desktop**
   - The server works with mock data out of the box
   - No external dependencies required

2. **Study the implementation**
   - See how tools, prompts, and resources are built
   - Understand MCP protocol patterns

3. **Extend with your own features**
   - Add new tools following the examples
   - Create custom prompts for your use case

4. **Connect to your own APIs**
   - Replace Business Central with any API
   - Adapt the patterns to your needs

---

## 🛠️ How to Extend

### Understanding the MCP Server Components

The workshop server demonstrates **three main MCP capabilities:**

#### 1️⃣ **Tools** (Functions Claude can call)
- Located in: `server_workshop.py` → `handle_list_tools()` and `handle_call_tool()`
- Examples: `get_customers`, `get_items`, `get_currency_exchange_rates`
- **How to add your own:**
  ```python
  # In handle_list_tools(), add:
  types.Tool(
      name="your_tool_name",
      description="What your tool does",
      inputSchema={
          "type": "object",
          "properties": {
              "param1": {"type": "string", "description": "Parameter description"}
          }
      }
  )
  
  # In handle_call_tool(), add:
  elif tool_name == "your_tool_name":
      result = await client.your_api_method(arguments.get("param1"))
      return [types.TextContent(type="text", text=json.dumps(result))]
  ```

#### 2️⃣ **Prompts** (Pre-configured Claude prompts)
- Located in: `server_workshop.py` → `handle_list_prompts()` and `handle_get_prompt()`
- Examples: `customer_analysis`, `vendor_analysis`
- **How to add your own:**
  ```python
  # In handle_list_prompts(), add:
  types.Prompt(
      name="your_prompt_name",
      description="What your prompt does",
      arguments=[
          types.PromptArgument(
              name="param1",
              description="Parameter description",
              required=True
          )
      ]
  )
  
  # In handle_get_prompt(), add case for your prompt
  ```

#### 3️⃣ **Resources** (Static data files)
- Located in: `server_workshop.py` → `handle_list_resources()` and `handle_read_resource()`
- Examples: CSV and JSON files in `data/` folder
- **How to add your own:**
  ```python
  # In handle_list_resources(), add:
  types.Resource(
      uri=AnyUrl("file://data/your_file.csv"),
      name="Your Resource Name",
      description="What this resource contains",
      mimeType="text/csv"
  )
  ```

### Practical Workshop Exercise

The repository includes **working examples** you can study:

- ✅ **`vendor_analysis` prompt**: Example of adding a new prompt
- ✅ **`get_currency_exchange_rates` tool**: Example of adding a new tool
- ✅ **Test suite**: `test_workshop_exercise.py` shows how to validate your additions

---

## 📖 Additional Resources

### 🆘 Support

If you encounter problems:

1. 📖 Review the **Troubleshooting** section in [WORKSHOP_GUIDE_EN.md](WORKSHOP_GUIDE_EN.md)
2. 🔍 Check logs in Claude Desktop (View → Developer → Developer Tools)
3. 🌐 Verify credentials if using Business Central
4. ✅ Run `python tests/validate_workshop.py` to check your setup

### 📚 Learning More

- **MCP Specification**: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- **MCP Documentation**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Claude Desktop**: [claude.ai](https://claude.ai)

---

**🚀 Enjoy building with MCP and Business Central!**

*Workshop Duration: 20-30 minutes • Focus: STDIO Transport • Based on MCP SDK*
