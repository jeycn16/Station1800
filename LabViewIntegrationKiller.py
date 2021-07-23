import os
try:
    os.system('taskkill /f /im LabViewIntegration.exe')
except:
    pass
try:
    os.system('taskkill /f /im BringGUI2Front.exe')
except:
    pass