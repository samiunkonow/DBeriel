import requests

json = {"amount": 20}
url = requests.post(f"http://localhost:9000/api/add_to_inventory/1/1/Josue/", params=json)
print(url.text)