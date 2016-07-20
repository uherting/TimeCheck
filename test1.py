#!/usr/bin/python3

import sys
import os
import xml.etree.ElementTree as ET

ps_str = '+10h'
new_status = 0
time_on="12:22"

if (new_status == 0):
    p1 = ps_str.find('+')
    p2 = ps_str.find('h')
    if ((p1 > -1) & (p2 > -1) & (p1 < p2)):
        add_val = ps_str[p1+1:p2]
        print('add_val = #' + add_val +'#')
        
sys.exit()

# Test 
# um Module zu finden, wird sys.path modifiziert
path_to_libs = '/home/ITHertU1/GIT_ROOT/Raspi/libs'
sys.path.append(path_to_libs)
for path in sys.path:
    print(path)
    
def get_filename():
    print('test')

get_filename()

sys.exit()

