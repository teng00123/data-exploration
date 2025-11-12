import requests

url = 'http://192.168.20.47/v1/messages'
params = {
    'user': 'abc-123',
    'conversation_id': '940d1796-2c39-4c4a-bf61-d5365a55df35'
}
headers = {
    'Authorization': 'Bearer app-AIYOjZykXjYKX9q5loKfGlay'
}

response = requests.get(url, params=params, headers=headers)

# 打印响应内容
print(response.status_code)
print(response.json())
