from lxml import etree
par=etree.parse("/home/salman/Documents/amp_data/AMP/AMP_ap_list_2016-03-05-01-40.xml")	
print par.getroot()																					