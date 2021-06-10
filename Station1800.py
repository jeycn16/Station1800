from tkinter import *

# key down function
from PIL import ImageTk, Image

class data:
    def __init__(self, badge, serialNumber, puma, latch1, latch2):
        self.badge = badge
        self.serialNumber = serialNumber
        self.puma = puma
        self.latch1 = latch1
        self.latch2 = latch2


def raise_frame(frame):
    """
    Moves frame to the top of the GUI
    """
    frame.tkraise()

def login(frame, text_entry):
    data.badge = text_entry.get()
    if data.badge.isdigit():
        raise_frame(frame)
    else:
        print("error")


#Second Page
def click():
    # text_entry.get()
    window =Tk()
    window.title("Station 1800 Scanning (Machine, Puma)")
    window.configure(background="navy")
    Label(window, text="Scan the Machine (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=1,
                                                                                                         column=0,
                                                                                                         sticky=W)
    text_entry2 = Entry(window, width=25, bg="white")
    text_entry2.grid(row=2, column=0, sticky=W)
    Label(window, text="Scan the Puma (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=5,
                                                                                                         column=0,
                                                                                                         sticky=W)
    text_entry3 = Entry(window, width=25, bg="white")
    text_entry3.grid(row=6, column=0, sticky=W)



def main():
    # Define window parameters
    window = Tk()
    window.title("Station 1800 Scanning")
    window.configure(background="navy")


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
    Label(frame1, image=photo, bg='black').grid(row=2, column=2, stick=E)
    Label(frame1, text="Scan your ID (Station 1800):", bg="black", fg="white", font="none 12 bold").grid(row=1,
                                                                                                         column=0,
                                                                                                         sticky=W)
    text_entry = Entry(frame1, width=20, bg="white")
    text_entry.grid(row=2, column=0, sticky=W)

    Button(frame1, text="SUBMIT", padx=6, command=lambda: login(frame2, text_entry), bg="red").grid(row=3, column=0, sticky=W)

    #######################
    ###    FRAME 2      ###
    #######################

    Label(frame2, text="Scan the Machine (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=0,
                                                                                                             column=0,
                                                                                                  sticky=W)
    text_entry2 = Entry(frame2, width=25, bg="white")
    text_entry2.grid(row=1, column=0, sticky=W)
    Label(frame2, text="Scan the Puma (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=2,
                                                                                                          column=0,
                                                                                                          sticky=W)
    text_entry3 = Entry(frame2, width=25, bg="white")
    text_entry3.grid(row=3, column=0, sticky=W)

    Label(frame2, text="Scan the  (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=4,
                                                                                                             column=0,
                                                                                                             sticky=W)
    text_entry4 = Entry(frame2, width=25, bg="white")
    text_entry4.grid(row=5, column=0, sticky=W)

    Label(frame2, text="Scan the  (Station 1800):", bg="black", fg="white", font="none 24 bold").grid(row=6,
                                                                                                             column=0,
                                                                                                             sticky=W)
    text_entry5 = Entry(frame2, width=25, bg="white")
    text_entry5.grid(row=7, column=0, sticky=W)


    # Select Frame 1 as the initial frame
    raise_frame(frame1)

    window.mainloop()


if __name__ == "__main__":
    data = data("","","","","")
    main()