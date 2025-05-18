import pygetwindow as gw

def get_window_position(window_title):
    # หาหน้าต่างที่มีชื่อใกล้เคียง
    windows = gw.getWindowsWithTitle(window_title)
    if not windows:
        print("ไม่พบหน้าต่าง")
        return None

    win = windows[0]  # เลือกหน้าต่างแรกที่เจอ
    if win.isMinimized:
        print("หน้าต่างถูกย่อ")
        return None

    if not win.isActive:
        print("หน้าต่างไม่ใช้งาน")
        return None

    return {
        "left": win.left,
        "top": win.top,
        "width": win.width,
        "height": win.height
    }
if  __name__ == '__main__':
    # ทดสอบ
    info = get_window_position("Ragnarok")  # ใส่ชื่อหน้าต่างเกมที่คุณเห็นใน Title bar
    if info:
        print(f"ตำแหน่งหน้าต่าง: {info}")
