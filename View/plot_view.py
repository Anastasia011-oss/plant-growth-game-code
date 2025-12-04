import tkinter as tk
from tkinter import simpledialog, messagebox
import os

IMAGE_DIR = os.path.join(os.getcwd(), "image")

class PlotView:
    def __init__(self, root, index, controller, saved_plot=None):
        self.controller = controller
        self.model = None  # Модель растения
        self.frame = tk.Frame(root, bd=2, relief="ridge", width=160, height=160)
        self.frame.grid(row=index // 3, column=index % 3, padx=5, pady=5)
        self.frame.grid_propagate(False)

        # Загружаем изображения
        self.images = {
            "empty": tk.PhotoImage(width=160, height=160),  # пустое поле
            "wheat_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_wheat.PNG")),
            "wheat_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_wheat.png")),
            "wheat_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_wheat_is_ripe.png")),
            "grapes_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_grapes.png")),
            "grapes_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_grapes.png")),
            "grapes_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_grapes_is_ripe.png")),
            "pineapple_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_pineapple.png")),
            "pineapple_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_pineapple.png")),
            "pineapple_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_pineapple_is_ripe.png")),
            "apple_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_apple_tree.png")),
            "apple_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_apple_tree.png")),
            "apple_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_apple_tree_is_ripe.png")),
            "melon_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_melon.png")),
            "melon_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_melon.png")),
            "melon_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_melon_is_ripe.png")),
            "sunflower_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_sunflower.png")),
            "sunflower_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_sunflower.png")),
            "sunflower_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_sunflower_is_ripe.png")),
        }

        # Метка с изображением
        self.img_label = tk.Label(self.frame, image=self.images["empty"])
        self.img_label.place(relx=0.5, rely=0.45, anchor="center")

        # Текстовая метка
        self.text_label = tk.Label(
            self.frame, text="Пусто", font=("Arial", 10),
            wraplength=150, justify="center"
        )
        self.text_label.place(relx=0.5, rely=0.9, anchor="center")

        # Кнопка посадки / сбора
        self.btn = tk.Button(self.frame, text="Посадить", command=self.plant_window)
        self.btn.place(relx=0.5, rely=0.95, anchor="center")

        # Восстанавливаем состояние из сохранения
        if saved_plot:
            self.load_saved(saved_plot)

    def load_saved(self, data):
        state = data.get("state")
        plant_id = data.get("plant_id")
        remaining = data.get("remaining", 0)

        if state == "empty" or plant_id is None:
            self.reset()
        else:
            from Model.plant_base import PlantModel
            plant = next((p for p in self.controller.plants if p.id == plant_id), None)
            if not plant:
                self.reset()
                return
            self.model = PlantModel(plant)
            self.model.state = state
            self.model.remaining = remaining

            # отображаем текущее состояние
            if state == "growing":
                self.update_growing(self.model.remaining // 1000, plant.name)
                self.tick()
            elif state == "ready":
                self.update_ready(plant.name)

    def plant_window(self):
        options = [p.name for p in self.controller.plants]
        choice = simpledialog.askstring("Посадка", "Введите растение:\n" + "\n".join(options))
        if not choice:
            return
        plant = next((p for p in self.controller.plants if p.name.lower() == choice.lower()), None)
        if not plant:
            messagebox.showerror("Ошибка", "Такого растения нет")
            return
        self.plant_crop(plant)

    def plant_crop(self, plant):
        from Model.plant_base import PlantModel
        self.model = PlantModel(plant)
        self.model.state = "growing"
        self.model.remaining = getattr(plant, "grow_time", 5000)
        self.update_growing(self.model.remaining // 1000, plant.name)
        self.tick()
        self.controller.save_game()

    def update_growing(self, sec, plant_name):
        plant_name = plant_name.lower()
        key = {
            "пшеница": "wheat_stage1" if sec > 2500 else "wheat_stage2",
            "виноград": "grapes_stage1" if sec > 2000 else "grapes_stage2",
            "ананас": "pineapple_stage1" if sec > 4000 else "pineapple_stage2",
            "яблоня": "apple_stage1" if sec > 3500 else "apple_stage2",
            "дыня": "melon_stage1" if sec > 4000 else "melon_stage2",
            "подсолнух": "sunflower_stage1" if sec > 1500 else "sunflower_stage2"
        }.get(plant_name, "empty")

        img = self.images[key]
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"Растёт...\n{sec} сек")
        self.btn.config(state="disabled")

    def update_ready(self, plant_name):
        key = {
            "пшеница": "wheat_ready",
            "виноград": "grapes_ready",
            "ананас": "pineapple_ready",
            "яблоня": "apple_ready",
            "дыня": "melon_ready",
            "подсолнух": "sunflower_ready"
        }.get(plant_name.lower(), "empty")

        img = self.images[key]
        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"{plant_name.capitalize()}\nСозрело!")
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
            self.controller.save_game()
            self.frame.after(1000, self.tick)
