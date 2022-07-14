import requests


url = "http://10.1.20.193:8080/test/add_balance"

payload = {"uid": 1090250105, "balance": 500000000, "currency": 1000}

result = requests.post(url=url, params=payload)
print(result)
