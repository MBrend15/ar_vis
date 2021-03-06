import os 
import xml.etree.ElementTree
path='/home/salman/Documents/amp_project/client_ap_assoc/amp_data/AMP'

serial_num_list=[]
def xml_parser(path):
	for filename in os.listdir(path):
		if 'ap_list' in filename:
		    fullname=os.path.join(path,filename)
		    e = xml.etree.ElementTree.parse(fullname).getroot()
		    if e!=None:	
                       for atype in e.findall('ap'):
         		   ap_id=atype.get('id')
                           device_category=atype.find('device_category').text 
                           ##Check if device is of type other category, then serial number does not exist
                           if atype.find('serial_number') != None:
                              ser_num=atype.find('serial_number').text
                           else:
                              ser_num=0

                           lan_mac=atype.find('lan_mac').text
                           ap_name=atype.find('name').text
                           ##Check if device is access_point only then controller_id exists like switch,other. sometimes data is missing"
                           if atype.find('controller_id') != None: 
                              controller_id=atype.find('controller_id').text
                           else:
                              controller_id=0

                           print(lan_mac,ap_name,device_category,ser_num,ap_id,controller_id)
                           #Adding support for the radio mac's might be needed in the future
                           print "These are the radio mac's" 
                           for radio_mac in atype.findall('radio'):
                               radio_index=radio_mac.get('index')                             
                               radio_mac=radio_mac.find('radio_mac').text               
                               print (radio_index,radio_mac)                               

xml_parser(path)        			                                                                                                                                          
