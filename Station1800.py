import os
import subprocess
import clipboard
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
import time


# TODO
# bring Gui to forefront after logging in and after macro

# Define classes



class _time:
    def __init__(self, clockIn, lastScan):
        self.clockIn = clockIn
        self.lastScan = lastScan

class data:
    def __init__(self, badge, serialNumber, puma, MDL1, MDL2, unitSize):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2
        self.unitSize = unitSize


class inputField:
    def __init__(self, Badge, Serial, Puma, MDL1, MDL2):
        self.Badge = Badge
        self.Serial = Serial
        self.Puma = Puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2

class driver:
    def __init__(self, driver):
        self.driver = driver


# Define functions

# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#
#     return os.path.join(base_path, relative_path)

def resource_path(relative):
    return os.path.join(os.environ.get("_MEIPASS2", os.path.abspath(".")), relative)

def raise_frame(frame, inputField):
    """
    Moves frame to the top of the GUI, sets focus on the indicated input field
    """
    frame.tkraise()
    inputField.focus_set()


def displayError(message):
    """
    Displays an Error box with the desired message in it
    """
    messagebox.showerror("Error", message)


def login(nextFrame, selfInputField, nextInputField):
    """
    Saves the badge number to data.badge and displays the next frame of the GUI, setting the focus on the next input
    field (serial number input field).

    If a wrong badge number is input it displays an error message and clears the badge input field
    """
    data.badge = selfInputField.get()
    if data.badge.isdigit() and len(data.badge) <= 6 and len(data.badge) >= 4:
        driver.driver = MESLogIn(data)                                                                                # MES Integration
        workingTime.clockIn = time.perf_counter()
        ClearField(inputField.Serial)
        ClearField(inputField.Puma)
        ClearField(inputField.MDL1)
        ClearField(inputField.MDL2)

        raise_frame(nextFrame, nextInputField)
        BringGUI2Front(nextFrame, nextInputField)


    else:
        displayError("Invalid ID")
        # Clear entry field
        ClearField(selfInputField)


def Logout(nextFrame):
    MESLogout(driver.driver)
    ClearField(inputField.Badge)
    raise_frame(nextFrame, inputField.Badge)


def BringGUI2Front(frame, nextInputField):
    frame.focus_force()
    nextInputField.focus_set()


def ClearField(inputField):
    """
    Clears the input field provided
    """
    inputField.delete(0,END)


def clearUnitEntryFields():
    """
    Clears every input field in the second frame (serial number, puma, MDL1, MDL2)
    """
    for entry in (inputField.Serial, inputField.Puma, inputField.MDL1, inputField.MDL2):
        ClearField(entry)
    data.serialNumber = ""
    data.puma = ""
    data.MDL1 = ""
    data.MDL2 = ""


