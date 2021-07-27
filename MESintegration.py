from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from tkinter import messagebox
import time
import os

def fileList(directory, *extension):
    """
    This program takes a directory path as input, then returns a list with all the files inside that folder
    that end with the extensions provided
    """
    programs = []

    for extns in extension[0]:
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.lower().endswith(extns):
                    programs.append(filename)
        else:
            print("Invalid directory path")
    return programs


def LaunchBrowser():
    # For testing
    # MESWebSite = "http://fit-wcapp-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=e0a7e9d4-02f2-4c6d-898c-8714b73c8c08&FormLink=NGDF%20Station%209050"

    driver = None
    MESWebSite = "http://FIT-WCAPP-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=E0A7E9D4-02F2-4C6D-898C-8714B73C8C08&FormLink=NGDF%20Station%201800"
    # import Chrome web driver

    listOfChromeDrivers = fileList(".\\Drivers\\", [".exe"])

    for x in listOfChromeDrivers:
        try:
            driver = webdriver.Chrome(os.path.join(".\\Drivers\\", x))
            driver.get(MESWebSite)
            return driver
        except:
            pass
    print("None of the drivers worked")
    exit(0)


"""    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(MESWebSite)
        return driver
    except:

        listOfChromeDrivers = fileList(".\\Drivers\\", [".exe"])

        for x in listOfChromeDrivers:
            try:
                driver = webdriver.Chrome(x)
                driver.get(MESWebSite)
                return driver
            except:
                pass
        print("None of the drivers worked")"""



def pressButton(driver, findBy, errorMessage, ID=None, XPath=None):
    if findBy == "ID":
        try:
            x = driver.find_element_by_id(ID)
        except:
            print(errorMessage)
        else:
            x.click()

    elif findBy == "XPath":
        try:
            x = driver.find_element_by_xpath(XPath)
        except:
            print(errorMessage)
        else:
            x.click()

    return driver


def waitForWebsite(driver, findBy, item, waitTime):
    if findBy == "ID":
        try:
            WebDriverWait(driver, waitTime).until(
                EC.presence_of_element_located((By.ID, item))
            )
        except:
            # Item wasn't found
            if item == "sampleoverlay":
                print("No sample required. Carry on")
                time.sleep(0.5)
                return driver
            else:
                print("Couldn't find item: " + item)
                messagebox.showwarning("Warning", "Couldn't find item: " + item)
            return
    time.sleep(0.5)
    if item == "sampleoverlay":
        messagebox.showwarning("Warning", "Sample required\nPlease, resolve this issue before continuing.\nAccept this message ONLY after the sample requirement has been satisfiyed")
    return driver




def fillEntryBox(driver,findBy, errorMessage, text, ID=None, XPath=None, Class=None):
    x = None
    if findBy == "ID":
        try:
            x = driver.find_element_by_id(ID)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)

    elif findBy == "XPath":
        try:
            x = driver.find_element_by_xpath(XPath)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)

    elif findBy == "Class":
        try:
            x = driver.find_element_by_class_name(Class)
        except:
            print(errorMessage)
        else:
            x.clear()
            x.send_keys(text)
    return driver, x



#--------------------------------------------------------------------------------------------------------------#
def MESLogIn(data):
    driver = LaunchBrowser()
    driver = waitForWebsite(driver, "ID", "LogInButton", 10)
    driver,_ = fillEntryBox(driver, "ID", "Couldn't find id", data.badge, ID="BadgeIDTextBox")
    driver = pressButton(driver, "ID", "Couldn't find login button", ID="LogInButton")
    driver = waitForWebsite(driver, "ID", "T7", 10)
    return driver


#--------------------------------------------------------------------------------------------------------------#
def MESWork(data, driver):
    driver = waitForWebsite(driver, "ID", "sampleoverlay", 5)
    driver,_ = fillEntryBox(driver, "ID", "Couldn't find serial entry box", data.serialNumber, ID="T7")                 # Input serial number
    driver = pressButton(driver, "XPath", "Couldn't find load button", XPath="/html/body/form/div/div[10]/div[2]/div/div/div[1]/div[1]/div[4]/div/div[2]/div[5]/div[1]/div[4]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/button")
    driver = waitForWebsite(driver, "ID", "E2frameEmbedPage", 10)

    # Switch to contentFrame iFrame
    driver.switch_to.frame("E2frameEmbedPage")
    driver = waitForWebsite(driver, "ID", "T2", 10)


    if data.unitType == "DF" or data.unitType == "IR":
        driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.puma, ID="T2")
        entryBox.send_keys(Keys.RETURN)
        time.sleep(2)


    driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.MDL1, ID="T2")
    entryBox.send_keys(Keys.RETURN)
    time.sleep(2)


    if data.unitSize == 48 or data.unitSize == 60:
        driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.MDL2, ID="T2")
        entryBox.send_keys(Keys.RETURN)
        time.sleep(2)

    driver.switch_to.default_content()
    return driver


#--------------------------------------------------------------------------------------------------------------#
def MESLogout(driver):
    driver.quit()


if __name__ == "__main__":
    pass