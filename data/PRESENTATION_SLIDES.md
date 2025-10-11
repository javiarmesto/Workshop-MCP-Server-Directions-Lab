# 🎓 MCP Server Workshop - Presentation Slides

> **Guía resumida para convertir en slides de presentación**  
> Taller de Servidor MCP con integración Business Central

---

## 📊 SLIDE 1: Portada

### MCP Server Workshop
**Construyendo un Servidor MCP con StreamableHTTP**

- 🏢 Integración con Microsoft Dynamics 365 Business Central
- 🔧 Model Context Protocol (MCP)
- 🌐 StreamableHTTP + Server-Sent Events (SSE)
- 👨‍💻 Taller Práctico Hands-On

**Autor**: Javier Armesto González  
**Repositorio**: github.com/javiarmesto/Workshop-MCP-Server-Directions

---

## 📊 SLIDE 2: Objetivos del Workshop

### ¿Qué Aprenderás?

✅ **Fundamentos del Protocolo MCP**
- Arquitectura y componentes
- JSON-RPC y comunicación cliente-servidor

✅ **Implementación de Servidor MCP**
- StreamableHTTP con SSE
- Gestión de sesiones y transporte

✅ **Integración con APIs**
- Conexión con Business Central
- Autenticación Azure AD

✅ **Creación de Herramientas Personalizadas**
- Tools, Prompts y Resources
- Extensibilidad del servidor

---

## 📊 SLIDE 3: Duración y Prerrequisitos

### ⏱️ Duración Estimada

- **Ruta Rápida**: 30 minutos
  - Setup básico y testing
- **Ruta Completa**: 2-3 horas
  - Incluye ejercicios de personalización

### 🔧 Prerrequisitos

**Software**:
- Python 3.12+
- pip, Git
- Editor de código (VS Code, PyCharm)

**Conocimientos** (básicos):
- Programación en Python
- Conceptos HTTP/REST API
- Formato JSON
- Línea de comandos

**Opcional**:
- Credenciales Azure AD
- Acceso a Business Central
- Claude Desktop

---

## 📊 SLIDE 4: Arquitectura MCP - Vista General

```
┌─────────────────────────────────────┐
│   CLAUDE DESKTOP / CLIENT           │
│   (MCP Protocol Consumer)           │
└──────────────┬──────────────────────┘
               │ MCP Protocol (JSON-RPC)
               │ StreamableHTTP + SSE
               ▼
┌─────────────────────────────────────┐
│   server_workshop.py                │
│   (MCP Server Implementation)       │
│                                     │
│   ┌──────┐ ┌──────┐ ┌──────┐      │
│   │TOOLS │ │PROMPTS│ │RESOURCES│   │
│   └──┬───┘ └──────┘ └──────┘      │
│      │                             │
│      ▼                             │
│   client.py                        │
│   (Business Central API Client)    │
└──────────────┬──────────────────────┘
               │ OAuth 2.0
               ▼
┌─────────────────────────────────────┐
│   MICROSOFT DYNAMICS 365            │
│   BUSINESS CENTRAL (OData APIs)     │
└─────────────────────────────────────┘
```

---

## 📊 SLIDE 5: Componentes Principales

### 🎯 5 Componentes Clave

**1. MCP Server** (`server_workshop.py`)
- Punto de entrada principal
- Maneja JSON-RPC requests
- Implementa Tools, Prompts, Resources

**2. Configuration** (`config.py` + `.env`)
- Gestión de variables de entorno
- Credenciales Azure AD y BC
- Validación de configuración

**3. Business Central Client** (`client.py`)
- Comunicación con APIs de BC
- Flujo de autenticación OAuth
- Métodos para queries (customers, items, orders)

**4. Azure Authentication** (`azure_auth.py`)
- OAuth 2.0 con Azure AD
- Adquisición y refresh de tokens
- Modo mock si no hay credenciales

