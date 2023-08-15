import json

import requests


def validate_api_key(openai_api_key: str) -> bool:
    url = 'https://api.openai.com/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {openai_api_key}',
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Say this is a test!"}],
        "temperature": 0.7
    }
    data = json.dumps(data).encode('utf-8')
    print("Validating your OpenAI API key...")
    try:
        result = requests.post(url, data=data, headers=headers)
        if result.status_code == 200:
            return True
        else:
            print("  OpenAI result status_code:", result.status_code)
            print("  OpenAI response:", result.json())
    except Exception as exc:
        print("  OpenAI exception:", exc)

    return False
