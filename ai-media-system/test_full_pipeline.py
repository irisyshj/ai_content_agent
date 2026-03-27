#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Full Pipeline Test"""
import requests
import json
import subprocess
import time
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("Starting API server for full test...")
server_proc = subprocess.Popen(
    [sys.executable, "api_server.py", "--host", "127.0.0.1", "--port", "5004"],
    cwd="C:\\Users\\irisf\\Documents\\Obsidian Vault\\10_geekbang\\pre_claw\\ai-media-system",
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

time.sleep(3)

try:
    data = {
        "content": """Artificial Intelligence is transforming how we work and live. Machine learning models can now understand and generate human-like text, images, and even code.

## Key Concepts

### Neural Networks
Neural networks are computing systems inspired by the human brain. They learn patterns from vast amounts of data.

### Large Language Models
LLMs like GPT and Claude can engage in human-like conversation and perform complex reasoning tasks.

> The future is already here.

## Applications

* Content creation
* Code generation
* Data analysis

This technology will continue to evolve rapidly.""",
        "title": "AI Technology: A Comprehensive Guide",
        "theme": "green"
    }

    resp = requests.post(
        "http://127.0.0.1:5004/api/v1/pipeline/run",
        json=data,
        timeout=60
    )

    result = resp.json()
    print("Status:", resp.status_code)
    print("Success:", result.get('success'))

    if result.get('success'):
        article = result.get('article', {})
        print("Title:", article.get('title'))
        print("Word count:", article.get('word_count'))
        print("Has HTML:", bool(result.get('html')))

        # Save HTML
        html = result.get('html', '')
        with open('full_output.html', 'w', encoding='utf-8') as f:
            f.write(html)
        print("HTML saved to: full_output.html")
    else:
        print("Error:", result.get('error'))

except Exception as e:
    print(f"Error: {e}")

finally:
    server_proc.terminate()
    server_proc.wait(timeout=5)
