# module/log_config.py

import logging
import os
from datetime import datetime

def setup_logging(log_folder="logs", log_file_prefix="bot", level=logging.DEBUG, console_output=True, file_output=True, mode='w'):
    """
    ตั้งค่าระบบ logging ของโปรแกรม

    Args:
        log_folder (str): ชื่อ Folder สำหรับเก็บ Log (จะถูกสร้างใน Root Project)
        log_file_prefix (str): คำนำหน้าชื่อไฟล์ Log (เช่น 'ragnarok_bot', 'ldplayer_bot')
        level (int): ระดับ Log ต่ำสุดที่ต้องการเก็บ (เช่น logging.DEBUG, logging.INFO, ...)
        console_output (bool): ต้องการให้แสดง Log ที่ Console หรือไม่
        file_output (bool): ต้องการให้บันทึก Log ลงไฟล์หรือไม่
        mode (str): 'w' (เขียนทับ) หรือ 'a' (ต่อท้าย) สำหรับ FileHandler
    """
    # สร้าง Folder log ถ้ายังไม่มี
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # กำหนดชื่อไฟล์ Log ด้วย Timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file_name = f"{log_file_prefix}_{timestamp}.log"
    log_path = os.path.join(log_folder, log_file_name)

    # ตั้งค่า root logger
    # ลบ handler เดิมออกก่อน หากมีการตั้งค่ามาก่อน (ป้องกัน log ซ้ำถ้าเรียกซ้ำ)
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # กำหนด format ของ Log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    handlers = []

    if console_output:
        # Handler สำหรับ Console Output
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        handlers.append(console_handler)

    if file_output:
        # Handler สำหรับ File Output
        file_handler = logging.FileHandler(log_path, mode=mode, encoding='utf-8')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # ตั้งค่า root logger ด้วย handlers และ level ที่กำหนด
    # ควรตั้ง level ของ root logger ให้ต่ำที่สุดที่ต้องการเก็บทั้งหมด (เช่น DEBUG)
    # แล้วตั้ง level ใน handler แต่ละตัวเพื่อควบคุมการแสดงผลจริง
    logging.root.setLevel(logging.DEBUG) # root logger ควรเก็บละเอียดทั้งหมด
    for handler in handlers:
        handler.setLevel(level) # แต่ handler จะแสดงผลตาม level ที่ต้องการ

    # เพิ่ม handlers เข้าไปที่ root logger
    for handler in handlers:
        logging.root.addHandler(handler)


    # ไม่จำเป็นต้องคืนค่า logger เพราะตั้งค่า root logger แล้ว Module อื่นจะเรียกใช้ได้เลย
    # หากต้องการ logger สำหรับ module/log_config เอง
    # logger = logging.getLogger(__name__)
    # logger.info("ตั้งค่า Logging เรียบร้อย.")
    print(f"ตั้งค่า Logging เรียบร้อย. Log บันทึกที่ {log_path}" if file_output else "ตั้งค่า Logging เรียบร้อย (Console Output เท่านั้น)")


# วิธีการใช้งาน logger ใน Module อื่นๆ (หลังจากเรียก setup_logging ในไฟล์ main แล้ว)
# ในไฟล์ tasks/ragnarok/g_login.py, module/game_utils.py ฯลฯ
#
# import logging
# logger = logging.getLogger(__name__) # สร้าง logger สำหรับ module นั้นๆ โดยใช้ชื่อ module เป็นชื่อ logger
#
# def some_function():
#     logger.info("ข้อความ Log ระดับ INFO")
#     logger.debug("ข้อความ Log ระดับ DEBUG") # จะแสดงถ้า level ที่ตั้งค่าอนุญาต
#     logger.warning("ข้อความ Log ระดับ WARNING")
#     logger.error("ข้อความ Log ระดับ ERROR")