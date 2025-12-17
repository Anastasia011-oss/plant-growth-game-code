import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path
from Model.plant_base import Plant
from Model.fertilizer import Fertilizer
from View.plot_view import PlotView
from save_manager import save_game, load_game
from Services.ResourceService import ResourceService
import logging

def setup_logger():
    documents_path = Path.home() / "Documents"
    project_folder = documents_path / "PlantGame"
    project_folder.mkdir(exist_ok=True)
    log_file = project_folder / "game.log"

    logger = logging.getLogger("GameLogger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Старт программы")
    return logger

logger = setup_logger()

class AppController:
    MAX_PLOTS = 16

    def __init__(self):
        logger.info("Запуск игры")
        self.root = tk.Tk()
        self.root.title("Ферма MVC")
        self.images_dir = Path(__file__).parent.parent / "Images"

        try:
            self.resources = ResourceService.load_resources()
            logger.info("Ресурсы загружены успешно")
        except Exception as e:
            logger.exception("Ошибка при загрузке ресурсов")
            raise e

        self.plants = [
            Plant(
                int(pid),
                pdata["name"],
                pdata["grow_time"],
                images={stage: str(self.images_dir / Path(path).name)
                        for stage, path in pdata.get("images", {}).items()}
            )
            for pid, pdata in self.resources["plants"].items()
        ]
        logger.info(f"Загружено {len(self.plants)} растений")

        self.fertilizers = [
            Fertilizer(key, fdata["name"], fdata["multiplier"], fdata["price"])
            for key, fdata in self.resources["fertilizers"].items()
        ]
        logger.info(f"Загружено {len(self.fertilizers)} типов удобрений")

        self.sell_prices = {int(pid): pdata["sell_price"] for pid, pdata in self.resources["plants"].items()}
        self.plot_count = self.resources["plots"]["count"]
        self.balance = self.resources["player"]["starting_balance"]

        saved_data = load_game()
        if saved_data:
            self.balance = saved_data.get("balance", self.balance)
            self.barn = {int(k): v for k, v in saved_data.get("barn", {}).items()}
            self.inventory = saved_data.get("inventory", {f.key: 0 for f in self.fertilizers})
            self.saved_plots = saved_data.get("plots", {})
            self.plot_count = saved_data.get("plot_count", self.plot_count)
            logger.info("Сохранение загружено успешно")
        else:
            self.barn = {}
            self.inventory = {f.key: 0 for f in self.fertilizers}
            self.saved_plots = {}
            logger.info("Сохранений не найдено, старт новой игры")

        top = tk.Frame(self.root)
        top.pack(pady=10)

        self.balance_label = tk.Label(top, text=f"Баланс: {self.balance}₴", font=("Arial", 14))
        self.balance_label.pack()

        tk.Button(top, text="Купить удобрение", command=self.buy_fertilizer).pack(pady=5)
        tk.Button(top, text="Магазин грядок", command=self.buy_plot_window).pack(pady=5)
        tk.Button(top, text="Продать урожай", command=self.sell_crop).pack(pady=5)

        self.farm_frame = tk.Frame(self.root)
        self.farm_frame.pack(pady=10)

        self.plots = []
        for i in range(self.plot_count):
            plot_data = self.saved_plots.get(str(i))
            fert_count = plot_data.get("fertilizer_count", 0) if plot_data else 0
            self.plots.append(PlotView(self.farm_frame, i, self, saved_plot=plot_data, fertilizer_count=fert_count))

        self.barn_label = tk.Label(self.root, text="")
        self.barn_label.pack()
        self.update_barn_label()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        logger.info("Инициализация интерфейса завершена")
        self.root.mainloop()

    def on_close(self):
        self.save_game()
        logger.info("Игра закрыта")
        self.root.destroy()

    def get_plot_price(self, plot_number):
        if plot_number < 7:
            return 50 + plot_number * 80
        elif plot_number == 7:
            return 1500
        elif plot_number == 10:
            return 1000
        else:
            increments = [1000, 1500, 2000, 3000, 3000, 3000, 3000]
            extra_index = plot_number - 8
            increment = increments[extra_index] if extra_index < len(increments) else increments[-1]
            previous_price = self.get_plot_price(plot_number - 1)
            return previous_price + increment

    def choose_fertilizer_for_bundle(self):
        options = [f"{f.name} — {f.price}₴" for f in self.fertilizers if f.key != "none"]
        choice = simpledialog.askstring("Выбор удобрения",
                                        "Выберите удобрение для комплекта (5 шт):\n" + "\n".join(options))
        if not choice:
            logger.info("Выбор удобрения отменен пользователем")
            return None
        fert = next((f for f in self.fertilizers if f.name.lower() == choice.lower()), None)
        if fert:
            logger.info(f"Выбрано удобрение: {fert.name}")
        else:
            logger.warning(f"Удобрение '{choice}' не найдено")
        return fert

    def buy_plot_window(self):
        if self.plot_count >= self.MAX_PLOTS:
            logger.info("Попытка купить грядку при максимуме")
            return

        offers = [f"Грядка №{i+1} — {self.get_plot_price(i)}₴" for i in range(self.plot_count, self.MAX_PLOTS)]
        choice = simpledialog.askstring("Покупка грядки",
                                        "Доступные грядки:\n" + "\n".join(offers) +
                                        "\n\nВведите номер грядки для покупки:")
        if not choice:
            logger.info("Покупка грядки отменена пользователем")
            return

        try:
            number = int(choice) - 1
        except ValueError:
            logger.warning(f"Ошибка ввода номера грядки: {choice}")
            return

        if number < self.plot_count or number >= self.MAX_PLOTS:
            logger.warning(f"Недоступная грядка: {number+1}")
            return

        base_price = self.get_plot_price(number)
        answer = simpledialog.askstring("Дополнительно", "Хотите купить грядку с удобрением? (да/нет)")
        fert_count_to_apply = 0

        if answer and answer.lower() == "да":
            fert = self.choose_fertilizer_for_bundle()
            if fert is None:
                logger.info("Покупка грядки с удобрением отменена")
                return
            total_price = base_price + fert.price * 5
            if self.balance < total_price:
                logger.warning(f"Недостаточно средств для покупки грядки №{number+1} с удобрением")
                return
            self.balance -= total_price
            self.inventory[fert.key] += 5
            self.update_balance()
            fert_count_to_apply = 5
            logger.info(f"Куплена грядка №{number+1} с 5 удобрениями ({fert.name})")
        else:
            if self.balance < base_price:
                logger.warning(f"Недостаточно средств для покупки грядки №{number+1}")
                return
            self.balance -= base_price
            self.update_balance()
            logger.info(f"Куплена грядка №{number+1} без удобрений")

        self.plot_count = number + 1
        plot_data = self.saved_plots.get(str(number))
        self.plots.append(PlotView(self.farm_frame, number, self, saved_plot=plot_data, fertilizer_count=fert_count_to_apply))
        self.save_game()

    def buy_fertilizer(self):
        options = [f"{f.name} ({f.price}₴)" for f in self.fertilizers if f.key != "none"]
        choice = simpledialog.askstring("Покупка", "Введите название удобрения:\n" + "\n".join(options))
        if not choice:
            logger.info("Покупка удобрения отменена пользователем")
            return
        fert = next((f for f in self.fertilizers if f.name.lower() == choice.lower()), None)
        if not fert:
            logger.warning(f"Попытка купить несуществующее удобрение: {choice}")
            return
        if self.balance < fert.price:
            logger.warning(f"Недостаточно средств для покупки удобрения: {fert.name}")
            return
        self.balance -= fert.price
        self.inventory[fert.key] += 1
        self.update_balance()
        self.save_game()
        logger.info(f"Куплено удобрение: {fert.name}. В инвентаре: {self.inventory[fert.key]}")

    def sell_crop(self):
        if not self.barn:
            logger.info("Попытка продать урожай при пустом амбаре")
            return
        earned = sum(self.sell_prices.get(pid, 10) * qty for pid, qty in self.barn.items())
        self.balance += earned
        self.update_balance()

        for pid, qty in self.barn.items():
            plant_name = next((p.name for p in self.plants if p.id == pid), str(pid))
            logger.info(f"Собрано {qty} × {plant_name}")

        self.barn = {}
        self.update_barn_label()
        self.save_game()
        logger.info(f"Продан урожай, заработано {earned}₴")

    def update_balance(self):
        self.balance_label.config(text=f"Баланс: {self.balance}₴")

    def plant_seed(self, plot_index, plant_id):
        plot = self.plots[plot_index]
        plant = next((p for p in self.plants if p.id == plant_id), None)
        if plot and plant:
            plot.plant(plant)  # твоя логика посадки
            logger.info(f"Посажено растение {plant.name} на грядку №{plot_index+1}")
            self.save_game()

    def add_to_barn(self, pid):
        pid = int(pid)
        self.barn[pid] = self.barn.get(pid, 0) + 1
        self.update_barn_label()
        self.save_game()
        plant_name = next((p.name for p in self.plants if p.id == pid), str(pid))
        logger.info(f"Собрано растение: {plant_name} (ID: {pid})")

    def update_barn_label(self):
        if not self.barn:
            text = "пусто"
        else:
            text = ", ".join(f"{p.name}: {self.barn.get(p.id, 0)}"
                             for p in self.plants if self.barn.get(p.id, 0) > 0)
        self.barn_label.config(text="Амбар: " + text)

    def save_game(self):
        plots_data = {}
        for idx, plot in enumerate(self.plots):
            if plot.model:
                plots_data[str(idx)] = {
                    "state": plot.model.state,
                    "plant_id": plot.model.plant.id,
                    "remaining": plot.model.remaining,
                    "fertilizer_count": getattr(plot, "fertilizer_count", 0)
                }
            else:
                plots_data[str(idx)] = {
                    "state": "empty",
                    "plant_id": None,
                    "remaining": 0,
                    "fertilizer_count": 0
                }

        save_game({
            "balance": self.balance,
            "barn": self.barn,
            "inventory": self.inventory,
            "plots": plots_data,
            "plot_count": self.plot_count
        })
