import cv2

class FrameSource:
    def __init__(self, cam_id=0, sim=True):
        self.sim = sim
        self.cap = cv2.VideoCapture(cam_id) if not sim else None

    def frames(self):
        if self.sim:
            # Simülasyon: masaüstü/webcam yerine yapay görüntü üretimi
            import numpy as np
            while True:
                img = np.zeros((480, 640, 3), dtype=np.uint8)
                cv2.putText(img, "SIM MODE", (240,30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2)
                yield img
        else:
            if not self.cap or not self.cap.isOpened():
                raise RuntimeError("Kamera acilamadi")
            while True:
                ok, frame = self.cap.read()
                if not ok:
                    break
                yield frame

def preprocess_image(frame):
    return frame  # gerekirse blur, denoise vb. ekleyin
