from subprocess import Popen
import time
from shutil import which
from os import listdir, path
import re
import pytest
import atexit

display = None
xvfb_proc = None
XVFB = 'Xvfb'
LOCKDIR = '/tmp'


def get_open_display():
    # TODO find the general lock directory
    lock_re = re.compile(r'^\.X([0-9]+)-lock$')
    lock_files = [f for f in listdir(LOCKDIR) if lock_re.match(f)]
    displays = [int(lock_re.search(f).group(1)) for f in lock_files]
    open_display = min(
        [i for i in range(0,
                          max(displays or [0]) + 2) if i not in displays])
    return open_display


def start_server(display):
    xvfb = Popen([XVFB, ':%d' % display])
    # wait for the lock file to make sure the server is running
    lockfile = path.join(LOCKDIR, '.X%d-lock' % display)
    tries = 0
    while True:
        if path.exists(lockfile):
            break
        else:
            tries += 1

            if tries > 100:
                print('could not start x server')
                xvfb.kill()
                sys.exit(1)

            time.sleep(0.1)

    return xvfb


def check_dependencies():
    if not which(XVFB):
        print('Xvfb is required to run tests')
        print('Command "%s" not found in PATH' % XVFB)
        pytest.exit(127)


@atexit.register
def at_exit():
    if xvfb_proc:
        xvfb_proc.terminate()


def get_x11_display():
    global display
    global xvfb_proc

    if display:
        return display

    check_dependencies()
    open_display = get_open_display()
    xvfb_proc = start_server(open_display)
    display = ':%d' % open_display
    return display