def GoToNextEntry(selfEntry, attribute, nextEntry=None, MDL2_entry=None):
    """
    This function switches the focus from one entry box to the next

    ex. once the serial number is typed in by the user with the help of a scanner and the enter key is pressed (scanner
    does this automatically) we want to switch the focus to the next entry field automatically (in this case the puma entry field)
    This helps save time so the operator doesn't have to click anything on the screen.

    We'll get the length of the unit from the serial number. This parameter will tell us if the input field MDL2 is needed or not.
    If it's not needed the MDL2 input field will remain disabled. Otherwise it will be enabled (set to 'normal').
    Note: only 48" and 60" units require a second MDL.

    Once everything is scanned in the macro will execute automatically.

    EXECUTION

    The serial number is scanned in. This value is stored in data.serialNumber. The unit size is obtained based on this
    value and stored in data.unitSize. If a 48" or 60" unit is scanned the MDL2 entry field becomes enabled. Go to next
    entry field (Puma).

    Scan the Puma. This value is stored in data.puma. Go to next entry field (MDL1)

    Scan MDL1. This value is stored in data.MDL1.
        If a 30" or 36" unit is scanned the macro will execute once the MDL1 entry field is filled and enter is pressed
        If a 48" or 60" unit is scanned, go to next entry field (MDL2)

            Scan MDL2. This value is stored in data.MDL2. Macro will execute once the MDL2 entry field is filled and enter is pressed

    PARAMETERS

    :param selfEntry: the input field that you're currently typing in
    :param attribute: the attribute of the data class where you want to store what you just typed in the input field
    :param nextEntry: the input field you want to switch focus to. If this parameter is not specified it will take the value None
    :param MDL2_entry: the last input field (MDL2). If this parameter is not specified it will take the value None
    :return: No returns
    """
    # data.attribute = selfEntry.get()                            # Save serial number
    if attribute == "serialNumber":
        data.serialNumber = selfEntry.get()

        serialNum = data.serialNumber
        unitSize = ""

        if "$" in serialNum:
            unitSize = serialNum.split("$")[3]  #slicing through serial number to just the model code "DF48...."
            if unitSize.startswith("DF") or unitSize.startswith("IR"):
                try:
                    unitSize = int(unitSize[2:4])
                except:
                    displayError("Problems finding the unit size in serial")
                    ClearField(selfEntry)                       # Clear entry field
            else:
                displayError("Problems finding the unit type in serial")
                ClearField(selfEntry)                           # Clear entry field
        else:
            displayError("Serial string could not be parsed")
            ClearField(selfEntry)                               # Clear entry field

        data.unitSize = unitSize                                # Save unit size

        if data.unitSize == 48 or data.unitSize == 60:      # Change the state of MDL2 entry field to normal if unit is 48" or 60"
            MDL2_entry['state'] = "normal"

    elif attribute == "puma":
        data.puma = selfEntry.get()

    elif attribute == "MDL1":
        data.MDL1 = selfEntry.get()

    elif attribute == "MDL2":
        data.MDL2 = selfEntry.get()

    else:
        print("Error\nBad entry field")

    if nextEntry != None:                                       # If a next entry field is provided, switch focus to that field
        nextEntry.focus_set()
    else:                                                       # If a next entry field is not provided, it's because we reached the final entry field
        doMacro()                                               # execute macro

    if attribute == "MDL1":                                     # If we're scanning MDL1, go to next entry field (MDL2) if unit requires it.
        if (data.unitSize == 48 or data.unitSize == 60):
            nextEntry.focus_set()
        else:                                                   # Otherwise execute macro
            doMacro()


def submit():
    data.serialNumber = inputField.Serial.get()
    data.puma = inputField.Puma.get()
    data.MDL1 = inputField.MDL1.get()
    data.MDL2 = inputField.MDL2.get()
    doMacro()



def doMacro():
    print("Saving Values")
    print(data.serialNumber)
    sotredValues_Path = os.path.join(HiddenFolder, "Stored values.txt")
    with open(sotredValues_Path, 'w') as outfile:
        outfile.write(str(data.badge) + "\n")
        outfile.write(data.serialNumber + "\n")
        outfile.write(str(data.unitSize) + "\n")
        outfile.write(data.puma + "\n")
        outfile.write(data.MDL1 + "\n")
        outfile.write(data.MDL2 + "\n")


    # Put path to the txt file in ram memory
    clipboard.copy(sotredValues_Path)
    # clipboard.copy(".\\Stored values.txt")

    time.sleep(5)
    print("Start LabViewIntegration")
    # Call a macro to start the test
    subprocess.call([".\\Macro\\LabViewIntegration.exe"])                                                             # LabView Integration


    print("Start MES integration")
    driver.driver = MESWork(data, driver.driver)            # Call driver and input data                              # MES Integration
    # driver.driver = MESCheckTest(data, driver.driver)            # Call driver and input data
    clearUnitEntryFields()                                  # Clear entry fields and data stored
    inputField.MDL2["state"] = "disabled"
                               # Disable MDL2 input field
    inputField.Serial.focus_set()                           # Set focus on serial input field

    workingTime.lastScan = time.perf_counter()              # Taking time after each unit done

    if workingTime.lastScan - workingTime.clockIn > 28800:  #logout after 8 hours
        messagebox.showwarning("Shift Over", "Your shift for the day is over, bye")
        Logout(loginFrame)


