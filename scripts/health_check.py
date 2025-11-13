#!/usr/bin/env python3
"""Health check script for the AI Math Tutor API."""

import sys
import requests
import time


def check_health(url: str = "http://localhost:8000/health", max_retries: int = 5):
    """Check if the API is healthy.
    
    Args:
        url: Health check endpoint URL
        max_retries: Maximum number of retry attempts
        
    Returns:
        True if healthy, False otherwise
    """
    print(f"🔍 Checking API health at {url}...")
    
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API is healthy!")
                print(f"   Status: {data.get('status')}")
                print(f"   Service: {data.get('service')}")
                return True
            else:
                print(f"⚠️  Attempt {attempt}/{max_retries}: Status code {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"⚠️  Attempt {attempt}/{max_retries}: Connection failed")
        except requests.exceptions.Timeout:
            print(f"⚠️  Attempt {attempt}/{max_retries}: Request timeout")
        except Exception as e:
            print(f"⚠️  Attempt {attempt}/{max_retries}: {e}")
        
        if attempt < max_retries:
            print("   Retrying in 2 seconds...")
            time.sleep(2)
    
    print("❌ API health check failed")
    return False


def check_openai_endpoint(url: str = "http://localhost:8000/api/v1/models"):
    """Check if the OpenAI-compatible endpoint is working.
    
    Args:
        url: Models endpoint URL
        
    Returns:
        True if working, False otherwise
    """
    print(f"\n🔍 Checking OpenAI-compatible endpoint at {url}...")
    
    try:
        response = requests.get(url, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            models = data.get('data', [])
            print("✅ OpenAI-compatible endpoint is working!")
            print(f"   Available models: {len(models)}")
            for model in models:
                print(f"     - {model.get('id')}")
            return True
        else:
            print(f"⚠️  Status code {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Run all health checks."""
    print("🏥 AI Math Tutor Health Check")
    print("=" * 50)
    
    # Check main health endpoint
    health_ok = check_health()
    
    # Check OpenAI-compatible endpoint
    openai_ok = check_openai_endpoint()
    
    print("\n" + "=" * 50)
    if health_ok and openai_ok:
        print("✅ All health checks passed!")
        sys.exit(0)
    else:
        print("❌ Some health checks failed")
        sys.exit(1)


if __name__ == "__main__":
    main()

