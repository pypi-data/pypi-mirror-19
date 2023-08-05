''' 
Version 1 22nd December 2016
Pete White
This is a Python module to simplify operations via F5 iControl REST interface
Installation - copy to your python library directory eg /lib/python2.7
Example:
#!/usr/bin/env python
from iCR import iCR
# Connect to BIG-IP
bigip = iCR("172.24.9.132","admin","admin")
#Retrieve a list of Virtual Servers
virts = bigip.get("ltm/virtual")
for vs in virts['items']:
   print vs['name']


'''
###############################################################################
import json
import requests
# Disable warnings about insecure
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class iCR:
   
   def __init__(self,hostname,username,password,**kwargs):
     # Setup variables
     self.icr_session = ""
     self.raw = ""
     self.code = ""
     self.folder = ""
     self.icr_link = ""
     self.headers = ""
     self.timeout = 30
     self.port = 443
     self.debug = False
     
     # manage keyword arguments
     self.timeout = kwargs.pop('timeout', 30)
     self.port = kwargs.pop('port', 443)
     self.icontrol_version = kwargs.pop('icontrol_version', '')
     self.folder = kwargs.pop('folder', '')
     self.token = kwargs.pop('token', False)
     self.debug = kwargs.pop('debug', False)
     # Create HTTP session
     icr_session = requests.session()
     # not going to validate the HTTPS certifcation of the iControl REST service
     icr_session.verify = False
     # we'll use JSON in our request body and expect it back in the responses
     # Use iWorkflow token if presented
     if self.token:
        icr_session.headers.update({'X-F5-Auth-Token': self.token, 'Content-Type': 'application/json'})
     else:
        icr_session.auth = (username, password)
        icr_session.headers.update({'Content-Type': 'application/json'})
     self.icr_session = icr_session
     self.icr_url = 'https://%s/mgmt/tm/' % hostname
   
   # Retrieve objects - use GET method
   # To Do - partitions - deal with select etc and add documentation
   def get(self,url,**kwargs):
     # Deal with keywords
     select = kwargs.pop('select', '')
     top = kwargs.pop('top', '')
     skip = kwargs.pop('skip', '')
     # Deal with URI and select, top, etc
     if "?" not in url:
       url_delimeter = "?"
     else:
       url_delimeter = "&"
     
     if select:
       url = url + url_delimeter + "$select=" + select
       url_delimeter = "&"
     if top:
       url = url + url_delimeter + "$top=" + top
       url_delimeter = "&"
     if skip:
       url = url + url_delimeter + "$skip=" + skip
       url_delimeter = "&"
     if self.folder:
         url = url + url_delimeter +"$filter=partition+eq+" + self.folder
         url_delimeter = "&"      
     if self.icontrol_version:
         url = url + url_delimeter + 'ver=' + self.icontrol_version
         url_delimeter = "&"
     
     request_url = self.icr_url + url
     if self.debug:
	    print "DEBUG: Get URL:" + request_url
     try:
        response = self.icr_session.get(request_url,timeout = self.timeout)
     except Exception, e:
        self.error = e
        if self.debug:
           print "DEBUG: Get requests error:" + str(self.error)
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
	    print "DEBUG: Get Response Status Code:" + str(self.code)
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False
   
   # Create objects - use POST and send data
   def create(self,url,data):
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     json_data = json.dumps(data) 
     if self.debug:
        print "DEBUG: Create URL:" + request_url
        print "DEBUG: Create Data:" + str(data)
        print "DEBUG: Create JSON Data:" + str(json_data)
     try:
        response = self.icr_session.post(request_url,json_data,timeout = self.timeout)
     except Exception, e:
        self.error = e
        if self.debug:
           print "DEBUG: Create requests error:" + str(self.error)
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
	    print "DEBUG: Create Response Status Code:" + str(self.code)
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False

   # Modify existing objects - use PUT and send data
   def modify(self,url,data,**kwargs):
     # Deal with keywords
     patch = kwargs.pop('patch', '')
     
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     if self.debug:
        print "DEBUG: Modify URL:" + request_url
     try:
        if patch:
           response = self.icr_session.patch(request_url,data,timeout = self.timeout)
        else:
           response = self.icr_session.put(request_url,data,timeout = self.timeout)
     except Exception, e:
        self.error = e
        if self.debug:
           print "DEBUG: Modify requests error:" + str(self.error)
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
	    print "DEBUG: Modify Response Status Code:" + str(self.code)
     self.headers = response.headers
     if response.status_code < 400:
       return json.loads(response.text)
     else:
       return False
	   
   # Delete existing objects - use PUT and send data
   def delete(self,url):
     if self.icontrol_version:
       request_url = self.icr_url + url + '?ver=' + self.icontrol_version
     else:
       request_url = self.icr_url + url
     if self.debug:
        print "DEBUG: Delete URL:" + request_url
     try:
        response = self.icr_session.delete(request_url,timeout = self.timeout)
     except Exception, e:
        self.error = e
        if self.debug:
           print "DEBUG: Delete requests error:" + str(self.error)
        return False
     self.raw = response.text
     self.code = response.status_code
     if self.debug:
	    print "DEBUG: Delete Response Status Code:" + str(self.code)
     self.headers = response.headers
     if response.status_code < 400:
       return True
     else:
       return False