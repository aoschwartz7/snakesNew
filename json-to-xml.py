import xml.etree.ElementTree as gfg
import json
import os


# Opening JSON file containing extracted label annotation data and saving
# variables we need (image title, box label dimensions)
def extract_json(json_file):
    # Open JSON file
    with open(json_file) as file:
        data = json.load(file)
        for image in data:
            # Get JPG title
            jpg_title = image["External ID"]

            # Calculate number of boxed objects per image
            num_objects = len(image["Label"]["objects"])

            # Verify object title(s) are called "snake"
            for i in range(num_objects):
                object_title = image["Label"]["objects"][i]["title"]
                if object_title != "snake":
                    print("Image was labeled as ", object)
                    break

            # Calculate dimensions for objects
            for i in range(num_objects):
                coordinates = calculate_dimensions(image, i)
                create_xml(jpg_title, num_objects, coordinates)


#
# # Calculate box label dimensions
def calculate_dimensions(image, i):
    # Extract box label dimensions
    top = image["Label"]["objects"][i]["bbox"]["top"]
    left = image["Label"]["objects"][i]["bbox"]["left"]
    height = image["Label"]["objects"][i]["bbox"]["height"]
    width = image["Label"]["objects"][i]["bbox"]["width"]

    # print("top:", top)
    # print("left:", left)
    # print("height:",height)
    # print("width:", width)

    # Convert dimensions to xmin, xmax, ymin, ymax
    xmin = str(left)
    xmax = str(int(left) + int(width)) # TODO:
    ymin = str(int(top) - int(height)) # TODO:
    ymax = str(top)

    # print("")
    # print("xmin:", xmin)
    # print("xmax:", xmax)
    # print("ymin:", ymin)
    # print("ymax:", ymax)
    return xmin, ymin, xmax, ymax
#
# Create XML container for JPG title and structure
def create_xml(jpg_title, num_objects, coordinates):

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

    for i in range(num_objects):
        object = gfg.Element("object")
        root.append(object)

        name = gfg.SubElement(object, "name")
        name.text = "snake"

        pose = gfg.SubElement(object, "pose")
        pose.text = "Unspecified"

        truncated = gfg.SubElement(object, "truncated")
        truncated.text = "0"

        difficult = gfg.SubElement(oject, "difficult")
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

    with open (jpg_title + ".xml", "wb") as files:
        tree.write(files)




if __name__ == '__main__':
    extract_json("/Users/alecschwartz/Desktop/labelbox-exported/export-2020-09-02T01_26_04.802Z.json")
