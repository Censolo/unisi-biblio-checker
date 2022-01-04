# description:  script for checking status of each library in Siena
# author:       Giulio Centini
# version:      1.0
# license:      GNU GPL 3
# driver:       geckodriver-v0.29

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import Select
from time import sleep
import datetime   
import sys         
import itertools
import threading       

done = False
#loading animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            sys.stdout.write('\rconnection success. Retrieving information:')
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        sleep(0.1)
    sys.stdout.write('\r')

t = threading.Thread(target=animate)
t.start()

#################################################################################
# initializing web driver (headless)
options = Options()
options.headless = True
driver = webdriver.Firefox(options=options)
#################################################################################

try:
    driver.get('http://www.sba.unisi.it/prenotazioni')
    done = True
except Exception:
    done = True
    print("\rUnable to reach www.sba.unisi.it - server could be offline")
    sys.exit()
    
today = str(datetime.date.today().day)

def Delay(x=2):
    sleep(x)    # default delay time between operations is 2, if not specified

Delay(1)
cookieButton    = driver.find_element_by_id('cn-accept-cookie')             # cookies (in conflitto con gli elementi da selezionare)
drop1           = Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/form/div[1]/div[2]/select')) # biblioteca
drop2           = Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/form/div[2]/div[2]/select'))  # servizio
drop3           = Select(driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div/div[2]/div[1]/div/div[1]/div[1]/form/div[3]/div[2]/select'))   # luogo

# accept cookies to clear webDriver layout
Delay()    # delay necessario all'esecuzione
cookieButton.click()
Delay()    # delay necessario all'esecuzione

def checkDiism():
    done_=False
    def loadingDiism():
        print('')
        for c in itertools.cycle(['|', '/', '-', '\\']):
            if done_:
                break
            sys.stdout.write('\rDIISM: loading ' + c)
            sys.stdout.flush()
            sleep(0.1)
        sys.stdout.write('\r ')
        
    t = threading.Thread(target=loadingDiism)
    t.start()
    
    drop1.select_by_value('6')  # DIISM
    Delay()
    driver.execute_script("window.scrollBy(0, -20);")
    Delay()
    drop2.select_by_value('2')  # postazione pc
    Delay()
    driver.execute_script("window.scrollBy(0, -20);")
    Delay()
    driver.execute_script("window.scrollBy(0, -20);")
    Delay()
    drop3.select_by_value('10') # sala lettura (non week-end)
    Delay()
    try:
        pickDay = driver.find_element_by_link_text(today)
        Delay(5)
        pickDay.click()
    except Exception:
        done_ = True
        print("\rDIISM: closed.     ")
        return      # interrompo ricerca in questa biblioteca
    Delay(3)
    button = driver.find_element_by_class_name('time-row')
    spanValue = button.find_element_by_tag_name('span').text
    done_= True
    print('DIISM: ', spanValue[1:-1])
    return

# def checkEcon()
# def checkLaw()
# def checkRosa()

#################################################################################
# Script Main
checkDiism()
# checkEcon()
# checkLaw()
# checkRosa()
driver.quit()
