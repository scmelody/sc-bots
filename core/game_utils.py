import sys
import os
import time
from time import sleep
import json
from sympy import true
from module.Myclassbot import *
from module.Classclick import *
import pytesseract
from datetime import datetime
from module.arduino import *

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            img = os.path.join(folder, filename)#cv.imread(os.path.join(folder, filename), cv.IMREAD_GRAYSCALE)
            if img is not None:
                images.append(img)
    return images

def load_imges(list_folder_paths):
    path_images = {}
    for folder in list_folder_paths:
        # ดึงชื่อโฟลเดอร์สุดท้าย
        #folder_name = os.path.basename(folder)
        name = folder.replace('\\', '_').replace('imgs_', '')
        #monster_img = monster_img+load_images_from_folder(folder_path)
        
        images = load_images_from_folder(folder)
        path_images[name] = images  # ใช้ชื่อ folder เป็น key และภาพเป็น value
        # ลบ key ที่ value เป็น []
        filtered_data = {k: v for k, v in path_images.items() if v != []}
    return filtered_data

def read_folder( folder_path):
    folders = []
    for f in os.listdir(folder_path):
        if f:
            folders.append(os.path.join(folder_path, f))
    return folders

def read_folder_sub( folder_path):
    list_folder_paths = []
    # อ่านโฟลเดอร์ทั้งหมดรวม subfolder
    for root, dirs,files in os.walk(folder_path):
        for dir in dirs:
            list_folder_paths.append(os.path.join(root, dir))
    return list_folder_paths

def read_subfolders(path, max_depth):
    subfolders = []
    for root, dirs, files in os.walk(path):
        # คำนวณระดับชั้นปัจจุบัน
        depth = root[len(path):].count(os.sep)
        if depth < max_depth:
            subfolders.extend([os.path.join(root, d) for d in dirs])
    return subfolders

def dict_keys_contain(data,text):
    # กรองเฉพาะ key ที่มี 'pixal'
    if isinstance(text, str):
        filtered_dict = {k: v for k, v in data.items() if text in k}
    if isinstance(text, list):
        filtered_dict = {
            k: v for k, v in data.items() 
            if all(word in k for word in text)
        }
    return filtered_dict

def find_imgs_screen(windows,images,capture_rect=None,threshold=0.8,paralle_mode = False,debug=False):
    if capture_rect is None:
        screenshot_tmp = windows.screenshot()
    else:
        screenshot_tmp = windows.screenshot(capture_rect)

    #screenshot_tmp.save("test.png")
    found_monster = {}
    group_points = {}
    group_monster_points_all =[]
    for name, imgs in images.items():
        dict_imgs = {'name': name, 'imgs': imgs}
        _bot = Classbot(screenshot_tmp, dict_imgs,debug=debug)
        if paralle_mode:
            group_point = _bot.search_parallel(debug=debug,threshold=threshold)
        else:
            group_point = _bot.search(debug=debug,threshold=threshold)
        group_points[f'{name}'] = group_point
        #group_monster_points_all = group_monster_points_all+group_point

    #print(group_monster_points)

    return group_points

def find_imgs(windows,images,capture_rect=None,threshold=0.8,paralle_mode = False,debug=False):
    if capture_rect is None:
        screenshot_tmp = windows.screenshot()
    else:
        screenshot_tmp = windows.screenshot(capture_rect)

    #screenshot_tmp.save("test.png")
    found_monster = {}
    group_points = {}
    group_monster_points_all =[]
    for name, imgs in images.items():
        dict_imgs = {'name': name, 'imgs': imgs}
        _bot = Classbot(screenshot_tmp, dict_imgs,debug=debug)
        if paralle_mode:
            group_point = _bot.search_parallel(debug=debug,threshold=threshold)
        else:
            group_point = _bot.search(debug=debug,threshold=threshold)
        group_points[f'{name}_point'] = group_point
        #group_monster_points_all = group_monster_points_all+group_point

    #print(group_monster_points)

    return group_points

def find_imgs_2(bot,images,capture_rect=None,threshold=0.8,paralle_mode = False,debug=False):

    screenshot_tmp = bot.mainimg
    #screenshot_tmp.save("test.png")
    found_monster = {}
    group_points = {}
    group_monster_points_all =[]
    for name, imgs in images.items():
        dict_imgs = {'name': name, 'imgs': imgs}
        #_bot = Classbot(screenshot_tmp, dict_imgs,debug=True)
        bot.tempimg=dict_imgs
        if paralle_mode:
            group_point = bot.search_parallel(debug=debug,threshold=threshold)
        else:
            group_point = bot.search(debug=debug,threshold=threshold)
        group_points[f'{name}_point'] = group_point
        #group_monster_points_all = group_monster_points_all+group_point

    #print(group_monster_points)

    return group_points

