import requests

for i in range(100):
    response = requests.get('http://localhost')
    print(response.text)
