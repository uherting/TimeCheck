#!/usr/bin/python3

import os
import time
import datetime
#from datetime import date, timedelta
import xml.etree.ElementTree as ET

def determine_XML_filename():
    file_name_with_path = __file__
    xml_file = '.' # join string
    to_be_joined = (os.path.splitext(file_name_with_path)[0], "xml") # sequence
    return(xml_file.join(to_be_joined))

def getXMLroot(xml_filename):
    tree = ET.parse(xml_filename)
    return(tree.getroot())

def output():
    print_scr('precedence_list:')
    for name in precedence_list:
        print_scr('  ='+name+'=')

    print_scr('supported_tag_list:')
    for name in supported_tag_list:
        print_scr('  ='+name+'=')

def get_data_list(tag_obj):
    ret_list = [ ]
    ret_list.append(tag.get('name'))
    ret_list.append(tag.get('on'))
    ret_list.append(tag.get('off'))
    return(ret_list)
    
def set_res_tag_stat(int_val):
    results_per_tag_stat[working_item+'/'+str(wi_cnt)] = str(int_val)
    
def set_res_tag_on(txt):
    results_per_tag_on[working_item+'/'+str(wi_cnt)] = txt

def set_res_tag_off(txt):
    results_per_tag_off[working_item+'/'+str(wi_cnt)] = txt

# calc date for tag 'once' a time off with duration (e.g. '+3h')
def calc_duration(xml_date_for_comparison, xml_time_on_for_comparison, xml_time_off_for_comparison, p1, p2):
    time_add = xml_time_off_for_comparison[p1+1:p2]
    
    ret_val = 0

    print_scr('  calc_duration -> xml_date_for_comparison =' + xml_date_for_comparison)
    print_scr('                -> xml_time_on_for_comparison =' + xml_time_on_for_comparison)
    print_scr('                -> xml_time_off_for_comparison =' + xml_time_off_for_comparison)
    print_scr('                -> p1 =' + str(p1))
    print_scr('                -> p2 =' + str(p2))
    print_scr('                -> time_add =' + time_add)
    
    (ps_hh, ps_mm) = get_ints(xml_time_on_for_comparison)
    
    datetime_now = datetime.datetime.now()

    datetime_on = datetime.datetime.strptime(xml_date_for_comparison, '%Y%m%d')
    datetime_on = datetime_on.replace(hour=ps_hh, minute=ps_mm, second=0, microsecond=0)
    datetime_off = datetime_on + datetime.timedelta(hours=int(time_add))
    
    print_scr('  datetime_now = '+datetime_now.strftime('%d/%m/%Y %H:%M:%S'))
    print_scr('  datetime_on = '+datetime_on.strftime('%d/%m/%Y %H:%M:%S'))
    print_scr('  datetime_off = '+datetime_off.strftime('%d/%m/%Y %H:%M:%S'))
    

    if ((datetime_on < datetime_now) & (datetime_off > datetime_now)):
        set_res_tag_on(datetime_on.strftime('%d/%m/%Y %H:%M:%S'))
        set_res_tag_off(datetime_off.strftime('%d/%m/%Y %H:%M:%S'))
        ret_val = 1
    
    set_res_tag_stat(ret_val)

    print_scr('ret_val=' + str(ret_val))

    return(ret_val)
    

# check whether tag 'once' has got a time off with duration (e.g. '+3h')
def has_duration(xml_date_for_comparison, xml_time_on_for_comparison, xml_time_off_for_comparison):
    ret_val = 0
    
    p1 = xml_time_off_for_comparison.find('+')
    p2 = xml_time_off_for_comparison.find('h')
    
    if ((p1 > -1) & (p2 > -1) & (p1 < p2)):
        ret_val = 1

    return(p1, p2, ret_val)
    
def get_data_tuple(tag_obj, attr_name='name'):
    ret_tuple = (tag.get(attr_name), tag.get('on'), tag.get('off'))
    return(ret_tuple)
    
def print_scr(text='', end_str='\n'):
    if (debugging == 1):
        print(text, end=end_str)

def print_defs_per_tag(tag_arr, txt=''):
    print_scr('results for: '+txt)
    
    for k, v in tag_arr.items(): 
        print_scr('  '+k+'='+v)

    print_scr('')
    
