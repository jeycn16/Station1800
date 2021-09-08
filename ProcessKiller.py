import subprocess
# import os

def process_exists(process_name):
    """
    Pull this code straight from stackoverflow #NoShame
    https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows-with-python

    Credit to: ewerybody

    This code takes in an application or program (i.e.: Notepad.exe) and returns True or False depending on whether it's
    running or not

    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    These parameters make subprocess work with pyinstaller. Without them, the exe would not start
    """


    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use built-in check_output right away
    output = subprocess.check_output(call, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

def killProcess(application):
    if process_exists(application):
        try:
            # os.system('taskkill /f /im ' + application)
            subprocess.call("TASKKILL /f  /IM " + application)
        except:
            pass
    else:
        print(application + " not found")


if __name__ == "__main__":
    app1 = "LabViewIntegration.exe"
    app2 = "BringGUI2Front.exe"


    killProcess(app1)
    killProcess(app2)
