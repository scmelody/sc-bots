import win32gui
import win32ui
import win32con
import numpy as np
from ctypes import windll, byref, sizeof
from ctypes.wintypes import RECT
from PIL import Image
from core.detect_window import *
import pygetwindow as gw

class WindowCapture:
    def __init__(self, window_name):
        self.window_name = window_name
        if window_name == "Ragnarok":
            self.hwnd = win32gui.FindWindow("Ragnarok", "Ragnarok")
        elif window_name == "Ragnarok Landverse":
            self.hwnd = win32gui.FindWindow(window_name, window_name)
        elif window_name == "GNJOY - Google Chrome":
            self.hwnd = win32gui.FindWindow('Chrome_WidgetWin_1', 'GNJOY - Google Chrome')
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))

    def get_window_postion(self):
        return get_window_position(self.window_name)
    
    def windows_resize(self,window_name,size):
        for win in gw.getWindowsWithTitle(window_name):
            if window_name in win.title:
                window_title = win
                break

        if window_title:
            # ทำให้หน้าต่าง LDPlayer อยู่ด้านหน้า
            window_title.activate()

            # ปรับขนาดหน้าต่างเป็น 964x555
            window_title.resizeTo(size[0], size[1])
            print("ปรับขนาดหน้าต่างเรียบร้อย!")
        else:
            print("ไม่พบหน้าต่าง LDPlayer")
    def get_window_rect(self,hwnd):
        rect = RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9  # ค่าที่ใช้กับ DwmGetWindowAttribute
        windll.dwmapi.DwmGetWindowAttribute(hwnd, DWMWA_EXTENDED_FRAME_BOUNDS, byref(rect), sizeof(rect))
        return rect.left, rect.top, rect.right, rect.bottom
    
    
    def capture_window(self,hwnd, capture_rect=None):
        left, top, right, bottom = win32gui.GetWindowRect(hwnd)

        width = right - left
        height = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, width, height)
        save_dc.SelectObject(bitmap)

        save_dc.BitBlt((0, 0), (width, height), mfc_dc, (0, 0), win32con.SRCCOPY)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[..., :3]  # ตัด alpha ออก
        img = np.ascontiguousarray(img)

        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwnd_dc)

        return img



    def screenshot(self, capture_rect=None):
        if capture_rect is None:
            left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        else:
            x,y,w,h = capture_rect
            capture_rect = [x, y, (x*2)+w, (y*2)+h]
            left, top, right, bottom = capture_rect

        # ปรับขนาดของพื้นที่ที่ต้องการ
        capture_w = right - left
        capture_h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # ปรับขนาดของ bitmap ให้ตรงกับพื้นที่ที่ต้องการบันทึก
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, capture_w, capture_h)
        save_dc.SelectObject(bitmap)
        

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[..., :3]
        img = np.ascontiguousarray(img)

        img = img[top:capture_h, left:capture_w, :]
        
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)
        
        pil_img = Image.fromarray(img)
        pil_img.save("test.png")
        return img

    def mask_player_area(self,img, box_area):
        x, y, w, h = box_area
        img[y:y+h, x:x+w] = 0  # ใส่เป็นสีดำ
        return img

    def screenshot_grayScale(self, capture_rect=None):
        if capture_rect is None:
            left, top, right, bottom = win32gui.GetClientRect(self.hwnd)
        else:
            x,y,w,h = capture_rect
            capture_rect = [x, y, (x*2)+w, (y*2)+h]
            left, top, right, bottom = capture_rect

        # ปรับขนาดของพื้นที่ที่ต้องการ
        capture_w = right - left
        capture_h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()

        # ปรับขนาดของ bitmap ให้ตรงกับพื้นที่ที่ต้องการบันทึก
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, capture_w, capture_h)
        save_dc.SelectObject(bitmap)
        

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[..., :3]
        img = np.ascontiguousarray(img)

        img = img[top:capture_h, left:capture_w, :]
        
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)
        
        pil_img = Image.fromarray(img)
        pil_img = pil_img.convert("L")
        # ใช้ Thresholding เพื่อปรับค่าพิกเซลให้ชัดเจนขึ้น
        pil_img = pil_img.point(lambda p: p > 150 and 255)  # Threshold to make text more distinct
        pil_img.save("test.png")
        return pil_img