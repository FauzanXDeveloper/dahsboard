#!/usr/bin/env python3
"""
Test script to verify the AI Data Analyst Dashboard installation
Run this script to check if all dependencies are properly installed
"""

import sys
import subprocess
import importlib

def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.8+")
        return False

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name} - Installed")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_all_dependencies():
    """Check all required dependencies"""
    print("\nChecking required packages...")
    
    packages = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('plotly', 'plotly'),
        ('openai', 'openai'),
        ('sqlalchemy', 'sqlalchemy'),
        ('openpyxl', 'openpyxl'),
        ('python-dotenv', 'dotenv'),
        ('psycopg2-binary', 'psycopg2'),
        ('pymysql', 'pymysql')
    ]
    
    all_installed = True
    for package_name, import_name in packages:
        if not check_package(package_name, import_name):
            all_installed = False
    
    return all_installed

def check_env_file():
    """Check if .env file exists"""
    import os
    print("\nChecking configuration...")
    
    if os.path.exists('.env'):
        print("✅ .env file exists")
        
        # Check if OpenAI API key is set
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key and api_key != 'your_openai_api_key_here':
            print("✅ OpenAI API key is configured")
        else:
            print("⚠️  OpenAI API key not configured (AI features will be limited)")
        
        return True
    else:
        print("❌ .env file not found")
        print("   Run: copy .env.example .env")
        return False

def test_streamlit():
    """Test if Streamlit can be launched"""
    print("\nTesting Streamlit...")
    try:
        result = subprocess.run([sys.executable, '-m', 'streamlit', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Streamlit {version} - Ready to launch")
            return True
        else:
            print("❌ Streamlit test failed")
            return False
    except Exception as e:
        print(f"❌ Streamlit test error: {e}")
        return False

def generate_sample_data():
    """Generate sample data files for testing"""
    print("\nGenerating sample data...")
    try:
        import pandas as pd
        import numpy as np
        from datetime import datetime
        
        # Simple sample data
        np.random.seed(42)
        data = {
            'Date': pd.date_range('2024-01-01', periods=100),
            'Product': np.random.choice(['A', 'B', 'C'], 100),
            'Sales': np.random.randint(100, 1000, 100),
            'Region': np.random.choice(['North', 'South'], 100)
        }
        
        df = pd.DataFrame(data)
        df.to_csv('test_data.csv', index=False)
        print("✅ Sample data created: test_data.csv")
        return True
    except Exception as e:
        print(f"❌ Sample data generation failed: {e}")
        return False

def main():
    """Main test function"""
    print("🔍 AI Data Analyst Dashboard - Installation Test")
    print("=" * 50)
    
    # Check Python version
    python_ok = check_python_version()
    
    # Check dependencies
    deps_ok = check_all_dependencies()
    
    # Check configuration
    config_ok = check_env_file()
    
    # Test Streamlit
    streamlit_ok = test_streamlit()
    
    # Generate sample data
    sample_ok = generate_sample_data()
    
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print(f"Python Version: {'✅' if python_ok else '❌'}")
    print(f"Dependencies: {'✅' if deps_ok else '❌'}")
    print(f"Configuration: {'✅' if config_ok else '❌'}")
    print(f"Streamlit: {'✅' if streamlit_ok else '❌'}")
    print(f"Sample Data: {'✅' if sample_ok else '❌'}")
    
    if all([python_ok, deps_ok, streamlit_ok]):
        print("\n🎉 Installation test PASSED!")
        print("You can now run: streamlit run app.py")
        
        if not config_ok:
            print("\n⚠️  Don't forget to configure your .env file for AI features")
    else:
        print("\n❌ Installation test FAILED!")
        print("Please fix the issues above before running the application")
        
        if not deps_ok:
            print("\nTo install missing packages:")
            print("pip install -r requirements.txt")
    
    return all([python_ok, deps_ok, streamlit_ok])

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
