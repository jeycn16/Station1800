import os
import subprocess
import clipboard
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog
from MESintegration import MESLogIn
from MESintegration import MESWork
from MESintegration import MESLogout
import time
import configparser
from shutil import copyfile


class _time:
    def __init__(self, clockIn, lastScan):
        self.clockIn = clockIn
        self.lastScan = lastScan

class data:
    def __init__(self, badge, serialNumber, puma, MDL1, MDL2, unitSize, unitType):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2
        self.unitSize = unitSize
        self.unitType = unitType

class inputField:
    def __init__(self, Badge, Serial, Puma, MDL1, MDL2, runbttn_image, runbttn_tlrnc, checkbttn_image, checkbttn_tlrnc, waitMul, keyWord):
        self.Badge = Badge
        self.Serial = Serial
        self.Puma = Puma
        self.MDL1 = MDL1
        self.MDL2 = MDL2
        self.runbttn_image = runbttn_image
        self.runbttn_tlrnc = runbttn_tlrnc
        self.checkbttn_image = checkbttn_image
        self.checkbttn_tlrnc = checkbttn_tlrnc
        self.waitMul = waitMul
        self.keyWord = keyWord

class settingsData:
    def __init__(self, runButtonTolerance, runButtonTolerance_entryValue,
                 greenCheckButtonTolerance, greenCheckButtonTolerance_entryValue,
                 waitMultiplier, waitMultiplier_entryValue,
                 testFinishedKeyWord, testFinishedKeyWord_entryValue):

        self.runButtonTolerance_entryValue = runButtonTolerance_entryValue
        self.runButtonTolerance = runButtonTolerance
        self.greenCheckButtonTolerance = greenCheckButtonTolerance
        self.greenCheckButtonTolerance_entryValue = greenCheckButtonTolerance_entryValue
        self.waitMultiplier = waitMultiplier
        self.waitMultiplier_entryValue = waitMultiplier_entryValue
        self.testFinishedKeyWord = testFinishedKeyWord
        self.testFinishedKeyWord_entryValue = testFinishedKeyWord_entryValue

class driver:
    def __init__(self, driver):
        self.driver = driver


###################################################################################################################
###                                                                                                             ###
###                                       GENERAL FUNCTIONS                                                      ###
###                                                                                                             ###
###################################################################################################################

def RiseGUI(): #raising GUI to the front of the screen using Macro Scheduler
    subprocess.call([".\\Macro\\bringGUI2Front.exe"])


"""def BringGUI2Front(frame, nextInputField):
    frame.focus_force()
    nextInputField.focus_set()"""


def raise_frame(frame, inputField=None): #raising a certain frame
    """
    Moves frame to the top of the GUI, sets focus on the indicated input field
    """
    frame.tkraise()
    frame.focus_force()
    if inputField != None:
        inputField.focus_set()


def selectImageFile(imageType):

    sourceFile = filedialog.askopenfilename(
        initialdir=".\\Macro\\Macro image files", title='Select image file',
        filetypes=(("JPG files", "*.jpg"), ("BMP files", "*.bmp"), ("All files", "*.*")))

    # Copy image file to the Macro images folder
    # if not os.path.isfile(os.path.join(".\\Macro\\Macro image files", os.path.split(filename)[1])):
    #     copyfile(filename, os.path.join(".\\Macro\\Macro image files", os.path.split(filename)[1]))

    destinationFile = os.path.join(".\\Macro\\Macro image files", os.path.split(sourceFile)[1])
    try:
        copyfile(sourceFile, destinationFile)
    except:
        pass
    if imageType == "RunButton":
        inputField.runbttn_image = "Macro image files\\" + os.path.split(sourceFile)[1]
    elif imageType == "CheckButton":
        inputField.checkbttn_image = "Macro image files\\" + os.path.split(sourceFile)[1]


