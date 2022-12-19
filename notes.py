from __future__ import division
import math
import time
import cairo
import gi
import random
import sys

from gi.repository import Gtk, Gdk, Adw


gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')


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
        self.set_size_request(200, 200)

        mouse_event_controller = Gtk.GestureClick.new()
        mouse_event_controller.connect('pressed', self.mouse_press)
        mouse_event_controller.connect('released', self.mouse_release)

        self.add_controller(mouse_event_controller)

        mouse_move_controller = Gtk.EventControllerMotion.new()
        mouse_move_controller.connect("motion", self.mouse_move)
        self.add_controller(mouse_move_controller)

        print(dir(Gtk))
        #mouse_release_controller = Gdk.GestureClick.new()
        #mouse_release_controller.connect('release', self.mouse_release)
        #self.add_controller(mouse_release_controller)
        
        self.brushes = []

    def draw(self, widget, cr, *args):
        da = widget
        print(args)
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
            

    def mouse_press(self, gesture,data, x, y):
        print(gesture.get_button())
        if gesture.get_button() == 1:
            rgba_color = (random.random(), random.random(), random.random(), 0.5)
            brush = Brush(12, rgba_color)
            brush.add_point((x, y))
            self.brushes.append(brush)
            self.queue_draw()
        elif gesture == Gdk.BUTTON_SECONDARY:
            self.brushes = []

    def mouse_release(self, gesture,data, x, y):
        self.queue_draw()


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.width = 400
        self.height = 400
        self.canvas = Canvas(self.height)

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