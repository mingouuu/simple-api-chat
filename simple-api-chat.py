import requests
import json

#流式输出推理内容和回答内容
class ProcessResponse:
    def __init__(self):
        self.reasoning_content = ""
        self.content = ""
        self.first_reasoning_header = True
        self.first_content_header = True  

    def process(self, response):
        """流式响应处理核心方法"""
        try:
            for line in response.iter_lines():
                if not line:
                    continue
                
                decoded_line = line.decode('utf-8').replace("data: ", "")
                if decoded_line == "[DONE]":
                    break

                try:
                    chunk = json.loads(decoded_line)
                except json.JSONDecodeError as e:
                    print(f"JSON 解析错误: {e}，数据: {decoded_line}")
                    continue

                # 合并 choice 和 delta 处理逻辑
                if chunk.get('choices') and chunk['choices'][0].get('delta'):
                    delta = chunk['choices'][0]['delta']
                    
                    # 合并内容处理逻辑
                    if delta.get('reasoning_content'):
                        self.print_result(delta['reasoning_content'], 'reasoning_content')
                    
                    if delta.get('content'):
                        self.print_result(delta['content'], 'content')  

        except Exception as e:
            print(f"处理异常: {e}")
        
        if not self.first_content_header:
            print("\n" + "=" * 50)
        return self.reasoning_content, self.content

    def print_result(self, content_part, content_type):
        """通用内容处理"""
        if content_type == 'reasoning_content':
            self.reasoning_content += content_part
            if self.first_reasoning_header:
                print("\n" + "=" * 50)
                print("Reasoning_Content:\n" + "=" * 50)
                self.first_reasoning_header = False
            print(content_part, end='', flush=True)
            
        elif content_type == 'content':
            self.content += content_part
            if self.first_content_header:
                print("\n" + "=" * 50)
                print("\nContent:\n" + "=" * 50)  
                self.first_content_header = False
            print(content_part, end='', flush=True)
            

# 配置请求的 payload 数据
def get_payload(system_content, user_content, model, assistant_content=None, messages=None):
    """
    配置请求的 payload 数据
    :param system_content: 系统角色的提示内容
    :param user_content: 用户角色的输入内容
    :param model: 选择的模型
    :param assistant_content: 助手角色的回复内容，可选
    :param messages: 历史对话消息列表，可选
    :return: 包含请求参数的字典
    """
    messages.append({
        "role": "user",
        "content": user_content
    })
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


# 主函数
def main():
    """
    主函数，协调各个模块的功能
    """
    # 定义请求的 URL
    url = "https://api.siliconflow.cn/v1/chat/completions"
    
    # 获取 API Key，无默认值，要求用户必须输入
    api_key = input("请输入你的 API Key：").strip()
    while not api_key:
        api_key = input("API Key 不能为空，请重新输入：").strip()

    # 获取模型选择，若用户跳过则使用默认值
    default_model = "deepseek-ai/DeepSeek-R1-0528-Qwen3-8B"
    model = input(f"请输入模型名称（默认：{default_model}）：").strip() or default_model

    # 获取 system 提示内容，若用户跳过则使用默认值
    default_system_content = "你是一名专业的编程助手，擅长协助编写代码并会用通俗的语言解答问题"
    system_content = input(f"请输入system的提示内容：（默认：{default_system_content}）").strip() or default_system_content

    messages = [
        {
            "role": "system",
            "content": system_content
        }
    ]

    first_input = True  
    default_user_content = "接下来我为提供我的代码，请帮助我改正代码中的可能存在的问题。"
    
    while True:
        # 根据首次输入显示不同提示
        if first_input:
            prompt = f"请输入你的问题或代码：（默认：{default_user_content}）"
            first_input = False
        else:
            prompt = "请输入你的问题或代码：（输入 'q' 或按 'ctrl+c' 退出）："
        
        user_content = input(prompt).strip() or default_user_content
        if user_content.lower() == 'q':
            break


        # 调用 get_payload 函数生成请求的 payload 数据
        payload = get_payload(system_content, user_content, model, messages=messages)
        # 调用 get_headers 函数生成请求的 headers 数据
        headers = get_headers(api_key)
        # 调用 request 函数发送请求
        response = requests.post(url, json=payload, headers=headers, stream=True)
        # 调用 ProcessResponse 类处理响应数据
        processor = ProcessResponse()
        _, content = processor.process(response)
        # 将本次对话添加到历史消息中
        messages.append({
            "role": "user",
            "content": user_content
        })
        messages.append({
            "role": "assistant",
            "content": content
        })


if __name__ == "__main__":
    main()