def displayError(message): #displaying an error message
    """
    Displays an Error box with the desired message in it
    """
    messagebox.showerror("Error", message)


def login(selfFrame, nextFrame, selfInputField, nextInputField): #logging in function
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


    else:
        displayError("Invalid ID")
        # Clear entry field
        ClearField(selfInputField)
        raise_frame(selfFrame, selfInputField)


def Logout(nextFrame): #logout function
    MESLogout(driver.driver)
    ClearField(inputField.Badge)
    raise_frame(nextFrame, inputField.Badge)


def ClearField(inputField): #clearing the text box
    """
    Clears the input field provided
    """
    inputField.delete(0,END)


def clearUnitEntryFieldsAndWipeOutData(): #clears data for entry boxes and empty class variables
    """
    Clears every input field in the second frame (serial number, puma, MDL1, MDL2)
    Wipes out data
    """
    for entry in (inputField.Serial, inputField.Puma, inputField.MDL1, inputField.MDL2):
        ClearField(entry)
    data.serialNumber = ""
    data.puma = ""
    data.MDL1 = ""
    data.MDL2 = ""
    data.unitSize = ""
    data.unitType = ""


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

        try:
            unitSize = serialNum.split("$")[3]  #slicing through serial number to just the model code "DF48...."
            if unitSize.startswith("ICBDF") or unitSize.startswith("ICBIR"):
                try:
                    data.unitType = unitSize[0:5]
                    unitSize = int(unitSize[5:7])
                except:
                    displayError("Problems finding the unit size in ICB unit")
                    ClearField(selfEntry)  # Clear entry field
            elif unitSize.startswith("DF") or unitSize.startswith("IR"):
                try:
                    data.unitType = unitSize[0:2]
                    unitSize = int(unitSize[2:4])
                except:
                    displayError("Problems finding the unit size in regular")
                    ClearField(selfEntry)                       # Clear entry field
            else:
                displayError("Problems finding the unit type in serial")
                ClearField(selfEntry)                           # Clear entry field
        except:
            displayError("Serial string could not be parsed")
            ClearField(selfEntry)                               # Clear entry field
            selfEntry.focus_set()

        data.unitSize = unitSize # Save unit size


        if data.unitSize == 48 or data.unitSize == 60:      # Change the state of MDL2 entry field to normal if unit is 48" or 60"
            MDL2_entry['state'] = "normal"

        if data.unitType == "DF" or data.unitType == "IR":
            inputField.Puma["state"] = "normal"

    elif attribute == "puma":
        data.puma = selfEntry.get()

    elif attribute == "MDL1":
        data.MDL1 = selfEntry.get()

    elif attribute == "MDL2":
        data.MDL2 = selfEntry.get()

    else:
        print("Error\nBad entry field")

    if nextEntry == None:
        doMacro()
    else:
        nextEntry.focus_set()

    if (data.unitType == "ICBDF" or data.unitType == "ICBIR") and nextEntry == inputField.Puma:
        inputField.MDL1.focus_set()

    if attribute == "MDL1":                                     # If we're scanning MDL1, go to next entry field (MDL2) if unit requires it.
        if (data.unitSize == 48 or data.unitSize == 60):
            nextEntry.focus_set()
        else:                                                   # Otherwise execute macro
            doMacro()



def submit(): #saving entered values into class variable
    data.serialNumber = inputField.Serial.get()
    try:
        data.puma = inputField.Puma.get()
    except:
        pass
    data.MDL1 = inputField.MDL1.get()
    try:
        data.MDL2 = inputField.MDL2.get()
    except:
        pass
    doMacro()


