#!/usr/bin/env python3
"""
Test Environment for Binance Trading Bot
Testing without API key first
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing module imports...")
    
    modules_to_test = [
        "requests",
        "binance",
        "ccxt", 
        "pandas",
        "numpy",
        "websocket",
        "dotenv",
        "psutil",
        "ntplib"
    ]
    
    failed_imports = []
    
    for module in modules_to_test:
        try:
            if module == "binance":
                import binance
            elif module == "websocket":
                import websocket
            else:
                __import__(module)
            print(f"   ✅ {module}")
        except ImportError as e:
            print(f"   ❌ {module}: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def test_binance_connection():
    """Test basic Binance API connection without API key"""
    print("\n🔍 Testing Binance API connection...")
    
    try:
        import requests
        
        # Test public endpoints (no API key needed)
        test_urls = [
            "https://api.binance.com/api/v3/ping",
            "https://api.binance.com/api/v3/time",
            "https://api.binance.com/api/v3/exchangeInfo"
        ]
        
        for url in test_urls:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {url.split('/')[-1]}")
                else:
                    print(f"   ⚠️  {url.split('/')[-1]} - Status: {response.status_code}")
            except Exception as e:
                print(f"   ❌ {url.split('/')[-1]} - Error: {e}")
                
    except ImportError:
        print("   ❌ requests module not available")

def test_ccxt_connection():
    """Test CCXT library connection"""
    print("\n🔍 Testing CCXT library...")
    
    try:
        import ccxt
        
        # Test with Binance
        exchange = ccxt.binance({
            'sandbox': True,  # Use testnet
            'enableRateLimit': True,
        })
        
        try:
            # Test public API
            ticker = exchange.fetch_ticker('BTC/USDT')
            print(f"   ✅ CCXT Binance connection - BTC/USDT: ${ticker['last']:.2f}")
        except Exception as e:
            print(f"   ⚠️  CCXT Binance connection - Error: {e}")
            
    except ImportError:
        print("   ❌ ccxt module not available")

def test_websocket():
    """Test WebSocket functionality"""
    print("\n🔍 Testing WebSocket...")
    
    try:
        import websocket
        
        # Test WebSocket connection to Binance
        def on_message(ws, message):
            print("   ✅ WebSocket message received")
            ws.close()
            
        def on_error(ws, error):
            print(f"   ❌ WebSocket error: {error}")
            
        def on_close(ws, close_status_code, close_msg):
            print("   ✅ WebSocket connection closed")
            
        def on_open(ws):
            print("   ✅ WebSocket connection opened")
            # Close immediately for test
            ws.close()
        
        # Test WebSocket connection
        ws = websocket.WebSocketApp(
            "wss://stream.binance.com:9443/ws/btcusdt@ticker",
            on_open=on_open,
            on_message=on_message,
            on_error=on_error,
            on_close=on_close
        )
        
        # Run for a short time
        import threading
        wst = threading.Thread(target=ws.run_forever)
        wst.daemon = True
        wst.start()
        
        # Wait a bit then close
        import time
        time.sleep(3)
        ws.close()
        
    except ImportError:
        print("   ❌ websocket module not available")

def test_system_resources():
    """Test system resources"""
    print("\n🔍 Testing system resources...")
    
    try:
        import psutil
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        print(f"   CPU Usage: {cpu_percent}%")
        
        # Memory
        memory = psutil.virtual_memory()
        print(f"   Memory Usage: {memory.percent}%")
        print(f"   Available Memory: {memory.available / (1024**3):.2f} GB")
        
        # Disk
        disk = psutil.disk_usage('/')
        print(f"   Disk Usage: {disk.percent}%")
        print(f"   Free Disk: {disk.free / (1024**3):.2f} GB")
        
        return True
    except ImportError:
        print("   ❌ psutil module not available")
        return False

def test_time_sync():
    """Test time synchronization"""
    print("\n🔍 Testing time synchronization...")
    
    try:
        import ntplib
        import time
        
        client = ntplib.NTPClient()
        response = client.request('pool.ntp.org')
        offset = abs(response.offset)
        
        if offset < 1:
            print(f"   ✅ Time sync OK - Offset: {offset:.3f}s")
        else:
            print(f"   ⚠️  Time offset: {offset:.3f}s")
            
        return True
    except ImportError:
        print("   ❌ ntplib module not available")
        return False

def create_sample_config():
    """Create sample configuration file"""
    print("\n📝 Creating sample configuration...")
    
    sample_config = """# Binance Trading Bot Configuration
# Copy this to .env file and fill in your API keys

# Binance API Configuration
BINANCE_API_KEY=your_api_key_here
BINANCE_SECRET_KEY=your_secret_key_here

# Testnet Configuration (set to true for testing)
BINANCE_TESTNET=true

# Trading Configuration
TRADING_PAIR=BTCUSDT
POSITION_SIZE=0.001
LEVERAGE=10

# Risk Management
STOP_LOSS_PERCENT=2.0
TAKE_PROFIT_PERCENT=4.0
MAX_POSITION_SIZE=0.01

# Technical Analysis
RSI_PERIOD=14
RSI_OVERBOUGHT=70
RSI_OVERSOLD=30

# Logging
LOG_LEVEL=INFO
LOG_FILE=trading_bot.log
"""
    
    with open("sample_config.env", "w") as f:
        f.write(sample_config)
    
    print("   ✅ sample_config.env created")
    print("   📋 Edit this file with your API keys")

def main():
    """Main test function"""
    print("🚀 Environment Test for Binance Trading Bot")
    print("=" * 50)
    print(f"Test time: {datetime.now()}")
    
    # Run all tests
    imports_ok = test_imports()
    test_binance_connection()
    test_ccxt_connection()
    test_websocket()
    resources_ok = test_system_resources()
    time_ok = test_time_sync()
    
    # Create sample config
    create_sample_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    if imports_ok and resources_ok and time_ok:
        print("✅ Environment is READY for bot deployment")
        print("\n🎯 Next steps:")
        print("   1. Get API keys from Binance Testnet")
        print("   2. Edit sample_config.env with your API keys")
        print("   3. Rename sample_config.env to .env")
        print("   4. Test with small amounts first")
        print("   5. Monitor bot performance")
    else:
        print("❌ Environment needs additional setup")
        if not imports_ok:
            print("   - Some Python modules are missing")
        if not resources_ok:
            print("   - System resource monitoring unavailable")
        if not time_ok:
            print("   - Time synchronization issues")
    
    print("\n💡 Tips:")
    print("   - Always test with testnet first")
    print("   - Start with small position sizes")
    print("   - Monitor bot logs regularly")
    print("   - Set up proper risk management")

if __name__ == "__main__":
    main()