**5. Session Manager** (`simple_session_manager.py`)
- Gestión de sesiones HTTP
- Interface mínima sin persistencia

---

## 📊 SLIDE 6: Opciones de Transporte - HTTP vs STDIO

### 🔀 Dos Implementaciones

| Característica | **HTTP** (server_workshop.py) | **STDIO** (server_stdio.py) |
|---|---|---|
| **Transporte** | HTTP + SSE | stdin/stdout |
| **Acceso Red** | ✅ Sí | ❌ No |
| **Claude Desktop** | ❌ No | ✅ Sí |
| **Copilot Studio** | ✅ Sí | ❌ No |
| **Múltiples Clientes** | ✅ Sí | ❌ No |
| **Testing** | PowerShell, curl, Postman | Claude Desktop |
| **Producción** | ✅ Sí (con HTTPS) | ⚠️ Solo local |
| **Puerto** | 8000 (configurable) | No requiere |

---

## 📊 SLIDE 7: Cuándo Usar Cada Transporte

### 🌐 Usar HTTP (`server_workshop.py`) cuando:

- ✅ Necesitas testing con MCP Inspector
- ✅ Integración con Copilot Studio
- ✅ Deploy en producción
- ✅ Acceso remoto al servidor MCP
- ✅ Múltiples clientes simultáneos
- ✅ Desarrollo y debugging con herramientas web

### 💻 Usar STDIO (`server_stdio.py`) cuando:

- ✅ Integración con Claude Desktop
- ✅ Acceso solo local
- ✅ Setup más simple
- ✅ Comunicación proceso-a-proceso

### 💡 Usa Ambos:
- Pueden ejecutarse simultáneamente
- HTTP para testing/desarrollo
- STDIO para Claude Desktop
- Comparten la misma configuración

---

## 📊 SLIDE 8: Archivos Clave - `.env` y `config.py`

### 🔐 `.env` - Configuración de Entorno

```env
# Azure Active Directory
AZURE_CLIENT_ID=your-app-client-id
AZURE_CLIENT_SECRET=your-app-secret
AZURE_TENANT_ID=your-tenant-id

# Business Central
BC_ENVIRONMENT=production
BC_COMPANY_ID=your-company-guid

# Server
SERVER_PORT=8000
LOG_LEVEL=INFO
```

**Beneficios**:
- Separa credenciales del código
- Diferentes configs por entorno
- Protegido por `.gitignore`
- **Modo mock si faltan credenciales** ✨

---

## 📊 SLIDE 9: Archivos Clave - `client.py`

### 📡 Business Central API Client

**Responsabilidades**:
- Autenticación con tokens Azure AD
- Comunicación HTTP con endpoints OData
- Recuperación de datos (customers, items, orders)
- Manejo de errores y fallback a datos mock

**Métodos Principales**:
```python
async def get_customers(filter=None, top=50)
async def get_items(filter=None, top=50)
async def get_sales_orders(filter=None, top=50)
async def get_currency_exchange_rates(currency_code=None, top=20)
```

**Flujo de Datos**:
```
User → Claude → MCP Server → Client → Azure AD → BC API → Response
```

---

## 📊 SLIDE 10: Archivos Clave - `server_workshop.py`

### 🚀 Servidor MCP Principal

**Componentes**:

1. **Inicialización del Servidor**
```python
server = Server("business-central-workshop")
bc_client = BusinessCentralClient()
```

2. **Handlers de Tools**
```python
@server.list_tools()    # Lista herramientas disponibles
@server.call_tool()     # Ejecuta una herramienta
```

3. **Handlers de Prompts**
```python
@server.list_prompts()  # Lista prompts disponibles
@server.get_prompt()    # Genera mensajes de prompt
```

4. **Handlers de Resources**
```python
@server.list_resources() # Lista archivos de datos
@server.read_resource()  # Lee contenido de recursos
```

