import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GLib
import os
from subprocess import Popen, PIPE, STDOUT
from .gtk_window_starter import GtkWindowStarter
from i3ipc import Con
import uuid

class TestWindow:
    def __init__(self, sway, title, window_starter):
        self.id = -1
        self.sway = sway
        self.title = title
        env = os.environ.copy()
        self.con = None

        window_starter.start_window(title)
        print('starting the window')

        self.con = sway.ipc.get_tree().find_named(title)
        '''
        def on_window_new(ipc, e):
            if e.container.name == title:
                self.id = e.container.id
                self.con = e.container
                ipc.main_quit()

        sway.ipc.on('window::new', on_window_new)
        sway.ipc.main(timeout=1)
        sway.ipc.off(on_window_new)
        '''

        if self.con == None:
            raise Exception('could not open a new window')

    def close(self):
        self.con.command('kill')

        def on_window_close(ipc, e):
            if e.container.name == self.title:
                ipc.main_quit()

        self.sway.ipc.on('window::close', on_window_close)
        self.sway.ipc.main(timeout=5)
        self.sway.ipc.off(on_window_close)

    def focus(self):
        self.con.command('focus')

    def command(self, cmd):
        self.con.command(cmd)


class Sway:
    window_counter = 1

    def __init__(self, ipc, display, variant):
        self.ipc = ipc
        self.display = display
        self.variant = variant

        self.window_starter = GtkWindowStarter(display)
        self.window_starter.start()

    def open_window(self, title=None):
        if not title:
            title = 'window-%d' % Sway.window_counter
            Sway.window_counter += 1

        return TestWindow(self, title, self.window_starter)

    def focused(self):
        root = self.ipc.get_tree()
        return root.find_focused()

    def cmd(self, content):
        return self.ipc.command(content)

    def workspace(self):
        return self.ipc.get_tree().find_focused().workspace()
