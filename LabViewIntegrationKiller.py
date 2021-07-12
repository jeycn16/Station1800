import os
try:
    os.system('taskkill /f /im LabViewIntegration.exe')
except:
    pass