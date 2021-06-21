from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time


def LaunchBrowser():
    MESWebSite = "http://fit-wcapp-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=e0a7e9d4-02f2-4c6d-898c-8714b73c8c08&FormLink=NGDF%20Station%209050"


    # import Chrome web driver
    path = ".\\Drivers\\chromedriver.exe"
    # driver = webdriver.Chrome(path)
    driver = webdriver.Chrome(ChromeDriverManager().install())


    driver.get(MESWebSite)

    return driver


def logIntoMES(driver, user):
    # Find Login field
    try:
        usr = driver.find_element_by_id("BadgeIDTextBox")
    except:
        print("Couldn't find id")
    else:
        usr.clear()
        usr.send_keys(user)
        # return driver
        # fillEntryBox(driver, user)


    # Press login button
    try:
        loginButton = driver.find_element_by_id("LogInButton")
    except:
        print("Couldn't login")
    else:
        loginButton.click()

    return driver



def waitForWebsite(driver, findBy, item):

    if findBy == "ID":
        try:
            driver = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, item))
            )
        except:
            print("Couldn't find item")
            return
    time.sleep(0.5)
    return driver


def fillEntryBox(driver, text):
    try:
        serialEntry = driver.find_element_by_id("T7")       # serialEntry
    except:
        print("Couldn't find serial entry box")
    else:
        serialEntry.clear()
        serialEntry.send_keys(text)
    return driver

def SubmitSerial(driver):
    try:
        loadBttn = driver.find_element_by_xpath("/html/body/form/div/div[10]/div[2]/div/div/div[1]/div[1]/div[4]/div/div[2]/div[5]/div[1]/div[4]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/button")
    except:
        print("Couldn't find load button")
    else:
        loadBttn.click()
    return driver





#--------------------------------------------------------------------------------------------------------------#
def MESLogIn(data):
    driver = LaunchBrowser()
    # driver = waitForWebsite(driver, "ID", "LogInButton")
    driver = logIntoMES(driver, data.badge)
    driver = waitForWebsite(driver, "ID", "T7")
    return driver

def MESWork(data, driver):
    driver = fillEntryBox(driver, data.serialNumber)                 # Input serial number
    driver = SubmitSerial(driver)
    return driver

def MESLogout(driver):
    driver.quit()


if __name__ == "__main__":
    pass