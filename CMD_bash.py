# import numpy
# np = numpy

#pre 2018
import os
import subprocess
#------------------------------------
#subfunc: execute CMD, version 1
def exeCMD(cmd):
    print("running CMD: "+cmd)
    try:
        info=subprocess.check_output(cmd, shell=True,stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        raise RuntimeError("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
    print(info)
    return

def checkMakeDir(directory):
    if os.path.exists(directory):
        return True
    else:
        os.makedirs(directory)
        return False
#------------------------------------