import subprocess

def process_exists(process_name):

    """
    Pull this code straight from stackoverflow #NoShame
    https://stackoverflow.com/questions/7787120/check-if-a-process-is-running-or-not-on-windows-with-python

    Credit to: ewerybody

    This code takes in an application or program (i.e.: Notepad.exe) and returns True or False depending on whether it's
    running or not
    """
    call = 'TASKLIST', '/FI', 'imagename eq %s' % process_name
    # use buildin check_output right away
    output = subprocess.check_output(call).decode()
    # check in last line for process name
    last_line = output.strip().split('\r\n')[-1]
    # because Fail message could be translated
    return last_line.lower().startswith(process_name.lower())

print(process_exists('LabViewIntegration.exe'))