#!/usr/bin/env python3
import os
import requests
import sys
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")

# Write to a file instead of stdout to avoid terminal issues
output_file = "openai_test_result.txt"

with open(output_file, "w") as f:
    f.write("=== OPENAI API KEY TEST ===\n")
    f.write(f"API Key length: {len(api_key)} characters\n")
    f.write(f"API Key: {api_key[:20]}...{api_key[-4:]}\n")
    f.write(f"Model: {model}\n")
    f.write("\n")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "Say 'test successful' if you can read this."}],
        "max_tokens": 20
    }

    try:
        f.write("Testing OpenAI API...\n")
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        f.write(f"Status Code: {resp.status_code}\n")
        f.write("\n")

        if resp.status_code == 200:
            f.write("✅ OpenAI API key works!\n")
            result = resp.json()
            f.write(f"Response: {result['choices'][0]['message']['content']}\n")
            f.write("\n")
            f.write("SUCCESS! The API key is valid and working.\n")
        elif resp.status_code == 401:
            f.write("❌ 401 Unauthorized - API key is invalid or revoked\n")
            f.write(f"Response: {resp.text[:500]}\n")
        else:
            f.write(f"❌ Error {resp.status_code}\n")
            f.write(f"Response: {resp.text[:500]}\n")

    except Exception as e:
        f.write(f"❌ Exception: {e}\n")
        import traceback
        traceback.print_exc(file=f)

print(f"Test complete. Results written to {output_file}")

