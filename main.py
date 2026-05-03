import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.root.geometry("500x550")
        self.history_file = "history.json"
        
        # Переменные настроек
        self.length_var = tk.IntVar(value=12)
        self.use_letters = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_specials = tk.BooleanVar(value=True)
        
        self.create_widgets()
        self.load_history()

    def create_widgets(self):
        # --- Секция настроек ---
        settings_frame = ttk.LabelFrame(self.root, text="Настройки")
        settings_frame.pack(pady=10, padx=10, fill="x")

        ttk.Label(settings_frame, text="Длина пароля:").pack()
        self.length_label = ttk.Label(settings_frame, text="12")
        self.length_label.pack()
        
        self.slider = ttk.Scale(settings_frame, from_=4, to=32, variable=self.length_var, 
                                orient="horizontal", command=self.update_label)
        self.slider.pack(fill="x", padx=20, pady=5)

        ttk.Checkbutton(settings_frame, text="Буквы (a-z, A-Z)", variable=self.use_letters).pack(anchor="w", padx=20)
        ttk.Checkbutton(settings_frame, text="Цифры (0-9)", variable=self.use_digits).pack(anchor="w", padx=20)
        ttk.Checkbutton(settings_frame, text="Спецсимволы (!@#...)", variable=self.use_specials).pack(anchor="w", padx=20)

        # --- Кнопка и результат ---
        ttk.Button(self.root, text="Сгенерировать пароль", command=self.generate).pack(pady=10)
        
        self.result_entry = ttk.Entry(self.root, font=("Arial", 14), justify="center")
        self.result_entry.pack(pady=5, padx=10, fill="x")

        # --- Таблица истории ---
        history_frame = ttk.LabelFrame(self.root, text="История")
        history_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.tree = ttk.Treeview(history_frame, columns=("Password"), show="headings")
        self.tree.heading("Password", text="Пароль")
        self.tree.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

    def update_label(self, event):
        self.length_label.config(text=str(self.length_var.get()))

    def generate(self):
        length = self.length_var.get()
        chars = ""
        if self.use_letters.get(): chars += string.ascii_letters
        if self.use_digits.get(): chars += string.digits
        if self.use_specials.get(): chars += string.punctuation

        if not chars:
            messagebox.showwarning("Ошибка", "Выберите хотя бы один тип символов!")
            return

        password = "".join(random.choice(chars) for _ in range(length))
        self.result_entry.delete(0, tk.END)
        self.result_entry.insert(0, password)
        
        self.add_to_history(password)

    def add_to_history(self, pwd):
        self.tree.insert("", 0, values=(pwd,))
        self.save_history()

    def save_history(self):
        items = [self.tree.item(item)["values"][0] for item in self.tree.get_children()]
        with open(self.history_file, "w") as f:
            json.dump(items, f)

    def load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r") as f:
                    items = json.load(f)
                    for item in reversed(items):
                        self.tree.insert("", 0, values=(item,))
            except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
