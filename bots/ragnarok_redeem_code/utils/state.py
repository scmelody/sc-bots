# 🧩 Shared context object and config loader
import json
import sys
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from core.Windowscapture import WindowCapture
from core.Classclick import Click
from core.arduino import find_arduino_port
import time

class BotContext:
    def __init__(self, config_path):
        self.config_path = config_path
        self.config = self.load_config()

        # เตรียม WindowCapture และ Click
        self.window_name = self.config.get("window_name", "Ragnarok Code")
        self.windows = WindowCapture(self.window_name)

        self.arduino = None
        if self.config.get("use_arduino", True):
            port = find_arduino_port()
            if port:
                import serial
                self.arduino = serial.Serial(port, 9600, timeout=1)

        self.click = Click(self.window_name, arduino=self.arduino)
        self.hwid = self.click.gethwid_ragclassic()

        # Redeem settings
        self.codes = self.config.get("codes", [])
        self.threshold = self.config.get("threshold", 0.9)
        self.max_attempts = self.config.get("max_attempts", 3)
        self.image_paths = self.config.get("image_paths", {})
        self.offset = self.config.get("click_offset", {"x": 7, "y": 32})

        # Logging
        self.log_file = self.config.get("log_file", "redeem_log.txt")

    def wait(self, seconds):
        time.sleep(seconds)

    def log(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        log_entry = f"{timestamp} {msg}\n"
        print(log_entry.strip())

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)

    def load_config(self):
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            return json.load(f)
