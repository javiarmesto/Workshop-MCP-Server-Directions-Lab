# 🎓 MCP Server Workshop - Support Slides

> **Compact presentation slides for workshop delivery**  
> MCP Server Workshop with STDIO Transport for Claude Desktop  
> Business Central Integration

---

## 📊 SLIDE 1: Workshop Introduction

### 🚀 MCP Server Workshop
**Building an MCP Server with STDIO Transport**

**What we'll build:**
- 🔧 MCP Server with STDIO transport
- 🏢 Business Central API integration
- 💬 Claude Desktop integration
- 📊 Tools, Prompts & Resources

**Duration:** 20-30 minutes hands-on

**Repository:** github.com/javiarmesto/Workshop-MCP-Server-Directions

---

## 📊 SLIDE 2: Workshop Structure & Objectives

### 📋 9-Step Workshop Flow

**Steps 1-4:** Environment Setup
- Python 3.12+ virtual environment
- Install dependencies (`mcp`, `httpx`, `msal`)
- Validate setup with `validate_workshop.py`

**Steps 5-7:** MCP Server Configuration
- Configure Claude Desktop (`claude_desktop_config.json`)
- Test connection with Claude
- Verify tools are available

**Step 8:** Connection Validation
- Test MCP tools in Claude
- Verify prompts and resources

**Step 9:** Hands-On Exercises ⭐
- **Part A:** Test existing tools (get_customers, get_currency_exchange_rates)
- **Part B:** Implement new tools (get_sales_orders, get_payment_terms)

### ✅ Learning Outcomes
- Understand MCP architecture (Tools, Prompts, Resources)
- Configure STDIO transport for Claude Desktop
- Create Business Central API integrations
- Build custom MCP tools with copy-paste examples

---

## 📊 SLIDE 3: MCP Architecture Overview

### 🏗️ System Architecture

```
┌─────────────────────────────────┐
│      CLAUDE DESKTOP             │
│   (MCP Client - JSON-RPC)       │
└──────────────┬──────────────────┘
               │ STDIO (stdin/stdout)
               ▼
┌─────────────────────────────────┐
│   server_workshop.py            │
│   (MCP Server - STDIO)          │
├─────────────────────────────────┤
│  Tools │ Prompts │ Resources    │
└──────┬───────────┬──────────────┘
       │           │
       ▼           ▼
┌──────────────┐  ┌───────────────┐
│   client.py  │  │  data/ (CSV)  │
│  (BC Client) │  │  Mock Data    │
└──────┬───────┘  └───────────────┘
       │ OAuth 2.0
       ▼
┌─────────────────────────────────┐
│   BUSINESS CENTRAL (OData API)  │
└─────────────────────────────────┘
```

### 🔑 Key Components
- **STDIO Transport:** Direct process communication (no ports/networking)
- **Tools:** Functions Claude can call (get_customers, get_items, etc.)
- **Prompts:** Pre-configured templates (customer_analysis, vendor_analysis)
- **Resources:** CSV/JSON data files exposed to Claude
- **Mock Mode:** Works without BC credentials (default)

---

## 📊 SLIDE 4: Configuration & Setup

### ⚙️ Quick Setup Commands

```bash
# 1. Clone and navigate
git clone https://github.com/javiarmesto/Workshop-MCP-Server-Directions.git
cd Workshop-MCP-Server-Directions

# 2. Create virtual environment
python -m venv workshop-env
.\workshop-env\Scripts\activate  # Windows
source workshop-env/bin/activate  # macOS/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Validate setup
python validate_workshop.py
```

### 📝 Claude Desktop Configuration

**Location:**
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Config:**
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

⚠️ **Critical:** Use **absolute paths** only!

### ✅ Validation Prompts
```
"What MCP tools do you have available?"
"Show me the top 5 customers"
```

---

## 📊 SLIDE 5: Step 9 - Hands-On Exercises

### 🎯 Part A: Testing Existing Tools (10 min)

**Exercise 1: Test get_customers + customer_analysis**
```
"Show me the list of customers"
"Give me a customer analysis using the prompt"
```

**Exercise 2: Test get_currency_exchange_rates**
```
"Show me currency exchange rates"
"Get exchange rates for USD"
```

### 🎯 Part B: Implementing New Tools (15 min)

**Exercise 3: Implement get_sales_orders**
1. Create `data/sales_orders.csv` (mock data)
2. Add `get_sales_orders()` method in `src/client.py`
3. Register tool in `server_workshop.py` (list_tools)
4. Implement handler in `server_workshop.py` (call_tool)
5. Test: `"Show me sales orders"`

**Exercise 4: Implement get_payment_terms**
1. Create `data/payment_terms.csv` (mock data)
2. Add `get_payment_terms()` method in `src/client.py`
3. Register tool in `server_workshop.py` (list_tools)
4. Implement handler in `server_workshop.py` (call_tool)
5. Test: `"Show me payment terms"`

### 📖 Complete Code
All copy-paste code available in **WORKSHOP_GUIDE_EN.md** (Step 9)

---

## 📊 SLIDE 6: Resources & Next Steps

### 📚 Documentation & References

**Workshop Materials:**
- 📖 `WORKSHOP_GUIDE_EN.md` - Complete step-by-step guide
- ✅ `validate_workshop.py` - Setup validation script
- 📦 `data/` - Mock CSV files for testing
- 💻 Repository: github.com/javiarmesto/Workshop-MCP-Server-Directions

**MCP Protocol:**
- 🌐 Spec: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- 📖 Docs: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- 🛠️ Python SDK: `pip install mcp`

**Business Central:**
- 📘 [BC API Reference](https://learn.microsoft.com/dynamics365/business-central/dev-itpro/api-reference/)
- 🔐 [Azure AD Auth](https://learn.microsoft.com/azure/active-directory/)

### 🎯 Next Steps

**Today:**
- Complete all Step 9 exercises
- Test with different prompts
- Experiment with mock data

**This Week:**
- Add your own custom tools
- Try real Business Central connection (optional)
- Explore prompts and resources

**This Month:**
- Build tools for your business needs
- Integrate with other APIs
- Share with your team

### 🆘 Troubleshooting

**Server not appearing?**
- Verify absolute paths in config
- Restart Claude Desktop
- Check `validate_workshop.py` passes

**Tools not working?**
- Test: `python server_workshop.py`
- Check mock data files exist
- Review Claude Desktop logs

---


