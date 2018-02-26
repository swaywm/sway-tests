#!/usr/bin/env python3
from argparse import ArgumentParser
import time
from threading import Thread
import sys
import uuid

parser = ArgumentParser(description='A helper program to open up a test window')
parser.add_argument('--title', help='the title of the window', default=uuid.uuid4())

args = parser.parse_args()

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

win = Gtk.Window(title=args.title)
win.connect('delete-event', Gtk.main_quit)
win.show_all()

Gtk.main()
