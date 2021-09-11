# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.keys import Keys
# from tkinter import messagebox
# import time
# import os
# from selenium.webdriver.chrome.options import Options
# # from selenium
# import selenium.common.exceptions as sex
#
# webdriver.ChromeOptions().add_argument("--ignore-certificate-errors")
# chrome_options = Options()
# chrome_options.add_experimental_option("detach", True)
#
# def LaunchBrowser():
#
#     MESWebSite = "https://www.google.com"
#     # import Chrome web driver
#
#     driver = webdriver.Chrome(os.path.join(".\\Drivers\\chromedriver V92.exe"))
#     driver.get(MESWebSite)
#     return driver
#
# # import httplib
# import socket
#
# from selenium.webdriver.remote.command import Command
#
# def get_status(driver):
#     try:
#         driver.execute(Command.STATUS)
#         print("Alive")
#     except:
#         print("Dead")
#
# if __name__ == "__main__":
#     driver = LaunchBrowser()
#     """    while True:
#         get_status(driver)
#         time.sleep(1)"""
#
#     """    DISCONNECTED_MSG = 'Unable to evaluate script: disconnected: not connected to DevTools\n'
#
#     while True:
#         driverMSG = driver.get_log('driver')[0]['message']
#         if driverMSG == DISCONNECTED_MSG:
#             print('Browser window closed by user')
#         else:
#             print("all gucci")
#         time.sleep(1)"""
#
#
#
#     """while True:
#         try:
#             x = driver.find_element_by_class_name("ddlsv-cta_")
#             print("Found")
#         except:
#             print("not found")
#         time.sleep(1)"""
#
#     while True:
#         try:
#             driver.switch_to.default_content()
#             print("All gucci")
#         except Exception as e:
#             print(str(e))
#             # print(sex.WebDriverException.msg)
#             # print(WebDriver.webDriverException)
#
#             if str(e).startswith("Message: chrome not reachable") == True:
#                 # if e.startswith("Message: chrome not reachable") == True:
#                 print("Can't reach")
#         else:
#             time.sleep(1)
#


# import win32gui, win32con
#
# # hwnd = win32gui.FindWindow("Notepad", None)
# hwnd = win32gui.FindWindow("Standard Test Interface", None)
# win32gui.SetForegroundWindow(hwnd)
# # hwnd = win32gui.GetForegroundWindow()
# win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)

import ctypes

user32 = ctypes.WinDLL('user32')
hwnd = user32.FindWindow("Standard Test Interface", None)
SW_MAXIMISE = 3

hWnd = user32.GetForegroundWindow()

user32.ShowWindow(hWnd, SW_MAXIMISE)