""" 
In this module we have functions to plot data on map of Warsaw.
As well as functions plotting data on conventional charts.
"""

import cv2
import matplotlib.pyplot as plt
from pathlib import Path
import copy

from Data_reading.modifying_dfs import Aliases as als


IMAGE_FILE_NAME = 'warsaw.png'
IMG_WIDTH = 1220
IMG_HIGHT = 800

LEFT_LOWER_CORNER_COORDS = (52.12383466080289, 20.745455267261764)
RIGHT_UP_CORNER_COORDS = (52.36283029032839, 21.305206537911488)

COLOR_MAP_TYPE = 'viridis'

def load_map_image():
    dir = Path(__file__).parent / IMAGE_FILE_NAME
    dir = str(dir)
    
    image = cv2.imread(dir)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  
    return image


def normalise_points_and_values(points_and_values):
    """ 
    in this function points and values is list of tuples
    tuples are the following: (lat, lon, value)
    what we want to do is to map all tuples so that
    lat and lon correspond to image coordinates 
    and all values are in (0, 1]
    """
    def map_point(edge1, edge2, between, image_s):
        distance_overall = edge2 - edge1
        distance_partial = between - edge1
        
        mapped = (distance_partial / distance_overall) * image_s
        return mapped
    
    def map_lat(ours):
        rightmost = RIGHT_UP_CORNER_COORDS[0]
        leftmost = LEFT_LOWER_CORNER_COORDS[0]
        
        return IMG_HIGHT - map_point(leftmost, rightmost, ours, IMG_HIGHT)
        
    def map_lon(ours):
        upper = RIGHT_UP_CORNER_COORDS[1]
        lower = LEFT_LOWER_CORNER_COORDS[1]
        
        return map_point(lower, upper, ours, IMG_WIDTH)
    
    def is_in_image(point_and_value):
        lat = point_and_value[0]
        lon = point_and_value[1]
        return 0 <= lat <= IMG_HIGHT and 0 <= lon <= IMG_WIDTH
        
    cmap = plt.colormaps.get_cmap(COLOR_MAP_TYPE)
    max_value = max([x[2] for x in points_and_values])
    
    for i, (lat, lon, value) in enumerate(points_and_values):
        new_lat = map_lat(lat)
        new_lon = map_lon(lon)
        new_value = cmap(value / max_value)

        points_and_values[i] = (new_lat, new_lon, new_value)
        
    points_and_values = list(filter(is_in_image, points_and_values))
    return points_and_values

def plot_points_on_map(points_and_values, title = 'Stats on map', 
                       width = 10, height = 8, dot_size = 20):
    points_and_values = copy.deepcopy(points_and_values)
    plt.figure(figsize=(width, height))
    
    image = load_map_image()
    plt.imshow(image)
    
    points_and_values = normalise_points_and_values(points_and_values)
    for lat, lon, color in points_and_values:
        plt.scatter(lon, lat, color = color, s = dot_size)  
        
    plt.title(title)  
    plt.axis('off') 
    plt.show()
    
# Function to create a horizontal bar plot
def plot_barh(data, x_col, y_col, title, xlabel, ylabel, color='skyblue'):
    plt.figure(figsize=(10, 6))
    
    plt.barh(data[x_col], data[y_col], color=color)
    
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    
    plt.gca().invert_yaxis()
    
    plt.tight_layout()
    plt.show()

def visualize_overspeed_percentage_within_line(data):
    plot_barh(data, 
              x_col = als.LINE.value, 
              y_col = als.OVERSPEED_PERCENTAGE.value,
              title = 'Overspeed Frequency of Bus Lines',
              xlabel = 'Bus Line',
              ylabel = 'Overspeed Frequency (Percentage)')

def visualize_overspeed_in_places(data):
    plot_barh(data, x_col='place', y_col='overspeed_percentage',
              title='Overspeed Percentage at Different Places',
              xlabel='Overspeed Percentage',
              ylabel='Place')

def plot_most_delayed_bus_stops(delayed_bus_stops_df):
    plot_barh(delayed_bus_stops_df, 
              x_col = als.PLACE.value, 
              y_col = als.DELAY.value,
              title = 'Most Delayed Bus Stops',
              xlabel = 'Delay (minutes)',
              ylabel = 'Bus Stop')

def plot_shortest_expected_waiting_bus_stops(shortest_waiting_bus_stops_df):
    plot_barh(shortest_waiting_bus_stops_df, 
              x_col = als.PLACE.value,
              y_col = als.EXPECTED_WAITING.value,
              title = 'Bus Stops with Shortest Expected Waiting Time',
              xlabel = 'Expected Waiting Time (minutes)',
              ylabel = 'Bus Stop')

    
if __name__ == '__main__':
    p1 = (52.187213539950555, 20.911449507005816, 0.5)
    p2 = (52.207213539950555, 20.911449507005816, 1)
    p3 = (52.227213539950555, 20.911449507005816, 20)
    p4 = (52.247213539950555, 20.911449507005816, 1)
    p = [p1, p2, p3, p4]
    plot_points_on_map(p, "xd", 15, 12)