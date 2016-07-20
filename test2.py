#!/usr/bin/python3

import os
import sys

# um Module zu finden, wird sys.path modifiziert
path_to_libs = '/home/ITHertU1/GIT_ROOT/Raspi/libs'
sys.path.append(path_to_libs)
for path in sys.path:
    print(path)

from xml.basic.basic_et import RP_BasicET

def get_filename():
    file_name_with_path = __file__
    xml_file = '.' # join string
    to_be_joined = (os.path.splitext(file_name_with_path)[0], "xml") # sequence
    return(xml_file.join(to_be_joined))

xml_file = get_filename()

xml = RP_BasicET(xml_file)
xml_root = xml.getroot()