def GUI():
    global loginFrame
    """
    This is the user interface. It contains only the buttons and entry boxes that the user can interact with
    """
    # Define window parameters
    window = Tk()
    # window.attributes('-topmost', True)
    window.title("Station 1800 Scanning")
    # window.geometry('626x403')
    window.resizable(width=False, height=False)

    icon_Path = ".\\Media\\SmartGuy_Ico.ico"
    # icon_Path = resource_path(".\\Media\\SmartGuy_Ico.ico")
    window.iconbitmap(icon_Path)

    backgroungImage_Path = ".\\Media\\Wolf Logo.jpg"
    # backgroungImage_Path = resource_path(".\\Media\\Wolf Logo.jpg")
    backgroungImage = ImageTk.PhotoImage(Image.open(backgroungImage_Path))

    # Place frames
    loginFrame = Frame(window)
    scanFrame = Frame(window)
    for frame in (loginFrame, scanFrame):
        frame.grid(row=0, column=0, sticky='news')


    ###################################################################################################################
    ###                                                 FRAME 1                                                     ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the initial screen where operator has to input his/her badge number so they can start            ###
    ###   scanning units                                                                                            ###
    ###################################################################################################################
    f1_iniRow = 0
    f1_iniCol = 0

    wolfLogo = Label(loginFrame, image=backgroungImage)
    # wolfLogo = Label(loginFrame, bg="black")
    wolfLogo.grid(row=f1_iniRow, column=f1_iniCol, sticky='w')
    f1_iniRow += 1

    text1 = Label(loginFrame, text="Welcome", fg="black", font=('times','35', 'bold'))
    text1.grid(row=f1_iniRow, column=f1_iniCol)
    f1_iniRow += 1

    text2 = Label(loginFrame, text="Scan your ID:", fg="black", font=('times','25'))
    text2.grid(row=f1_iniRow, column=f1_iniCol)
    f1_iniRow += 1

    inputField.Badge = Entry(loginFrame, width=10, bg="white", font=('times','25'), justify='center')
    inputField.Badge.grid(row=f1_iniRow, column=f1_iniCol, ipady=10)
    inputField.Badge.focus_set()
    f1_iniRow += 1

    logIn_Bttn = Button(loginFrame, text="Log in", command=lambda: login(scanFrame, inputField.Badge, inputField.Serial), bg="gray", font=('times','15'), relief=RAISED, borderwidth=5)
    logIn_Bttn.grid(row=f1_iniRow, column=f1_iniCol, pady=8, sticky='s')
    inputField.Badge.bind('<Return>', lambda event: login(scanFrame, inputField.Badge, inputField.Serial))


    # Select Frame 1 as the initial frame
    raise_frame(loginFrame, inputField.Badge)

    ###################################################################################################################
    ###                                                 FRAME 2                                                     ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the screen where operator has to scan the serial number, puma, MDL 1, and MDL2 (if required)     ###
    ###                                                                                                             ###
    ###################################################################################################################
    f2_iniRow = 0
    f2_iniCol = 0
    f2_padx = 10
    f2_pady = 10

    text3 =Label(scanFrame, text= "Scan pallet label:", fg="black", font=('times','25'))
    text3.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1


    inputField.Serial = Entry(scanFrame, width=25, bg="white", font=('times','10'))
    inputField.Serial.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    # inputField.Serial.focus_set()
    inputField.Serial.bind('<Return>', lambda event: GoToNextEntry(inputField.Serial , "serialNumber", inputField.Puma, inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0


    text4 = Label(scanFrame, text= "Scan Puma:", fg="black", font=('times','25'))
    text4.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.Puma = Entry(scanFrame, width=25, bg="white")
    inputField.Puma.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.Puma.bind('<Return>', lambda event: GoToNextEntry(inputField.Puma, "puma", inputField.MDL1))
    f2_iniRow += 1
    f2_iniCol = 0

    text5 = Label(scanFrame, text= "Scan MDL:", fg="black", font=('times','25'))
    text5.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL1 = Entry(scanFrame, width=25, bg="white")
    inputField.MDL1.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL1.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL1, "MDL1", inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0

    text6 = Label(scanFrame, text="Scan MDL:", fg="black", font=('times', '25'))
    text6.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL2 = Entry(scanFrame, width=25, bg="white")
    inputField.MDL2.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL2.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL2, "MDL2"))
    inputField.MDL2["state"] = "disabled"
    f2_iniRow += 1
    f2_iniCol = 0

    logOut_Bttn = Button(scanFrame, text="Log out", command=lambda: Logout(loginFrame), bg="gray", font=('times', '15'), relief=RAISED, borderwidth=5)
    logOut_Bttn.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    Submit_Bttn = Button(scanFrame, text="Submit", command=lambda: submit(), bg="gray", font=('times', '15'), relief=RAISED, borderwidth=5)
    Submit_Bttn.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)


    # raise_frame(scanFrame)

    window.mainloop()


if __name__ == "__main__":
    # Initialize variables
    data = data("","","","","","")
    inputField = inputField(None, None, None, None, None)
    driver = driver(None)
    workingTime = _time(0, 0)


    # Create hidden folder to store data
    HiddenFolder = os.path.join(os.path.expanduser("~"), 'Documents', 'Macro for 1800')
    if not os.path.isdir(HiddenFolder):
        os.mkdir(HiddenFolder)
        # This makes the folder invisible
        subprocess.check_call(["attrib", "+H", HiddenFolder])


    # Execute GUI
    GUI()
