import xml.etree.ElementTree as gfg
from fuzzywuzzy import process
import json

# Create list of object types found in dataset
object_types = ["snake", "snakeHead", "snakeRattle"]

# Opening JSON file containing extracted label annotation data and saving
# variables we need (image title, box label dimensions)
def extract_json(json_file):
    """ Open JSON file created from exporting labels of Labelbox.com boxed objects
    we want to use for training data.
    Extract relevant information: JPG title, number of objects, and
    bounding box dimensions.
    Args:
        json_file: path to JSON export file
    """

    with open(json_file) as file:
        data = json.load(file)
        for image in data:
            # Get JPG title
            jpg_title = image["External ID"]
            # Check if image does not contain any images
            if "objects" not in image["Label"]:
                continue

            # Calculate number of boxed objects per image
            num_objects = len(image["Label"]["objects"])

            # Get object type and box coordinates
            object_list = []

            for i in range(num_objects):
                object_type = image["Label"]["objects"][i]["title"]
                # print(object_type)
                # Verify object type
                object_type = process.extract(object_type, object_types, limit=1)
                object_type = object_type[0][0]
                coordinates = calculate_dimensions(image, i)
                object_list.append({object_type:coordinates})

            # for debugging
            for objects in object_list:
                    for object in objects:
                        object_name = object
                        coordinates = objects[object]
                        print(jpg_title, object_name, coordinates)

            # Create XML file formatted for YOLOv3 model training data
            create_xml(jpg_title, object_list)
            print(" ")

# # Calculate box label dimensions
def calculate_dimensions(image, i):
    """ Bounding box dimensions from JSON export need to be converted to xmin,
    ymin, xmax, ymax values.
    Args:
        image: JPG we are working with.
        i: bounding box within JPG.
    Returns:
        xmin, ymin, xmax, ymax: Euclidean coordinates for XML
    """
    # Extract box label dimensions
    top = image["Label"]["objects"][i]["bbox"]["top"]
    left = image["Label"]["objects"][i]["bbox"]["left"]
    height = image["Label"]["objects"][i]["bbox"]["height"]
    width = image["Label"]["objects"][i]["bbox"]["width"]

    # Convert dimensions to xmin, xmax, ymin, ymax
    xmin = str(left)
    xmax = str(int(left) + int(width))
    ymin = str(top)
    ymax = str(int(top) + int(height))

    return xmin, ymin, xmax, ymax

# Create XML container for JPG title and structure
def create_xml(jpg_title, object_list):
    root = gfg.Element("annotation")

    folder = gfg.Element("folder")
    folder.text = "images"
    root.append(folder)

    filename = gfg.Element("filename")
    filename.text = jpg_title
    root.append(filename)

    path = gfg.Element("path")
    path.text = "/Users/alecschwartz/Desktop/workspace/snakes/images/" + jpg_title
    root.append(path)

    source = gfg.Element("source")
    root.append(source)
    database = gfg.SubElement(source, "database")
    database.text = "Unknown"

    size = gfg.Element("size")
    root.append(size)

    width = gfg.SubElement(size, "width")
    height = gfg.SubElement(size, "height")
    depth = gfg.SubElement(size, "depth")

    width.text = "2048"
    height.text = "1536"
    depth.text = "3"

    segmented = gfg.Element("segmented")
    segmented.text = "0"
    root.append(segmented)

    for objects in object_list:
        for object in objects:
            object_name = object
            coordinates = objects[object]

            object = gfg.Element("object")
            root.append(object)

            name = gfg.SubElement(object, "name")
            name.text = object_name

            pose = gfg.SubElement(object, "pose")
            pose.text = "Unspecified"

            truncated = gfg.SubElement(object, "truncated")
            truncated.text = "0"

            difficult = gfg.SubElement(object, "difficult")
            difficult.text = "0"

            bndbox = gfg.SubElement(object, "bndbox")
            xmin = gfg.SubElement(bndbox, "xmin")
            ymin = gfg.SubElement(bndbox, "ymin")
            xmax = gfg.SubElement(bndbox, "xmax")
            ymax = gfg.SubElement(bndbox, "ymax")

            xmin.text = coordinates[0]
            ymin.text = coordinates[1]
            xmax.text = coordinates[2]
            ymax.text = coordinates[3]


    tree = gfg.ElementTree(root)
    # Remove .JPG from jpg_title
    jpg_title = jpg_title[:-4]
    with open ("annotations_test/" + jpg_title + ".xml", "wb") as files:
        tree.write(files)


if __name__ == '__main__':
    extract_json("export-2020-09-08T21_25_13.516Z.json")
    # extract_json("/Users/alecschwartz/Desktop/labelbox-exported/export-2020-09-02T01_26_04.802Z.json")
