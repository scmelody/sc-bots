import win32api,win32gui,win32con
from core.keyboardData import VK_CODE
import serial
import winreg
from time import sleep
class Click:
    def __init__(self,windowsname,arduino=None):
        self.windowsname = windowsname
        self.arduino = arduino
    def gethwid(self):
        hwid = win32gui.FindWindow('LDPlayerMainFrame',self.windowsname)
        childs = win32gui.FindWindowEx(hwid,None,'RenderWindow','TheRender')
        return childs
    
    def gethwid_edge(self):
        hwid = win32gui.FindWindow('Chrome_WidgetWin_1',self.windowsname)
        return hwid
    
    def gethwid_ragclassic(self):
        hwid = win32gui.FindWindow('Ragnarok','Ragnarok')
        return hwid
    
    def gethwid_raglan(self,name):
        hwid = win32gui.FindWindow('Ragnarok Landverse','Ragnarok Landverse')
        return hwid
    
    def gethwid_ragcls4(self,name):
        hwid = win32gui.FindWindow(name,self.windowsname)
        return hwid
    def getfirefoxid(self):
        hwid = win32gui.FindWindow('MozillaWindowClass',self.windowsname)
        return hwid
    
    def getchromeid(self):
        hwid = win32gui.FindWindow('Chrome_WidgetWin_1',self.windowsname)
        return hwid      
    
    def control_click(self,hwid,x,y):
        l_param = win32api.MAKELONG(x,y)
        win32gui.SendMessage(hwid,win32con.WM_LBUTTONDOWN,win32con.MK_LBUTTON,l_param)
        win32gui.SendMessage(hwid,win32con.WM_LBUTTONUP,win32con.MK_LBUTTON,l_param)
        # Constants for Windows messages
        
        
    def send_key(self,hwid,key):
        keycode = VK_CODE[key]
        #OX70 คือ F11 เอามาจาก 
        #http://www.kbdedit.com/manual/low_level_vk_list.html
        win32api.SendMessage(hwid, win32con.WM_KEYDOWN,keycode, 0)
        win32api.SendMessage(hwid, win32con.WM_KEYUP,keycode, 0)
        
    def send_input(self,hwid, msg):
        for c in msg:
            if c == "\n":
                win32api.SendMessage(hwid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(hwid, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32api.SendMessage(hwid, win32con.WM_CHAR, ord(c), 0)
                
    def bring_window_to_top(self,hwnd):
        try:
            # ตรวจสอบว่า hwnd มีอยู่จริง
            if not win32gui.IsWindow(hwnd):
                print("Invalid hwnd")
                return

            # ดึงหน้าต่างขึ้นมาด้านบนสุด
            win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)  # แสดงหน้าต่าง (ถ้าถูกย่อไว้)
            win32gui.SetForegroundWindow(hwnd)  # ตั้งให้เป็นหน้าต่างที่ Active
            #print("Window is now active and on top.")
        except Exception as e:
            print(f"Error: {e}")
            
    def send_key_PC(self,hwid,key):
        self.bring_window_to_top(hwid)
        keycode = VK_CODE[key]
        #OX70 คือ F11 เอามาจาก 
        #http://www.kbdedit.com/manual/low_level_vk_list.html
        win32api.SendMessage(hwid, win32con.WM_KEYDOWN,keycode, 0)
        win32api.SendMessage(hwid, win32con.WM_KEYUP,keycode, 0)

    def send_input_PC(self,hwid, msg):
        #self.bring_window_to_top(hwid)
        for c in msg:
            if c == "\n":
                win32api.SendMessage(hwid, win32con.WM_KEYDOWN, win32con.VK_RETURN, 0)
                win32api.SendMessage(hwid, win32con.WM_KEYUP, win32con.VK_RETURN, 0)
            else:
                win32api.SendMessage(hwid, win32con.WM_CHAR, ord(c), 0)

    def send_command(self,cmd):
        self.arduino.write(f"{cmd}\n".encode())
        sleep(0.2)
        
    def send_key_arduino(self,hwid,key):
        self.bring_window_to_top(hwid)
        self.send_command(key)

    def send_input_arduino(self,hwid,msg):
        self.bring_window_to_top(hwid)
        self.send_command(msg)

    def cick_move_mouse_arduino(self,hwid,x, y,window_position={'left': 0, 'top': 0, 'width': 0, 'height': 0},resol=1):
        try:
            self.bring_window_to_top(hwid)
            # ✅ Toggle Enhance Pointer Precision ก่อนส่งคำสั่ง
            #self.toggle_pointer_precision()
            # ดึงตำแหน่งเมาส์ปัจจุบัน
            current_x, current_y = win32api.GetCursorPos()
            x= x-(current_x-window_position['left'])
            y = (window_position['top']-current_y)+y
            self.send_command(f"MOVE,{x},{y},{resol}")
            #new_current_x, new_current_y = win32api.GetCursorPos()
            #print(f"start x= {current_x}, y= {current_y}")
            #print(f"x= {x}, y= {y} --> x move : {new_current_x},Y move : {new_current_y}")
            #print(f"MOVE DIF x= {new_current_x-current_x}, y= {new_current_y-current_y}")
            self.send_command("Click")
        except Exception as e:
            print(f"Error: {e}")

    def move_mouse_arduino(self,hwid,x, y,window_position={'left': 0, 'top': 0, 'width': 0, 'height': 0},resol=1):
        try:
            self.bring_window_to_top(hwid)
            current_x, current_y = win32api.GetCursorPos()
            x= x-(current_x-window_position['left'])
            y = (window_position['top']-current_y)+y
            self.send_command(f"MOVE,{x},{y},{resol}")
        except Exception as e:
            print(f"Error: {e}")

    def toggle_pointer_precision(self):
        try:
            path = r"Control Panel\Mouse"
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, path, 0, winreg.KEY_ALL_ACCESS)

            # อ่านค่าเดิม
            current_value, _ = winreg.QueryValueEx(key, "MouseSpeed")
            new_value = "0" if current_value == "1" else "1"

            winreg.SetValueEx(key, "MouseSpeed", 0, winreg.REG_SZ, new_value)
            winreg.SetValueEx(key, "MouseThreshold1", 0, winreg.REG_SZ, "6" if new_value == "1" else "0")
            winreg.SetValueEx(key, "MouseThreshold2", 0, winreg.REG_SZ, "10" if new_value == "1" else "0")

            winreg.CloseKey(key)

            print(f"Toggled Enhance Pointer Precision to: {'ON' if new_value == '1' else 'OFF'}")

        except Exception as e:
            print(f"Failed to toggle pointer precision: {e}")

    # Function to simulate drag and drop
    def drag_and_drop(self,hwid, start_pos, end_pos):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        WM_MOUSEMOVE = 0x0200
        # Convert coordinates to Windows format
        start_x, start_y = start_pos
        end_x, end_y = end_pos
        start_point = win32api.MAKELONG(start_x, start_y)
        end_point = win32api.MAKELONG(end_x, end_y)
        # Simulate left button down event
        win32api.PostMessage(hwid, WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_point)
        # Simulate mouse movement while dragging
        win32api.PostMessage(hwid, WM_MOUSEMOVE, 0, end_point)
        # Simulate left button up event
        win32api.PostMessage(hwid, WM_LBUTTONUP, 0, end_point)

    # Function to simulate click-and-hold
    def click_and_hold(self,hwid, position, hold_duration=0.1):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        # Convert coordinates to Windows format
        x, y = position
        point = win32api.MAKELONG(x, y)
        # Simulate left button down event
        win32api.PostMessage(hwid, WM_LBUTTONDOWN, win32con.MK_LBUTTON, point)
        # Hold the click for the specified duration
        #sleep(hold_duration)
        # Simulate left button up event
        #win32api.PostMessage(hwnd, WM_LBUTTONUP, 0, point)
        # Calculate the delay between each step
        # Simulate left button up event
        #sleep(hold_duration)
        #win32api.PostMessage(hwid, WM_LBUTTONUP, 0, point)   
    # Function to simulate click-and-hold with mouse movement
    def click_hold_and_move(self,hwnd, start_position, end_position, hold_duration):
        WM_LBUTTONDOWN = 0x0201
        WM_LBUTTONUP = 0x0202
        WM_MOUSEMOVE = 0x0200
        # Convert coordinates to Windows format
        start_x, start_y = start_position
        end_x, end_y = end_position
        start_point = win32api.MAKELONG(start_x, start_y)
        end_point = win32api.MAKELONG(end_x, end_y)
        # Simulate left button down event
        win32api.PostMessage(hwnd, WM_LBUTTONDOWN, win32con.MK_LBUTTON, start_point)
        # Calculate the distance to move
        dx = end_x - start_x
        dy = end_y - start_y
        # Calculate the number of steps for mouse movement
        num_steps = max(abs(dx), abs(dy))
        # Calculate the delay between each step
        delay = hold_duration / num_steps
        # Perform mouse movement
        for step in range(1, num_steps + 1):
            # Calculate the intermediate position
            x = start_x + int(dx * step / num_steps)
            y = start_y + int(dy * step / num_steps)
            point = win32api.MAKELONG(x, y)
            # Simulate mouse movement
            win32api.PostMessage(hwnd, WM_MOUSEMOVE, 0, point)
            # Delay between each step
            sleep(delay)
        # Simulate left button up event
        win32api.PostMessage(hwnd, WM_LBUTTONUP, 0, end_point)        
    def cick_move_mouse_pc(self,hwid,x, y):
        try:
            self.bring_window_to_top(hwid)
            # บันทึกตำแหน่งเมาส์ปัจจุบัน
            original_pos = win32api.GetCursorPos()
            hwnd = win32gui.FindWindow(self.windowsname, self.windowsname)  # Change t
            # Get the window's client area position (top-left corner)
            rect = win32gui.GetWindowRect(hwnd)
            # Calculate the absolute screen coordinates of the point to click
            screen_x = rect[0] + x
            screen_y = rect[1] + y
            # Move the mouse to the specified coordinates
            win32api.SetCursorPos((screen_x, screen_y))
            # Adding a short delay can help ensure the click is registered
            sleep(0.1)
            # Perform a left mouse button click
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
            sleep(0.2)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
            sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
