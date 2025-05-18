import tkinter as tk
from tkinter import ttk

class RedeemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ragnarok Redeem Bot")

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, fill='both', expand=True)

        self.create_tab_redeem()
        self.create_tab_logs()
        self.create_tab_settings()
        self.create_tab_manual()

    def create_tab_redeem(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='🔑 Redeem Code')

        ttk.Label(frame, text="โค้ดที่จะเติม:").pack(pady=5)
        self.code_entry = ttk.Entry(frame)
        self.code_entry.pack(pady=5)

        ttk.Button(frame, text="✨ เติมโค้ด", command=self.redeem_code).pack(pady=10)

    def create_tab_logs(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='📜 Log')

        self.log_text = tk.Text(frame, height=15)
        self.log_text.pack(fill='both', expand=True)

    def create_tab_settings(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='⚙️ Settings')

        ttk.Label(frame, text="Threshold:").pack()
        self.threshold_entry = ttk.Entry(frame)
        self.threshold_entry.insert(0, "0.9")
        self.threshold_entry.pack()

    def create_tab_manual(self):
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text='🖱 Manual')

        ttk.Label(frame, text="พิกัด X, Y:").pack()
        self.coord_entry = ttk.Entry(frame)
        self.coord_entry.pack()

        ttk.Button(frame, text="คลิกทดสอบ", command=self.click_test).pack()

    def redeem_code(self):
        code = self.code_entry.get()
        self.log_text.insert(tk.END, f"เติมโค้ด: {code}\n")

    def click_test(self):
        coords = self.coord_entry.get()
        self.log_text.insert(tk.END, f"ทดสอบคลิกที่: {coords}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = RedeemGUI(root)
    root.mainloop()
