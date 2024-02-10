import cv2
import matplotlib.pyplot as plt
from pathlib import Path

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
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
    return image

def normalise_points_and_values(points_and_values):
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

def plot_points_on_map(points_and_values, width = 10, height = 8):
    plt.figure(figsize=(width, height))
    
    image = load_map_image()
    plt.imshow(image)
    
    points_and_values = normalise_points_and_values(points_and_values)
    for lat, lon, color in points_and_values:
        plt.scatter(lon, lat, color=color, s=10)  
        
    plt.axis('off') 
    plt.show()

if __name__ == '__main__':
    p1 = (52.187213539950555, 20.911449507005816, 0.5)
    p2 = (52.207213539950555, 20.911449507005816, 1)
    p3 = (52.227213539950555, 20.911449507005816, 20)
    p4 = (52.247213539950555, 20.911449507005816, 1)
    p = [p1, p2, p3, p4]
    plot_points_on_map(p, 15, 12)
    
    

