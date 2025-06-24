# Simple API Chat

这是一个简单的 Python 脚本，用于与大语言模型 API 进行交互，并以流式方式获取和展示模型的推理过程与最终结果。

## 功能

* **API 交互**：通过 `requests` 库与指定的 API 端点进行通信。
* **参数配置**：
    * 支持配置 `system`, `user`, 和 `assistant` 角色的内容。
    * 允许用户自定义模型名称。
    * 可以调整如 `temperature`, `top_p`, `max_tokens` 等多种模型参数。
* **流式输出**：能够以流的形式接收和处理 API 的响应，并实时展示模型的 `reasoning_content` (推理过程)。
* **结果展示**：在所有内容接收完毕后，清晰地展示最终的 `content` (回复内容)。
* **用户输入**：通过命令行交互式地获取 API Key、模型名称以及各角色的内容。

## 环境要求

* Python 3
* `requests` 库

## 安装

1.  克隆或下载本仓库。
2.  安装所需的 Python 依赖库：
    ```bash
    pip install -r requirements.txt
    ```

## 使用方法

1.  本程序调用的 API `base_url` 来自 [硅基流动 (SiliconFlow)](https://cloud.siliconflow.cn/i/hjshxbt8)，您可以在其官网免费申请 API Key，并免费使用默认模型。

<div align="center">

![image](https://github.com/user-attachments/assets/d7b510f9-81cc-422f-9bef-392ce074bc2a)

</div>
2. 在终端中运行 Python 脚本：
    ```bash
    python simple-api-chat.py
    ```
3.  根据提示输入你的信息：
    * **API Key**：输入您在硅基流动申请的 API 密钥。
    * **模型名称**：可选，如果留空，将使用默认模型 `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B`。
    * **System 提示内容**：可选，如果留空，将使用默认内容 "你是一名专业的编程助手，擅长协助编写代码并会用通俗的语言解答问题"。
    * **User 输入内容**：可选，如果留空，将使用默认内容 "以下是我的代码，请你为我进行优化"。
    * **Assistant 回复内容**：可选，可以留空。

## 代码结构说明

* `get_payload(...)`：构建发送给 API 的请求体（payload），包含了模型参数和对话消息。
* `get_headers(...)`：构建请求头，主要是包含了授权信息 (API Key)。
* `process_response(...)`：处理 API 返回的流式响应。它会逐行解析数据，并区分 `reasoning_content` 和 `content` 进行打印。
* `print_result(...)`：在接收完所有响应后，格式化并打印最终的 `content`。
* `main()`：主函数，负责协调用户输入、发送请求、处理响应和打印结果的整个流程。
