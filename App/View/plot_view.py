import tkinter as tk
from tkinter import messagebox
from pathlib import Path

class PlotView:
    def __init__(self, root, index, controller, saved_plot=None, fertilizer_count=0):
        self.controller = controller
        self.model = None
        self.fertilizer_count = fertilizer_count

        self.frame = tk.Canvas(root, width=160, height=160, bd=0, highlightthickness=0)
        self.frame.grid(row=index // 3, column=index % 3, padx=5, pady=5)
        self.draw_3d_border()

        self.images = {"empty": tk.PhotoImage(width=160, height=160)}
        resources_path = Path(__file__).parent.parent / "Resources"
        images_path = resources_path / "Images"

        for plant_id, plant in self.controller.resources["plants"].items():
            for key, rel_path in plant.get("images", {}).items():
                full_path = images_path / Path(rel_path).name
                if full_path.exists():
                    self.images[f"{plant['name'].lower()}_{key}"] = tk.PhotoImage(file=str(full_path))

        self.img_label = tk.Label(self.frame, image=self.images["empty"], bd=0)
        self.img_label.place(relx=0.5, rely=0.45, anchor="center")

        self.text_label = tk.Label(self.frame, text="Пусто", font=("Arial", 10),
                                   wraplength=150, justify="center", bd=0)
        self.text_label.place(relx=0.5, rely=0.9, anchor="center")

        self.btn = tk.Button(self.frame, text="Посадить", command=self.plant_window)
        self.btn.place(relx=0.5, rely=0.95, anchor="center")

        if saved_plot:
            self.load_saved(saved_plot)

    def draw_3d_border(self):
        self.frame.create_line(0, 0, 160, 0, fill="#CCCCCC", width=3)
        self.frame.create_line(0, 0, 0, 160, fill="#CCCCCC", width=3)
        self.frame.create_line(0, 160, 160, 160, fill="#666666", width=3)
        self.frame.create_line(160, 0, 160, 160, fill="#666666", width=3)

    def load_saved(self, data):
        state = data.get("state", "empty")
        plant_id = data.get("plant_id")
        remaining = data.get("remaining", 0)
        self.fertilizer_count = data.get("fertilizer_count", 0)

        if state == "empty" or plant_id is None:
            self.reset()
        else:
            plant = next((p for p in self.controller.plants if p.id == plant_id), None)
            if not plant:
                self.reset()
                return
            from App.Model.plant_base import PlantModel
            self.model = PlantModel(plant)
            self.model.state = state
            self.model.remaining = remaining

            if state == "growing":
                self.update_growing(self.model.remaining // 1000, plant.name)
                self.tick()
            elif state == "ready":
                self.update_ready(plant.name)

    def plant_window(self):
        win = tk.Toplevel(self.frame)
        win.title("Посадка")
        win.grab_set()

        tk.Label(win, text="Выберите растение:", font=("Arial", 11, "bold")).pack(pady=5)
        plant_var = tk.StringVar()
        for plant in self.controller.plants:
            tk.Radiobutton(win, text=plant.name, variable=plant_var,
                           value=plant.name, anchor="w").pack(fill="x", padx=15)

        # Выбор удобрения
        tk.Label(win, text="Выберите удобрение (опционально):", font=("Arial", 11, "bold")).pack(pady=5)
        fert_var = tk.StringVar(value="none")
        for fert in self.controller.fertilizers:
            tk.Radiobutton(win, text=f"{fert.name} ({fert.price}₴)", variable=fert_var,
                           value=fert.key, anchor="w").pack(fill="x", padx=15)

        def on_ok():
            plant_choice = plant_var.get()
            fert_choice = fert_var.get()
            if not plant_choice:
                messagebox.showwarning("Ошибка", "Выберите растение")
                return

            plant = next((p for p in self.controller.plants if p.name.lower() == plant_choice.lower()), None)
            if plant:
                self.plant_crop(plant, fert_choice)

            win.destroy()

        tk.Button(win, text="OK", width=10, command=on_ok).pack(pady=10)

    # ---- метод, который вызывается кнопкой ----
    def plant_crop(self, plant, fert_key="none"):
        fert_count_to_use = 0
        if fert_key != "none" and self.controller.inventory.get(fert_key, 0) > 0:
            # используем максимум 5, но если меньше в инвентаре — используем столько, сколько есть
            fert_count_to_use = min(5, self.controller.inventory[fert_key])
            self.controller.inventory[fert_key] -= fert_count_to_use
            # засчитываем прогресс только по фактическому количеству использованных удобрений
            if fert_count_to_use > 0:
                self.controller.update_missions("fertilizer", fert_count_to_use)

        self.fertilizer_count = fert_count_to_use
        self.controller.plant_seed(self.controller.plots.index(self), plant.id)

    # ---- метод реальной посадки ----
    def plant(self, plant):
        from App.Model.plant_base import PlantModel
        self.model = PlantModel(plant)
        self.model.state = "growing"

        grow_time = getattr(plant, "grow_time", 5000)
        fert_bonus = 1 + 0.1 * self.fertilizer_count
        self.model.remaining = int(grow_time / fert_bonus) if self.fertilizer_count < 5 else 1000

        self.update_growing(self.model.remaining // 1000, plant.name)
        self.tick()
        self.controller.save_game()

    # ---- Обновление роста ----
    def update_growing(self, sec, plant_name):
        name = plant_name.lower()
        grow_time = 5000
        for pid, pdata in self.controller.resources["plants"].items():
            if pdata["name"].lower() == name:
                grow_time = pdata.get("grow_time", 5000)
                break

        key = f"{name}_stage1" if sec > grow_time // 2 else f"{name}_stage2"
        img = self.images.get(key, self.images["empty"])

        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"Растёт...\n{sec} сек")
        self.btn.config(state="disabled")

    # ---- Готово к сбору ----
    def update_ready(self, plant_name):
        key = f"{plant_name.lower()}_ready"
        img = self.images.get(key, self.images["empty"])
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"{plant_name}\nСозрело!")
        self.btn.config(state="normal", text="Собрать", command=self.collect_crop)

    # ---- Сбор урожая ----
    def collect_crop(self):
        if self.model and self.model.plant:
            self.controller.add_to_barn(self.model.plant.id)
        self.fertilizer_count = max(0, self.fertilizer_count - 1)
        self.reset()
        self.controller.save_game()

    # ---- Сброс грядки ----
    def reset(self):
        img = self.images["empty"]
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text="Пусто")
        self.btn.config(text="Посадить", command=self.plant_window, state="normal")
        self.model = None
        self.controller.save_game()

    # ---- Таймер роста ----
    def tick(self):
        if not self.model or self.model.state != "growing":
            return

        self.model.remaining -= 1000
        if self.model.remaining <= 0:
            self.model.remaining = 0
            self.model.state = "ready"
            self.update_ready(self.model.plant.name)
            self.controller.save_game()
        else:
            self.update_growing(self.model.remaining // 1000, self.model.plant.name)
            self.frame.after(1000, self.tick)
