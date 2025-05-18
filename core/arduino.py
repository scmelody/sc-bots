import serial.tools.list_ports

def find_arduino_port():
    # หาพอร์ตทั้งหมดที่เชื่อมต่อ
    ports = serial.tools.list_ports.comports()
    
    for port in ports:
        print(f"พอร์ต: {port.device}, ชื่อ: {port.description}")
        
        # ตรวจสอบว่าเป็นพอร์ตของ Arduino หรือไม่
        if 'Arduino' in port.description:
            print(f"พบ Arduino ที่พอร์ต: {port.device}")
            return port.device
    
    print("ไม่พบ Arduino")
    return None


if  __name__ == '__main__':
    # เรียกใช้ฟังก์ชันเพื่อหาพอร์ต
    arduino_port = find_arduino_port()
    if arduino_port:
        print(f"Arduino เชื่อมต่อที่พอร์ต: {arduino_port}")
    else:
        print("ไม่พบการเชื่อมต่อกับ Arduino")
