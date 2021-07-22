# def serialParser(serialNum):
#     if "$" in serialNum:
#         unitSize = serialNum.split("$")[3]  # slicing through serial number to just the model code "DF48...."
#         print(unitSize)
#         if unitSize.startswith("DF") or unitSize.startswith("IR"):
#             unitSize = int(unitSize[2:4])
#             print(unitSize)
#         else:
#             print("invalid serial")
#     else:
#         print("invalid serial")
#
#
# serialParser("5610447$18593497$M641070$DF48650G/S/P")
#
# import time
#
#
# initial_Time = time.perf_counter()
#
#
# # time.sleep(5)
#
# finalTime = time.perf_counter()
#
# print(finalTime - initial_Time)
#
# def fileList(directory, *extension):
#     """
#     This program takes a directory path as input, then returns a list with all the files inside that folder
#     that end with the extensions provided
#     """
#     programs = []
#     import os
#     for extns in extension[0]:
#         if os.path.isdir(directory):
#             for filename in os.listdir(directory):
#                 if filename.lower().endswith(extns):
#                     programs.append(filename)
#         else:
#             print("Invalid directory path")
#     return programs
#
# listOfChromeDrivers = fileList(".\\Drivers\\", [".exe"])
# for x in listOfChromeDrivers:
#     print(x)


# semi-transparent-stipple-demo.py
# note: stipple only works for some objects (like rectangles)
# and not others (like ovals).  But it's better than nothing...

from tkinter import *

def redrawAll(canvas):
    canvas.delete(ALL)
    # draw a red rectangle on the left half
    canvas.create_rectangle(0, 0, 250, 600, fill="red")
    # draw semi-transparent rectangles in the middle
    canvas.create_rectangle(200,  75, 300, 125, fill="blue", stipple="")
    canvas.create_rectangle(200, 175, 300, 225, fill="blue", stipple="gray75")
    canvas.create_rectangle(200, 275, 300, 325, fill="blue", stipple="gray50")
    canvas.create_rectangle(200, 375, 300, 425, fill="blue", stipple="gray25")
    canvas.create_rectangle(200, 475, 300, 525, fill="gray", stipple="gray12")

def init(canvas):
    redrawAll(canvas)

########### copy-paste below here ###########

def run():
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=500, height=600)
    canvas.pack()
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", mousePressed)
    # root.bind("<Key>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()