# GUI for bot configuration
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import os

class ConfigGUI:
    def __init__(self, root, config_path="config.json"):
        self.root = root
        self.root.title("🛠 Ragnarok Bot Config")
        self.config_path = config_path
        self.config = self.load_config()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        self.create_tab_general()
        self.create_tab_images()
        self.create_tab_codes()
        self.create_tab_advanced()

        ttk.Button(root, text="💾 Save Config", command=self.save_config).pack(pady=10)

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        else:
            messagebox.showerror("Error", "config.json not found.")
            return {}

    def create_tab_general(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="⚙️ General")

        ttk.Label(frame, text="Window Name").pack()
        self.window_name = tk.StringVar(value=self.config.get("window_name", ""))
        ttk.Entry(frame, textvariable=self.window_name).pack()

        self.use_arduino = tk.BooleanVar(value=self.config.get("use_arduino", True))
        ttk.Checkbutton(frame, text="Use Arduino", variable=self.use_arduino).pack()

        ttk.Label(frame, text="Click Method (pc/arduino)").pack()
        self.click_method = tk.StringVar(value=self.config.get("click_method", "arduino"))
        ttk.Entry(frame, textvariable=self.click_method).pack()

    def create_tab_images(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🖼 Image Paths")

        self.image_paths = {}
        image_data = self.config.get("image_paths", {})

        for key in ["code_input", "submit_button", "confirm_button"]:
            ttk.Label(frame, text=key).pack()
            var = tk.StringVar(value=image_data.get(key, ""))
            entry = ttk.Entry(frame, textvariable=var, width=50)
            entry.pack()
            btn = ttk.Button(frame, text="📂 Browse", command=lambda v=var: self.browse_image(v))
            btn.pack(pady=2)
            self.image_paths[key] = var

    def browse_image(self, var):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg")])
        if file_path:
            var.set(file_path)

    def create_tab_codes(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🔑 Redeem Codes")

        self.codes_text = tk.Text(frame, height=10)
        self.codes_text.pack(fill='both', expand=True)
        for code in self.config.get("codes", []):
            self.codes_text.insert(tk.END, code + "\n")

    def create_tab_advanced(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text="🧪 Advanced")

        ttk.Label(frame, text="Threshold").pack()
        self.threshold = tk.DoubleVar(value=self.config.get("threshold", 0.9))
        ttk.Entry(frame, textvariable=self.threshold).pack()

        ttk.Label(frame, text="Max Attempts").pack()
        self.max_attempts = tk.IntVar(value=self.config.get("max_attempts", 3))
        ttk.Entry(frame, textvariable=self.max_attempts).pack()

        ttk.Label(frame, text="Click Offset X / Y").pack()
        offset = self.config.get("click_offset", {"x": 7, "y": 32})
        self.offset_x = tk.IntVar(value=offset.get("x", 7))
        self.offset_y = tk.IntVar(value=offset.get("y", 32))
        ttk.Entry(frame, textvariable=self.offset_x).pack()
        ttk.Entry(frame, textvariable=self.offset_y).pack()

    def save_config(self):
        new_config = {
            "window_name": self.window_name.get(),
            "use_arduino": self.use_arduino.get(),
            "click_method": self.click_method.get(),
            "threshold": self.threshold.get(),
            "max_attempts": self.max_attempts.get(),
            "click_offset": {
                "x": self.offset_x.get(),
                "y": self.offset_y.get()
            },
            "codes": self.codes_text.get("1.0", tk.END).strip().splitlines(),
            "image_paths": {k: v.get() for k, v in self.image_paths.items()}
        }

        with open(self.config_path, 'w') as f:
            json.dump(new_config, f, indent=2)

        messagebox.showinfo("Success", "Config saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConfigGUI(root)
    root.mainloop()