5. **HTTP Server Setup**
```python
app = Starlette(routes=[...])
uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## 📊 SLIDE 11: Instalación Paso a Paso (1/3)

### 📥 Paso 1: Clonar Repositorio

```bash
git clone https://github.com/javiarmesto/Workshop-MCP-Server-Directions.git
cd Workshop-MCP-Server-Directions
```

### 🐍 Paso 2: Verificar Python

```bash
python --version
# Debe mostrar: Python 3.12.x o superior
```

**Si no tienes Python 3.12+**:
- Windows: python.org
- macOS: `brew install python@3.12`
- Linux: `sudo apt install python3.12`

---

## 📊 SLIDE 12: Instalación Paso a Paso (2/3)

### 🌍 Paso 3: Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv workshop-env

# Activar
# Windows:
workshop-env\Scripts\activate

# macOS/Linux:
source workshop-env/bin/activate
```

### 📦 Paso 4: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Se instalan**:
- `mcp` - Model Context Protocol SDK
- `httpx` - Cliente HTTP
- `starlette` - Framework ASGI
- `uvicorn` - Servidor ASGI
- `pydantic` - Validación de datos
- `python-dotenv` - Carga de .env

---

## 📊 SLIDE 13: Instalación Paso a Paso (3/3)

### ⚙️ Paso 5: Configurar Variables de Entorno

```bash
# Copiar template
cp .env.example .env

# Editar .env con tus credenciales
```

### ✅ Paso 6: Validar Setup

```bash
python validate_workshop.py
```

**Output esperado**:
```
✅ Python Version: 3.12.x - OK
✅ Dependencies: All installed
✅ Files: All required files present
✅ Configuration: .env file found
✅ Data Files: All sample data accessible
✅ Server Import: server_workshop.py loads successfully
```

---

## 📊 SLIDE 14: Ejecutar el Servidor

### 🚀 Iniciar Servidor HTTP

```bash
python server_workshop.py
```

**Output esperado**:
```
🚀 Starting BC Workshop MCP Server...

Configuration:
✓ Server name: bc-workshop-server
✓ Server port: 8000
✓ Endpoints: / (health), /mcp (MCP protocol)

INFO: Uvicorn running on http://0.0.0.0:8000
```

### 🧪 Probar Health Endpoint

```bash
curl http://localhost:8000/

# Respuesta:
{
  "name": "bc-workshop-server",
  "version": "1.0",
  "status": "running"
}
```

---

## 📊 SLIDE 15: Testing - Listar Tools

### 📋 Obtener Herramientas Disponibles

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/mcp" -Method POST `
  -Headers @{ 
    "Content-Type" = "application/json"; 
    "Accept" = "application/json, text/event-stream" 
  } `
  -Body '{
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": 1
  }'
```

**Tools Disponibles**:
- `get_customers` - Lista de clientes
- `get_items` - Lista de productos
- `get_sales_orders` - Órdenes de venta
- `get_customer_details` - Detalles de cliente específico
- `get_item_details` - Detalles de producto específico
- `get_currency_exchange_rates` - Tasas de cambio

---

## 📊 SLIDE 16: Testing - Ejecutar Tool

### 🛠️ Ejemplo: Obtener Clientes

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/mcp" -Method POST `
  -Headers @{ 
    "Content-Type" = "application/json"; 
    "Accept" = "application/json, text/event-stream" 
  } `
  -Body '{
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
      "name": "get_customers",
      "arguments": {"top": 5}
    },
    "id": 2
  }'
```

**Respuesta**: Datos de clientes
- Adatum Corporation
- Trey Research
- School of Fine Art
- Alpine Ski House
- Relecloud

---

## 📊 SLIDE 17: MCP Inspector - Testing Visual

### 🔍 ¿Qué es MCP Inspector?

Herramienta oficial de Anthropic para debugging de servidores MCP:

