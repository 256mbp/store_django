import requests
from pprint import pprint

response = requests.get("http://api.thedogapi.com/v1/breeds/1")
pprint(response.text)

headers = {'X-Request-Id': 'my-request-id'}
response = requests.get('https://example.org', headers=headers)
response.request.headers

requests.get("http://randomuser.me/api/?gender=female&nat=de").json()

query_params = {"gender": "female", "nat": "de"}
requests.get("http://randomuser.me/api/", params=query_params).json()

endpoint = "http://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos"
api_key = 'DEMO_KEY'
query_params = {"api_key": api_key, "earth_date": '2022-07-01'}
response = requests.get(endpoint, params=query_params)
response