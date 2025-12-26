#!/usr/bin/env python3
import requests
import sys

def test_server(server_url="http://127.0.0.1:8000"):
    print(f"Testing server connection at {server_url}...")
    print("-" * 50)
    
    try:
        health_response = requests.get(f"{server_url}/health", timeout=5)
        if health_response.status_code == 200:
            print(f"✓ Health check passed: {health_response.json()}")
        else:
            print(f"✗ Health check failed: Status {health_response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"✗ Connection failed: Cannot connect to {server_url}")
        print("\nPossible issues:")
        print("  1. Server is not running")
        print("  2. Server is running on a different port")
        print("  3. Firewall is blocking the connection")
        print("  4. WSL networking issue (if using WSL)")
        return False
    except requests.exceptions.Timeout:
        print(f"✗ Connection timeout: Server did not respond in time")
        return False
    except Exception as error:
        print(f"✗ Error: {str(error)}")
        return False
    
    try:
        root_response = requests.get(f"{server_url}/", timeout=5)
        if root_response.status_code == 200:
            print(f"✓ Root endpoint working: {root_response.json()}")
        else:
            print(f"✗ Root endpoint failed: Status {root_response.status_code}")
            return False
    except Exception as error:
        print(f"✗ Root endpoint error: {str(error)}")
        return False
    
    print("-" * 50)
    print("✓ Server is running and accessible!")
    print(f"\nYou can access:")
    print(f"  - API Docs: {server_url}/docs")
    print(f"  - Health Check: {server_url}/health")
    print(f"  - Root: {server_url}/")
    return True

if __name__ == "__main__":
    test_url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"
    
    test_passed = test_server(test_url)
    sys.exit(0 if test_passed else 1)