- 📋 Lista tools, prompts y resources
- 🧪 Testing de tools con parámetros custom
- 👁️ Inspección de request/response
- 🐛 Debugging de implementaciones MCP
- 📊 Respuestas en tiempo real

### 🚀 Instalación y Uso

```powershell
# Requiere Node.js 18+
node --version

# Lanzar Inspector (no requiere instalación)
npx @modelcontextprotocol/inspector http://localhost:8000/mcp
```

**Abre automáticamente**:
- Interface web en navegador
- Panel de Tools, Prompts, Resources
- Visor de Request/Response

---

## 📊 SLIDE 18: ngrok - Exposición Pública

### 🌐 ¿Qué es ngrok?

Crea túneles seguros desde internet a tu máquina local:

**Casos de Uso**:
- 🌍 Testing remoto desde cualquier dispositivo
- 🤝 Integraciones externas (Copilot Studio)
- 📱 Testing desde móvil
- 👥 Demos instantáneos

### 📥 Instalación

```powershell
# Opción 1: Chocolatey
choco install ngrok

# Opción 2: Scoop
scoop install ngrok

# Opción 3: Download manual
# https://ngrok.com/
```

### 🔑 Configuración

```powershell
# Obtener authtoken en ngrok.com
ngrok config add-authtoken YOUR_TOKEN
```

---

## 📊 SLIDE 19: ngrok - Uso Básico

### 🚀 Crear Túnel

```powershell
# Paso 1: Iniciar servidor MCP
python server_workshop.py

# Paso 2: Crear túnel (nueva terminal)
ngrok http 8000
```

**Output**:
```
Forwarding    https://abc123.ngrok.io -> http://localhost:8000
```

### 🧪 Probar URL Pública

```powershell
# Test desde PowerShell
Invoke-RestMethod -Uri "https://abc123.ngrok.io/" -Method GET

# Test con MCP Inspector
npx @modelcontextprotocol/inspector https://abc123.ngrok.io/mcp
```

### 🔒 Seguridad

⚠️ **Solo para testing, nunca producción**
- Usar datos mock
- Limitar tiempo de exposición
- Monitorear requests en http://127.0.0.1:4040

---

## 📊 SLIDE 20: Integración con Copilot Studio

### 🤖 Conectar MCP Server a Copilot Studio

**Paso 1**: Crear túnel ngrok
```powershell
ngrok http 8000
# URL pública: https://abc123.ngrok.io
```

**Paso 2**: Configurar en Copilot Studio
- URL: `https://abc123.ngrok.io/mcp`
- Method: POST
- Headers:
  - `Content-Type: application/json`
  - `Accept: application/json, text/event-stream`

**Paso 3**: Usar tools en Copilot
- "Get my top 5 customers" → `get_customers`
- "Show item details for 1896-S" → `get_item_details`
- "List recent sales orders" → `get_sales_orders`

---

## 📊 SLIDE 21: Integración con Claude Desktop

### 💬 Configurar Claude Desktop

**Ubicación del config**:
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Configuración** (usar `server_stdio.py`):
```json
{
  "mcpServers": {
    "business-central-workshop": {
      "command": "python",
      "args": [
        "/absolute/path/to/Workshop-MCP-Server-Directions/server_stdio.py"
      ],
      "env": {
        "PYTHONPATH": "/absolute/path/to/Workshop-MCP-Server-Directions"
      }
    }
  }
}
```

**⚠️ Importante**: Usar rutas absolutas, no relativas

### 🧪 Testing

1. Reiniciar Claude Desktop
2. Buscar indicador de servidor MCP (ícono de herramientas)
3. Probar prompts:
   - "Show me available Business Central tools"
   - "Get top 5 customers"

---

## 📊 SLIDE 22: Ejercicios Prácticos

### 🎯 Ejercicio 1: Explorar Prompts

**Ya implementado** - Estudiar código:
```python
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
```

### 🎯 Ejercicio 2: Explorar Tools

