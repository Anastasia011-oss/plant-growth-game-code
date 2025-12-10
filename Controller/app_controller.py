import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
from Model.plant_base import Plant
from Model.fertilizer import Fertilizer
from View.plot_view import PlotView
from save_manager import save_game, load_game
from Services.ResourceService import ResourceService

class AppController:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Ферма MVC")

        self.images_dir = Path(__file__).parent.parent / "Images"

        self.resources = ResourceService.load_resources()

        self.plants = [
            Plant(
                int(pid),
                pdata["name"],
                pdata["grow_time"],
                images={stage: str(self.images_dir / Path(path).name) for stage, path in pdata.get("images", {}).items()}
            )
            for pid, pdata in self.resources["plants"].items()
        ]

        self.fertilizers = [
            Fertilizer(key, fdata["name"], fdata["multiplier"], fdata["price"])
            for key, fdata in self.resources["fertilizers"].items()
        ]

        self.sell_prices = {int(pid): pdata["sell_price"] for pid, pdata in self.resources["plants"].items()}

        self.plot_count = self.resources["plots"]["count"]
        self.balance = self.resources["player"]["starting_balance"]

        saved_data = load_game()
        if saved_data:
            self.balance = saved_data.get("balance", self.balance)
            self.barn = {int(k): v for k, v in saved_data.get("barn", {}).items()}
            self.inventory = saved_data.get("inventory", {f.key: 0 for f in self.fertilizers})
            self.saved_plots = saved_data.get("plots", {})
        else:
            self.barn = {}
            self.inventory = {f.key: 0 for f in self.fertilizers}
            self.saved_plots = {}

        top = tk.Frame(self.root)
        top.pack(pady=10)
        self.balance_label = tk.Label(top, text=f"Баланс: {self.balance}₴", font=("Arial", 14))
        self.balance_label.pack()
        tk.Button(top, text="Купить удобрение", command=self.buy_fertilizer).pack(pady=5)
        tk.Button(top, text="Продать урожай", command=self.sell_crop).pack(pady=5)

        self.farm_frame = tk.Frame(self.root)
        self.farm_frame.pack(pady=10)
        self.plots = []
        for i in range(self.plot_count):
            plot_data = self.saved_plots.get(str(i))
            self.plots.append(PlotView(self.farm_frame, i, self, saved_plot=plot_data))

        self.barn_label = tk.Label(self.root, text="")
        self.barn_label.pack()
        self.update_barn_label()

        self.root.mainloop()

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
        self.save_game()
        messagebox.showinfo("Куплено", f"Вы купили {fert.name}.\nВ инвентаре: {self.inventory[fert.key]}")

    def sell_crop(self):
        if not self.barn:
            messagebox.showinfo("Амбар пуст", "У вас нет урожая для продажи.")
            return
        earned = sum(self.sell_prices.get(pid, 10) * qty for pid, qty in self.barn.items())
        self.balance += earned
        self.update_balance()
        self.barn = {}
        self.update_barn_label()
        self.save_game()
        messagebox.showinfo("Продано!", f"Вы заработали {earned}₴")

    def update_balance(self):
        self.balance_label.config(text=f"Баланс: {self.balance}₴")

    def add_to_barn(self, pid):
        pid = int(pid)
        self.barn[pid] = self.barn.get(pid, 0) + 1
        self.update_barn_label()
        self.save_game()

    def update_barn_label(self):
        if not self.barn:
            text = "пусто"
        else:
            text = ", ".join(f"{p.name}: {self.barn.get(p.id,0)}" for p in self.plants if self.barn.get(p.id,0) > 0)
        self.barn_label.config(text="Амбар: " + text)

    def save_game(self):
        plots_data = {}
        for idx, plot in enumerate(self.plots):
            if plot.model:
                plots_data[str(idx)] = {
                    "state": plot.model.state,
                    "plant_id": plot.model.plant.id,
                    "remaining": plot.model.remaining
                }
            else:
                plots_data[str(idx)] = {
                    "state": "empty",
                    "plant_id": None,
                    "remaining": 0
                }

        save_game({
            "balance": self.balance,
            "barn": self.barn,
            "inventory": self.inventory,
            "plots": plots_data
        })
