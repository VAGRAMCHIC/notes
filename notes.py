#from __future__ import division
import math
import time
import cairo
import gi
import random
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw

from src.drawing import Brush, Canvas


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = 400
        self.height = 400
        self.canvas = Canvas(self.height)
        self.canvas.set_halign(Gtk.Align.FILL)
        self.canvas.set_valign(Gtk.Align.FILL)
        self.canvas_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        self.canvas_box.set_halign(Gtk.Align.FILL)
        self.canvas_box.set_valign(Gtk.Align.FILL)
        self.set_child(self.canvas_box)
        self.canvas_box.append(self.canvas)


class App(Adw.Application):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application = app)
        self.win.present()

    def close(self, window):
        Gtk.main_quit()

if __name__ == "__main__":
    app=App(application_id="com.example.GtkApplication")
    app.run(sys.argv)