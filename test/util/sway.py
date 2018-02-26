import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
from subprocess import Popen, PIPE, STDOUT

import time

class TestWindow:
    def __init__(self, sway, title):
        self.id = -1
        self.sway = sway
        self.title = title
        env = os.environ.copy()

        if sway.variant == 'sway':
            del env['DISPLAY']
            env['WAYLAND_DISPLAY'] = sway.display
        elif sway.variant == 'i3':
            del env['WAYLAND_DISPLAY']
            env['DISPLAY'] = sway.display

        self.proc = Popen(['test/util/gtk-window.py', '--title', title], env=env, stdout=PIPE, stderr=STDOUT)

    def wait_for_map(self):
        # XXX use the window::new event
        while True:
            q = self.sway.ipc.get_tree().find_named(self.title)

            if not q:
                time.sleep(0.01)
                continue

            con = q[0]
            self.id = con.id
            break

class Sway:
    window_counter = 0

    def __init__(self, ipc, display, variant):
        self.ipc = ipc
        self.display = display
        self.variant = variant


    def open_window(self):

        title = 'window-%d' % Sway.window_counter
        Sway.window_counter += 1

        win = TestWindow(self, title)
        win.wait_for_map()

        return win
