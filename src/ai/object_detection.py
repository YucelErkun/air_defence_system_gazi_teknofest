import torch
import numpy as np
import cv2

class TargetDetector:
    def __init__(self, conf_threshold=0.45, use_color=True, use_motion=True):
        self.conf = conf_threshold
        self.use_color = use_color
        self.use_motion = use_motion
        try:
            self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
        except Exception:
            self.model = None  # çevrimdışı/arm'da indirilemeyebilir

        self.prev_gray = None

    def detect_multiple_methods(self, frame):
        dl = self.deep_learning_detection(frame) if self.model is not None else []
        color = self.color_based_detection(frame) if self.use_color else []
        motion = self.motion_detection(frame) if self.use_motion else []
        all_t = dl + color + motion
        return self._nms_merge(all_t)

    def deep_learning_detection(self, frame):
        results = self.model(frame)  # otomatik preprocess
        targets = []
        for det in results.xyxy[0].cpu().numpy():
            x1,y1,x2,y2,conf,cls = det
            if conf < self.conf: 
                continue
            cx, cy = (x1+x2)/2, (y1+y2)/2
            targets.append({
                "bbox": [int(x1), int(y1), int(x2), int(y2)],
                "confidence": float(conf),
                "class": int(cls),
                "center": (float(cx), float(cy))
            })
        return targets

    def color_based_detection(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        ranges = {
            "red": [(0,100,100),(10,255,255)],
            "blue":[(100,100,100),(130,255,255)]
        }
        masks = []
        for (lo, hi) in ranges.values():
            masks.append(cv2.inRange(hsv, np.array(lo), np.array(hi)))
        mask = np.clip(sum(masks), 0, 255).astype(np.uint8)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        targets = []
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w*h < 500: 
                continue
            cx, cy = x+w/2, y+h/2
            targets.append({
                "bbox":[x,y,x+w,y+h],
                "confidence":0.5,
                "class":-1,
                "center":(float(cx), float(cy))
            })
        return targets

    def motion_detection(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if self.prev_gray is None:
            self.prev_gray = gray
            return []
        diff = cv2.absdiff(gray, self.prev_gray)
        self.prev_gray = gray
        _, th = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        th = cv2.medianBlur(th, 5)
        contours, _ = cv2.findContours(th, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        t = []
        for c in contours:
            x,y,w,h = cv2.boundingRect(c)
            if w*h < 800:
                continue
            cx, cy = x+w/2, y+h/2
            t.append({"bbox":[x,y,x+w,y+h],"confidence":0.4,"class":-2,"center":(float(cx), float(cy))})
        return t

    def _nms_merge(self, targets, iou_thr=0.4):
        # Basit NMS: sınıf bağımsız
        def iou(a,b):
            ax1,ay1,ax2,ay2=a["bbox"]
            bx1,by1,bx2,by2=b["bbox"]
            inter_x1, inter_y1 = max(ax1,bx1), max(ay1,by1)
            inter_x2, inter_y2 = min(ax2,bx2), min(ay2,by2)
            iw, ih = max(0, inter_x2-inter_x1), max(0, inter_y2-inter_y1)
            inter = iw*ih
            area_a = (ax2-ax1)*(ay2-ay1)
            area_b = (bx2-bx1)*(by2-by1)
            union = area_a+area_b-inter+1e-6
            return inter/union
        targets = sorted(targets, key=lambda t: t["confidence"], reverse=True)
        kept = []
        for t in targets:
            if all(iou(t,k) < iou_thr for k in kept):
                kept.append(t)
        return kept
