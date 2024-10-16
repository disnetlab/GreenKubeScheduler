from __future__ import division 
import xml.etree.ElementTree as etree 

# Import library for handling XML import requests 

# Import library to implement HTTP requests
import codecs  
time_max = 300
ClusterControllerIP = 'http://130.194.136.23:80'

# Prepare the links for the cluster controller's login page and device overview page after a session is established
loginLink = ClusterControllerIP + '/culture/login'
logoutLink = ClusterControllerIP + '/culture/logout'
deviceLink = ClusterControllerIP + '/culture/DeviceOverview.dml' 

# Prepare the data payload needed to POST to the cluster controller to establish an authentication session
payload = {     "Language": "LangEN", # Specify language for the session - note that this field MUST be included to log in!     
                "Userlevels": "User",
                #"Userlevels": "Installer", # Username to log into the cluster controller
                "password": "6x?TaKw_8v"  # Password to log into the cluster controller     
                # "password": "0000"
                }
failure_val = -1
global_val = {
        "5100463701": {"value": failure_val, "unit": "W", "tag": "GPA_SB40", "name": "Power Absorbed"},
        "5100463601": {"value": failure_val, "unit": "W", "tag": "GSP_SB40", "name": "Supplied Power"},
        "5100463707": {"value": failure_val, "unit": "W", "tag": "GPA_SBS", "name": "Power Absorbed"},
        "5100463607": {"value": failure_val, "unit": "W", "tag": "GSP_SBS", "name": "Supplied Power"},
        "5100295A07": {"value": failure_val, "unit": "%", "tag": "BSC", "name": "Battery State of Charge"},
        "5100263F01": {"value": failure_val, "unit": "W", "tag": "SolarP", "name": "Solar Power"}
        }
inverters_info = [{"id": "342:1992031615:i",
                    "attrsAC": ["5100463701",
                                "5100463601",
                                "5100263F01"]},
                    {
                        "id": "346:1901008064:i",
                        "attrsAC": ["5100463607",
                                    "5100463707"],
                        "attrsBA": ["5100295A07",
                            ]
                        }]

def main_handler(name):     
    # Establish a connection to the cluster controller and POST the login payload to create a session
    s = requests.session()
    s.post(loginLink, data=payload)
    for dev in inverters_info:
        id = dev.get("id")         
    # Grab the XML responses for the Instantaeous Values tab of the AC and DC sides of the inverter, based on its serial number
    dcLink = ClusterControllerIP + '/culture/DeviceOverview.dml?__newTab=&__deviceKey=' + id \
            + '&__selected=hp.processDataOverview__&__selectedCategory=5#5'
    acLink = ClusterControllerIP + '/culture/DeviceOverview.dml?__newTab=&__deviceKey=' + id + \
            '&__selected=hp.processDataOverview__&__selectedCategory=6#6'
    batteryLink = ClusterControllerIP + '/culture/DeviceOverview.dml?__newTab=&__deviceKey=' + id + \
            '&__selected=hp.processDataOverview__&__selectedCategory=9#9'

def get_values(root, attrs):
    for at in attrs:
        global_val[at]["value"] = -1
        for element in root.iter(tag="XmlItem"):
            addr = element.attrib.get("address")
            if addr and (addr in attrs):
                for val in element.iter(tag='Value'):
                    if val.text:
                        global_val[addr]["value"] = val.text
                        break
                    if dev.get("attrsBA"):
                        baResponse = s.get(batteryLink)
                        content = baResponse.text.encode('ascii', 'ignore')
                        temptree = etree.fromstring(content)
                        tree = etree.ElementTree(temptree)
                        root = tree.getroot()
                        attrs = dev.get("attrsBA")
                        get_values(root, attrs)
                        if dev.get("attrsAC"):
                            acResponse = s.get(acLink)
                            content = acResponse.text.encode('ascii', 'ignore')
                            temptree = etree.fromstring(content)
                            tree = etree.ElementTree(temptree)
                            root = tree.getroot()
                            attrs = dev.get("attrsAC")
                            get_values(root, attrs)
                            if dev.get("attrsDC"):
                                dcResponse = s.get(dcLink)
                                content = dcResponse.text.encode('ascii', 'ignore')
                                temptree = etree.fromstring(content)
                                tree = etree.ElementTree(temptree)
                                root = tree.getroot()
                                attrs = dev.get("attrsDC")
                                get_values(root, attrs)
                                s.post(logoutLink, data=payload)     
                                # print(global_val)
                                return 0

def metric_handler(name):
    code = name
    global global_val
    val = global_val[code]["value"]
    try:
        val = float(val)
        return val
    except ValueError:
        return 0

def metric_init(params):
    global descriptors, global_val
    descriptors = [{
        'name': "SMA_Query",
        'call_back': main_handler,
        'time_max': time_max,
        'value_type': 'float',
        'units': "None",
        'slope': 'both',
        'format': '%f',
        'description': "A dummy metric for SMA connection and Query",
        'groups': "energy"
        }]
    for k in global_val.keys():
        descriptors.extend([
            {
                'name': k,
                'call_back': metric_handler,
                'time_max': time_max,
                'value_type': 'float',
                'units': global_val[k]["unit"],
                'slope': 'both',
                'format': '%f',
                'description': global_val[k]["name"],
                'groups': "energy"
                }
            ])
        return descriptors

def metric_cleanup():
    '''Clean up the metric module.
    This function must exist and explicitly named 'metric_cleanup' in your module.It will be called only once when
    mond is shutting
    down.
    Any module clean up code can be executed here and the function must not return a value.
    '''
    pass   
# This code is for debugging and unit testing
if __name__ == '__main__':
    metric_init({})     
    #print(descriptors)
    for i in range(1):
        for d in descriptors:
            v = d['call_back'](d['name'])
            print('value for %s is %u' % (d['name'], v))