def getParametersFrom_ini_File(pathTo_ini_file, *args):
    """
    Assume a .ini file of the form:

    [people]
    Peter = Not cool
    Jeyc = Cool dude

    [countries]
    Venezuela = Tamos mal
    Denmark = Rich



    This function retrieves a value (or values), from a .ini file. The inputs to this function are:

        pathTo_ini_file: The path to the .ini file i.e.: "C:\\Users\\This is my ini file.ini"

        *args: a list (or lists), containing the parent and the child of the value you want to return
        i.e.: ["people", "Peter"], ["countries", "Denmark"]


    This function returns a list with the wanted values pulled from the .ini file
    i.e.: ["Not cool", "Rich"]

    """
    parameters = []

    fileConfig = configparser.ConfigParser()
    fileConfig.read(pathTo_ini_file)

    for arg in args:
        parameters.append(fileConfig.get(arg[0], arg[1]))

    return parameters


def saveParametersTo_ini_File(pathTo_ini_file, *args):
    """
    This function updates an .ini file with the new parameters fed. If the ini file doesn't exist, it will create it.
    The inputs to this function are:

        pathTo_ini_file: The path to the .ini file i.e.: "C:\\Users\\This is my ini file.ini"

        *args: a list (or lists), containing the parent, child, and new value you want for this tag.

    Example:
    Assume you have a .ini file of the form:

    [people]
    Peter = Not cool
    Jeyc = Cool dude

    [countries]
    Venezuela = Tamos mal
    Denmark = Rich

    and want to update the value for Peter to "He aight", and Venezuela to "Seguimos mal". All you have to do is input
    the path to the .ini file and a list(s) containing the parent, child, and new value, i.e.:

        saveParametersTo_ini_File("C:\\Users\\This is my ini file.ini", ["people", "Peter", "He aight"], ["countries", "Venezuela", "Seguimos mal"])

    you should see your .ini file updated to:

    [people]
    Peter = He aight
    Jeyc = Cool dude

    [countries]
    Venezuela = Seguimos mal
    Denmark = Rich
    """

    # Create config file
    iniFileConfig = configparser.ConfigParser()

    # Check to see if .ini file exists, if it does read it
    if os.path.isfile(pathTo_ini_file):
        # Create ini file
        iniFileConfig.read(pathTo_ini_file)

    # Update values
    for arg in args:
        if arg[2] != None:# or arg[2] != "" or arg[2] != "None":
            iniFileConfig.set(arg[0], arg[1], str(arg[2]))

    # save file
    with open(pathTo_ini_file, 'w') as configfile:
            iniFileConfig.write(configfile)


def settings(selfFrame):
    global frameBeforeSettings
    frameBeforeSettings = selfFrame
    # Read Macro settings and store values
    settingsFromIni = getParametersFrom_ini_File(".\\Macro\\Macro Settings.ini",
                                ["ImageTolerances", "runButtonTolerance"],
                                ["ImageTolerances", "greenCheckButtonTolerance"],
                                ["Miscellaneous", "waitMultiplier"],
                                ["Miscellaneous", "testFinishedKeyWord"])

    macroSettings.runButtonTolerance = settingsFromIni[0]
    macroSettings.greenCheckButtonTolerance = settingsFromIni[1]
    macroSettings.waitMultiplier = settingsFromIni[2]
    macroSettings.testFinishedKeyWord = settingsFromIni[3]

    # Set Entry boxes initial values
    macroSettings.runButtonTolerance_entryValue.set(macroSettings.runButtonTolerance)
    macroSettings.greenCheckButtonTolerance_entryValue.set(macroSettings.greenCheckButtonTolerance)
    macroSettings.waitMultiplier_entryValue.set(macroSettings.waitMultiplier)
    macroSettings.testFinishedKeyWord_entryValue.set(macroSettings.testFinishedKeyWord)


    # Raise settings frame
    raise_frame(settingsFrame)


