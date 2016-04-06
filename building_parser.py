import os 
import xml.etree.ElementTree
path='/home/salman/Documents/amp_project/client_ap_assoc/amp_data/AMP'

serial_num_list=[]
def xml_parser(path):
	for filename in os.listdir(path):
		if 'visualrf_building' in filename:
		    fullname=os.path.join(path,filename)
		    e = xml.etree.ElementTree.parse(fullname).getroot()
		    if e!=None:	
                       for atype in e.findall('building'):
         		   ap_name=atype.get('name')
                           ap_latitude=atype.get('latitude')
                           ap_longitude=atype.get('longitude')
                           ap_address=atype.find('address').text
                           height=atype.get('floor_height_ft')

                           """
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
                           """
                           print(ap_name,ap_latitude,ap_longitude,ap_address,height)



xml_parser(path)        			                                                                                                                                          
