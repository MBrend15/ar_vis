#Module: Aruba Client Data Parser
#Authors: Salman and Brendan
#Purpose: To parse aruba client xml data and store in a PostGres DB
#Input: Directory
#Output: Parsed data (potentially)
#comments: takes forever, needs to determine a more efficient methodology

#parse library
import xml.etree.ElementTree as ET

#these libraries enable directory manipulation
import shutil
import glob
import fnmatch
import os
from datetime import datetime

#define master dictionary to use throughout
master_dict = {}

##############################################################################################################################################################
#optional functions

#create function to organize ramp client data based on size and ssid
def org_ramp_files(FileName): 
    for name in os.listdir(FileName):
        #for file size bigger than 249 bytes, again means there is actual information in there
        file_info = os.stat(os.path.join(FileName,name))
        file_size = file_info.st_size
        file_name = os.path.join(FileName,name)
        if file_size > 249:
             #initially parse file
            tree = ET.parse(file_name)
            for child in tree._root:
                    x = 0 
                    y = 0
                    #for ssids in an association, determine if eduroam or connect_vt, then move file to the appropriate folder, use a counter in the event that
                    #the file contains both connect_vt and eduroam
                    for Assoc in child.findall('association'):
                        for ssid in Assoc.findall('ssid'):
                            ssid_txt = ssid.text
                            if ssid_txt == 'eduroam' and x == 0: 
                                file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\org_client\\amp_eduroam', name)
                                os.rename(file_name, file_name2) 
                                x = 1
                            elif ssid_txt == 'CONNECTtoVT-Wireless' and y == 0: 
                                file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\org_client\\amp_connect_vt\\', name)
                                os.rename(file_name, file_name2)                                
                                y = 1
                            elif (ssid_txt == 'CONNECTtoVT-Wireless' and x == 1) or (ssid_txt == 'eduroam' and y == 1): 
                                file_name2 = file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\org_client\\amp_both\\', name)
                                os.rename(file_name, file_name2)
                                break

    return 0;

#quick function to parse visrf files and see what we get
def parse_visrf(FileName):
    tree = ET.parse(FileName)
    root = tree.getroot()
    for child in root: 
        print(child.attrib)
        print(child.get('mac'))
        for radio in child.findall('radio'):
            print(radio.attrib)
        
    print(root.attrib)

###############################################################################################################################################################
#function definitions

def parse_file(FileName):

    #iterate over all files in the directory
    for name in os.listdir(FileName):
        file_nm = os.path.join(FileName, name)
        tree = ET.parse(file_nm)
        #for the child in the root
        for child in tree._root:
            mac_addr = child.get('mac')
            ass_id =  ''
            apid = ''
            start = ''
            stop = ''
            
            
            #find all instances of an association and pull client mac, assoc id, conn and disconn times
            for Assoc in child.findall('association'):
                
		lan_addr = []
           	ass_prop = []

                ass_id =  Assoc.get('id')
                apid = Assoc[0].text
                start = Assoc[2].text
                stop = Assoc[3].text
                x = 0

                #compile all the above into a collection
                ass_prop.append(mac_addr) 
                ass_prop.append(ass_id)
                ass_prop.append(apid)
                ass_prop.append(start)
                ass_prop.append(stop)

                #compile client_key to enter into dictionary. composed of mac, ap, and association start time
                client_key = mac_addr+'_'+start+'_'+apid
            
                    #iterate to discover and then write all lan addresses
                for LAN in Assoc.findall('lan_elements'):               
                    for lan_ele in LAN.findall('lan'):
                        lan_addr.append(lan_ele.get('ip_address'))                
                
                    #add lan_elemnets to the back end of the collection
                    ass_prop.append(lan_addr)

                #add collection to dictionary with key as concatenation of apid_mac_start
                global master_dict 
                add2Dict(master_dict, client_key, ass_prop)                                                                        
    
    #return a copy of the master dictionary                        
    return 0;            

def add2Dict(sampDic, term, info_collec):     
    #is term already in dictionary? 
    result1 = term in sampDic    
    #if not add it with count of 1, if so append the count
    if result1 == False:
        sampDic[term] = info_collec
    #else: 
    #    print('Did not add')
    return 0

#create function that purges main directory of irrelevant files
def file_purge(file_name):
    for name in os.listdir(file_name): 
        dlt_file = os.path.join(file_name, name)
        file_size = os.path.getsize(dlt_file)
        #is file bigger than 250 bytes, then delete
        if file_size < 250:
            os.remove(dlt_file)
    return 0





#############################################################################################################################################################
#main

print datetime.now().time() 
#file_purge('/home/brendan/Documents/ar_vis/.git/amp_data/AMP/client_detail')
file_purge('/home/brendan/Documents/ar_vis/.git/amp_data/RAMP/client_detail')
parse_file('/home/brendan/Documents/ar_vis/.git/amp_data/AMP/client_detail')
parse_file('/home/brendan/Documents/ar_vis/.git/amp_data/RAMP/client_detail')
print master_dict['F8:A9:D0:1A:F5:71_2016-02-22T09:50:43-05:00_TOR-A25AP03B']	
print datetime.now().time() 
print master_dict['F8:A9:D0:1A:F5:71_2016-02-20T19:11:49-05:00_T101-878BA1035A']	


##############################################################################################################################################################
#rubbish

#write to files etc
#with open(client_dict, 'a') as samp: 
#                    samp.write('\n'+mac_addr+'_'+start+'_'+apid+', '+ass_id+', '+apid+', '+start+', '+stop+', ')
#                    samp.close()
#                    with open(client_dict, 'a') as samp: 
#                         samp.write(lan_addr[x]+', ')  
#                         samp.close()



