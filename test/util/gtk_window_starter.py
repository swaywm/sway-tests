#!/usr/bin/env python3
from argparse import ArgumentParser
import time
from multiprocessing import Process
import sys
import uuid
import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from dbus.exceptions import DBusException
import os

class GtkService(dbus.service.Object):
    def __init__(self, window_starter):
        DBusGMainLoop(set_as_default=True)
        name = '/org/swaywm/test/' + str(window_starter.dbus_name)
        self.gtk = window_starter.gtk
        self.gdk = window_starter.gdk
        self.display = window_starter.display
        bus = dbus.SessionBus()
        bus_name = dbus.service.BusName('org.swaywm.test' + str(window_starter.dbus_name), bus=bus)
        dbus.service.Object.__init__(self, bus_name, name)

    @dbus.service.method('org.swaywm.test', in_signature='s')
    def start_window(self, title):
        display = self.gdk.Display.open(self.display)
        screen = display.get_screen(0)
        win = self.gtk.Window(title=title)
        win.set_screen(screen)
        win.show_all()

class GtkWindowStarter(Process):
    index = 0

    def __init__(self, display):
        GtkWindowStarter.index += 1

        self.display = display
        self.main_loop = None
        self.gtk = None
        self.bus = None
        self.dbus_name = str(GtkWindowStarter.index)
        super(GtkWindowStarter, self).__init__()

    def run(self):
        import gi
        gi.require_version('Gtk', '3.0')
        gi.require_version('Gdk', '3.0')
        from gi.repository import Gtk, Gdk, GLib

        self.gtk = Gtk
        self.gdk = Gdk

        self.main_loop = GLib.MainLoop()

        self.service = GtkService(self)
        self.main_loop.run()

    def _send_start_window(self, title):
        if self.bus is None:
            bus = dbus.SessionBus()

        obj = bus.get_object('org.swaywm.test' + str(self.dbus_name), f'/org/swaywm/test/{self.dbus_name}')
        iface = dbus.Interface(obj, dbus_interface='org.swaywm.test')
        iface.start_window(title)

    def start_window(self, title):
        last_exception = None
        for i in range(0, 100):
            try:
                self._send_start_window(str(title))
                return
            except DBusException as e:
                last_exception = e
                time.sleep(0.01)

        raise last_exception
