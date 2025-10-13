<#
.SYNOPSIS
    Configures Claude Desktop to use the MCP Workshop Server

.DESCRIPTION
    This script automatically:
    - Detects your workshop and Python paths
    - Creates/updates Claude Desktop configuration
    - Backs up existing configuration
    - Opens the config file for review
    - Provides instructions to restart Claude Desktop

.EXAMPLE
    .\configure_claude.ps1
    
.NOTES
    Author: Workshop MCP Server
    Version: 1.0
#>

[CmdletBinding()]
param()

# Color functions for better output
function Write-Step { param($Message) Write-Host "[STEP] $Message" -ForegroundColor Cyan }
function Write-Success { param($Message) Write-Host "[OK] $Message" -ForegroundColor Green }
function Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Yellow }
function Write-Error-Custom { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " CLAUDE DESKTOP MCP CONFIGURATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Get workshop paths
Write-Step "Detecting workshop paths..."

$workshopPath = (Get-Location).Path
$pythonExe = Join-Path $workshopPath "workshop-env\Scripts\python.exe"
$serverScript = Join-Path $workshopPath "server_workshop.py"

# Verify files exist
if (-not (Test-Path $pythonExe)) {
    Write-Error-Custom "Python executable not found: $pythonExe"
    Write-Info "Please run setup.ps1 first to create the virtual environment"
    exit 1
}

if (-not (Test-Path $serverScript)) {
    Write-Error-Custom "Server script not found: $serverScript"
    Write-Info "Please ensure you're in the workshop directory"
    exit 1
}

Write-Success "Workshop directory: $workshopPath"
Write-Success "Python executable: $pythonExe"
Write-Success "Server script: $serverScript"
Write-Host ""

# Step 2: Convert paths to JSON format (forward slashes)
Write-Step "Converting paths to JSON format..."

$pythonPathJson = $pythonExe -replace '\\', '/'
$serverPathJson = $serverScript -replace '\\', '/'
$workshopPathJson = $workshopPath -replace '\\', '/'

Write-Success "Paths ready for JSON configuration"
Write-Host ""

# Step 3: Locate Claude Desktop config
Write-Step "Locating Claude Desktop configuration..."

$claudeConfigDir = Join-Path $env:APPDATA "Claude"
$claudeConfigFile = Join-Path $claudeConfigDir "claude_desktop_config.json"

Write-Info "Config file location: $claudeConfigFile"

# Create directory if it doesn't exist
if (-not (Test-Path $claudeConfigDir)) {
    Write-Info "Creating Claude config directory..."
    New-Item -ItemType Directory -Path $claudeConfigDir -Force | Out-Null
    Write-Success "Directory created"
}

Write-Host ""

# Step 4: Backup existing configuration
if (Test-Path $claudeConfigFile) {
    Write-Step "Backing up existing configuration..."
    
    $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backupFile = Join-Path $claudeConfigDir "claude_desktop_config.backup.$timestamp.json"
    
    Copy-Item $claudeConfigFile $backupFile
    Write-Success "Backup saved: $backupFile"
    Write-Host ""
}

# Step 5: Create new configuration
Write-Step "Creating MCP server configuration..."

$config = @{
    mcpServers = @{
        "bc-workshop-server" = @{
            command = $pythonPathJson
            args = @($serverPathJson)
            env = @{
                PYTHONPATH = $workshopPathJson
            }
        }
    }
}

# Convert to JSON with proper formatting
$jsonConfig = $config | ConvertTo-Json -Depth 10

Write-Success "Configuration generated"
Write-Host ""

# Step 6: Write configuration file
Write-Step "Writing configuration to file..."

try {
    # Ensure UTF-8 encoding without BOM
    [System.IO.File]::WriteAllText($claudeConfigFile, $jsonConfig, [System.Text.UTF8Encoding]::new($false))
    Write-Success "Configuration file updated successfully"
} catch {
    Write-Error-Custom "Failed to write configuration file: $_"
    exit 1
}

Write-Host ""

# Step 7: Display configuration
Write-Host "============================================================" -ForegroundColor Green
Write-Host " CONFIGURATION SUMMARY" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Server Name: bc-workshop-server" -ForegroundColor White
Write-Host "Python Path: $pythonPathJson" -ForegroundColor White
Write-Host "Server Path: $serverPathJson" -ForegroundColor White
Write-Host "PYTHONPATH: $workshopPathJson" -ForegroundColor White
Write-Host ""

Write-Host "Configuration file:" -ForegroundColor Yellow
Write-Host $claudeConfigFile -ForegroundColor White
Write-Host ""

# Step 8: Verify JSON is valid
Write-Step "Validating JSON configuration..."

try {
    $testRead = Get-Content $claudeConfigFile -Raw | ConvertFrom-Json
    Write-Success "JSON configuration is valid"
} catch {
    Write-Error-Custom "Invalid JSON configuration: $_"
    Write-Info "Please check the configuration file manually"
}

Write-Host ""

# Step 9: Open configuration file
Write-Step "Opening configuration file for review..."
Start-Process notepad.exe -ArgumentList $claudeConfigFile
Write-Success "Configuration file opened in Notepad"
Write-Host ""

# Step 10: Show next steps
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " NEXT STEPS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Review the configuration in Notepad (just opened)" -ForegroundColor Yellow
Write-Host "2. Close Notepad (configuration is already saved)" -ForegroundColor Yellow
Write-Host "3. QUIT Claude Desktop completely (not just minimize)" -ForegroundColor Yellow
Write-Host "4. Restart Claude Desktop" -ForegroundColor Yellow
Write-Host "5. Look for the MCP indicator (tool/plugin icon)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Test in Claude Desktop with these prompts:" -ForegroundColor Green
Write-Host '  - "What MCP servers are connected?"' -ForegroundColor White
Write-Host '  - "Show me available tools"' -ForegroundColor White
Write-Host '  - "Get the top 5 customers from Business Central"' -ForegroundColor White
Write-Host ""
Write-Host "Expected: 6 tools available (get_customers, get_items, etc.)" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " CONFIGURATION COMPLETE!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
