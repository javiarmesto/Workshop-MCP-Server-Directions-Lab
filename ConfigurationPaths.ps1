# Configuration Paths Script
# Generates configuration paths for both Claude Desktop and MCP Inspector
# Usage: .\ConfigurationPaths.ps1

# Get workshop path
$workshopPath = (Get-Location).Path

# Display header
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " CONFIGURATION PATHS" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Display workshop path
Write-Host "Workshop Path:" -ForegroundColor Yellow
Write-Host "  $workshopPath" -ForegroundColor White
Write-Host ""

# Python executable path
$pythonExe = "$workshopPath\workshop-env\Scripts\python.exe"
Write-Host "Python Executable:" -ForegroundColor Yellow
Write-Host "  $pythonExe" -ForegroundColor White
Write-Host ""

# Server script path
$serverScript = "$workshopPath\server_workshop.py"
Write-Host "Server Script:" -ForegroundColor Yellow
Write-Host "  $serverScript" -ForegroundColor White
Write-Host ""

# Convert paths to JSON format (forward slashes) for Claude Desktop
$pythonJson = $pythonExe -replace '\\', '/'
$serverJson = $serverScript -replace '\\', '/'
$workshopJson = $workshopPath -replace '\\', '/'

# Display Claude Desktop configuration
Write-Host "============================================================" -ForegroundColor Green
Write-Host " FOR CLAUDE DESKTOP (JSON format)" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host "Command:    $pythonJson" -ForegroundColor White
Write-Host "Args:       $serverJson" -ForegroundColor White
Write-Host "PYTHONPATH: $workshopJson" -ForegroundColor White
Write-Host ""

# Display MCP Inspector configuration
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host " FOR MCP INSPECTOR (Windows format)" -ForegroundColor Magenta
Write-Host "============================================================" -ForegroundColor Magenta
Write-Host "Transport Type: STDIO" -ForegroundColor White
Write-Host "Command:        $pythonExe" -ForegroundColor White
Write-Host "Arguments:      $serverScript" -ForegroundColor White
Write-Host "Env (optional): PYTHONPATH=$workshopPath" -ForegroundColor White
Write-Host ""