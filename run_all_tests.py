#!/usr/bin/env python3
"""
Test runner for all data quality validations
"""

import subprocess
import sys

def run_script(script_name):
    """Run a Python script and return success status"""
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True)
        print(f"\n{'='*50}")
        print(f"🚀 RUNNING: {script_name}")
        print(f"{'='*50}")
        print(result.stdout)
        if result.stderr:
            print(f"❌ ERRORS in {script_name}:")
            print(result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Failed to run {script_name}: {e}")
        return False

def main():
    """Run all test scripts"""
    scripts = [
        "great_expectations_validator.py",
        "pydantic_validator.py", 
        "config_schema.py"
    ]
    
    print("🧪 RUNNING ALL DATA QUALITY TESTS")
    print("=" * 50)
    
    results = {}
    for script in scripts:
        results[script] = run_script(script)
    
    print(f"\n{'='*50}")
    print("📊 TEST SUMMARY")
    print(f"{'='*50}")
    
    for script, success in results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{script}: {status}")
    
    all_passed = all(results.values())
    if all_passed:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n💡 Some tests failed. Check the output above.")
        sys.exit(1)

if __name__ == "__main__":
    main()