def saveSettings(previousFrame):
    # Update ini file with new settings
    saveParametersTo_ini_File(".\\Macro\\Macro Settings.ini",
                              ["ImagePaths", "runbutton", inputField.runbttn_image],
                              ["ImagePaths", "greencheckbutton", inputField.checkbttn_image],
                              ["ImageTolerances", "runButtonTolerance", inputField.runbttn_tlrnc.get()],
                              ["ImageTolerances", "greencheckbuttontolerance", inputField.checkbttn_tlrnc.get()],
                              ["Miscellaneous", "waitmultiplier", inputField.waitMul.get()],
                              ["Miscellaneous", "testfinishedkeyword", inputField.keyWord.get()])


    # Raise settings frame
    raise_frame(previousFrame)


def doMacro(): #Macro is performed
    sotredValues_Path = (".\\Macro\\Stored values.txt")
    with open(sotredValues_Path, 'w') as outfile:
        outfile.write(str(data.badge) + "\n")
        outfile.write(str(data.unitSize) + "\n")
        outfile.write(data.unitType + "\n")
        outfile.write(data.serialNumber + "\n")
        outfile.write(data.puma + "\n")
        outfile.write(data.MDL1 + "\n")
        outfile.write(data.MDL2 + "\n")

    # Put path to the txt file in ram memory
    clipboard.copy(sotredValues_Path)

    # Call a macro to start the test
    subprocess.call([".\\Macro\\LabViewIntegration.exe"])                                                             # LabView Integration

    # Start MES integration
    driver.driver = MESWork(data, driver.driver)            # Call driver and input data                              # MES Integration

    clearUnitEntryFieldsAndWipeOutData()                    # Clear entry fields and data stored
    inputField.Puma["state"] = "disabled"                   # Disable Puma input field
    inputField.MDL2["state"] = "disabled"                   # Disable MDL2 input field

    RiseGUI()                                               # Bring GUI to front again
    inputField.Serial.focus_set()                           # Set focus on serial input field

    workingTime.lastScan = time.perf_counter()              # Taking time after each unit done

    if workingTime.lastScan - workingTime.clockIn > 28800:  #logout after 8 hours
        messagebox.showwarning("Shift Over", "Your shift for the day is over, bye")
        Logout(loginFrame)


###################################################################################################################
###                                                                                                             ###
###                                    GRAPHICAL USER INTERFACE                                                 ###
###                                             GUI                                                             ###
###################################################################################################################


