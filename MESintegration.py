from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time


def LaunchBrowser():
    # For testing
    # MESWebSite = "http://fit-wcapp-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=e0a7e9d4-02f2-4c6d-898c-8714b73c8c08&FormLink=NGDF%20Station%209050"


    MESWebSite = "http://FIT-WCAPP-01.subzero.com:8000/EnterpriseConsole/BPMUITemplates/Default/Repository/Site/CustomLogin.aspx?ListItemId=E0A7E9D4-02F2-4C6D-898C-8714B73C8C08&FormLink=NGDF%20Station%201800"
    # import Chrome web driver
    path = ".\\Drivers\\chromedriver.exe"
    # driver = webdriver.Chrome(path)
    driver = webdriver.Chrome(ChromeDriverManager().install())


    driver.get(MESWebSite)

    return driver


# def logIntoMES(driver, user):
#     # Find Login field
#     try:
#         usr = driver.find_element_by_id("BadgeIDTextBox")
#     except:
#         print("Couldn't find id")
#     else:
#         usr.clear()
#         usr.send_keys(user)
#         # return driver
#         # fillEntryBox(driver, user)
#
#
#     # Press login button
#     try:
#         loginButton = driver.find_element_by_id("LogInButton")
#     except:
#         print("Couldn't login")
#     else:
#         loginButton.click()
#
#     return driver


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



def waitForWebsite(driver, findBy, item):

    if findBy == "ID":
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, item))
            )
        except:
            print("Couldn't find item")
            return
    time.sleep(0.5)
    return driver


# def fillEntryBox(driver, text):
#     try:
#         serialEntry = driver.find_element_by_id("T7")       # serialEntry
#     except:
#         print("Couldn't find serial entry box")
#     else:
#         serialEntry.clear()
#         serialEntry.send_keys(text)
#     return driver



def fillEntryBox(driver,findBy, errorMessage, text, ID=None, XPath=None, Class=None):
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


# def SubmitSerial(driver):
#     try:
#         loadBttn = driver.find_element_by_xpath("/html/body/form/div/div[10]/div[2]/div/div/div[1]/div[1]/div[4]/div/div[2]/div[5]/div[1]/div[4]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/button")
#     except:
#         print("Couldn't find load button")
#     else:
#         loadBttn.click()
#     return driver





#--------------------------------------------------------------------------------------------------------------#
def MESLogIn(data):
    driver = LaunchBrowser()
    driver = waitForWebsite(driver, "ID", "LogInButton")
    driver,_ = fillEntryBox(driver, "ID", "Couldn't find id", data.badge, ID="BadgeIDTextBox")
    driver = pressButton(driver, "ID", "Couldn't find login button", ID="LogInButton")
    driver = waitForWebsite(driver, "ID", "T7")
    return driver

def MESWork(data, driver):
    driver,_ = fillEntryBox(driver, "ID", "Couldn't find serial entry box", data.serialNumber, ID="T7")                 # Input serial number
    driver = pressButton(driver, "XPath", "Couldn't find load button", XPath="/html/body/form/div/div[10]/div[2]/div/div/div[1]/div[1]/div[4]/div/div[2]/div[5]/div[1]/div[4]/div/div/div[1]/div[1]/div[4]/div/div[2]/div/div[1]/div[2]/button")
    driver = waitForWebsite(driver, "ID", "E2frameEmbedPage")

    # Switch to contentFrame iFrame
    driver.switch_to.frame("E2frameEmbedPage")
    driver = waitForWebsite(driver, "ID", "T2")
    driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.puma, ID="T2")
    entryBox.send_keys(Keys.RETURN)
    time.sleep(10)
    driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.MDL1, ID="T2")
    entryBox.send_keys(Keys.RETURN)
    time.sleep(10)
    if data.unitSize == 48 or data.unitSize == 60:
        driver, entryBox = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.MDL2, ID="T2")
        entryBox.send_keys(Keys.RETURN)
        time.sleep(10)
    # driver = fillEntryBox(driver, "XPath", "Couldn't find vendor barcode entry box, Xpath", data.puma, XPath="/html/body/form/div/div[7]/div[2]/div/div/div[1]/div/div[4]/div/div[2]/div[2]/div[1]/div[2]/input")
    # time.sleep(1)
    # try:
    #     driver = fillEntryBox(driver, "ID", "Couldn't find vendor barcode entry box, ID", data.puma, ID="T2")
    # except:
    #     pass
    # try:
    #     driver = fillEntryBox(driver, "Class", "Couldn't find vendor barcode entry box", data.puma, ID="T2")
    # except:
    #     pass
    # driver = fillEntryBox(driver, "T2", "Couldn't find vendor barcode entry box", data.MDL1)
    # time.sleep(1)
    driver.switch_to.default_content()
    return driver

def MESLogout(driver):
    driver.quit()


if __name__ == "__main__":
    pass