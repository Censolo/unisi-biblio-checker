# description:  script for checking status of each library in Siena
# author:       Giulio Centini
# version:      1.0
# license:      GNU GPL 3

import requests
from requests import get
import json
import datetime   
from time import sleep
import sys         
import itertools
import threading    

ver = "1.0"

print("UNISI libraries status checker", "version", ver)

done = False
#loading animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write('\r            ')

t = threading.Thread(target=animate)
t.start()

#################################################################################

def GetCount(worker, service, location):               # LUOGO ("sala lettura"), SERVIZIO ("postaz. studio"), BIBLIOTECA (es. "Sala Rosa")
    date    = datetime.date.today().isoformat()        # already string "YYYY-MM-DD"
    url     = "http://www.sba.unisi.it/wp-admin/admin-ajax.php?worker=" + str(worker) + "&service=" + str(service) + "&location=" + str(location) + "&action=ea_date_selected&date=" + date
    r   = requests.get(url = url)
    try:
        r.raise_for_status()
    except requests.exceptions.HTTPError:
        print("\r Unable to connect to sba.unisi.it", "program terminated.", sep='\n')
        sys.exit()
        
    data     = json.loads(r.text)    # json format
    try:
        data = data[0]               # removed [ ] from json -> now a dictionary
    except Exception:
        return "closed."
    
    return "available spots = " + str(data['count'])          #returning count
#################################################################################
#main execution

diismCount  = GetCount(10, 2, 6)
EconCount   = GetCount(2, 2, 2)
LawCount    = GetCount(1, 2, 1)
RosaCount   = GetCount(8, 2, 8)

# TO-DO: exception handling!

done = True

print("\rDIISM:     ", diismCount)
print("ECONOMICS: ", EconCount)
print("LAW:       ", LawCount)
print("SALA ROSA: ", RosaCount)
