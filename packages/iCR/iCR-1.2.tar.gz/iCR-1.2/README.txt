This is a python module to simplify using iControl REST.

Install using pip:

pip install iCR
As simple as:

#!/usr/bin/env python
from iCR import iCR
bigip = iCR("172.24.9.132","admin","admin")
virtuals = bigip.get("ltm/virtual")
for vs in virtuals['items']:
  print vs['name']
This prints out a list of Virtual Servers.

Supported methods:

init(hostname,username,password,[timeout,port,icontrol_version,folder,token,debug])
get(url,[select,top,skip])
create(url,data)
modify(url,data,[patch=True])
delete(url)
Module Variables:

icr_session - the link to the requests session
raw - the raw returned JSON
code - the returned HTTP Status Code eg 200
error - in the case of error, the exception error string
headers - the response headers
Features: iControl version, debug mode, folders, iWorkflow tokens, select, top, skip