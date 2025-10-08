#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Choice Toolkit - Test Script
Test API connection
"""
import openai
import os

def test_api_connection():
    """Test API connection"""
    print("Choice Toolkit API Connection Test")
    print("=" * 50)

    api_key = os.getenv("API_KEY", "YOUR_API_KEY_HERE")
    base_url = os.getenv("BASE_URL", "https://api.openai.com/v1")
    client = openai.OpenAI(api_key=api_key, base_url=base_url)
    print("API Key:" + api_key[:5] + "..." + api_key[-5:])
    print("Base URL:" + base_url)
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": "This is a test message."}],
            max_tokens=50,
            temperature=0.0
        )
        print(f"✅ API connection successful\nmodel response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False
    return True

if __name__ == "__main__":
    test_api_connection()