#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Example for Choice Toolkit
Copy this file to config.py and fill in your actual API keys
"""

import os

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.nuwaapi.com/v1")

# Example usage:
# export OPENAI_API_KEY="sk-your-actual-api-key-here"
# export OPENAI_BASE_URL="https://api.openai.com/v1"
