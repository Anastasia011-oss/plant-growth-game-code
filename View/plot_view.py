import tkinter as tk
from tkinter import simpledialog, messagebox
from pathlib import Path

class PlotView:
    def __init__(self, root, index, controller, saved_plot=None):
        self.controller = controller
        self.model = None
        self.frame = tk.Frame(root, bd=2, relief="ridge", width=160, height=160)
        self.frame.grid(row=index // 3, column=index % 3, padx=5, pady=5)
        self.frame.grid_propagate(False)

        self.images = {"empty": tk.PhotoImage(width=160, height=160)}
        resources_path = Path(__file__).parent.parent / "Resources"
        images_path = resources_path / "Images"

        for plant_id, plant in self.controller.resources["plants"].items():
            for key, rel_path in plant.get("images", {}).items():
                full_path = images_path / Path(rel_path).name  # берём только имя файла
                if full_path.exists():
                    self.images[f"{plant['name'].lower()}_{key}"] = tk.PhotoImage(file=str(full_path))

        self.img_label = tk.Label(self.frame, image=self.images["empty"])
        self.img_label.place(relx=0.5, rely=0.45, anchor="center")

        self.text_label = tk.Label(self.frame, text="Пусто", font=("Arial", 10),
                                   wraplength=150, justify="center")
        self.text_label.place(relx=0.5, rely=0.9, anchor="center")

        self.btn = tk.Button(self.frame, text="Посадить", command=self.plant_window)
        self.btn.place(relx=0.5, rely=0.95, anchor="center")

        if saved_plot:
            self.load_saved(saved_plot)

    def load_saved(self, data):
        state = data.get("state", "empty")
        plant_id = data.get("plant_id")
        remaining = data.get("remaining", 0)

        if state == "empty" or plant_id is None:
            self.reset()
        else:
            plant = next((p for p in self.controller.plants if p.id == plant_id), None)
            if not plant:
                self.reset()
                return
            from Model.plant_base import PlantModel
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
            tk.Radiobutton(
                win,
                text=plant.name,
                variable=plant_var,
                value=plant.name,
                anchor="w"
            ).pack(fill="x", padx=15)

        def on_ok():
            choice = plant_var.get()
            if not choice:
                messagebox.showwarning("Ошибка", "Выберите растение")
                return

            plant = next((p for p in self.controller.plants if p.name.lower() == choice.lower()), None)
            if plant:
                self.plant_crop(plant)

            win.destroy()

        tk.Button(win, text="OK", width=10, command=on_ok).pack(pady=10)

    def plant_crop(self, plant):
        from Model.plant_base import PlantModel
        self.model = PlantModel(plant)
        self.model.state = "growing"
        self.model.remaining = getattr(plant, "grow_time", 5000)
        self.update_growing(self.model.remaining // 1000, plant.name)
        self.tick()
        self.controller.save_game()

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

    def update_ready(self, plant_name):
        key = f"{plant_name.lower()}_ready"
        img = self.images.get(key, self.images["empty"])
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"{plant_name}\nСозрело!")
        self.btn.config(state="normal", text="Собрать", command=self.collect_crop)

    def collect_crop(self):
        if self.model and self.model.plant:
            self.controller.add_to_barn(self.model.plant.id)
        self.reset()
        self.controller.save_game()

    def reset(self):
        img = self.images["empty"]
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text="Пусто")
        self.btn.config(text="Посадить", command=self.plant_window, state="normal")
        self.model = None
        self.controller.save_game()

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