**Ya implementado** - Revisar:
- Tool definition en `server_workshop.py`
- Client method en `src/client.py`
- Testing con PowerShell o Inspector

### 🎯 Ejercicio 3: Crear Tu Propio Tool

**Desafío**: Añadir tool para obtener información de vendors

**Pistas**:
1. Definir tool en `handle_list_tools()`
2. Handler en `handle_call_tool()`
3. Método en `client.py` (opcional)
4. Test con PowerShell o Claude Desktop

---

## 📊 SLIDE 23: Estructura de Datos - Resources

### 📁 Data Resources Disponibles

**Archivos CSV en `/data`**:

1. **`categories.csv`** - Categorías de productos
   - CAT001: Office Furniture
   - CAT002: Office Accessories
   - CAT003: Coffee Machines
   - CAT004: Coffee Accessories
   - CAT005: Coffee and Consumables

2. **`prices.csv`** - Precios y stock

3. **`substitutes.csv`** - Productos sustitutos

4. **`price-analysis.json`** - Análisis procesado

**Acceso vía MCP**:
```
URI: file://data/categories.csv
URI: file://analysis/price-analysis.json
```

---

## 📊 SLIDE 24: Troubleshooting - Problemas Comunes

### ❌ Servidor no inicia

**Error**: `ModuleNotFoundError: No module named 'mcp'`
```bash
pip install -r requirements.txt
```

**Error**: `Port 8000 is already in use`
```bash
# Cambiar puerto en .env
SERVER_PORT=8001

# O matar proceso existente
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

### ❌ Problemas de configuración

**Error**: `AZURE_CLIENT_ID not found`
```bash
cp .env.example .env
# Editar .env con credenciales
```

### ❌ Claude Desktop no muestra servidor

1. Verificar rutas absolutas en config
2. Reiniciar Claude Desktop completamente
3. Revisar logs de Claude Desktop

---

## 📊 SLIDE 25: Mejores Prácticas

### ✅ Desarrollo

- 📝 Usar logging apropiado (`LOG_LEVEL=DEBUG`)
- 🧪 Testing incremental con Inspector
- 📁 Separar configuración del código (.env)
- 🔄 Modo mock para desarrollo sin credenciales
- 📊 Monitorear logs del servidor

### ✅ Seguridad

- 🔐 Nunca commitear credenciales al repo
- 🔒 Usar HTTPS en producción
- 🛡️ Validar inputs en tools
- ⚠️ ngrok solo para testing, no producción
- 🔑 Rotar tokens regularmente

### ✅ Performance

- ⚡ Usar async/await correctamente
- 💾 Cache de tokens de autenticación
- 🎯 Limitar resultados con parámetro `top`
- 📉 Filtrar datos en API, no en cliente

---

## 📊 SLIDE 26: Extensibilidad del Servidor

### 🔧 Cómo Extender el Servidor

**1. Añadir Nuevo Tool**:
```python
# En handle_list_tools()
types.Tool(
    name="mi_nuevo_tool",
    description="Descripción del tool",
    inputSchema={...}
)

# En handle_call_tool()
if name == "mi_nuevo_tool":
    result = await mi_logica(arguments)
    return format_response(result)
```

**2. Añadir Nuevo Prompt**:
```python
# En handle_list_prompts()
types.Prompt(
    name="mi_prompt",
    description="Descripción",
    arguments=[...]
)

# En handle_get_prompt()
if name == "mi_prompt":
    return crear_mensajes(arguments)
