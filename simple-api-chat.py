import requests
import json


def get_payload(system_content, user_content, model, assistant_content=None):
    """
    配置请求的 payload 数据
    :param system_content: 系统角色的提示内容
    :param user_content: 用户角色的输入内容
    :param model: 选择的模型
    :param assistant_content: 助手角色的回复内容，可选
    :return: 包含请求参数的字典
    """
    messages = [
        {
            "role": "system",
            "content": system_content
        },
        {
            "role": "user",
            "content": user_content
        }
    ]
    if assistant_content:
        messages.append({
            "role": "assistant",
            "content": assistant_content
        })

    return {
        "model": model,
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
        "messages": messages
    }


def get_headers(api_key):
    """
    配置请求的 headers 数据
    :param api_key: 用户输入的 API Key
    :return: 包含请求头信息的字典
    """
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def send_request(url, payload, headers):
    """
    发送 POST 请求
    :param url: 请求的 URL
    :param payload: 请求的 payload 数据
    :param headers: 请求的 headers 数据
    :return: 请求的响应对象
    """
    return requests.post(url, json=payload, headers=headers, stream=True)


def process_response(response):
    """
    处理请求的响应数据
    :param response: 请求的响应对象
    :return: 处理后的 reasoning_content 和 content
    """
    reasoning_content = ""
    content = ""
    first_reasoning_output = True  # 标记是否是第一次输出 reasoning_content
    last_reasoning_output = False  # 标记是否是最后一次输出 reasoning_content
    try:
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode('utf-8').replace("data: ", "")
                if decoded_line == "[DONE]":
                    last_reasoning_output = True  # 标记为最后一次输出
                    break
                try:
                    chunk = json.loads(decoded_line)
                    if 'choices' in chunk and chunk['choices']:
                        choice = chunk['choices'][0]
                        if 'delta' in choice:
                            delta = choice['delta']
                            if 'reasoning_content' in delta and delta['reasoning_content'] is not None:
                                reasoning_part = delta['reasoning_content']
                                reasoning_content += reasoning_part
                                if first_reasoning_output:
                                    print("Reasoning_Content:")
                                    print("=" * 50)
                                    first_reasoning_output = False  # 第一次输出后标记为 False
                                print(reasoning_part, end='', flush=True)
                                if last_reasoning_output:
                                    print("\n" + "=" * 50)
                            elif 'content' in delta and delta['content'] is not None:
                                content_part = delta['content']
                                content += content_part
                except json.JSONDecodeError as json_err:
                    print(f"JSON decoding error: {json_err}, Line: {decoded_line}")
                    continue
                except KeyError as key_err:
                    print(f"Key error: {key_err}, Chunk: {chunk}")
                    continue
    except Exception as e:
        print(f"An error occurred: {e}")
    return reasoning_content, content


def print_result(content):
    """
    打印最终的 content 结果
    :param content: 处理后的 content 数据
    """
    print("\n\n" + "=" * 50)
    print("Content:")
    print("=" * 50)
    print(content)
    print("=" * 50)


def main():
    """
    主函数，协调各个模块的功能
    """
    # 获取 API Key，无默认值，要求用户必须输入
    api_key = input("请输入你的 API Key：").strip()
    while not api_key:
        api_key = input("API Key 不能为空，请重新输入：").strip()

    # 获取模型选择，若用户跳过则使用默认值
    default_model = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
    model = input(f"请输入模型名称（默认：{default_model}）：").strip() or default_model

    # 获取 system 提示内容，若用户跳过则使用默认值
    default_system_content = "你是一名专业的编程助手，擅长协助编写代码并会用通俗的语言解答问题"
    system_content = input("请输入system的提示内容：（默认：你是一名专业的编程助手，擅长协助编写代码并会用通俗的语言解答问题）").strip() or default_system_content
    
    # 获取 user 输入内容，若用户跳过则使用默认值
    default_user_content = "以下是我的代码，请你为我进行优化"
    user_content = input("请输入user的输入内容：（默认：以下是我的代码，请你为我进行优化）").strip() or default_user_content
    
    # 获取 assistant 回复内容，允许跳过，若跳过则为 None
    default_assistant_content = None
    assistant_content = input("请输入assistant的回复内容（允许跳过）：").strip() or default_assistant_content

    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 调整参数顺序
    payload = get_payload(system_content, user_content, model, assistant_content)
    headers = get_headers(api_key)
    response = send_request(url, payload, headers)
    _, content = process_response(response)
    print_result(content)


if __name__ == "__main__":
    main()