#!/usr/bin/env python3

import i3ipc
from util.x_display import get_x11_display
from util.sway import Sway
from subprocess import Popen, PIPE, STDOUT, check_output
import os
import sys
import time
import pytest
from shutil import which

XVFB = 'Xvfb'
XEPHYR = 'Xephyr'
LSOF = 'lsof'

sway_path = ''
headless = False

def check_dependencies(variant, headless):
    if variant == 'i3':

        xvfb_path = which(XVFB)
        lsof_path = which(LSOF)
        xephyr_path = which(XEPHYR)

        if not lsof_path:
            pytest.exit('''
            lsof is required to run tests
            Command "{}" not found in PATH
            '''.format(LSOF))

        if headless and not xvfb_path:
            pytest.exit('''
            Xvfb is required to run tests in headless mode
            Command "{}" not found in PATH
            '''.format(XVFB))

        if not headless and not xephyr_path:
            pytest.exit('''
            Xephyr is required to run tests in headless mode
            Command "{}" not found in PATH
            '''.format(XEPHYR))


def pytest_addoption(parser):
    parser.addoption("--sway", help="the sway binary to test")
    parser.addoption("--headless", help="run in headless mode", action='store_true')


def pytest_generate_tests(metafunc):
    global sway_path, headless
    if metafunc.config.getoption('sway'):
        sway_path = metafunc.config.getoption('sway')

        if metafunc.config.getoption('headless'):
            headless = True

    else:
        pytest.exit(
            'missing required argument: --sway to determine sway binary location'
        )


@pytest.fixture(scope='function')
def sway():
    assert sway_path

    version = check_output([sway_path, '--version']).decode('utf-8')

    variant = 'unknown'

    if version.startswith('i3'):
        variant = 'i3'
    elif version.startswith('sway'):
        variant = 'sway'
    else:
        print('unknown binary variant')
        print(version)
        pytest.exit('Unknown binary variant\n%s'.format(version))

    check_dependencies(variant, headless)

    display = None
    proc = None

    if variant == 'i3':
        xserver_command = ''

        if headless:
            xserver_command = which(XVFB)
        else:
            xserver_command = which(XEPHYR)

        display = get_x11_display(xserver_command)
        env = os.environ.copy()
        env['DISPLAY'] = display
        proc = Popen(
            [sway_path, '-c', 'test/configs/default.conf'],
            env=env,
            stdout=PIPE,
            stderr=STDOUT)
    elif variant == 'sway':
        if headless:
            proc = Popen(
                [sway_path, '-H', '-d', '-c', 'test/configs/default.conf'],
                stdout=PIPE,
                stderr=STDOUT)
        else:
            proc = Popen(
                [sway_path, '-d', '-c', 'test/configs/default.conf'],
                stdout=PIPE,
                stderr=STDOUT)

    with proc:

        def get_socketpath(pid, variant):
            uid = os.getuid()
            if variant == 'sway':
                fmt = '/run/user/{uid}/sway-ipc.{uid}.{pid}.sock'
            elif variant == 'i3':
                fmt = '/run/user/{uid}/i3/ipc-socket.{pid}'
            return fmt.format(uid=uid, pid=pid)

        socket_path = get_socketpath(proc.pid, variant)

        ipc = None
        tries = 0

        while True:
            try:
                ipc = i3ipc.Connection(socket_path=socket_path)
                break
            except Exception as e:
                tries += 1
                if (tries > 100):
                    raise e
                time.sleep(0.001)

        if variant == 'sway':
            # XXX this is a hacky way to get the WAYLAND_DISPLAY
            ipc.command('exec env')
            while not display:
                line = str(proc.stdout.readline(), 'utf-8')
                if 'WAYLAND_DISPLAY' in line:
                    display = line.split('=')[1].rstrip()
                    break

        sway = Sway(ipc, display, variant)
        yield sway
        proc.terminate()
