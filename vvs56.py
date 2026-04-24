import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

# Глобальные переменные
expenses = []

# Загрузка данных
def load_data():
    global expenses
    if os.path.exists("expenses.json"):
        with open("expenses.json", "r", encoding="utf-8") as f:
            expenses = json.load(f)
    else:
        expenses = []

# Сохранение данных
def save_data():
    with open("expenses.json", "w", encoding="utf-8") as f:
        json.dump(expenses, f, ensure_ascii=False, indent=4)

# Добавление расхода
def add_expense():
    amount_text = amount_var.get()
    category = category_var.get()
    date_text = date_var.get()

    # Проверка суммы
    try:
        amount = float(amount_text)
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительную сумму")
        return

    # Проверка даты
    try:
        date_obj = datetime.strptime(date_text, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Введите дату в формате ГГГГ-ММ-ДД")
        return

    expense = {
        "amount": amount,
        "category": category,
        "date": date_text
    }
    expenses.append(expense)
    save_data()
    refresh_table()
    clear_form()

def clear_form():
    amount_var.set("")
    category_var.set(categories[0])
    date_var.set(datetime.now().strftime("%Y-%m-%d"))

# Обновление таблицы
def refresh_table(filtered=None):
    for row in tree.get_children():
        tree.delete(row)
    data_to_show = filtered if filtered is not None else expenses
    for exp in data_to_show:
        tree.insert("", tk.END, values=(exp["date"], exp["category"], exp["amount"]))

# Фильтр по категории
def filter_category():
    cat = filter_category_var.get()
    filtered = [e for e in expenses if e["category"] == cat]
    refresh_table(filtered)

# Фильтр по дате
def filter_date():
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Некорректный формат дат")
        return
    filtered = [e for e in expenses if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end]
    refresh_table(filtered)

# Расчёт общей суммы за период
def calculate_total():
    start_date = start_date_var.get()
    end_date = end_date_var.get()
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except:
        messagebox.showerror("Ошибка", "Некорректный формат дат")
        return
    total = sum(e["amount"] for e in expenses if start <= datetime.strptime(e["date"], "%Y-%m-%d") <= end)
    total_label.config(text=f"Общая сумма: {total:.2f}")

# Основной интерфейс
root = tk.Tk()
root.title("Учёт расходов")

load_data()

# Переменные
amount_var = tk.StringVar()
category_var = tk.StringVar()
date_var = tk.StringVar()

categories = ["Еда", "Транспорт", "Развлечения", "Прочее"]
category_var.set(categories[0])

# Ввод формы
ttk.Label(root, text="Сумма:").grid(row=0, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=amount_var).grid(row=0, column=1, padx=5, pady=5)

ttk.Label(root, text="Категория:").grid(row=1, column=0, padx=5, pady=5)
ttk.OptionMenu(root, category_var, *categories).grid(row=1, column=1, padx=5, pady=5)

ttk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5)
ttk.Entry(root, textvariable=date_var).grid(row=2, column=1, padx=5, pady=5)
date_var.set(datetime.now().strftime("%Y-%m-%d"))

ttk.Button(root, text="Добавить расход", command=add_expense).grid(row=3, column=0, columnspan=2, pady=10)

# Таблица расходов
columns = ("Дата", "Категория", "Сумма")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

refresh_table()

# Фильтр по категории
ttk.Label(root, text="Фильтр по категории:").grid(row=5, column=0, padx=5, pady=5)
filter_category_var = tk.StringVar()
filter_category_var.set(categories[0])
ttk.OptionMenu(root, filter_category_var, *categories).grid(row=5, column=1, padx=5, pady=5)
ttk.Button(root, text="Фильтр", command=filter_category).grid(row=5, column=2, padx=5)

# Фильтр по дате
ttk.Label(root, text="Дата от:").grid(row=6, column=0, padx=5, pady=5)
start_date_var = tk.StringVar()
ttk.Entry(root, textvariable=start_date_var).grid(row=6, column=1, padx=5, pady=5)
start_date_var.set(datetime.now().strftime("%Y-%m-%d"))

ttk.Label(root, text="до:").grid(row=7, column=0, padx=5, pady=5)
end_date_var = tk.StringVar()
ttk.Entry(root, textvariable=end_date_var).grid(row=7, column=1, padx=5, pady=5)
end_date_var.set(datetime.now().strftime("%Y-%m-%d"))

ttk.Button(root, text="Посчитать сумму за период", command=calculate_total).grid(row=8, column=0, columnspan=2, pady=10)
total_label = ttk.Label(root, text="Общая сумма: 0.00")
total_label.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()
