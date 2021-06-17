import tkinter
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox


# Define classes
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


# Define functions
def raise_frame(frame):
    """
    Moves frame to the top of the GUI
    """
    frame.tkraise()


def displayError(message):
    """
    Displays an Error box with the desired message in it
    """
    messagebox.showerror("Error", message)


def login(nextFrame, inputField):
    """
    Saves the badge number to data.badge and displays the next frame of the GUI.

    If a wrong badge number is input it displays an error message and clears the badge input field
    """
    data.badge = inputField.get()
    if data.badge.isdigit() and len(data.badge) <= 6 and len(data.badge) >= 4:
        raise_frame(nextFrame)
    else:
        displayError("Invalid ID")
        # Clear entry field
        ClearField(inputField)


def logoff(frame, inputField):
    raise_frame(frame)
    ClearField(inputField)


def ClearField(inputField):
    """
    Clears the input field provided
    """
    inputField.delete(0,END)


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
    data.attribute = selfEntry.get()                            # Save serial number

    if attribute == "serialNumber":                             # Get unit size if serial number was scanned
        data.unitSize = data.attribute[:2]

        if data.unitSize == "48" or data.unitSize == "60":      # Change the state of MDL2 entry field to normal if unit is 48" or 60"
            MDL2_entry['state'] = "normal"

    if nextEntry != None:                                       # If a next entry field is provided, switch focus to that field
        nextEntry.focus_set()
    else:                                                       # If a next entry field is not provided, it's because we reached the final entry field
        doMacro()                                               # execute macro

    if attribute == "MDL1":                                     # If we're scanning MDL1, go to next entry field (MDL2) if unit requires it.
        if (data.unitSize == "48" or data.unitSize == "60"):
            nextEntry.focus_set()
        else:                                                   # Otherwise execute macro
            doMacro()


def doMacro():
    print("hey macrooooo")
    for entry in (inputField.Serial, inputField.Puma, inputField.MDL1, inputField.MDL2):
        ClearField(entry)
    inputField.Serial.focus_set()


def GUI():
    """
    This is the user interface. It contains only the buttons and entry boxes that the user can interact with
    """
    # Define window parameters
    window = Tk()
    window.title("Station 1800 Scanning")
    # window.geometry('626x403')
    window.resizable(width=False, height=False)

    image = "OIP.jpg"
    photo = ImageTk.PhotoImage(Image.open(image))

    # Place frames
    frame1 = Frame(window)
    frame2 = Frame(window)
    for frame in (frame1, frame2):
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

    wolfLogo = Label(frame1, image=photo)
    wolfLogo.grid(row=f1_iniRow, column=f1_iniCol, sticky='w')
    f1_iniRow += 1

    text1 = Label(frame1, text="Welcome", fg="black", font=('times','35', 'bold'))
    text1.grid(row=f1_iniRow, column=f1_iniCol)
    f1_iniRow += 1

    text2 = Label(frame1, text="Scan your ID:", fg="black", font=('times','25'))
    text2.grid(row=f1_iniRow, column=f1_iniCol)
    f1_iniRow += 1

    badge_inputField = Entry(frame1, width=10, bg="white", font=('times','25'), justify='center')
    badge_inputField.grid(row=f1_iniRow, column=f1_iniCol, ipady=10)
    badge_inputField.focus_set()
    f1_iniRow += 1

    logIn_Bttn = Button(frame1, text="Log in", command=lambda: login(frame2, badge_inputField), bg="gray", font=('times','15'), relief=RAISED, borderwidth=5)
    logIn_Bttn.grid(row=f1_iniRow, column=f1_iniCol, pady=8, sticky='s')
    badge_inputField.bind('<Return>', lambda event: login(frame2, badge_inputField))


    # Select Frame 1 as the initial frame
    raise_frame(frame1)

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

    text3 =Label(frame2, text= "Scan pallet label:", fg="black", font=('times','25'))
    text3.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.Serial = Entry(frame2, width=25, bg="white", font=('times','10'))
    inputField.Serial .grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.Serial .focus_set()
    inputField.Serial .bind('<Return>', lambda event: GoToNextEntry(inputField.Serial , "serialNumber", inputField.Puma, inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0


    text4 = Label(frame2, text= "Scan Puma:", fg="black", font=('times','25'))
    text4.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.Puma = Entry(frame2, width=25, bg="white")
    inputField.Puma.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.Puma.bind('<Return>', lambda event: GoToNextEntry(inputField.Puma, "puma", inputField.MDL1))
    f2_iniRow += 1
    f2_iniCol = 0

    text5 = Label(frame2, text= "Scan MDL:", fg="black", font=('times','25'))
    text5.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL1 = Entry(frame2, width=25, bg="white")
    inputField.MDL1.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL1.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL1, "MDL1", inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0

    text6 = Label(frame2, text="Scan MDL:", fg="black", font=('times', '25'))
    text6.grid(row=f2_iniRow, column=f2_iniCol, sticky='e', padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL2 = Entry(frame2, width=25, bg="white")
    inputField.MDL2.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL2.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL2, "MDL2"))
    inputField.MDL2["state"] = "disabled"
    # f2_iniRow += 1
    # f2_iniCol = 0


    # raise_frame(frame2)

    window.mainloop()


if __name__ == "__main__":
    # Initialize variables
    data = data("","","","","","")
    inputField = inputField(None, None, None, None, None)

    # Execute GUI
    GUI()
