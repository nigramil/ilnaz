import tkinter as tk
from tkinter import ttk, messagebox
import json
import random
import string
import os

# Файл для хранения истории паролей
HISTORY_FILE = 'password_history.json'

class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Password Generator")
        self.history = []

        # Настройки длины пароля
        self.length_label = tk.Label(root, text="Длина пароля:")
        self.length_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.length_scale = tk.Scale(root, from_=4, to=32, orient=tk.HORIZONTAL)
        self.length_scale.set(12)
        self.length_scale.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Чекбоксы для символов
        self.var_digits = tk.IntVar(value=1)
        self.var_letters = tk.IntVar(value=1)
        self.var_symbols = tk.IntVar(value=0)

        self.chk_digits = tk.Checkbutton(root, text="Цифры (0-9)", variable=self.var_digits)
        self.chk_letters = tk.Checkbutton(root, text="Буквы (a-z, A-Z)", variable=self.var_letters)
        self.chk_symbols = tk.Checkbutton(root, text="Спецсимволы", variable=self.var_symbols)

        self.chk_digits.grid(row=1, column=0, sticky='w', padx=5)
        self.chk_letters.grid(row=1, column=1, sticky='w', padx=5)
        self.chk_symbols.grid(row=1, column=2, sticky='w', padx=5)

        # Кнопка генерации
        self.btn_generate = tk.Button(root, text="Сгенерировать пароль", command=self.generate_password)
        self.btn_generate.grid(row=2, column=0, columnspan=3, pady=10)

        # Поле для отображения пароля
        self.password_var = tk.StringVar()
        self.entry_password = tk.Entry(root, textvariable=self.password_var, font=('Arial', 14), width=50)
        self.entry_password.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        # Таблица истории
        self.history_label = tk.Label(root, text="История паролей:")
        self.history_label.grid(row=4, column=0, sticky='w', padx=5)
        self.tree = ttk.Treeview(root, columns=('password'), show='headings', height=10)
        self.tree.heading('password', text='Пароль')
        self.tree.grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Кнопки для работы с историей
        self.btn_clear_history = tk.Button(root, text="Очистить историю", command=self.clear_history)
        self.btn_clear_history.grid(row=6, column=0, pady=5)
        self.btn_copy = tk.Button(root, text="Копировать последний", command=self.copy_last)
        self.btn_copy.grid(row=6, column=1, pady=5)
        self.btn_save_history = tk.Button(root, text="Сохранить историю", command=self.save_history)
        self.btn_save_history.grid(row=6, column=2, pady=5)

        # Загрузка истории
        self.load_history()

        # Обработка закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def generate_password(self):
        length = self.length_scale.get()
        charset = ''
        if self.var_digits.get():
            charset += string.digits
        if self.var_letters.get():
            charset += string.ascii_letters
        if self.var_symbols.get():
            charset += string.punctuation

        if not charset:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы один тип символов.")
            return

        password = ''.join(random.choice(charset) for _ in range(length))
        self.password_var.set(password)

        # Добавляем в историю
        self.history.append(password)
        self.update_history_table()

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            try:
                with open(HISTORY_FILE, 'r', encoding='utf-8') as file:
                    self.history = json.load(file)
                self.update_history_table()
            except:
                self.history = []

    def save_history(self):
        with open(HISTORY_FILE, 'w', encoding='utf-8') as file:
            json.dump(self.history, file, ensure_ascii=False, indent=2)
        messagebox.showinfo("Сохранено", "История сохранена в файл.")

    def update_history_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for pw in self.history:
            self.tree.insert('', 'end', values=(pw,))

    def clear_history(self):
        self.history.clear()
        self.update_history_table()

    def copy_last(self):
        if self.history:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.history[-1])
            messagebox.showinfo("Копирование", "Последний пароль скопирован в буфер обмена.")
        else:
            messagebox.showwarning("Предупреждение", "История пуста.")

    def on_close(self):
        self.save_history()
        self.root.destroy()

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()