def GUI(): #GUI
    global loginFrame, scanFrame, settingsFrame
    """
    This is the user interface. It contains only the buttons and entry boxes that the user can interact with
    """

    # Define window parameters
    window = Tk()
    window.title("Macro for Station 1800, by Jeyc")
    window.resizable(width=False, height=False)


    icon_Path = ".\\Media\\SmartGuy_Ico.ico"
    window.iconbitmap(icon_Path)

    backgroungImage_Path = ".\\Media\\background.jpg"
    backgroungImage = ImageTk.PhotoImage(Image.open(backgroungImage_Path))

    # Place frames
    loginFrame = Frame(window)
    scanFrame = Frame(window)
    settingsFrame = Frame(window)
    for frame in (loginFrame, scanFrame, settingsFrame):
        frame.grid(row=0, column=0, sticky='news')


    ###################################################################################################################
    ###                                            LOGIN FRAME                                                      ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the initial screen where operator has to input his/her badge number so they can start            ###
    ###   scanning units                                                                                            ###
    ###################################################################################################################

    #Wolf Logo
    wolfLogo = Label(loginFrame, image=backgroungImage)
    wolfLogo.pack()

    text1 = Label(loginFrame, text="Welcome", fg="white", bg="#012B7D", font=('times','35', 'bold'))
    text1.place(relx=0.5, rely=0.2, anchor="center")

    text2 = Label(loginFrame, text="Scan your ID:", fg="white", bg="#0071AB", font=('times','25'))
    text2.place(relx=0.5, rely=0.4, anchor="center")

    inputField.Badge = Entry(loginFrame, width=10, bg="white", borderwidth=5, font=('times','25'), justify='center')
    inputField.Badge.place(relx=0.5, rely=0.7, anchor="center")
    inputField.Badge.focus_set()

    logIn_Bttn = Button(loginFrame, text="Log in", command=lambda: login(loginFrame, scanFrame, inputField.Badge, inputField.Serial), bg="light blue", font=('times','15'), relief=RAISED, borderwidth=5)
    logIn_Bttn.place(relx=0.5, rely=0.9, anchor="center")
    inputField.Badge.bind('<Return>', lambda event: login(loginFrame, scanFrame, inputField.Badge, inputField.Serial))

    optionsImage_Path = ".\\Media\\options.png"
    optionsImage_Path = ImageTk.PhotoImage(Image.open(optionsImage_Path))
    options_Bttn = Button(loginFrame, image=optionsImage_Path, bg="#012B7D", relief=RAISED, borderwidth=5, command= lambda: settings(loginFrame))
    options_Bttn.place(relx=0.87, rely=0.05)


    ###################################################################################################################
    ###                                         SETTINGS FRAME                                                      ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the screen where operator can change the Macro settings                                          ###
    ###                                                                                                             ###
    ###################################################################################################################
    options_relx1 = 0.05
    options_relx2 = 0.55
    options_relx3 = 0.55

    runButton_Bttn = Button(settingsFrame, text="Choose Run button\nimage...", font=('times', '10'), width=20, relief=RAISED, borderwidth=5, bg="light green", command= lambda: selectImageFile("RunButton"))
    runButton_Bttn.place(relx=options_relx1, rely=0.1, anchor="w")

    runbttn_tlrnc_LBL = Label(settingsFrame, text="Tolenrance: ", font=('times', '18'))
    runbttn_tlrnc_LBL.place(relx=options_relx2, rely=0.1, anchor="e")
    runbttn_tlrnc_LBL2 = Label(settingsFrame, text="Should be a number between 0 and 1. Recommended value: 0.7", font=('times', '10'))
    runbttn_tlrnc_LBL2.place(relx=options_relx2+.098, rely=0.18, anchor="center")

    macroSettings.runButtonTolerance_entryValue = StringVar()
    inputField.runbttn_tlrnc = Entry(settingsFrame, textvariable=macroSettings.runButtonTolerance_entryValue, width=4, bg="white", borderwidth=5, font=('times', '18'), justify='center')
    inputField.runbttn_tlrnc.place(relx=options_relx3, rely=0.1, anchor="w")


    checkButton_Bttn = Button(settingsFrame, text="Choose Check button\nimage...", font=('times', '10'), width=20, relief=RAISED, borderwidth=5, bg="light green", command= lambda: selectImageFile("CheckButton"))
    checkButton_Bttn.place(relx=options_relx1, rely=0.3, anchor="w")

    checkbttn_tlrnc_LBL = Label(settingsFrame, text="Tolenrance: ", font=('times', '18'))
    checkbttn_tlrnc_LBL.place(relx=options_relx2, rely=0.3, anchor="e")
    checkbttn_tlrnc_LBL2 = Label(settingsFrame, text="Should be a number between 0 and 1. Recommended value: 0.7", font=('times', '10'))
    checkbttn_tlrnc_LBL2.place(relx=options_relx2+.098, rely=0.38, anchor="center")

    macroSettings.greenCheckButtonTolerance_entryValue = StringVar()
    inputField.checkbttn_tlrnc = Entry(settingsFrame, textvariable=macroSettings.greenCheckButtonTolerance_entryValue, width=4, bg="white", borderwidth=5, font=('times', '18'), justify='center')
    inputField.checkbttn_tlrnc.place(relx=options_relx3, rely=0.3, anchor="w")


    waitMultiplier_LBL1 = Label(settingsFrame, text="Macro speed: ", font=('times', '18'))
    waitMultiplier_LBL1.place(relx=options_relx2, rely=0.5, anchor="e")
    waitMultiplier_LBL2 = Label(settingsFrame, text="The higher the number, the slower it runs. Recommended value between 1 and 3", font=('times', '10'))
    waitMultiplier_LBL2.place(relx=options_relx2, rely=0.58, anchor="center")

    macroSettings.waitMultiplier_entryValue = StringVar()
    inputField.waitMul = Entry(settingsFrame, textvariable=macroSettings.waitMultiplier_entryValue, width=4, bg="white", borderwidth=5, font=('times', '18'), justify='center')
    inputField.waitMul.place(relx=options_relx3, rely=0.5, anchor="w")

    keyWord_LBL1 = Label(settingsFrame, text="Cue word: ", font=('times', '18'))
    keyWord_LBL1.place(relx=options_relx2, rely=0.7, anchor="e")
    keyWord_LBL2 = Label(settingsFrame, text="The program will search for this word. It works as the cue to let it know the test was completed", font=('times', '10'))
    keyWord_LBL2.place(relx=options_relx2, rely=0.78, anchor="center")

    macroSettings.testFinishedKeyWord_entryValue = StringVar()
    inputField.keyWord = Entry(settingsFrame, textvariable=macroSettings.testFinishedKeyWord_entryValue, width=20, bg="white", borderwidth=5, font=('times', '18'), justify='left')
    inputField.keyWord.place(relx=options_relx3, rely=0.7, anchor="w")


    cancel_Bttn = Button(settingsFrame, text="Cancel", command=lambda: raise_frame(frameBeforeSettings), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    cancel_Bttn.place(relx=0.3, rely=0.9, anchor="center")

    Save_Bttn = Button(settingsFrame, text="Save", command=lambda: saveSettings(frameBeforeSettings), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    Save_Bttn.place(relx=0.7, rely=0.9, anchor="center")

    ###################################################################################################################
    ###                                             SCAN FRAME                                                      ###
    ###                                                                                                             ###
    ###                                                                                                             ###
    ###   Contains the screen where operator has to scan the serial number, puma, MDL 1, and MDL2 (if required)     ###
    ###                                                                                                             ###
    ###################################################################################################################

    text_Relx = 0.4
    IF_Relx = 0.45
    image_Relx = 0.905
    _rely = 0.1

    wolfLogo = Label(scanFrame, image=backgroungImage)
    wolfLogo.pack()

    text3 =Label(scanFrame, text= "Scan pallet label:", fg="white", bg="#011F67", font=('times','25'))
    text3.place(relx=text_Relx, rely=_rely, anchor="e")

    inputField.Serial = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.Serial.place(relx=IF_Relx, rely=_rely, anchor="w")
    inputField.Serial.bind('<Return>', lambda event: GoToNextEntry(inputField.Serial, "serialNumber", inputField.Puma, inputField.MDL2))

    labelImage = ImageTk.PhotoImage(Image.open(".\\Media\\label.jpg"))
    chip_Canvas = Label(scanFrame, image=labelImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely, anchor="w")



    text4 = Label(scanFrame, text= "Scan Puma:", fg="white", bg="#004694", font=('times','25'), justify="right")
    text4.place(relx=text_Relx, rely=_rely*3, anchor="e")

    inputField.Puma = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.Puma.place(relx=IF_Relx, rely=_rely * 3, anchor="w")
    inputField.Puma.bind('<Return>', lambda event: GoToNextEntry(inputField.Puma, "puma", inputField.MDL1))
    inputField.Puma["state"] = "disabled"

    chipImage = ImageTk.PhotoImage(Image.open(".\\Media\\chip.jpg"))
    chip_Canvas = Label(scanFrame, image=chipImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely*3, anchor="w")



    text5 = Label(scanFrame, text= "Scan MDL:", fg="white", bg="#0472A3", font=('times','25'), justify="right")
    text5.place(relx=text_Relx, rely=_rely*5, anchor="e")

    inputField.MDL1 = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.MDL1.place(relx=IF_Relx, rely=_rely*5, anchor="w")
    inputField.MDL1.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL1, "MDL1", inputField.MDL2))

    MDLImage = ImageTk.PhotoImage(Image.open(".\\Media\\MDL.png"))
    chip_Canvas = Label(scanFrame, image=MDLImage)
    chip_Canvas.place(relx=image_Relx, rely=_rely*5, anchor="w")



    text6 = Label(scanFrame, text="Scan MDL:", fg="white", bg="#2099C6", font=('times', '25'), justify="right")
    text6.place(relx=text_Relx, rely=_rely*7, anchor="e")

    inputField.MDL2 = Entry(scanFrame, width=15, bg="white", font=('times','25'), borderwidth=4)
    inputField.MDL2.place(relx=IF_Relx, rely=_rely * 7, anchor="w")
    inputField.MDL2.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL2, "MDL2"))
    inputField.MDL2["state"] = "disabled"

    MDL2Image = ImageTk.PhotoImage(Image.open(".\\Media\\MDL2.png"))
    chip_Canvas = Label(scanFrame, image=MDL2Image)
    chip_Canvas.place(relx=image_Relx, rely=_rely*7, anchor="w")



    logOut_Bttn = Button(scanFrame, text="Log out", command=lambda: Logout(loginFrame), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    logOut_Bttn.place(relx=0.3, rely=_rely*9, anchor="center")

    Submit_Bttn = Button(scanFrame, text="Submit", command=lambda: submit(), bg="light blue", font=('times', '15'), relief=RAISED, borderwidth=5)
    Submit_Bttn.place(relx=0.7, rely=_rely*9, anchor="center")

    options_Bttn2 = Button(scanFrame, image=optionsImage_Path, bg="#012B7D", relief=RAISED, borderwidth=5, command= lambda:settings(scanFrame))
    options_Bttn2.place(relx=0.938, rely=0.89, anchor="center")


    # Select Frame 1 as the initial frame
    raise_frame(loginFrame, inputField.Badge)
    # raise_frame(settingsFrame)
    # raise_frame(scanFrame,inputField.Serial)

    window.mainloop()


if __name__ == "__main__":
    # Initialize variables
    data = data("","","","","","","")
    inputField = inputField(None, None, None, None, None, None, None, None, None, None, None)
    macroSettings = settingsData("", "", "", "","", "", "", "")
    driver = driver(None)
    workingTime = _time(0, 0)


    """# Create hidden folder to store data
    HiddenFolder = os.path.join(os.path.expanduser("~"), 'Documents', 'Macro for 1800')
    if not os.path.isdir(HiddenFolder):
        os.mkdir(HiddenFolder)
        # This makes the folder invisible
        subprocess.check_call(["attrib", "+H", HiddenFolder])"""



    # Create the settings file that the macro will use for the LabViewIntegration
    macroSettings_Path = ".\\Macro\\Macro Settings.ini"
    if not os.path.isfile(macroSettings_Path):

        # Create settings file
        macroSettings = configparser.ConfigParser()

        # ImagePaths
        macroSettings["ImagePaths"] =   {
                                        "runButton": "Macro image files\RunButton.jpg",
                                        "greenCheckButton": "Macro image files\GreenCheckButton.jpg"
                                        }

        # ImageTolerances
        macroSettings["ImageTolerances"] = {}
        macroSettings["ImageTolerances"]["runButtonTolerance"] = "0.7"
        macroSettings["ImageTolerances"]["greenCheckButtonTolerance"] = "0.7"

        # Miscellaneous
        macroSettings["Miscellaneous"] = {}
        macroSettings["Miscellaneous"]["waitMultiplier"] = "1"
        macroSettings["Miscellaneous"]["testFinishedKeyWord"] = "Test Complete..."

        # save to a file
        with open(macroSettings_Path, 'w') as configfile:
            macroSettings.write(configfile)


    # Execute GUI
    GUI()
