import requests

API_KEY = '0bdffbdb-8621-41f8-9b60-274f1c623645'

PUBLIC_TRANSPORT_ROUTES_URL  = 'https://api.um.warszawa.pl/api/action/public_transport_routes'

BUS_STOP_COORDINATES_URL = 'https://api.um.warszawa.pl/api/action/dbstore_get'
BUS_STOP_RESOURCE_ID = 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'

TIME_TABLE_SUFFIX_URL = ''

def create_params(**kwargs):
    res_dict = {}
    for key, value in kwargs.items():
        if value != None:
            res_dict[key] = value
          
    print(res_dict)
    return res_dict

def get_data(url, parameters):
    response = requests.get(url, params = parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_public_transport_routes(api_key = API_KEY, **kwargs):
    parameters = create_params(apikey = api_key)
    data = get_data(PUBLIC_TRANSPORT_ROUTES_URL, parameters)
    return data
    
def get_bus_stop_coordinates(api_key = API_KEY, resource_id = BUS_STOP_RESOURCE_ID, sortBy = None, size = None, **kwargs):
    parameters = create_params(apikey = api_key, id = resource_id, sortBy = sortBy, size = size)
    data = get_data(BUS_STOP_COORDINATES_URL, parameters)
    return data


print(get_bus_stop_coordinates(size = 1))
    
