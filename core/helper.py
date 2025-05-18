from ultralytics import YOLO
import cv2
import numpy as np

def extract_detections(results, model):
    detections = []
    for result in results:
        boxes = result.boxes.xyxy.cpu().numpy()
        scores = result.boxes.conf.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        
        for box, score, cls in zip(boxes, scores, classes):
            x1, y1, x2, y2 = map(int, box)
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            label = f"{model.names[int(cls)]}:{score:.2f}"
            cls_name = model.names[int(cls)]
            
            detections.append({
                "box": (x1, y1, x2, y2),
                "x1": x1,  # เพิ่ม field นี้
                "x2": x2,  # เพิ่ม field นี้
                "y1": y1,  # เพิ่ม field นี้
                "y2": y2,  # เพิ่ม field นี้
                "score": score,
                "classid": cls,
                "label": label,
                "classname": cls_name,
                "center": (cx, cy)
            })
    
    detections_sorted = sorted(detections, key=lambda x: x["x1"])
    return detections_sorted
def group_nearby_digits(detections, x_threshold=50, y_threshold=30):
    if not detections:
        return []
    
    groups = []
    current_group = [detections[0]]
    
    for i in range(1, len(detections)):
        prev_det = current_group[-1]
        current_det = detections[i]
        
        # ใช้ x2 จาก dictionary โดยตรง
        x_distance = current_det['x1'] - prev_det['x2']
        y_distance = abs(current_det['center'][1] - prev_det['center'][1])
        
        if x_distance <= x_threshold and y_distance <= y_threshold:
            current_group.append(current_det)
        else:
            groups.append(current_group)
            current_group = [current_det]
    
    if current_group:
        groups.append(current_group)
    
    return groups


# ฟังก์ชันแปลงกลุ่ม detection เป็นข้อความ
def groups_to_text(groups):
    """
    แปลงกลุ่ม detection เป็นข้อความ
    Args:
        groups: List ของกลุ่ม detection
    Returns:
        List ของข้อความที่ได้จากแต่ละกลุ่ม
    """
    texts = []
    for group in groups:
        # เรียงกลุ่มจากซ้ายไปขวาอีกครั้ง (เพื่อความแน่นอน)
        sorted_group = sorted(group, key=lambda x: x['x1'])
        # สร้างข้อความโดยต่อ classname ของแต่ละ detection ในกลุ่ม
        text = ''.join([det['classname'] for det in sorted_group])
        texts.append(text)
    
    return texts

def create_mask(frame,reg):
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask,[reg],(255,255,255))
    return cv2.bitwise_and(frame,mask)

def filter_detections_by_classname(detections, classnames):
    """
    กรอง detection ที่ classname ตรงกับรายการที่กำหนด

    Parameters:
        detections (list): รายการ dict ผลลัพธ์จาก YOLO
        classnames (list or str): class ที่ต้องการกรอง (สามารถใส่ได้หลาย class)

    Returns:
        list: detection ที่ตรงกับ class ที่ต้องการ
    """
    if isinstance(classnames, str):
        classnames = [classnames]
    
    filtered = [d for d in detections if d.get('classname') in classnames]
    return filtered
