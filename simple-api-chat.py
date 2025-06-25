import requests
import json


class ProcessResponse:
    def __init__(self):
        self.reasoning_content = ""
        self.content = ""
        self.first_reasoning_output = True
        self.last_reasoning_output = False

    def is_last_line(self, decoded_line):
        """检查是否是最后一行 [DONE]"""
        return decoded_line == "[DONE]"

    def parse_json(self, decoded_line):
        """解析 JSON 数据，处理解析错误"""
        try:
            return json.loads(decoded_line)
        except json.JSONDecodeError as json_err:
            print(f"JSON decoding error: {json_err}, Line: {decoded_line}")
            return None

    def get_choice(self, chunk):
        """从 chunk 中获取第一个 choice"""
        if 'choices' in chunk and chunk['choices']:
            return chunk['choices'][0]
        return None

    def get_delta(self, choice):
        """从 choice 中获取 delta"""
        if 'delta' in choice:
            return choice['delta']
        return None

    def process_reasoning_content(self, delta):
        """处理推理内容"""
        if 'reasoning_content' in delta and delta['reasoning_content'] is not None:
            reasoning_part = delta['reasoning_content']
            self.reasoning_content += reasoning_part
            if self.first_reasoning_output:
                print("Reasoning_Content:")
                print("=" * 50)
                self.first_reasoning_output = False
            print(reasoning_part, end='', flush=True)

    def process_content(self, delta):
        """处理回复内容"""
        if 'content' in delta and delta['content'] is not None:
            content_part = delta['content']
            self.content += content_part

    def process(self, response):
        """
        处理请求的响应数据
        :param response: 请求的响应对象
        :return: 处理后的 reasoning_content 和 content
        """
        try:
            # 逐行迭代响应内容
            for line in response.iter_lines():
                if not line:
                    continue
                # 解码响应行并去除 "data: " 前缀
                decoded_line = line.decode('utf-8').replace("data: ", "")
                if self.is_last_line(decoded_line):
                    self.last_reasoning_output = True
                    break
                chunk = self.parse_json(decoded_line)
                if chunk is None:
                    continue
                choice = self.get_choice(chunk)
                if choice is None:
                    continue
                delta = self.get_delta(choice)
                if delta is None:
                    continue
                self.process_reasoning_content(delta)
                self.process_content(delta)
        except Exception as e:
            # 处理其他异常
            print(f"An error occurred: {e}")
        return self.reasoning_content, self.content


# 配置请求的 payload 数据
def get_payload(system_content, user_content, model, assistant_content=None):
    """
    配置请求的 payload 数据
    :param system_content: 系统角色的提示内容
    :param user_content: 用户角色的输入内容
    :param model: 选择的模型
    :param assistant_content: 助手角色的回复内容，可选
    :return: 包含请求参数的字典
    """
    # 初始化消息列表，包含系统角色和用户角色的消息
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
    # 如果提供了助手角色的回复内容，则添加到消息列表中
    if assistant_content:
        messages.append({
            "role": "assistant",
            "content": assistant_content
        })

    # 返回包含所有请求参数的字典
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


# 配置请求的 headers 数据（api key）
def get_headers(api_key):
    """
    配置请求的 headers 数据
    :param api_key: 用户输入的 API Key
    :return: 包含请求头信息的字典
    """
    # 返回包含授权信息和内容类型的请求头字典
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


# 打印最终的 content 结果
def print_result(content):
    """
    打印最终的 content 结果
    :param content: 处理后的 content 数据
    """
    # 打印分隔线和标题
    print("\n\n" + "=" * 50)
    print("Content:")
    print("=" * 50)
    # 打印最终的回复内容
    print(content)
    # 打印分隔线
    print("=" * 50)


# 主函数
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

    # 定义请求的 URL
    url = "https://api.siliconflow.cn/v1/chat/completions"
    # 调用 get_payload 函数生成请求的 payload 数据
    payload = get_payload(system_content, user_content, model, assistant_content)
    # 调用 get_headers 函数生成请求的 headers 数据
    headers = get_headers(api_key)
    # 调用 request 函数发送请求
    response = requests.post(url, json=payload, headers=headers, stream=True)
    # 调用 ProcessResponse 类处理响应数据
    processor = ProcessResponse()
    _, content = processor.process(response)
    # 调用 print_result 函数打印最终结果
    print_result(content)


if __name__ == "__main__":
    main()