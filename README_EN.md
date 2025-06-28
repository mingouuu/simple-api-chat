<div align="center">
<h1>Simple API Chat</h1>
</div>
<div align="center">
<p>English | <a href="README.md">简体中文</a></p>
</div>

This is a simple Python script designed to interact with large language model APIs and streamingly retrieve and display the model's reasoning process and final results.

## Features

* **API Interaction**: Communicates with the specified API endpoint using the `requests` library.
* **Parameter Configuration**:
    * Supports configuring the content for `system`, `user`, and `assistant` roles.
    * Allows users to customize the model name.
    * Enables adjustment of various model parameters such as `temperature`, `top_p`, and `max_tokens`.
* **Streaming Output**: Capable of receiving and processing API responses in a streaming manner, and displaying the model's `reasoning_content` (reasoning process) in real - time.
* **Result Display**: Clearly presents the final `content` (response content) after all content has been received.
* **User Input**: Interactively obtains the API Key, model name, and content for each role through the command line.

## Environment Requirements

* Python 3
* `requests` library

## Installation

1. Clone or download this repository.
2. Install the required Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. The `API key` used in this program is from [SiliconFlow](https://cloud.siliconflow.cn/i/hjshxbt8). You can apply for an API Key for free on its official website and use the default model for free.

<div align="center">

![image](https://github.com/user-attachments/assets/d7b510f9-81cc-422f-9bef-392ce074bc2a)

</div>

   You can also switch to other large - model providers or third - party providers by modifying parameters such as `API key`, `base url`, and `model`.

2. Run the Python script in the terminal:
    ```bash
    python simple-api-chat.py
    ```
    
3. Enter your information as prompted:
    * **API Key**: Enter the API key you applied for on SiliconFlow.
    * **Model Name**: Optional. If left blank, the default model `deepseek-ai/DeepSeek-R1-0528-Qwen3-8B` will be used.
    * **System Prompt Content**: Optional. If left blank, the default content "You are a professional programming assistant, proficient in assisting with code writing and answering questions in plain language" will be used.
    * **User Input Content**: Optional. If left blank, the default content "Here is my code, please optimize it for me" will be used.
    * **Assistant Response Content**: Optional. Can be left blank.

## Code Structure Explanation

* `get_payload(...)`: Constructs the request body (payload) sent to the API, including model parameters and conversation messages.
* `get_headers(...)`: Constructs the request headers, mainly containing authorization information (API Key).
* `process_response(...)`: Processes the streaming response returned by the API. It parses the data line by line and distinguishes between `reasoning_content` and `content` for printing.
* `print_result(...)`: Formats and prints the final `content` after all responses have been received.
* `main()`: The main function, responsible for coordinating the entire process of user input, sending requests, processing responses, and printing results.
