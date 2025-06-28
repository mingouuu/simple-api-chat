import requests

url = "https://api.siliconflow.cn/v1/chat/completions"

payload = {
    "model": "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B",
    "stream": True,
    "max_tokens": 512,
    "thinking_budget": 4096,
    "min_p": 0.05,
    "temperature": 0.7,
    "top_p": 0.7,
    "top_k": 50,
    "frequency_penalty": 0.5,
    "n": 1,
    "stop": [],
    "response_format": {"type": "text"},
    "messages": [
        {
            "role": "system",
            "content": "你是一名专业的法律助手"
        },
        {
            "role": "user",
            "content": "民法典是什么时候颁布的？"
        }
    ]
}

api_key = input("请输入你的 API Key：")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}



# 发送请求时设置 stream=True
response = requests.request("POST", url, json=payload, headers=headers, stream=True)

print("=" * 50)
print(f"HTTP Status Code: {response.status_code}") 
print("=" * 50)
print("\n\n" + "=" * 50)
# 正确迭代方式（使用关键字参数）
for chunk in response.iter_content(None, decode_unicode=False):
    if chunk:
        print(chunk.decode('utf-8'), flush=True)

