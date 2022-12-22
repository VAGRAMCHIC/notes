from __future__ import division
import math
import time
import cairo
import gi
import random
import sys

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, Adw




class Brush(object):
    def __init__(self, width, rgba_color):
        self.width = width
        self.rgba_color = rgba_color
        self.stroke = []

    def add_point(self, point):
        self.stroke.append(point)

class Canvas(Gtk.DrawingArea):
    def __init__(self, height, **kwargs):
        super().__init__(**kwargs)
        self.set_draw_func(self.draw, None)
        self.set_size_request(400, 400)

        self.mouse_event_controller = Gtk.GestureClick.new()
        self.mouse_event_controller.connect('pressed', self.mouse_press)
        self.mouse_event_controller.connect('released', self.mouse_release)
        self.add_controller(self.mouse_event_controller)

        self.mouse_move_controller = Gtk.EventControllerMotion.new()
        self.mouse_move_controller.connect("motion", self.mouse_move)
        self.add_controller(self.mouse_move_controller)
      
        
        self.brushes = []


    def draw(self, widget, cr, *args):
        cr.set_source_rgba(255, 255, 255, 1)
        cr.paint()
        for brush in self.brushes:
            cr.set_source_rgba(*brush.rgba_color)
            cr.set_line_width(brush.width)
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in brush.stroke:
                cr.line_to(x, y)
            cr.stroke()


    def mouse_move(self, motion, x, y):
        if str(motion.get_current_event_state()) == str(Gdk.ModifierType.BUTTON1_MASK):
            try:
                curr_brush = self.brushes[-1]
                curr_brush.add_point((x, y))
            except:
                pass
        self.queue_draw()
            

    def mouse_press(self, gesture, data, x, y):
        if data == Gdk.BUTTON_PRIMARY:
            rgba_color = (random.random(), random.random(), random.random(), 0.5)
            brush = Brush(12, rgba_color)
            brush.add_point((x, y))
            self.brushes.append(brush)
            self.queue_draw()


    def mouse_release(self, gesture, data, x, y):
        if gesture.get_button() == Gdk.BUTTON_PRIMARY:
            self.queue_draw()


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