import os
import glob
import sys
import subprocess 


def detect_platform():
    # jetson, rpi, or docker in jetson nano 
    hardware = {'jetson', 'rpi', 'darwin'}
    res = str(subprocess.Popen(["uname -a"], shell=True, stdout=subprocess.PIPE).stdout.read())

    # Docker 
    if glob.glob('/docker_*.txt') is not None:
        if os.path.exists('/docker_jetson.txt'):
            return 'jetson'
        elif os.path.exists('/docker_rpi.txt'):
            return 'rpi'
        else:
            return 'test'


    elif 'tegra' in res:
        print("jetson") 
        return 'jetson' 
    else:
        return "unknown"


def get_duet_ip_address():
    return '0.0.0.0'


def detect_camera():
    """Doesn't work in a container""" 
    
    res = str(subprocess.Popen(["v4l2-ctl --list-devices"], shell=True, stdout=subprocess.PIPE).stdout.read()) 


detect_platform()