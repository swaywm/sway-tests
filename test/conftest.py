#!/usr/bin/env python3

import i3ipc
from util.x_display import get_x11_display
from util.sway import Sway
from subprocess import Popen, PIPE, STDOUT, check_output
import os
import sys
import time
import pytest

sway_path = ''


def pytest_addoption(parser):
    parser.addoption("--sway", help="the sway binary to test")


def pytest_generate_tests(metafunc):
    global sway_path
    if metafunc.config.getoption('sway'):
        sway_path = metafunc.config.getoption('sway')
    else:
        pytest.exit(
            'missing required argument: --sway to determine sway binary location'
        )


@pytest.yield_fixture()
def sway():
    assert (sway_path)

    version = check_output([sway_path, '--version']).decode('utf-8')

    variant = 'unknown'

    if version.startswith('i3'):
        variant = 'i3'
    elif version.startswith('sway'):
        variant = 'sway'
    else:
        print('unknown binary variant')
        print(version)
        pytest.exit()

    display = None
    proc = None

    if variant == 'i3':
        display = get_x11_display()
        env = os.environ.copy()
        env['DISPLAY'] = display
        proc = Popen(
            [sway_path, '-c', 'test/configs/default.conf'],
            env=env,
            stdout=PIPE,
            stderr=STDOUT)
    elif variant == 'sway':
        proc = Popen(
            [sway_path, '-H', '-d', '-c', 'test/configs/default.conf'],
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
