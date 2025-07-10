#!/usr/bin/env python3
"""
VPS Environment Check for Binance Trading Bot
This script checks if the VPS environment is ready for running the trading bot.
"""

import sys
import subprocess
import importlib.util
import os
from datetime import datetime

def check_python_version():
    """Check Python version"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    print(f"   Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 7:
        print("   ✅ Python version is suitable")
        return True
    else:
        print("   ❌ Python version is too old. Need Python 3.7+")
        return False

def check_pip():
    """Check if pip is available"""
    print("\n🔍 Checking pip availability...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ pip is available")
            return True
        else:
            print("   ❌ pip is not available")
            return False
    except Exception as e:
        print(f"   ❌ Error checking pip: {e}")
        return False

def check_required_packages():
    """Check if required packages are installed"""
    print("\n🔍 Checking required packages...")
    
    required_packages = [
        "requests",
        "python-binance",
        "ccxt",
        "pandas",
        "numpy",
        "websocket-client",
        "python-dotenv"
    ]
    
    missing_packages = []
    installed_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
            print(f"   ✅ {package} is installed")
            installed_packages.append(package)
        except ImportError:
            print(f"   ❌ {package} is missing")
            missing_packages.append(package)
    
    return installed_packages, missing_packages

def check_network_connectivity():
    """Check network connectivity to Binance"""
    print("\n🔍 Checking network connectivity...")
    
    test_urls = [
        "https://api.binance.com",
        "https://fapi.binance.com",
        "https://testnet.binancefuture.com"
    ]
    
    import requests
    
    for url in test_urls:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"   ✅ {url} is accessible")
            else:
                print(f"   ⚠️  {url} returned status {response.status_code}")
        except Exception as e:
            print(f"   ❌ {url} is not accessible: {e}")

def check_system_resources():
    """Check system resources"""
    print("\n🔍 Checking system resources...")
    
    try:
        import psutil
        
        # CPU info
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"   CPU cores: {cpu_count}")
        print(f"   CPU usage: {cpu_percent}%")
        
        # Memory info
        memory = psutil.virtual_memory()
        print(f"   Total RAM: {memory.total / (1024**3):.2f} GB")
        print(f"   Available RAM: {memory.available / (1024**3):.2f} GB")
        print(f"   Memory usage: {memory.percent}%")
        
        # Disk info
        disk = psutil.disk_usage('/')
        print(f"   Total disk: {disk.total / (1024**3):.2f} GB")
        print(f"   Free disk: {disk.free / (1024**3):.2f} GB")
        print(f"   Disk usage: {disk.percent}%")
        
        return True
    except ImportError:
        print("   ⚠️  psutil not installed, skipping system resource check")
        return False

def check_time_sync():
    """Check if system time is synchronized"""
    print("\n🔍 Checking system time...")
    
    try:
        import ntplib
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        offset = abs(response.offset)
        
        if offset < 1:  # Less than 1 second offset
            print("   ✅ System time is synchronized")
            return True
        else:
            print(f"   ⚠️  System time offset: {offset:.2f} seconds")
            return False
    except ImportError:
        print("   ⚠️  ntplib not installed, skipping time sync check")
        return False
    except Exception as e:
        print(f"   ❌ Error checking time sync: {e}")
        return False

def generate_requirements():
    """Generate requirements.txt for missing packages"""
    print("\n📝 Generating requirements.txt...")
    
    requirements = [
        "requests>=2.25.1",
        "python-binance>=1.0.15",
        "ccxt>=1.60.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0",
        "websocket-client>=1.2.0",
        "python-dotenv>=0.19.0",
        "psutil>=5.8.0",
        "ntplib>=0.4.0"
    ]
    
    with open("requirements.txt", "w") as f:
        for req in requirements:
            f.write(req + "\n")
    
    print("   ✅ requirements.txt generated")

def main():
    """Main function to run all checks"""
    print("🚀 VPS Environment Check for Binance Trading Bot")
    print("=" * 50)
    print(f"Check time: {datetime.now()}")
    
    # Run all checks
    python_ok = check_python_version()
    pip_ok = check_pip()
    installed, missing = check_required_packages()
    check_network_connectivity()
    check_system_resources()
    check_time_sync()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    
    if python_ok and pip_ok:
        print("✅ Basic Python environment is ready")
    else:
        print("❌ Python environment needs setup")
    
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        generate_requirements()
    else:
        print("✅ All required packages are installed")
    
    print("\n🎯 VPS READINESS ASSESSMENT:")
    if python_ok and pip_ok and not missing:
        print("✅ VPS is READY for trading bot deployment")
        print("   Next steps:")
        print("   1. Set up environment variables (.env file)")
        print("   2. Configure API keys")
        print("   3. Test with small amounts first")
    else:
        print("❌ VPS needs additional setup")
        print("   Please address the issues above before deployment")

if __name__ == "__main__":
    main()