def get_point(points):
    point =[]
    points = {k: v for k, v in points.items() if v != []}
    for key in points.keys():
        point = point+points[key]
    return point

def check_screen_active(points,key_n):
    name_keys={key_n:[]}
    points = {k: v for k, v in points.items() if v != []}
    #print(filtered_data)
    for key in points.keys():
        #name_keys.append(key)
        # แยกข้อมูลในรายการ
        key_value = key.split('_')

        # สร้างดิกชันนารีจากส่วนที่ต้องการ
        name_keys[key_n].append(key_value[len(key_value)-1])
    name_keys[key_n]=list(set(name_keys[key_n]))
    return name_keys

def screen_name_active(windows,dict_folder_paths,key_name=['screen']):
    points=find_imgs_screen(windows,dict_keys_contain(dict_folder_paths,key_name),threshold=0.90,paralle_mode=True)
    # ใช้ keys() และดึงค่าทั้งหมดออกมา
    screen = check_screen_active(points,key_name[0])
    if screen:
        return screen
    return False

def check_ingame(windows,dict_folder_paths,game_name):
    points=find_imgs(windows,dict_keys_contain(dict_folder_paths,[game_name,'ingame']),threshold=0.90)
    # ใช้ keys() และดึงค่าทั้งหมดออกมา
    point =[]
    for key in points.keys():
        point = point+points[key]
    if point:
        return True
    return False

def click_ld(hwid,click,point,x_add=0,y_add=-34,sleep_time=0.5):
    if point:
        click.control_click(hwid, point[0][0]+x_add, point[0][1]+y_add)
        sleep(sleep_time)
        return True
    return False

def click_web(hwid,click,point,x_add=0,y_add=0,sleep_time=0.5):
    if point:
        click.control_click(hwid, point[0][0]+x_add, point[0][1]+y_add)
        sleep(sleep_time)
        return True
    return False

def click_line_game(hwid,click,point,x_add=0,y_add=-5,sleep_time=0.5):
    if point:
        click.control_click(hwid, point[0][0]+x_add, point[0][1]+y_add)
        sleep(sleep_time)
        return True
    return False

def click_ld_loop(hwid,click,point,x_add=0,y_add=-34,sleep_time=0.5,loop=1):
    for i in range(0,loop):
        click.control_click(hwid, point[0][0]+x_add, point[0][1]+y_add)
        sleep(sleep_time)

def click_albion(click,point,x_add=0,y_add=0,sleep_time=0.5):
    if point:
        click.click_pc_albion( point[0][0]+x_add, point[0][1]+y_add)
        sleep(sleep_time)
        return True
    return False

def close_char_point(point,char_point):
    # คำนวณและเรียงลำดับตำแหน่งตามระยะทาง
    print(point)
    print(char_point)
    sorted_positions = sorted(point, key=lambda pos: np.sqrt((pos[0] - char_point[0])**2 + (pos[1] - char_point[1])**2))
    return sorted_positions

def text_img(windows,img=None,capture_rect=None,lang="eng"):
    if img is None:
        if capture_rect is None:
            img = windows.screenshot_rgb()
        else:
            img = windows.screenshot_rgb(capture_rect)
    # ระบุ path ของ Tesseract OCR (สำหรับ Windows เท่านั้น)
    pytesseract.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'
    # อ่านข้อความจากรูปภาพ
    text = pytesseract.image_to_string(img, lang=lang)  # lang="eng" สำหรับภาษาอังกฤษ
    return text


def find_check(windows,dict_folder_paths,key_name,debug=False,threshold=0.80,paralle_mode=False):
    try:
        points=find_imgs(windows,dict_keys_contain(dict_folder_paths,key_name),threshold=threshold,debug=debug,paralle_mode=paralle_mode)
        point =get_point(points)
        if point:
            return True
        return False
    except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")


def keyboard_msg_PC(hwid,click : Click,msg,print_sts = True):
    try:
        click.send_key_PC(hwid,'del')
        click.send_input_PC(hwid,msg)
        if print_sts:
            print(f"กรอกข้อความ {msg} สำเร็จ")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

