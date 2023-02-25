import requests

headers = {
    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
    'sec-ch-ua-platform': '"Windows"',
    'Referer': 'http://127.0.0.1:5000/',
    'DNT': '1',
    'sec-ch-ua-mobile': '?0',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50',
    'Content-Type': 'application/json',
}

data = '{"username":"user1","password":"password1"}'

response = requests.post('http://localhost:5000/login', headers=headers, data=data)
print(response.text)