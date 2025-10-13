# Workshop MCP Server - Automated Setup Script
# =================================================
# This script automates the complete setup process for the Workshop MCP Server
# Run this script from the workshop directory in PowerShell

param(
    [switch]$Force,  # Force recreation of virtual environment
    [switch]$Help    # Show help information
)

# Color functions for better output (with global scope)
function global:Write-Success { param($Message) Write-Host "[OK] $Message" -ForegroundColor Green }
function global:Write-Info { param($Message) Write-Host "[INFO] $Message" -ForegroundColor Cyan }
function global:Write-Warning { param($Message) Write-Host "[WARN] $Message" -ForegroundColor Yellow }
function global:Write-Error { param($Message) Write-Host "[ERROR] $Message" -ForegroundColor Red }
function global:Write-Step { param($Message) Write-Host "[STEP] $Message" -ForegroundColor Blue }

# Show help
if ($Help) {
    Write-Host @"
========================================
Workshop MCP Server - Setup Script
========================================

USAGE:
    .\setup.ps1                    # Normal setup
    .\setup.ps1 -Force             # Force recreate virtual environment
    .\setup.ps1 -Help              # Show this help

WHAT THIS SCRIPT DOES:
    1. Checks Python version (requires 3.12+)
    2. Creates/activates virtual environment
    3. Installs all required dependencies
    4. Verifies installation
    5. Shows next steps

REQUIREMENTS:
    - Python 3.12 or higher
    - PowerShell execution policy allowing scripts
    - Internet connection for package downloads

TROUBLESHOOTING:
    If you get execution policy errors, run:
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

"@
    exit 0
}

Write-Host @"
========================================
Workshop MCP Server - Automated Setup
========================================
Starting automated setup process...

"@ -ForegroundColor Magenta

# Step 1: Check execution policy
Write-Step "Checking PowerShell execution policy..."
$policy = Get-ExecutionPolicy -Scope CurrentUser
if ($policy -eq "Restricted") {
    Write-Warning "PowerShell execution policy is restricted."
    Write-Info "Attempting to set RemoteSigned policy for current user..."
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Success "Execution policy updated to RemoteSigned"
    }
    catch {
        Write-Error "Failed to update execution policy. Please run manually:"
        Write-Host "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser" -ForegroundColor Yellow
        exit 1
    }
}
else {
    Write-Success "Execution policy is acceptable: $policy"
}

# Function to find Python installation
function Find-Python {
    # Try common Python locations
    $pythonPaths = @(
        "python",  # Try PATH first
        "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python313\python.exe",
        "$env:LOCALAPPDATA\Programs\Python\Python312\python.exe",
        "C:\Python314\python.exe",
        "C:\Python313\python.exe",
        "C:\Python312\python.exe",
        "C:\Program Files\Python314\python.exe",
        "C:\Program Files\Python313\python.exe",
        "C:\Program Files\Python312\python.exe"
    )
    
    foreach ($path in $pythonPaths) {
        try {
            if ($path -eq "python") {
                $version = python --version 2>&1
                if ($LASTEXITCODE -eq 0) {
                    return "python"
                }
            }
            elseif (Test-Path $path) {
                $version = & $path --version 2>&1
                if ($LASTEXITCODE -eq 0) {
                    return $path
                }
            }
        }
        catch {
            continue
        }
    }
    return $null
}

# Step 2: Check Python version
Write-Step "Checking Python version..."
try {
    $pythonCmd = Find-Python
    if ($null -eq $pythonCmd) {
        Write-Error "Python is not installed or not found"
        Write-Info "Please install Python 3.12+ from https://python.org"
        Write-Info "Searched in common locations:"
        Write-Host "  - System PATH" -ForegroundColor Yellow
        Write-Host "  - $env:LOCALAPPDATA\Programs\Python\" -ForegroundColor Yellow
        Write-Host "  - C:\PythonXXX\" -ForegroundColor Yellow
        Write-Host "  - C:\Program Files\PythonXXX\" -ForegroundColor Yellow
        exit 1
    }
    
    # Get version from found Python
    if ($pythonCmd -eq "python") {
        $pythonVersion = python --version 2>&1
    } else {
        $pythonVersion = & $pythonCmd --version 2>&1
    }
    
    # Extract version number
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)\.(\d+)"
    if ($versionMatch) {
        $major = [int]$Matches[1]
        $minor = [int]$Matches[2]
        
        if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
            Write-Warning "Python version $pythonVersion detected. Python 3.12+ recommended."
            Write-Info "Found Python at: $pythonCmd"
            Write-Info "The workshop may work but some features might not be available."
        } else {
            Write-Success "Python version OK: $pythonVersion"
            Write-Info "Found at: $pythonCmd"
        }
    }
    else {
        Write-Warning "Could not parse Python version, but continuing..."
        Write-Info "Found Python at: $pythonCmd"
    }
}
catch {
    Write-Error "Error checking Python version: $_"
    exit 1
}

# Step 3: Check if we're in the right directory
Write-Step "Verifying workshop directory..."
if (!(Test-Path "requirements.txt")) {
    Write-Error "requirements.txt not found. Please run this script from the workshop directory."
    Write-Info "Expected structure:"
    Write-Host "  Workshop-MCP-Server-Directions-Lab/" -ForegroundColor Yellow
    Write-Host "  ├── requirements.txt" -ForegroundColor Yellow
    Write-Host "  ├── server_workshop.py" -ForegroundColor Yellow
    Write-Host "  └── setup.ps1 (this script)" -ForegroundColor Yellow
    exit 1
}

if (!(Test-Path "server_workshop.py")) {
    Write-Error "server_workshop.py not found. Please run this script from the workshop directory."
    exit 1
}

Write-Success "Workshop directory structure verified"

