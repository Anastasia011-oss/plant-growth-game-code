import tkinter as tk
from tkinter import simpledialog, messagebox
from Model.model import Plant, Fertilizer
from Controller.controller import PlotController


class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ферма MVC")

        # Данные игры
        self.balance = 50
        self.sell_prices = {
            1: 15,
            2: 30,
            3: 60,
        }

        self.plants = [
            Plant(1, "Пшеница", 5000),
            Plant(2, "Виноград", 4000),
            Plant(3, "Ананас", 9000),
        ]

        self.fertilizers = [
            Fertilizer("none", "Без удобрения", 1.0, 0),
            Fertilizer("fast", "Обычное удобрение", 0.8, 10),
            Fertilizer("super", "Суперудобрение", 0.6, 20),
        ]

        self.inventory = {f.key: 0 for f in self.fertilizers}
        self.barn = {}

        # Верхнее меню
        top = tk.Frame(self.root)
        top.pack(pady=10)

        self.balance_label = tk.Label(top, text=f"Баланс: {self.balance}₴", font=("Arial", 14))
        self.balance_label.pack()

        tk.Button(top, text="Купить удобрение", command=self.buy_fertilizer).pack(pady=5)
        tk.Button(top, text="Продать урожай", command=self.sell_crop).pack(pady=5)

        # Грядки
        self.farm_frame = tk.Frame(self.root)
        self.farm_frame.pack(pady=10)

        self.plots = [PlotController(self.farm_frame, i, self) for i in range(4)]

        # Амбар
        self.barn_label = tk.Label(self.root, text="Амбар: пусто")
        self.barn_label.pack()


        self.root.mainloop()

    # ---------------------------------------------
    #                ЛОГИКА ИГРЫ
    # ---------------------------------------------

    def buy_fertilizer(self):
        options = [f"{f.name} ({f.price}₴)" for f in self.fertilizers if f.key != "none"]
        choice = simpledialog.askstring("Покупка", "Введите название удобрения:\n" + "\n".join(options))

        if not choice:
            return

        fert = next((f for f in self.fertilizers if f.name.lower() == choice.lower()), None)

        if not fert:
            messagebox.showerror("Ошибка", "Такого удобрения нет")
            return

        if self.balance < fert.price:
            messagebox.showerror("Ошибка", "Недостаточно денег")
            return

        self.balance -= fert.price
        self.inventory[fert.key] += 1
        self.update_balance()

        messagebox.showinfo("Куплено", f"Вы купили {fert.name}.\nВ инвентаре: {self.inventory[fert.key]}")

    def sell_crop(self):
        if not self.barn:
            messagebox.showinfo("Амбар пуст", "У вас нет урожая для продажи.")
            return

        earned = 0

        for plant in self.plants:
            pid = str(plant.id)
            if pid in self.barn:
                qty = self.barn[pid]
                price = self.sell_prices.get(plant.id, 10)
                earned += qty * price

        if earned == 0:
            messagebox.showinfo("Нет товара", "Нечего продавать.")
            return

        self.balance += earned
        self.update_balance()

        self.barn = {}
        self.barn_label.config(text="Амбар: пусто")

        messagebox.showinfo("Продано!", f"Вы заработали {earned}₴")

    def update_balance(self):
        self.balance_label.config(text=f"Баланс: {self.balance}₴")

    def add_to_barn(self, pid):
        pid = str(pid)
        self.barn[pid] = self.barn.get(pid, 0) + 1

        text = ", ".join(
            f"{p.name}: {self.barn[str(p.id)]}"
            for p in self.plants if str(p.id) in self.barn
        )

        self.barn_label.config(text="Амбар: " + text)

    def get_plant(self, pid):
        return next(x for x in self.plants if x.id == pid)

    def get_fertilizer(self, key):
        return next(x for x in self.fertilizers if x.key == key)


