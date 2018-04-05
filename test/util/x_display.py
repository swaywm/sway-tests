from subprocess import Popen, check_output, CalledProcessError, PIPE
import sys
import time
from os import listdir, path
import re
import pytest
import atexit


def get_open_display():
    i = 0
    while True:
        try:
            # TODO to make this work in parallel, we'll need to have our own
            # lock directory
            if not path.exists('/tmp/.X%d-lock'):
                check_output(['lsof', '/tmp/.X11-unix/X%d' % i], stderr=PIPE)
        except CalledProcessError:
            return i
        i += 1


def start_server(xserver_command, display):
    xvfb = Popen(xserver_command + [':%d' % display])
    # wait for the lock file to make sure the server is running
    lockfile = '/tmp/.X%d-lock' % display
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


def get_x11_display(xserver_command):
    open_display = get_open_display()
    xvfb_proc = start_server(xserver_command, open_display)
    display = ':%d' % open_display
    return (xvfb_proc, display)
