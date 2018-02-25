#!/usr/bin/env python3

import i3ipc
from subprocess import Popen, PIPE, STDOUT
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


class Sway:
    def __init__(self, ipc, display):
        self.ipc = ipc
        self.display = display


@pytest.fixture()
def sway():
    print(sway_path)
    assert (sway_path)

    with Popen(
        [sway_path, '-H', '-d', '-c', 'test/sway.conf'],
            stdout=PIPE,
            stderr=STDOUT) as sway_proc:

        def get_socketpath(pid):
            uid = os.getuid()
            fmt = '/run/user/{uid}/sway-ipc.{uid}.{pid}.sock'
            return fmt.format(uid=uid, pid=pid)

        socket_path = get_socketpath(sway_proc.pid)

        ipc = None
        tries = 0

        while True:
            try:
                ipc = i3ipc.Connection(socket_path=socket_path)
                break
            except Exception as e:
                tries += 1
                if (tries > 10):
                    raise e
                time.sleep(0.1)

        # XXX this is a hacky way to get the WAYLAND_DISPLAY
        ipc.command('exec env')
        display = None
        while not display:
            line = str(sway_proc.stdout.readline(), 'utf-8')
            if 'WAYLAND_DISPLAY' in line:
                display = line.split('=')[1].rstrip()

        yield Sway(ipc, display)
        sway_proc.terminate()
