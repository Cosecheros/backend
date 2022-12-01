import xml.etree.ElementTree as ET
import requests

def fetch_xml():
    url = "https://ssl.smn.gob.ar/feeds/avisocorto_GeoRSS.xml"
    req = requests.get(url)
    coordinates_list = parse_xml(req.content)
    print(coordinates_list)
    return req.content


def parse_xml(req):
    coordinates_list = []
    root = ET.fromstring(req)
    print(root.tag)
    print(root.items)
    channel = root[0]
    item = channel.find("item")
    for child in channel:
        if child.tag == "item":
            coordinates = child.find("georss:polygon")
            if coordinates != None:
                coordinates_list.append(coordinates)
            else:
                print("None")
    return coordinates_list

fetch_xml()