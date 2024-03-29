""" 
Just downloading data, nothing more.
"""

import requests
import json

API_KEY = '30427848-d36c-4fb9-a953-32066860092a'

PUBLIC_TRANSPORT_ROUTES_URL  = 'https://api.um.warszawa.pl/api/action/public_transport_routes'

BUS_STOP_COORDINATES_URL = 'https://api.um.warszawa.pl/api/action/dbstore_get'
BUS_STOP_COORDINATES_RESRC_ID = 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3'

CURRENT_BUSES_POSITIONS_URL = 'https://api.um.warszawa.pl/api/action/busestrams_get'
CURRENT_BUSES_POSITIONS_RESRC_ID = 'f2e5503e-927d-4ad3-9500-4ab9e55deb59'

BUS_TIME_TABLE_URL = 'https://api.um.warszawa.pl/api/action/dbtimetable_get'
BUS_TIME_TABLE_RESRC_ID = 'e923fa0e-d96c-43f9-ae6e-60518c9f3238'


# creating dict out of kwargs
def create_params(**kwargs):
    res_dict = {}
    for key, value in kwargs.items():
        if value != None:
            res_dict[key] = value
          
    return res_dict

def get_data(url, parameters):
    response = requests.get(url, params = parameters)
    if response.status_code == 200:
        return response.json()
    else:
        return None
  
# downloading json, and returning data['result'] out of json  
def get_public_transport_routes(**kwargs):
    parameters = create_params(apikey = API_KEY)
    data = get_data(PUBLIC_TRANSPORT_ROUTES_URL, parameters)
    return data['result']

# downloading json, and returning data['result'] out of json  
def get_bus_stop_informations(sortBy = None, size = None, **kwargs):
    parameters = create_params(apikey = API_KEY, 
                               id = BUS_STOP_COORDINATES_RESRC_ID, 
                               sortBy = sortBy, 
                               size = size)
    data = get_data(BUS_STOP_COORDINATES_URL, parameters)
    return data['result']

# downloading json, and returning data['result'] out of json  
def get_curr_position_of_buses(line = None, **kwargs):
    we_want_buses = 1
    parameters = create_params(apikey = API_KEY, 
                               resource_id = CURRENT_BUSES_POSITIONS_RESRC_ID, 
                               line = line, 
                               type = we_want_buses)
    data = get_data(CURRENT_BUSES_POSITIONS_URL, parameters)
    return data['result']

# downloading json, but in this case we have mandatory arguments
def get_bus_time_table(bus_stop_nr, bus_stop_id, line, **kwargs):
    parameters = create_params(apikey = API_KEY, 
                               id = BUS_TIME_TABLE_RESRC_ID, 
                               busstopNr = bus_stop_nr, 
                               busstopId = bus_stop_id, 
                               line = line)
    data = get_data(BUS_TIME_TABLE_URL, parameters)
    return data




