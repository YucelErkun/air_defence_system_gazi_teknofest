import argparse, time
from utils.logger import get_logger
from utils.safety_protocols import SafetyProtocol
from core.servo_controller import ServoController
from core.firing_mechanism import FiringSystem
from core.vision_processing import FrameSource, preprocess_image
from ai.object_detection import TargetDetector
from ai.prediction_model import MotionPredictor
from core.tracking_algorithm import TargetTracker
from utils.calibration import PIDController
import yaml, pathlib, cv2

def load_cfg():
    cfg_path = pathlib.Path(__file__).resolve().parents[1] / "config" / "config.yaml"
    with open(cfg_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

class DefenseSystem:
    def __init__(self, cfg):
        self.log = get_logger("DefenseSystem")
        self.cfg = cfg
        sim = bool(cfg.get("sim", True))
        cam_id = cfg.get("camera_id", 0)

        self.frame_src = FrameSource(cam_id=cam_id, sim=sim)
        self.servo = ServoController(sim=sim)
        self.tracker = TargetTracker()
        self.firing = FiringSystem(sim=sim)
        self.safety = SafetyProtocol(cfg.get("safety", {}))

        pid = cfg.get("pid", {})
        self.pid_x = PIDController(kp=pid.get("kp",0.5), ki=pid.get("ki",0.1), kd=pid.get("kd",0.2))
        self.pid_y = PIDController(kp=pid.get("kp",0.5), ki=pid.get("ki",0.1), kd=pid.get("kd",0.2))

        self.detector = TargetDetector(conf_threshold=cfg.get("detector", {}).get("conf_threshold", 0.45),
                                       use_color=cfg.get("detector", {}).get("use_color", True),
                                       use_motion=cfg.get("detector", {}).get("use_motion", True))
        self.predictor = MotionPredictor(history_len=30)

    def run(self):
        self.log.info("Sistem başlatılıyor (sim=%s)...", self.servo.sim)
        for frame in self.frame_src.frames():
            processed = preprocess_image(frame)
            targets = self.detector.detect_multiple_methods(processed)

            if targets:
                primary = self._prioritize(targets)
                tracked = self.tracker.update(primary)
                predicted = self.predictor.predict(tracked)

                # Basit hata (offset) hesapları
                cx, cy = predicted.get("center", primary["center"])
                err_x = cx - processed.shape[1]/2
                err_y = cy - processed.shape[0]/2

                out_x = self.pid_x.update(err_x)
                out_y = self.pid_y.update(err_y)
                self.servo.move_relative(out_x, out_y)

                if self._is_locked(err_x, err_y) and self.safety.can_fire():
                    self.firing.engage()
            else:
                self.tracker.idle()

            self.safety.check_all(self.servo, self.frame_src)
            self._visualize(frame, targets)

    def _visualize(self, frame, targets):
        if not self.cfg.get("visualize", True):
            return
        vis = frame.copy()
        if targets:
            for t in targets:
                (x1,y1,x2,y2) = t["bbox"]
                cv2.rectangle(vis, (x1,y1), (x2,y2), (0,255,0), 2)
        cv2.imshow("Savunma Sistemi", vis)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            raise SystemExit

    def _prioritize(self, targets):
        # En yüksek güven + merkeze yakınlık basit puanlama
        h, w = 480, 640  # default fallback
        if "shape" in dir(cv2):
            pass
        def score(t):
            cx, cy = t["center"]
            center_dist = abs(cx - w/2) + abs(cy - h/2)
            return t["confidence"] - 0.0005*center_dist
        return sorted(targets, key=score, reverse=True)[0]

    def _is_locked(self, err_x, err_y, tol=8):
        return abs(err_x) < tol and abs(err_y) < tol

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sim", type=str, default="true")
    parser.add_argument("--camera", type=int, default=None)
    args = parser.parse_args()

    cfg = load_cfg()
    if args.camera is not None:
        cfg["camera_id"] = args.camera
    cfg["sim"] = (args.sim.lower() in ["1","true","yes","on"])

    DefenseSystem(cfg).run()