def get_int(val_tmp_str, ret_val=0):
    print_scr('-------- get_int')
    print_scr('val_tmp_str=#'+val_tmp_str+'#')
    
    val_tmp = val_tmp_str
    str_1 = val_tmp[:1]
    str_2 = val_tmp[1:]

    if str_1 == '0':
        val_str = str_2
        # print_scr('val_str shortened to:#'+val_str+'#')
    else:
        val_str = val_tmp_str

    if val_str == '':
        ret_val = 0
    else:
        #ret_val = 0
        ret_val = int(val_str)
    
    print_scr('')    
    
    return(ret_val)
  
def get_ints(str2int):
    print_scr('-------- get_ints')

    time_hh_str = ''
    time_mm_str = ''
    
    pos_colon = str2int.find(':')
    if pos_colon != -1:
        len_hh = pos_colon
        pos_mm = pos_colon + 1

        time_hh_str = str2int[:len_hh]
        time_mm_str = str2int[pos_mm:]
    print_scr('    time_hh_str=#'+time_hh_str + '#  /  time_mm_str=#'+time_mm_str+'#')

    time_hh = get_int(time_hh_str)
    time_mm = get_int(time_mm_str)

    print_scr('    time hh(int)=#', ' ')
    print_scr(time_hh, '#')
    print_scr('    time mm(int)=#', '')
    print_scr(time_mm, '#')
    print_scr('')
    
    return(time_hh, time_mm)

# check whether current day is in given duration    
def chk_day_frame(tmp_duration, day_for_comparison):
    ret_val = 0
    if tmp_duration == 'today':
        ret_val = 1
    else:
        pos_from = -1
        pos_to = -1
        pos_today = -1

        # try to find day_for_comparison (the current day) in days_of_week
        try:
            pos_today = days_of_week.index(day_for_comparison)
            print_scr('   pos_today', '=')
            print_scr(pos_today)
        except ValueError:
            pos_today = -1
            print_scr('index of day_for_comparison('+day_for_comparison+') not found in:', ' ')
            print_scr(days_of_week)
            ret_val = 0
        
        # check whether this is a dayToDay (Mon-Thu) frame or a single day (Mon)
        #print_scr(days_of_week)
        if '-' in tmp_duration:
            df_from = tmp_duration[0:3]
            df_to = tmp_duration[-3:]
            print_scr('   DayFrame:'+tmp_duration+' df_from='+df_from+' df_to='+df_to)
            if (df_from in days_of_week) and (df_to in days_of_week):
                # try to find df_from in days_of_week
                try:
                    pos_from = days_of_week.index(df_from)
                    print_scr('   pos_from', '=')
                    print_scr(pos_from)
                except ValueError:
                    pos_from = -1
                    print_scr('index of df_from('+df_from+') not found in:', ' ')
                    print_scr(days_of_week)
                    ret_val = 0

                # try to find df_to in days_of_week
                try:
                    pos_to = days_of_week.index(df_to)
                    print_scr('   pos_to', '=')
                    print_scr(pos_to)
                except ValueError:
                    pos_to = -1
                    print_scr('index of df_to('+df_to+') not found in:', ' ')
                    print_scr(days_of_week)
                    ret_val = 0
                # were the two days found?
                if (pos_today >= 0) and (pos_from >= 0) and (pos_to >= 0):
                    if (pos_from <= pos_today) and (pos_today <= pos_to):
                        ret_val = 1
                
        else:
            df_oneday = tmp_duration[0:3]
            print_scr('DateFrame:'+tmp_duration+' df_oneday='+df_oneday)
            if (df_oneday in days_of_week):
                # try to find df_oneday in days_of_week
                try:
                    pos_from = days_of_week.index(df_oneday)
                except ValueError:
                    pos_from = -1
                    print_scr('index of df_oneday('+df_oneday+') not found in:', ' ')
                    print_scr(days_of_week)
                    ret_val = 0
                if (pos_today >= 0) and (pos_from >= 0):
                    if (pos_from == pos_today):
                        ret_val = 1
    return(ret_val)
    
