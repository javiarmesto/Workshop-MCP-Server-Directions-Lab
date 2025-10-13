#!/usr/bin/env python3
"""
Simple MCP Server Test Script
==============================

This script tests the MCP server by sending a tools/list request
and displaying the available tools.

Usage:
    python test_server.py
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def test_mcp_server():
    """Test the MCP server by listing available tools"""
    print("\n" + "="*60)
    print("MCP SERVER TEST - Tools List")
    print("="*60 + "\n")
    
    # Get Python executable from virtual environment
    if sys.platform == "win32":
        python_exe = Path("workshop-env") / "Scripts" / "python.exe"
    else:
        python_exe = Path("workshop-env") / "bin" / "python"
    
    if not python_exe.exists():
        print("[ERROR] Virtual environment not found")
        print("        Run setup.ps1 first to create it")
        return False
    
    # Prepare MCP messages
    init_message = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {
                "name": "test-client",
                "version": "1.0.0"
            }
        }
    }
    
    initialized_notification = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized"
    }
    
    list_tools_message = {
        "jsonrpc": "2.0",
        "id": 2,
        "method": "tools/list",
        "params": {}
    }
    
    print("[INFO] Starting MCP server...")
    print("[INFO] Sending initialize, initialized, and tools/list requests...\n")
    
    try:
        # Start server process with UTF-8 encoding
        process = subprocess.Popen(
            [str(python_exe), "server_workshop.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='ignore',
            bufsize=1
        )
        
        # Send all messages (initialize -> initialized -> tools/list)
        input_data = (
            json.dumps(init_message) + "\n" + 
            json.dumps(initialized_notification) + "\n" +
            json.dumps(list_tools_message) + "\n"
        )
        
        # Wait for responses with timeout
        try:
            stdout, stderr = process.communicate(input=input_data, timeout=5)
        except Exception as e:
            print(f"[ERROR] Communication error: {e}")
            process.kill()
            return False
        
        if stdout is None:
            print("[ERROR] No output received from server")
            return False
        
        # Parse responses
        print("[SUCCESS] Server responded!\n")
        print("="*60)
        print("AVAILABLE TOOLS:")
        print("="*60 + "\n")
        
        found_tools = False
        for line in stdout.strip().split('\n'):
            if not line.strip():
                continue
            try:
                response = json.loads(line)
                if 'result' in response and 'tools' in response.get('result', {}):
                    tools = response['result']['tools']
                    found_tools = True
                    
                    for i, tool in enumerate(tools, 1):
                        print(f"{i}. {tool['name']}")
                        print(f"   Description: {tool.get('description', 'N/A')}")
                        print()
                    
                    print(f"[INFO] Total tools available: {len(tools)}")
                    break
            except json.JSONDecodeError:
                continue
        
        if not found_tools:
            print("[WARN] Could not parse tools from server response")
            print("\n[DEBUG] Raw stdout:")
            print(stdout[:500])
            if stderr:
                print("\n[DEBUG] stderr:")
                print(stderr[:500])
        
        print("\n" + "="*60)
        print("[SUCCESS] Test completed successfully!")
        print("="*60 + "\n")
        
        return found_tools
        
    except subprocess.TimeoutExpired:
        print("[ERROR] Server did not respond within timeout")
        process.kill()
        return False
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False
    finally:
        try:
            process.kill()
        except:
            pass

if __name__ == "__main__":
    print("\nMCP Workshop Server - Quick Test")
    print("=================================\n")
    
    # Check if we're in the right directory
    if not os.path.exists("server_workshop.py"):
        print("[ERROR] server_workshop.py not found")
        print("        Please run this script from the workshop directory")
        sys.exit(1)
    
    success = test_mcp_server()
    
    if success:
        print("\n[NEXT STEPS]")
        print("  1. Configure Claude Desktop with this MCP server")
        print("  2. Start working on the workshop exercises")
        print("  3. Check WORKSHOP_GUIDE_EN.md for instructions\n")
        sys.exit(0)
    else:
        print("\n[TROUBLESHOOTING]")
        print("  - Verify virtual environment is activated")
        print("  - Run: python validate_workshop.py")
        print("  - Check server_workshop.py for errors\n")
        sys.exit(1)
