from dataclasses import dataclass, field

@dataclass
class SafetyProtocol:
    cfg: dict = field(default_factory=dict)
    locked: bool = True

    def __post_init__(self):
        self.locked = bool(self.cfg.get("lock_enabled", True))

    def arm(self):
        self.locked = False

    def disarm(self):
        self.locked = True

    def can_fire(self) -> bool:
        return not self.locked

    def check_all(self, servo, frame_src):
        # Buraya hız/ivme, sınır, sensör hatası vb. kontroller eklenebilir
        pass
