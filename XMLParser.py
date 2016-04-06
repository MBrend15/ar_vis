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
import xlsxwriter
##############################################################################################################################################################
#deprecated functions

#function that searches for enhanced data within files in a given directory. May 
#have to be modified for linux. I started an update which i have since stopped to search through files
#and compare macs and file size, save the code in case I need it, but I don't need it presently
def searchDir(FileName): 
    x = 0
    size = 0
    name2 = ' ' 
    #search all contents of provided directory
    for name in os.listdir(FileName):

        #parse the file to determine mac
        tree = ET.parse(os.path.join(FileName, name))
        root = tree.getroot()
        curr_mac = root.getchildren('mac') 
        #determine file size as a more efficent way to determin if there is actual info in the
        #amp/ramp data files
        #file_size = os.path.getsize(os.path.join(FileName,name))
        #if the mac address is the same
        if  root.getchildren('mac') == curr_mac:    
            #determine file size
            file_info = os.stat(os.path.join(FileName,name))
            file_size = file_info.st_size  
            if x == 0: 
                size  = os.path.getsize(os.path.join(FileName,name))
                name2 = name
                x = x+1
            elif x > 0: 
                size2 = os.path.getsize(os.path.join(FileName,name))
                if size2 > size: 
                    name2 = name
                else : 
                    name2 = name2

    #parse file
    tree = ET.parse(os.path.join(FileName, name))

    #extract required data, by searching through successive children of the child of the root
    #for child in tree._root: 



    #if file_size > 249:         
    #   #initially parse file
    #   tree = ET.parse(os.path.join(FileName,name))
    #   #root = tree.getroot()
    #   print('*'+FileName+name+'*')
    #        #for the child in the root
    #        for child in tree._root:
    #            print('--------')
    #            print(child.get('mac'))
    #            print('--------')
    #            #find all instances of an association and pull client mac, assoc id, conn and disconn times
    #            for Assoc in child.findall('association'):
    #                print(Assoc.get('id'),', ', Assoc[0].text,', ', Assoc[2].text,', ', Assoc[3].text)
                                      
    return 0  

#create function to amp client data based on size and ssid
def org_amp_files(FileName): 
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
                    #for ssids in an association, determine if eduroam or connect_vt, then move fiel to the appropriate folder, use a counter in the event that
                    #the file contains both connect_vt and eduroam
                    for Assoc in child.findall('association'):
                        for ssid in Assoc.findall('ssid'):
                            ssid_txt = ssid.text
                            if ssid_txt == 'eduroam' and x == 0: 
                                file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\org_client\\amp_eduroam', name)
                                os.rename(file_name, file_name2) 
                                x = 1
                            elif ssid_txt == 'CONNECTtoVT-Wireless' and y == 0: 
                                file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\org_client\\amp_connect_vt\\', name)
                                os.rename(file_name, file_name2)                                
                                y = 1
                            elif (ssid_txt == 'CONNECTtoVT-Wireless' and x == 1) or (ssid_txt == 'eduroam' and y == 1): 
                                file_name2 = file_name2 = os.path.join('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\org_client\\amp_both\\', name)
                                os.rename(file_name, file_name2)
                                break

    return 0;

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
                    #for ssids in an association, determine if eduroam or connect_vt, then move fiel to the appropriate folder, use a counter in the event that
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
            lan_addr = []
            ass_prop = []
            #find all instances of an association and pull client mac, assoc id, conn and disconn times
            for Assoc in child.findall('association'):
                ass_prop.clear()
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

                #write to files etc
                #with open('test.txt', 'a') as samp: 
                #    samp.write('\n'+'-----'+'\n'+file_nm+'\n'+'-----'+'\n'+mac_addr+'_'+start+'_'+apid+', '+ass_id+', '+apid+', '+start+', '+stop+', ')
                #    samp.close()

                #compile client_key to enter into dictionary. composed of mac, ap, and association start time
                client_key = mac_addr+'_'+start+'_'+apid
            
                    #iterate to discover and then write all lan addresses
                for LAN in Assoc.findall('lan_elements'):
                    lan_addr.clear()
                    for lan_ele in LAN.findall('lan'):
                        lan_addr.append(lan_ele.get('ip_address'))
                        #with open('test.txt', 'a') as samp: 
                        #   samp.write(lan_addr[x]+', ')  
                        #   samp.close()
                           #x= x+1                    
                
                    #add lan_elemnets to the back end of the collection
                    ass_prop.append(lan_addr)

                #add collection to dictionary with key as concatenation of apid_mac_start
                global master_dict 
                master_dict = add2Dict(master_dict, client_key, ass_prop)                                                                        
    
    #return a copy of the master dictionary                        
    return master_dict;            

def add2Dict(sampDic, term, info_collec):     
    #is term already in dictionary? 
    result1 = term in sampDic    
    #if not add it with count of 1, if so append the count
    if result1 == False:
        sampDic[term] = info_collec
    #else: 
    #    print('Did not add')
    return sampDic

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
#main begins here
master_dict = {}
#print(datetime.time(datetime.now()))
#file_purge('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail')
#file_purge('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\client_detail')
#master_dict = parse_file('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\\AMP\org_client\\amp_connect_vt\\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-05-01-38.xml')
#master_dict = parse_file('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail')
#master_dict = parse_file('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\client_detail')

#for key in master_dict:
#    with open('test.txt', 'a') as samp: 
#         samp.write(key+'\n')
#         samp.close()
         
#    print(master_dict[key])

#print(datetime.time(datetime.now()))

#print(master_dict['78:D6:F0:75:89:B2_2016-02-23T09:30:43-05:00_TOR-A25AP03B'])

parse_visrf('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\AMP_visualrf_access_point_2016-03-05-01-41.xml')


##############################################################################################################################################################
#rubbish







#searchDir('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail')
#org_amp_files('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail')
#org_ramp_files('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\RAMP\client_detail')

#all code below used for experimentation/debugging. Want to keep it just in case

#tree = ET.parse('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml')
#root = tree.getroot()
#for child in root:
#    x = 0 
#    y = 0
#    for Assoc in child.findall('association'):
#        for ssid in Assoc.findall('ssid'):
#            ssid_txt = ssid.text
#            if ssid_txt == 'eduroam' and x == 0: 
#                os.rename('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml', 'D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\\amp_eduroam\\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml')
#                x = 1
#            elif ssid_txt == 'CONNECTtoVT-Wireless' and y == 0: 
#                os.rename('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml', 'D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\\amp_connect_vt\\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml')
#                y = 1
#            elif (ssid_txt == 'CONNECTtoVT-Wireless' and x == 1) or (ssid_txt == 'eduroam' and y == 1): 
#                os.rename('D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml', 'D:\Documents\ECE Project_Thesis\\amp_data\\amp_data\AMP\client_detail\\amp_both\\AMP_78-D6-F0-75-89-B2_client_detail_2016-03-06-06-11.xml')
#                break

#write to files etc
#with open(client_dict, 'a') as samp: 
#                    samp.write('\n'+mac_addr+'_'+start+'_'+apid+', '+ass_id+', '+apid+', '+start+', '+stop+', ')
#                    samp.close()
#                    with open(client_dict, 'a') as samp: 
#                         samp.write(lan_addr[x]+', ')  
#                         samp.close()