# central time compare function depending on the new status
def chk_time(ps_str, status_ps, new_status, time_on=""):
    ret_val = 0
    time_now = datetime.datetime.now()
    time_ps_cmp = datetime.datetime.now()

    (ps_hh, ps_mm) = get_ints(ps_str)
    
    time_ps_cmp = time_ps_cmp.replace(hour=ps_hh, minute=ps_mm, second=0, microsecond=0)    

    print_scr('  time_ps_cmp='+time_ps_cmp.strftime('%d/%m/%Y %H:%M:%S'))
    print_scr('  time_now='+time_now.strftime('%d/%m/%Y %H:%M:%S'))
    print_scr('  new_status='+str(new_status))
    
    if new_status == 1:
        if time_ps_cmp < time_now:
            ret_val = new_status
            print_scr('  (A)ret_val = new_status='+str(new_status))
        else:
            ret_val = status_ps
            print_scr('  (A)ret_val = status_ps')
    if new_status == 0:
        if time_now > time_ps_cmp:
            ret_val = new_status
            print_scr('  (B)ret_val = new_status='+str(new_status))
        else:
            ret_val = status_ps
            print_scr('  (B)ret_val = status_ps')
    print_scr('ret_val = ' + str(ret_val))
    return(ret_val)
    
# compare function for status on
def chk_time_on(status_ps, ps_str, new_status=1):
    ret_val = status_ps
    
    if ps_str != '':
        print_scr('== exec chk_time from chk_time_on with ps_str='+ps_str)
        set_res_tag_on(ps_str)
        ret_val = chk_time(ps_str, status_ps, new_status)
        
    return(ret_val)
    
# compare function for status off
def chk_time_off(status_ps, time_on, ps_str, new_status=0):
    ret_val = status_ps
    
    if ps_str != '':
        print_scr('== exec chk_time from chk_time_off with ps_str='+ps_str)
        set_res_tag_off(ps_str)
        ret_val = chk_time(ps_str, status_ps, new_status)
    
    return(ret_val)

# check whether current day fits in the given duration/day    
def chk_duration(status_ps, tmp_duration, time_on, time_off, day_for_comparison):
    in_day_frame = chk_day_frame(tmp_duration, day_for_comparison)
    
    if in_day_frame == 1:
        print_scr('      => in day frame')
        print_scr('')
        print_scr('=========  determining the status of the switch (1) ================')
        status_ps = chk_time_on(status_ps, time_on)
        print_scr('=========  determining the status of the switch (2) ================')
        status_ps = chk_time_off(status_ps, time_on, time_off)
        
        set_res_tag_stat(status_ps)
    else:
        print_scr('not in day frame')


    return(status_ps)
    
root = getXMLroot(determine_XML_filename())

#initialise
supported_tag_list = [ ]
precedence_list = [ ]
working_item_list = [ ]
ps_on_str = ''
ps_off_str = ''
status_ps = 0
cur_date = datetime.date.today()
results_per_tag_on = { } # a dictionary
results_per_tag_off = { } # a dictionary
results_per_tag_stat = { } # a dictionary
results_per_tag_cnt = { } # a dictionary


debugging = 0


# get supported tags
# only one tag called 'supported_tags' is allowed, if there are multiple then the last wins
#print_scr('supported_tag tag list:')
for supported_tag in root.findall('supported_tags'):
    names_string = supported_tag.get('names')
    supported_tag_list = names_string.split()

# get precedence list
# only one tag called 'precedence' is allowed, if there are multiple then the last wins
#print_scr('precedence tag list')
for precedence in root.findall('precedence'):
    names_string = precedence.get('order')
    precedence_list = names_string.split()

# durch precedence-Liste gehen, wenn in supported_tags vorhanden, dann zu working_item_list hinzufügen
for precedence in precedence_list:
    if precedence in supported_tag_list:
        working_item_list.append(precedence)
            
# Einlesen first_dow und Umwandeln in Integer
for first_dow in root.findall('first_dow'):
    names_string = first_dow.text
print_scr('first_dow=#'+names_string+'#')
first_dow = int(names_string)

# Generieren der Liste days_of_week (Strings) basierend auf first_dow
# a) find week_start and week_end for creating the list
a_sunday_date = datetime.date(2016, 4, 24) # get a sunday date
#week_start = a_sunday_date + timedelta(days=first_dow)
#week_end = a_sunday_date + timedelta(days=(first_dow+6))
#print_scr('a_sunday_date:', a_sunday_date.strftime('%d/%m/%Y %H:%M:%S'))
#print_scr('week_start:', week_start.strftime('%d/%m/%Y %H:%M:%S'))
#print_scr('week_end:', week_end.strftime('%d/%m/%Y %H:%M:%S'))
# b) create the list
days_of_week = [ ]
print_scr('dow:', ' ')
for i in range(first_dow, first_dow+7):
    tmp_day = a_sunday_date + datetime.timedelta(days=i)
    #print_scr('tmp_day:', tmp_day.strftime('%d/%m/%Y %H:%M:%S'))
    print_scr(tmp_day.strftime('%a'), ' ')
    days_of_week.append(tmp_day.strftime('%a'))
