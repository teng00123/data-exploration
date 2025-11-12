import requests
import json

# 1. 定义 API 的 URL 和你的密钥
# 请将 {api_key} 替换为你的实际 API Key
# api_url = "http://192.168.20.47/v1/workflows/run"
api_url = "http://192.168.20.47/v1/chat-messages"
# api_key = "app-w8mx1Yu2qTG7CRALo1SWvE6E"  # <--- 在这里填入你的 API Key
api_key = "app-AIYOjZykXjYKX9q5loKfGlay"  # <--- 问答

# 2. 设置请求头
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 3. 设置请求体
payload = {
    # "resources_cname":"遂宁电子表",
    # "summary":"遂宁电子表",
    "inputs": {
    # "resources_cname":"遂宁电子表",
    # "summary":"遂宁电子表",
    },
    "query":"编目目的是什么",
    "response_mode": "streaming",
    "user": "abc-123"
}

try:
    # 4. 发送 POST 请求
    # 使用 json=payload 会自动将字典序列化为 JSON 字符串，并设置正确的 Content-Type
    response = requests.post(api_url, headers=headers, json=payload, stream=True)

    # 5. 检查响应状态码
    response.raise_for_status()  # 如果状态码不是 2xx，会抛出 HTTPError

    # 6. 处理流式响应
    print("开始接收流式响应...")
    answer_str = ''
    document_name = ''
    document_content = ''
    for line in response.iter_lines():
        # 过滤掉 keep-alive 的空行
        if line:
            # Dify 的 SSE 流通常以 "data: " 开头，需要解码并解析
            decoded_line = line.decode('utf-8')
            if decoded_line.startswith("data: "):
                # 移除 "data: " 前缀
                json_string = decoded_line[6:]
                try:
                    # 解析 JSON 数据
                    data = json.loads(json_string)
                    # 在这里你可以处理数据，例如打印出来
                    answer_str += data.get('answer', '')
                    for i in data.get('retriever_resources',[]):
                        document_name += i.get('document_name', '')
                        document_content += i.get('document_content', '')
                    print(data)
                    # print(answer_str)
                    # print(document_name)
                    # print(document_content)
                except json.JSONDecodeError:
                    # 如果不是有效的 JSON，可能是事件结束标志如 "[DONE]"
                    print(f"收到非JSON数据: {json_string}")

except requests.exceptions.HTTPError as err:
    print(f"HTTP 错误: {err}")
except requests.exceptions.RequestException as e:
    print(f"请求发生错误: {e}")