```

**3. Añadir Nuevo Resource**:
```python
# En handle_list_resources()
types.Resource(
    uri="file://data/mi_archivo.csv",
    name="Mi Archivo",
    mimeType="text/csv"
)
```

---

## 📊 SLIDE 27: Casos de Uso Reales

### 🏢 Business Central Integration

**Consultas Comunes**:
- "Muéstrame los top 10 clientes por ventas"
- "¿Qué productos están bajo de stock?"
- "Dame un resumen de órdenes pendientes"
- "Analiza las tendencias de ventas del último mes"

### 🤖 Copilot Studio Integration

**Escenarios**:
- Asistente virtual para ventas
- Bot de soporte al cliente
- Análisis de datos empresariales
- Automatización de reportes

### 💬 Claude Desktop Integration

**Workflows**:
- Análisis de datos con IA
- Generación de informes
- Consultas en lenguaje natural
- Data exploration interactiva

---

## 📊 SLIDE 28: Arquitectura de Producción

### 🚀 Deploy a Producción

**Opciones de Hosting**:

1. **Azure App Service**
   - Integración nativa con Azure AD
   - HTTPS automático
   - Escalado automático

2. **AWS Lambda + API Gateway**
   - Serverless
   - Pay-per-use
   - Auto-scaling

3. **Docker Container**
   - Portabilidad
   - Consistencia entre entornos
   - Kubernetes-ready

**Consideraciones**:
- ✅ Usar HTTPS (TLS/SSL)
- ✅ Variables de entorno seguras
- ✅ Logging centralizado
- ✅ Monitoreo y alertas
- ✅ Rate limiting
- ✅ Autenticación/autorización

---

## 📊 SLIDE 29: Recursos y Documentación

### 📚 Referencias Importantes

**MCP Protocol**:
- 🌐 Especificación: [spec.modelcontextprotocol.io](https://spec.modelcontextprotocol.io)
- 📖 Documentación: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- 🛠️ SDK Python: `pip install mcp`

**Business Central**:
- 📘 API Reference: [Microsoft Docs - BC API](https://learn.microsoft.com/dynamics365/business-central/dev-itpro/api-reference/)
- 🔐 Azure AD Auth: [Microsoft Identity Platform](https://learn.microsoft.com/azure/active-directory/)

**Herramientas**:
- 🔍 MCP Inspector: `npx @modelcontextprotocol/inspector`
- 🌐 ngrok: [ngrok.com](https://ngrok.com)
- 💬 Claude Desktop: [claude.ai/download](https://claude.ai/download)

**Este Workshop**:
- 📦 Repositorio: [github.com/javiarmesto/Workshop-MCP-Server-Directions](https://github.com/javiarmesto/Workshop-MCP-Server-Directions)
- 📖 Guía Completa: `WORKSHOP_GUIDE_EN.md`
- ✅ Validación: `python validate_workshop.py`

---

## 📊 SLIDE 30: Próximos Pasos

### 🎯 Después del Workshop

**1. Personalizar el Servidor** (30 min)
- ✍️ Añade tus propios tools
- 🎨 Crea prompts específicos
- 📊 Conecta nuevas fuentes de datos

**2. Integrar con tus APIs** (1-2 horas)
- 🔌 Reemplaza Business Central con tu API
- 🔄 Adapta los patterns a tus necesidades
- 🧪 Testing exhaustivo

**3. Deploy en Producción** (2-4 horas)
- ☁️ Selecciona plataforma de hosting
- 🔒 Configura HTTPS y seguridad
- 📊 Setup de monitoring
- 🚀 Deploy y validación

**4. Aprender Más** 
- 📚 Estudiar especificación MCP
- 🎓 Explorar ejemplos avanzados
- 👥 Unirse a la comunidad MCP

---

## 📊 SLIDE 31: Conclusiones y Q&A

### ✅ Lo Que Has Aprendido

- 🏗️ Arquitectura y componentes de MCP
- 🔧 Implementación de servidor con StreamableHTTP
- 🌐 Diferencias entre transporte HTTP y STDIO
- 🛠️ Creación de Tools, Prompts y Resources
- 🧪 Testing con Inspector y ngrok
- 💬 Integración con Claude Desktop y Copilot Studio
- 🔐 Configuración y seguridad
- 📊 Troubleshooting común

### 🎉 ¡Felicidades!

Has completado el **MCP Server Workshop**

### ❓ Preguntas y Respuestas

**Contacto**:
- 📧 Email: [info del repo]
- 💬 Issues: GitHub repository
- 🌐 Documentación: WORKSHOP_GUIDE_EN.md

---

## 📊 SLIDE 32: Bonus - Snippets Útiles

### 🔧 PowerShell - List Tools

```powershell
$headers = @{
    "Content-Type" = "application/json"
    "Accept" = "application/json, text/event-stream"
}

