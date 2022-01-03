# description:  script for checking status of each library in Siena
# author:       Giulio Centini
# version:      1.0
# license:      GNU GPL 3
# driver:       geckodriver-v0.29

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 
import datetime   
import sys         
import itertools
import threading       

done = False
#loading animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\r')

t = threading.Thread(target=animate)
t.start()

# initializing web driver
# IMPLEMENT HEADLESS WEBDRIVER
driver = webdriver.Firefox()

try:
    driver.get('http://www.sba.unisi.it/prenotazioni')
    done = True
except Exception:
    done = True
    print("Unable to reach www.sba.unisi.it - server could be offline")
    sys.exit()
    
today = str(datetime.date.today().day)

drop1 = Select(driver.find_element_by_name('location')) # biblioteca
drop2 = Select(driver.find_element_by_name('service'))  # servizio
drop3 = Select(driver.find_element_by_name('worker'))   # luogo

def checkDiism():
    drop1.select_by_value('6')  # DIISM
    drop2.select_by_value('2')  # postazione pc
    drop3.select_by_value('41') # sala lettura (non week-end)
    try:
        pickDay = driver.find_element_by_link_text(today)
        pickDay.click()
    except Exception:
        print("\n closed.")
        return      # interrompo ricerca in questa biblioteca
    button = driver.find_element_by_class_name('time-row')
    spanValue = button.find_element_by_tag_name('span').text
    print(spanValue[1:-1])
    return

