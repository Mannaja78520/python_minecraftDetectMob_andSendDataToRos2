import numpy as np
from PIL import Image
import Xlib.display

class WindowCapture:

    # properties
    w = 0
    h = 0
    window = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0

    # constructor
    def __init__(self, identifier, id_type='name'):
        display = Xlib.display.Display()
        root = display.screen().root
        window_id_list = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType).value

        if id_type == 'name':
            self.window = self._get_window_by_name(display, window_id_list, identifier)
        elif id_type == 'pid':
            self.window = self._get_window_by_pid(display, window_id_list, identifier)
        elif id_type == 'windowid':
            self.window = display.create_resource_object('window', identifier)
        else:
            raise ValueError("Invalid id_type. Must be 'name', 'pid', or 'windowid'.")

        if not self.window:
            raise Exception(f'Window not found: {identifier}')

        # get the window size
        geometry = self.window.get_geometry()
        self.w = geometry.width
        self.h = geometry.height

        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = geometry.x + self.cropped_x
        self.offset_y = geometry.y + self.cropped_y

    def _get_window_by_name(self, display, window_id_list, name):
        for wid in window_id_list:
            window = display.create_resource_object('window', wid)
            if window.get_wm_name() and name in window.get_wm_name():
                return window
        return None

    def _get_window_by_pid(self, display, window_id_list, pid):
        for wid in window_id_list:
            window = display.create_resource_object('window', wid)
            window_pid = window.get_full_property(display.intern_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
            if window_pid and window_pid.value[0] == pid:
                return window
        return None

    def get_screenshot(self):
        raw = self.window.get_image(0, 0, self.w, self.h, Xlib.X.ZPixmap, 0xffffffff)
        img = Image.frombytes("RGB", (self.w, self.h), raw.data, "raw", "BGRX")
        img = np.array(img)

        # make image C_CONTIGUOUS
        img = np.ascontiguousarray(img)

        return img

    @staticmethod
    def list_window_names():
        display = Xlib.display.Display()
        root = display.screen().root
        window_id_list = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), Xlib.X.AnyPropertyType).value

        for wid in window_id_list:
            window = display.create_resource_object('window', wid)
            name = window.get_wm_name()
            if name is None:
                name = "(no name)"
            pid = window.get_full_property(display.intern_atom('_NET_WM_PID'), Xlib.X.AnyPropertyType)
            pid = pid.value[0] if pid else "(no PID)"
            print(f'Window ID: {hex(wid)}, Name: {name}, PID: {pid}')