import requests

endpoint = 'http://KRK4OFLTP00765:9874/onlySTRING'
response = requests.get(endpoint)
print(response.json())
