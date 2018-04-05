from subprocess import Popen, check_output, CalledProcessError, PIPE
import sys
import time
from os import listdir, path
import re
import pytest
import atexit

display = None
xvfb_proc = None
LOCKDIR = '/tmp'


def get_open_display():
    i = 0
    while True:
        try:
            check_output(['lsof', '/tmp/.X11-unix/X%d' % i], stderr=PIPE)
        except CalledProcessError:
            return i
        i += 1


def start_server(display, xserver_command):
    xvfb = Popen([xserver_command, ':%d' % display])
    # wait for the lock file to make sure the server is running
    lockfile = path.join(LOCKDIR, '.X%d-lock' % display)
    tries = 0
    while True:
        if path.exists(lockfile):
            break
        else:
            tries += 1

            if tries > 1000:
                print('could not start x server')
                xvfb.kill()
                sys.exit(1)

            time.sleep(0.001)

    return xvfb


@atexit.register
def at_exit():
    if xvfb_proc:
        xvfb_proc.terminate()


def get_x11_display(xserver_command):
    global display

    if display:
        return display

    check_dependencies()
    open_display = get_open_display()
    xvfb_proc = start_server(open_display)
    display = ':%d' % open_display
    return display
