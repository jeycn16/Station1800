import tkinter
from tkinter import *

# key down function
from PIL import ImageTk, Image

from tkinter import messagebox



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


def raise_frame(frame):
    """
    Moves frame to the top of the GUI
    """
    frame.tkraise()


def displayError(message):
    messagebox.showerror("Error", message)


def login(nextFrame, inputField):
    data.badge = inputField.get()
    if data.badge.isdigit() and len(data.badge) <= 6 and len(data.badge) >= 4:
        raise_frame(nextFrame)
    else:
        displayError("Invalid ID")
        # Clear entry field
        ClearField(inputField)


def logoff(frame, text_entry):
    raise_frame(frame)
    ClearField(text_entry)


def ClearField(inputField):
    inputField.delete(0,END)


def GoToNextEntry(selfEntry, attribute, nextEntry=None, MDL2_entry=None):
    data.attribute = selfEntry.get()

    if attribute == "serialNumber":
        data.unitSize = data.attribute[:2]

        if data.unitSize == "48" or data.unitSize == "60":
            MDL2_entry['state'] = "normal"

    if nextEntry != None:
        nextEntry.focus_set()
    else:
        doMacro()

    if attribute == "MDL1":
        if (data.unitSize == "48" or data.unitSize == "60"):
            nextEntry.focus_set()
        else:
            doMacro()


def doMacro():
    print("hey macrooooo")
    for entry in (inputField.Serial, inputField.Puma, inputField.MDL1, inputField.MDL2):
        ClearField(entry)
    inputField.Serial.focus_set()


def main():
    # Define window parameters
    window = Tk()
    window.title("Station 1800 Scanning")
    # window.geometry('626x403')
    window.resizable(width=False, height=False)


    image = "OIP.jpg"
    photo = ImageTk.PhotoImage(Image.open(image))


    frame1 = Frame(window)
    frame2 = Frame(window)

    # Place frames
    for frame in (frame1, frame2):
        frame.grid(row=0, column=0, sticky='news')


    #######################
    ###    FRAME 1      ###
    #######################
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
    # raise_frame(frame1)

    #######################
    ###    FRAME 2      ###
    #######################
    f2_iniRow = 0
    f2_iniCol = 0
    f2_padx = 5
    f2_pady = 10

    text3 =Label(frame2, text= "Scan unit:", fg="black", font=('times','25'))
    text3.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.Serial = Entry(frame2, width=25, bg="white", font=('times','10'))
    inputField.Serial .grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.Serial .focus_set()
    inputField.Serial .bind('<Return>', lambda event: GoToNextEntry(inputField.Serial , "serialNumber", inputField.Puma, inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0


    text4 = Label(frame2, text= "Scan Puma:", fg="black", font=('times','25'))
    text4.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.Puma = Entry(frame2, width=25, bg="white")
    inputField.Puma.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.Puma.bind('<Return>', lambda event: GoToNextEntry(inputField.Puma, "puma", inputField.MDL1))
    f2_iniRow += 1
    f2_iniCol = 0

    text5 = Label(frame2, text= "Scan MDL:", fg="black", font=('times','25'))
    text5.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL1 = Entry(frame2, width=25, bg="white")
    inputField.MDL1.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL1.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL1, "MDL1", inputField.MDL2))
    f2_iniRow += 1
    f2_iniCol = 0

    text6 = Label(frame2, text="Scan MDL:", fg="black", font=('times', '25'))
    text6.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    f2_iniCol += 1

    inputField.MDL2 = Entry(frame2, width=25, bg="white")
    inputField.MDL2.grid(row=f2_iniRow, column=f2_iniCol, sticky=W, padx=f2_padx, pady=f2_pady)
    inputField.MDL2.bind('<Return>', lambda event: GoToNextEntry(inputField.MDL2, "MDL2"))
    inputField.MDL2["state"] = "disabled"
    # f2_iniRow += 1
    # f2_iniCol = 0




    raise_frame(frame2)

    window.mainloop()


if __name__ == "__main__":
    data = data("","","","","","")
    inputField = inputField(None, None, None, None, None)
    main()