def keyboard_msg_arduino(hwid,click : Click,msg,print_sts = True):
    try:
        click.send_key_arduino(hwid,'Del')
        click.send_input_arduino(hwid,msg)
        if print_sts:
            print(f"กรอกข้อความ {msg} สำเร็จ")
        return True
    except Exception as e:
        print(f"เกิดข้อผิดพลาด: {e}")

def find_click(hwid,windows,click : Click,dict_folder_paths,debug=False,key_name=[],click_count=1,msg_text='',threshold=0.90,paralle_mode=False,add_x=0,add_y=0):
    try:
        points=find_imgs(windows,dict_keys_contain(dict_folder_paths,key_name),threshold=threshold)
        point =get_point(points)
        if point:
            win_posi = windows.get_window_postion()
            for i in range(click_count):
                click.cick_move_mouse_arduino(hwid,point[0][0]+add_x+7,point[0][1]+32+add_y,win_posi)
            print(msg_text)
            return True
        return False
    except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")

def wait_find_click(hwid,windows, click: Click, dict_folder_paths, debug=False, key_name=[], click_count=1, msg_text='', threshold=0.90, paralle_mode=False,add_x=0,add_y=0, time_out=5):
    """รอจนกว่า find_click จะสำเร็จ หรือหมดเวลา"""
    return wait_until_success(find_click,hwid, windows, click, dict_folder_paths, debug, key_name, click_count, msg_text, threshold, paralle_mode,add_x,add_y, timeout=time_out)

def wait_find_check(windows,dict_folder_paths,key_name,debug=False,threshold=0.90,paralle_mode=False, time_out=5):
    """รอจนกว่า find_click จะสำเร็จ หรือหมดเวลา"""
    return wait_until_success(find_check,windows,dict_folder_paths,key_name,debug,threshold,paralle_mode,timeout=time_out)

def wait_until_success(func, *args, timeout=5):
    """ เรียกใช้ฟังก์ชันซ้ำจนกว่าจะคืนค่า True หรือครบเวลา timeout วินาที """
    start_time = time.time()
    
    while not func(*args):
        if time.time() - start_time > timeout:
            print(f"Timeout: {func.__name__} ใช้เวลานานเกิน {timeout} วินาที")
            return False  # ออกจากลูปเมื่อครบเวลา
        
    return True  # สำเร็จในเวลาที่กำหนด

def get_current_time():
    # แสดงเวลาปัจจุบัน
    current_time = datetime.now()

    # ฟอร์แมตเวลาให้อยู่ในรูปแบบที่อ่านง่าย
    formatted_time = current_time.strftime("%H:%M:%S")  # ชั่วโมง:นาที:วินาที
    return formatted_time


def read_json_file(file):
    with open(file, 'r') as file:
            data = json.load(file)
    return data

def keyboard_down_up_find(hwid,windows,click : Click,dict_folder_paths,find_text=[''],debug=False,loop_find=10):
    try:
        for i in range(loop_find):
            points=find_imgs(windows,dict_keys_contain(dict_folder_paths,find_text),threshold=0.99,debug=debug,paralle_mode=False)
            point =get_point(points)
            if point:
                print(f"เลือก ข้อความ {find_text[len(find_text)-1]} สำเร็จ")
                return point
            if (i<=loop_find/2):
                click.send_key_PC(hwid,'down_arrow')
            else :
                click.send_key_PC(hwid,'up_arrow')
        return False
    except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")

def keyboard_down_find(hwid,windows,click : Click,dict_folder_paths,find_path='',find_text='',debug=False,loop_find=10):
    try:
        for i in range(loop_find):
            points=find_imgs(windows,dict_keys_contain(dict_folder_paths,[find_path,find_text]),threshold=0.99,debug=debug,paralle_mode=False)
            point =get_point(points)
            if point:
                print(f"เลือก ข้อความ {find_text} สำเร็จ")
                return True
            click.send_key_PC(hwid,'down_arrow')
        return False
    except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")

def keyboard_up_find(hwid,windows,click : Click,dict_folder_paths,find_path='',find_text='',debug=False,loop_find=10):
    try:
        for i in range(loop_find):
            points=find_imgs(windows,dict_keys_contain(dict_folder_paths,[find_path,find_text]),threshold=0.99,debug=debug,paralle_mode=False)
            point =get_point(points)
            if point:
                print(f"เลือก ข้อความ {find_text} สำเร็จ")
                return True
            click.send_key_PC(hwid,'up_arrow')
        return False
    except Exception as e:
                print(f"เกิดข้อผิดพลาด: {e}")