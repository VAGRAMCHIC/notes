from __future__ import division
import math
import time
import cairo
import gi; gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, Gdk, Adw
import random
import sys

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
        self.height = height
        
        mouse_event_controller = Gtk.GestureClick.new()
        mouse_event_controller.connect('pressed', self.mouse_press)
        self.add_controller(mouse_event_controller)

        mouse_move_controller = Gtk.EventControllerMotion.new()
        mouse_move_controller.connect("motion", self.mouse_move)
        self.add_controller(mouse_move_controller)
        
        self.brushes = []

    def draw(self, widget, cr):
        da = widget
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
        #cr.set_operator(cairo.OPERATOR_SOURCE)#gets rid over overlap, but problematic with multiple colors
        for brush in self.brushes:
            cr.set_source_rgba(*brush.rgba_color)
            cr.set_line_width(brush.width)
            cr.set_line_cap(1)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.new_path()
            for x, y in brush.stroke:
                cr.line_to(x, y)
            cr.stroke()

    def init_draw_area(self):
        draw_area = Gtk.DrawingArea()
        draw_area.set_draw_func(self.draw, None)
        #draw_area.set_motion_notify_event_func(self.mouse_move, None)
        #draw_area.connect('button-press-event', self.mouse_press)
        #draw_area.connect('button-release-event', self.mouse_release)
        #draw_area.set_events(draw_area.get_events() |
        #    Gdk.EventMask.BUTTON_PRESS_MASK |
        #    Gdk.EventMask.POINTER_MOTION_MASK |
        #    Gdk.EventMask.BUTTON_RELEASE_MASK)
        return draw_area

    def mouse_move(self, motion, x, y):
        print([x,y])
        if motion :
            curr_brush = self.brushes[-1]
            curr_brush.add_point((x, y))
            self.queue_draw()
            

    def mouse_press(self, gesture, data, x, y):
        if data.button == Gdk.BUTTON_PRIMARY:
            rgba_color = (random.random(), random.random(), random.random(), 0.5)
            brush = Brush(12, rgba_color)
            brush.add_point((data.x, data.y))
            self.brushes.append(brush)
            self.queue_draw()
        elif self.button == Gdk.BUTTON_SECONDARY:
            self.brushes = []

    def mouse_release(self, widget, event):
        widget.queue_draw()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = 400
        self.height = 400
        self.canvas = Canvas(self.height)
        self.canvas_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
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