print_scr('')
#    
#print_scr('days_of_week')
#print_scr(days_of_week)

print_scr()
print_scr('looping through working_item_list')
day_for_comparison = cur_date.strftime('%a')

# setup for (limited) testing
#working_item_list = [ ] # debugging only
#working_item_list.append('weekend') # debugging only
#working_item_list.append('weekday') # debugging only
#working_item_list.append('once') # debugging only

wi_cnt = 0
for working_item in working_item_list:
    wi_cnt = 0
    
    # for each working_item we start from scratch
    status_ps = 0
    for tag in root.findall(working_item):
        wi_cnt = wi_cnt + 1
        print_scr('working_item =' + working_item + '    wi_cnt = ' + str(wi_cnt))
        
        # react different on diffrent working items
        if working_item == 'once':
            # only for XML tag 'once'
            
            (xml_date_for_comparison, xml_time_on_for_comparison, xml_time_off_for_comparison) = get_data_tuple(tag, 'date')
            # check whether we are on the date given with the attr 'date'
            #cur_date_obj = datetime()cur_date_obj.
            
            (p1, p2, has_dur) = has_duration(xml_date_for_comparison, 
                                                xml_time_on_for_comparison, 
                                                xml_time_off_for_comparison)
            print_scr(' has_duration exec')
            if has_dur == 1:
                print_scr(' calc_duration exec')
                status_ps = calc_duration(xml_date_for_comparison, 
                                                    xml_time_on_for_comparison, 
                                                    xml_time_off_for_comparison,
                                                    p1, 
                                                    p2)
            else:
                date_for_comparison = cur_date.strftime('%Y%m%d')
                if date_for_comparison == xml_date_for_comparison:
                    print_scr('xml_time_on_for_comparison = #' + xml_time_on_for_comparison + '#')
                    print_scr('xml_time_off_for_comparison = #' + xml_time_off_for_comparison + '#')
                    status_ps = chk_duration(status_ps, day_for_comparison, xml_time_on_for_comparison, xml_time_off_for_comparison, day_for_comparison)
                
                    print_scr(' date_for_comparison='+date_for_comparison, ' ')
                    print_scr(' xml_date_for_comparison='+xml_date_for_comparison)
                    print_scr(' day_for_comparison='+day_for_comparison)
                    print_scr(' xml_time_on_for_comparison='+xml_time_on_for_comparison, ' ')
                    print_scr(' xml_time_off_for_comparison='+xml_time_off_for_comparison, ' ')
        else:
            # the ordinary way for all other XML tags
            
            # get data from current XML tag
            (tmp_duration, xml_time_on_for_comparison, xml_time_off_for_comparison) = get_data_tuple(tag, 'name')
            status_ps = chk_duration(status_ps, tmp_duration, xml_time_on_for_comparison, xml_time_off_for_comparison, day_for_comparison)
            
            print_scr('      tmp_duration='+tmp_duration, ' ')
            print_scr(' xml_time_on_for_comparison='+xml_time_on_for_comparison, ' ')
            print_scr(' xml_time_off_for_comparison='+xml_time_off_for_comparison, ' ')
    
    results_per_tag_cnt[working_item] = wi_cnt

print_scr('') 
print_scr('')
print_scr('')
print_scr('')

print_defs_per_tag(results_per_tag_on, 'results_per_tag_on')
print_defs_per_tag(results_per_tag_off, 'results_per_tag_off')
print_defs_per_tag(results_per_tag_stat, 'results_per_tag_stat')

for working_item in working_item_list:
    for i in range(1,results_per_tag_cnt[working_item]+1):
        acc_key = working_item+'/'+str(i)
        if acc_key in results_per_tag_stat:
            tmp_stat = int(results_per_tag_stat[acc_key])
            if tmp_stat == 1:
                status_ps = 1

print_scr('')
print_scr('')
print('status_ps (final) = ' + str(status_ps)) 

# EOF