# Step 4: Handle virtual environment
Write-Step "Managing virtual environment..."

$venvExists = Test-Path "workshop-env"
$shouldCreateVenv = $Force -or !$venvExists

if ($Force -and $venvExists) {
    Write-Info "Force flag detected. Removing existing virtual environment..."
    Remove-Item -Recurse -Force "workshop-env" -ErrorAction SilentlyContinue
    Write-Success "Existing virtual environment removed"
    $shouldCreateVenv = $true
}

if ($shouldCreateVenv) {
    Write-Step "Creating virtual environment..."
    if ($pythonCmd -eq "python") {
        $result = python -m venv workshop-env 2>&1
    } else {
        $result = & $pythonCmd -m venv workshop-env 2>&1
    }
    
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment"
        Write-Info "Error output: $result"
        Write-Info "Possible solutions:"
        Write-Host "  1. Install Python for current user (not system-wide)" -ForegroundColor Yellow
        Write-Host "  2. Check if Python installation is complete" -ForegroundColor Yellow
        Write-Host "  3. Try running as administrator" -ForegroundColor Yellow
        exit 1
    }
    Write-Success "Virtual environment created successfully"
}
else {
    Write-Info "Virtual environment already exists (use -Force to recreate)"
}

# Step 5: Activate virtual environment
Write-Step "Activating virtual environment..."
$activateScript = ".\workshop-env\Scripts\Activate.ps1"

if (!(Test-Path $activateScript)) {
    Write-Error "Virtual environment activation script not found at: $activateScript"
    Write-Info "Try running with -Force to recreate the virtual environment"
    exit 1
}

# Check if we're already in a virtual environment
if ($env:VIRTUAL_ENV) {
    Write-Info "Already in a virtual environment: $env:VIRTUAL_ENV"
    Write-Info "Deactivating current environment first..."
    if (Get-Command deactivate -ErrorAction SilentlyContinue) {
        deactivate
    }
}

Write-Info "Activating workshop virtual environment..."
& $activateScript

# Verify activation by checking the environment variable
if (!$env:VIRTUAL_ENV -or !(Test-Path $env:VIRTUAL_ENV)) {
    Write-Error "Virtual environment activation failed"
    Write-Info "Please try activating manually: .\workshop-env\Scripts\Activate.ps1"
    exit 1
}

Write-Success "Virtual environment activated: $env:VIRTUAL_ENV"

# Step 6: Upgrade pip
Write-Step "Upgrading pip..."
python -m pip install --upgrade pip --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Success "pip upgraded successfully"
}
else {
    Write-Warning "pip upgrade had issues, but continuing..."
}

# Step 7: Install dependencies
Write-Step "Installing workshop dependencies..."
Write-Info "This may take a few minutes depending on your internet connection..."

$installResult = python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install dependencies"
    Write-Info "Common solutions:"
    Write-Host "  1. Check internet connection" -ForegroundColor Yellow
    Write-Host "  2. Try running: python -m pip install --upgrade pip" -ForegroundColor Yellow
    Write-Host "  3. Check if corporate firewall is blocking downloads" -ForegroundColor Yellow
    Write-Host "  4. Try installing with: python -m pip install -r requirements.txt --user" -ForegroundColor Yellow
    exit 1
}

Write-Success "All dependencies installed successfully"

# Step 8: Run comprehensive verification
Write-Step "Running comprehensive verification..."
Write-Info "Using the official workshop validator..."

$validationResult = python validate_workshop.py
if ($LASTEXITCODE -eq 0) {
    Write-Success "Comprehensive validation passed!"
}
else {
    Write-Warning "Some validation checks failed, but setup is complete"
    Write-Info "Review the validation output above for details"
}

# Step 9: Check for optional .env configuration
Write-Step "Checking optional configuration..."
if (!(Test-Path ".env")) {
    if (Test-Path ".env.example") {
        Write-Info "Found .env.example file"
        Write-Warning "No .env file found - server will run with mock data"
        Write-Info "To connect to real Business Central:"
        Write-Host "  1. Copy .env.example to .env" -ForegroundColor Yellow
        Write-Host "  2. Edit .env with your Azure AD credentials" -ForegroundColor Yellow
        Write-Host "  3. Restart the server" -ForegroundColor Yellow
    }
}
else {
    Write-Success ".env file found - server configured for Business Central"
}

# Final success message
Write-Host @"

========================================
SETUP COMPLETED SUCCESSFULLY!
========================================

Your Workshop MCP Server is ready to use!

WHAT'S INSTALLED:
[OK] Python virtual environment (workshop-env)
[OK] All MCP Server dependencies
[OK] FastMCP framework
[OK] Business Central integration components

NEXT STEPS:
1. Read the workshop guide: WORKSHOP_GUIDE_EN.md
2. Test the server: python server_workshop.py --help
3. Configure Claude Desktop with your MCP server
4. Complete the workshop exercises

IMPORTANT REMINDERS:
[!] Always activate the virtual environment before working:
    .\workshop-env\Scripts\Activate.ps1

[!] Your prompt should show (workshop-env) when active

DOCUMENTATION:
   - Workshop Guide: WORKSHOP_GUIDE_EN.md
   - Troubleshooting: SETUP_TROUBLESHOOTING.md
   - README: README.md

NEED HELP?
   Check SETUP_TROUBLESHOOTING.md for common issues

Happy coding!

"@ -ForegroundColor Green

# Show current status
Write-Info "Current status:"
Write-Host "  Working Directory: $(Get-Location)" -ForegroundColor Cyan
Write-Host "  Python Command: $pythonCmd" -ForegroundColor Cyan
Write-Host "  Virtual Environment: $env:VIRTUAL_ENV" -ForegroundColor Cyan
Write-Host "  Status: ACTIVE" -ForegroundColor Green

exit 0