$body = @{
    jsonrpc = "2.0"
    method = "tools/list"
    params = @{}
    id = 1
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/mcp" `
    -Method POST -Headers $headers -Body $body
```

### 🔧 PowerShell - Call Tool

```powershell
$body = @{
    jsonrpc = "2.0"
    method = "tools/call"
    params = @{
        name = "get_customers"
        arguments = @{ top = 5 }
    }
    id = 2
} | ConvertTo-Json -Depth 3

Invoke-RestMethod -Uri "http://localhost:8000/mcp" `
    -Method POST -Headers $headers -Body $body
```

---

## 📊 SLIDE 33: Bonus - Comandos Rápidos

### ⚡ Comandos de Uso Frecuente

```bash
# Iniciar servidor
python server_workshop.py

# Iniciar servidor con debug
python server_workshop.py --log-level DEBUG

# Validar configuración
python validate_workshop.py

# Instalar dependencias
pip install -r requirements.txt

# Crear entorno virtual
python -m venv workshop-env

# Activar entorno (Windows)
workshop-env\Scripts\activate

# Activar entorno (macOS/Linux)
source workshop-env/bin/activate

# Verificar servidor
curl http://localhost:8000/

# Lanzar MCP Inspector
npx @modelcontextprotocol/inspector http://localhost:8000/mcp

# Crear túnel ngrok
ngrok http 8000
```

---

## 📊 SLIDE 34: Bonus - Estructura del Proyecto

```
Workshop-MCP-Server-Directions/
│
├── 📄 server_workshop.py          # Servidor MCP HTTP
├── 📄 server_stdio.py             # Servidor MCP STDIO
├── 📄 validate_workshop.py        # Script de validación
├── 📄 requirements.txt            # Dependencias Python
├── 🔒 .env.example                # Template de configuración
├── 📖 README.md                   # Documentación principal
├── 📖 WORKSHOP_GUIDE_EN.md        # Guía paso a paso
├── 📖 PRESENTATION_SLIDES.md      # Esta presentación
│
├── 📁 src/                        # Código fuente
│   ├── azure_auth.py              # Autenticación Azure AD
│   ├── client.py                  # Cliente Business Central
│   ├── config.py                  # Gestión de configuración
│   ├── event_store.py             # Almacenamiento de eventos
│   └── simple_session_manager.py  # Gestión de sesiones
│
└── 📁 data/                       # Datos de ejemplo
    ├── README.md                  # Documentación de datos
    ├── prices.csv                 # Precios y stock
    ├── categories.csv             # Categorías de productos
    ├── substitutes.csv            # Productos sustitutos
    └── price-analysis.json        # Análisis procesado
```

---

## 📊 FIN

### 🚀 ¡Gracias por Participar!

**Workshop MCP Server - Business Central Integration**

💡 **Recuerda**:
- Practica con los ejercicios
- Experimenta con tu propio código
- Consulta la documentación
- Comparte tu experiencia

📦 **Repositorio**: github.com/javiarmesto/Workshop-MCP-Server-Directions

👨‍💻 **Autor**: Javier Armesto González

**¡Éxito con tus proyectos MCP!** 🎉

---

> **Nota**: Este documento está diseñado para ser convertido en slides de presentación.  
> Cada sección marcada con "SLIDE X" representa una diapositiva individual.  
> Ajusta el contenido según el tiempo disponible y la audiencia.
