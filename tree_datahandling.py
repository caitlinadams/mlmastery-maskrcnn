import geopandas
import rasterio
import math

def extract_boxes(image_file, annot_file):

    # First load the image file to get the transfrom and shape
    with rasterio.ipen(image_file) as src:
        transform = src.transform
        width = src.width
        height = src.height
    
    boxes_gdf = geopandas.read_file(annot_file)

    boxes = []
    for index, box in boxes_gdf.iterrows():

        # Get coordinates in physical space
        minx, miny, maxx, maxy = box.bounds.to_numpy().flatten()

        # Transform to pixel space using reverse transfrom (~)
        left, top = ~transform * (minx, maxy)
        right, bottom = ~transform * (maxx, miny)

        coords = [left, bottom, right, top]
        floored_coords = [math.floor(coord) for coord in coords]

        boxes.append(floored_coords)

    return boxes, width, height






