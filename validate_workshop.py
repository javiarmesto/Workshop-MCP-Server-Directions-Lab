#!/usr/bin/env python3
"""
🧪 MCP WORKSHOP VALIDATION SCRIPT
=========================================

This script verifies that the workshop is configured correctly
and that all necessary dependencies and files are present.

Usage:
    python validate_workshop.py
"""

import os
import sys
import importlib
import json
from pathlib import Path

def print_header(title: str):
    """Print section header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def check_python_version():
    """Verify Python version"""
    print_header("Python Verification")
    
    version = sys.version_info
    if version >= (3, 12):
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.12+")
        return False

def check_dependencies():
    """Verify required dependencies"""
    print_header("Dependencies Verification")
    
    required_packages = [
        'mcp',
        'fastmcp', 
        'httpx',
        'anyio',
        'pydantic',
        'python_dotenv',
        'authlib',
        'starlette',
        'click',
        'typer',
        'uvicorn'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            # Special handling for python-dotenv
            if package == 'python_dotenv':
                importlib.import_module('dotenv')
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - NOT INSTALLED")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing dependencies: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    else:
        print(f"\n✅ All dependencies are installed")
        return True

def check_files():
    """Verify required files"""
    print_header("Files Verification")
    
    required_files = [
        'server_workshop.py',
        'requirements.txt',
        'README.md',
        '.env.example',
        'src/client.py',
        'src/config.py',
        'src/azure_auth.py'
    ]
    
    required_dirs = [
        'src',
        'data'
    ]
    
    data_files = [
        'data/README.md',
        'data/prices.csv',
        'data/categories.csv',
        'data/substitutes.csv',
        'data/price-analysis.json'
    ]
    
    missing = []
    
    # Verify main files
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing.append(file)
    
    # Verify directories
    for dir in required_dirs:
        if os.path.isdir(dir):
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ - NOT FOUND")
            missing.append(dir)
    
    # Verify data files
    for file in data_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - NOT FOUND")
            missing.append(file)
    
    if missing:
        print(f"\n⚠️  Missing files: {', '.join(missing)}")
        return False
    else:
        print(f"\n✅ All files are present")
        return True

def check_configuration():
    """Verify configuration"""
    print_header("Configuration Verification")
    
    # Verify if .env exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Load environment variables if dotenv is available
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            required_vars = [
                'AZURE_CLIENT_ID',
                'AZURE_CLIENT_SECRET', 
                'AZURE_TENANT_ID',
                'BC_ENVIRONMENT',
                'BC_COMPANY_ID'
            ]
            
            configured_vars = []
            missing_vars = []
            
            for var in required_vars:
                if os.getenv(var):
                    print(f"✅ {var} configured")
                    configured_vars.append(var)
                else:
                    print(f"⚠️  {var} not configured")
                    missing_vars.append(var)
            
            if missing_vars:
                print(f"\n⚠️  Unconfigured variables: {', '.join(missing_vars)}")
                print("   Server will run with mock data if BC credentials are missing")
                return True  # Not critical for workshop
            else:
                print(f"\n✅ Complete configuration")
                return True
                
        except ImportError:
            print("⚠️  python-dotenv not available - cannot verify configuration")
            return True
    
    else:
        print("⚠️  .env file not found")
        print("   Copy .env.example to .env and configure the variables")
        if os.path.exists('.env.example'):
            print("✅ .env.example available as template")
        return True  # Not critical for basic testing

def test_data_files():
    """Test reading data files"""
    print_header("Data Verification")
    
    try:
        # Test CSV files
        import csv
        
        csv_files = ['data/prices.csv', 'data/categories.csv', 'data/substitutes.csv']
        
        for csv_file in csv_files:
            if os.path.exists(csv_file):
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    rows = list(reader)
                    print(f"✅ {csv_file} - {len(rows)} records")
            else:
                print(f"❌ {csv_file} - Not found")
        
        # Test JSON file  
        json_file = 'data/price-analysis.json'
        if os.path.exists(json_file):
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"✅ {json_file} - Valid")
        else:
            print(f"❌ {json_file} - Not found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error reading data files: {e}")
        return False

def test_server_import():
    """Test server import"""
    print_header("Server Verification")
    
    try:
        # Change to workshop directory if we're not there
        current_dir = os.getcwd()
        if not os.path.exists('server_workshop.py'):
            workshop_dir = os.path.join(current_dir, 'workshop')
            if os.path.exists(workshop_dir):
                os.chdir(workshop_dir)
        
        # Try to import server modules
        sys.path.insert(0, '.')
        
        import server_workshop
        print("✅ server_workshop.py - Import successful")
        
        # Verify that main functions exist (STDIO version)
        if hasattr(server_workshop, 'main'):
            print("✅ main() function available")
        
        if hasattr(server_workshop, 'mcp_server'):
            print("✅ MCP server (STDIO) instantiated")
        
        if hasattr(server_workshop, 'handle_list_tools'):
            print("✅ Tool handlers available")
        
        return True
        
    except Exception as e:
        print(f"❌ Error importing server: {e}")
        return False

def main():
    """Main validation function"""
    print("🚀 MCP WORKSHOP VALIDATOR - BUSINESS CENTRAL (STDIO)")
    print("=" * 60)
    
    # Change to workshop directory if we're in the parent directory
    if os.path.exists('workshop') and not os.path.exists('server_workshop.py'):
        print("📁 Changing to workshop directory...")
        os.chdir('workshop')
    
    results = []
    
    # Run all checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Files", check_files()))
    results.append(("Configuration", check_configuration()))
    results.append(("Data Files", test_data_files()))
    results.append(("Server Import", test_server_import()))
    
    # Show summary
    print_header("VALIDATION SUMMARY")
    
    total_checks = len(results)
    passed_checks = sum(1 for _, passed in results if passed)
    
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {check_name}")
    
    print(f"\n📊 RESULT: {passed_checks}/{total_checks} checks passed")
    
    if passed_checks == total_checks:
        print("\n🎉 WORKSHOP READY! You can run:")
        print("   python server_workshop.py")
        return True
    else:
        print(f"\n⚠️  {total_checks - passed_checks} checks failed.")
        print("   Review the errors above and fix before continuing.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)