# description:  script for checking status of each library in Siena
# author:       Giulio Centini
# version:      1.0
# license:      GNU GPL 3
# driver:       geckodriver-v0.29

from selenium import webdriver
import time    
import sys         
import itertools
import threading       

# initializing web driver
driver = webdriver.Firefox()

done = False
#loading animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

try:
	driver.get('https://www.sba.unisi.it/prenotazioni')
except Exception:
	print("Unable to reach www.sba.unisi.it - server could be offline")



