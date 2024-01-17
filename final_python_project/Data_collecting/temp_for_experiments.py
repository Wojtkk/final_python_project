import requests
import json

# Replace 'YOUR_API_KEY' with your actual API key
api_key = '0bdffbdb-8621-41f8-9b60-274f1c623645'

# Define the API endpoint URL
url = 'https://api.um.warszawa.pl/api/action/public_transport_routes/'

# Define the parameters for the API request
params = {
    'apikey': api_key
}

# Make the API request
response = requests.get(url, params=params)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the JSON data from the response
    data = response.json()
    pretty_json = json.dumps(data, indent=4)
    print(pretty_json)
else:
    # Print an error message if the request was not successful
    print(f"Error: {response.status_code} - {response.text}")
