#from __future__ import division
import cairo
import gi
import random

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Gdk, GObject



class Brush(object):
    def __init__(self, width, rgba_color):
        self.width = width
        self.rgba_color = rgba_color
        self.stroke = []

    def add_point(self, point):
        self.stroke.append(point)



class ColorDialog():

    __gsignals__ = {
        "color-activated": (GObject.SIGNAL_RUN_FIRST, None,
                            (Gtk.ColorChooser, Gdk.RGBA))
    }

    def __init__(self) -> None:
        self.chooser = Gtk.ColorChooserDialog().new()
        self.chooser.show()
        self.chooser.set_title('color chose')
        self.chooser.set_modal(modal=True)
        self.chooser.connect('response', self.dialog_response)
        self.rgba = None
        self.chooser.connect('color-activated', self.on_color_activated)

    def dialog_response(self, widget, response):
        if response == Gtk.ResponseType.OK:
            widget.close()
            self.on_color_activated(self.chooser, self.get_rgba())
        widget.close()

    def on_color_activated(self, chooser, color):
        self.emit('color-activated', chooser, color)
        self.set_rgba(color)

    def get_rgba(self):
        return self.chooser.get_rgba()

    def set_rgba(self, color):
        self.chooser.set_rgba(color)

    def add_palette(self, orientation, colors_per_line, colors):
        self.chooser.add_palette(orientation, colors_per_line, colors)

    def on_close(self):
        self.on_color_activated(self.chooser, self.get_rgba())



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
      
        self.rgba_color = (0,0,0,1)

        self.color = None

        
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
            print(self.rgba_color[0], self.rgba_color[1], self.rgba_color[2], self.rgba_color[3])
        elif str(motion.get_current_event_state()) == str(Gdk.ModifierType.BUTTON3_MASK):
            try: 
                self.color = ColorDialog()
            except:
                pass

        self.queue_draw()
            

    def mouse_press(self, gesture, data, x, y):
        #print(dir(gesture.get_current_event_state()))
        #print(str(gesture.get_current_event_state()), str(Gdk.ModifierType.BUTTON1_MASK))
        if data == Gdk.BUTTON_PRIMARY:
            brush = Brush(12, self.rgba_color)
            brush.add_point((x, y))
            self.brushes.append(brush)
            self.queue_draw()


    def mouse_release(self, gesture, data, x, y):
        #print(str(gesture.get_current_event_state()), str(Gdk.ModifierType.BUTTON1_MASK))
        if gesture.get_button() == Gdk.BUTTON_PRIMARY:
            self.queue_draw()