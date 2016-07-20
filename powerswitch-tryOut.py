#!/usr/bin/python3

import os
import xml.etree.ElementTree as ET

file_name_with_path = __file__

xml_file = "." # join string
to_be_joined = (os.path.splitext(file_name_with_path)[0], "xml") # sequence
xml_file = xml_file.join(to_be_joined)

#print(file_name_with_path)
#print(xml_file)

tree = ET.parse(xml_file)
root = tree.getroot()

print("countries and neighbour list")
for country in root.findall('country'):
    rank = country.find('rank').text
    name = country.get('name')
    print(name, rank)
    for neighbour in country.findall('neighbour'):
        print("   neighbour:"+neighbour.get('name')+", direction:"+neighbour.get('direction'))
    print('')