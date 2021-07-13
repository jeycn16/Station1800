def serialParser(serialNum):
    if "$" in serialNum:
        unitSize = serialNum.split("$")[3]  # slicing through serial number to just the model code "DF48...."
        print(unitSize)
        if unitSize.startswith("DF") or unitSize.startswith("IR"):
            unitSize = int(unitSize[2:4])
            print(unitSize)
        else:
            print("invalid serial")
    else:
        print("invalid serial")


serialParser("5610447$18593497$M641070$DF48650G/S/P")

import time


initial_Time = time.perf_counter()


# time.sleep(5)

finalTime = time.perf_counter()

print(finalTime - initial_Time)

def fileList(directory, *extension):
    """
    This program takes a directory path as input, then returns a list with all the files inside that folder
    that end with the extensions provided
    """
    programs = []
    import os
    for extns in extension[0]:
        if os.path.isdir(directory):
            for filename in os.listdir(directory):
                if filename.lower().endswith(extns):
                    programs.append(filename)
        else:
            print("Invalid directory path")
    return programs

listOfChromeDrivers = fileList(".\\Drivers\\", [".exe"])
for x in listOfChromeDrivers:
    print(x)
