from requests import post

# тестовый файл для отправки post запроса
req = post("http://127.0.0.1:8000/questions/", json={"questions_num": 2})

print(req.content)
