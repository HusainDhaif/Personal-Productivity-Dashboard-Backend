#!/usr/bin/env python3
import sys
import os

def check_dependencies():
    print("Checking dependencies...")
    required_packages = [
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'pydantic',
        'python-dotenv'
    ]
    
    missing_packages = []
    for package_name in required_packages:
        try:
            import_name = package_name.replace('-', '_')
            __import__(import_name)
            print(f"  ✓ {package_name}")
        except ImportError:
            print(f"  ✗ {package_name} - MISSING")
            missing_packages.append(package_name)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip3 install " + " ".join(missing_packages))
        return False
    return True

def check_env_file():
    print("\nChecking environment configuration...")
    
    if not os.path.exists('.env'):
        print("  ⚠️  .env file not found")
        print("     The server will use default SQLite database")
        print("     Create .env file for custom database configuration")
        return True
    
    print("  ✓ .env file exists")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        database_url = os.getenv('DATABASE_URL')
        jwt_secret_key = os.getenv('JWT_SECRET')
        
        if database_url:
            print(f"  ✓ DATABASE_URL is set")
        else:
            print("  ⚠️  DATABASE_URL not set (will use SQLite fallback)")
        
        if jwt_secret_key:
            print(f"  ✓ JWT_SECRET is set")
        else:
            print("  ⚠️  JWT_SECRET not set (required for authentication)")
            return False
    except Exception as error:
        print(f"  ⚠️  Error reading .env: {str(error)}")
    
    return True

def check_imports():
    print("\nChecking application imports...")
    try:
        import main
        print("  ✓ main.py imports successfully")
        
        if hasattr(main, 'app'):
            print("  ✓ FastAPI app created")
        else:
            print("  ✗ FastAPI app not found in main.py")
            return False
        
        return True
    except Exception as error:
        print(f"  ✗ Import error: {str(error)}")
        import traceback
        traceback.print_exc()
        return False

def check_database_connection():
    print("\nChecking database connection...")
    try:
        from database import engine
        with engine.connect() as connection:
            print("  ✓ Database connection successful")
        return True
    except Exception as error:
        print(f"  ⚠️  Database connection issue: {str(error)}")
        print("     Server may still start, but database operations may fail")
        return True

def main():
    print("=" * 50)
    print("Server Startup Check")
    print("=" * 50)
    
    all_checks_passed = True
    
    if not check_dependencies():
        all_checks_passed = False
    
    if not check_env_file():
        all_checks_passed = False
    
    if not check_imports():
        all_checks_passed = False
    
    check_database_connection()
    
    print("\n" + "=" * 50)
    if all_checks_passed:
        print("✓ All checks passed! Server should start successfully.")
        print("\nStart the server with:")
        print("  python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
        print("  or")
        print("  ./start_server.sh")
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

