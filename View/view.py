import tkinter as tk
import os

IMAGE_DIR = os.path.join(os.getcwd(), "image")

class PlotView:
    def __init__(self, root, index, controller):
        self.controller = controller

        self.frame = tk.Frame(root, bd=2, relief="ridge", width=160, height=160)
        self.frame.grid(row=index // 3, column=index % 3, padx=5, pady=5)
        self.frame.grid_propagate(False)

        self.images = {
            "empty": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_wheat.PNG")),

            "wheat_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_wheat.PNG")),
            "wheat_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_wheat.png")),
            "wheat_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_wheat_is_ripe.png")),

            "grapes_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_grapes.png")),
            "grapes_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_grapes.png")),
            "grapes_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_grapes_is_ripe.png")),

            "pineapple_stage1": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "little_pineapple.png")),
            "pineapple_stage2": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "medium_pineapple.png")),
            "pineapple_ready": tk.PhotoImage(file=os.path.join(IMAGE_DIR, "the_pineapple_is_ripe.png")),
        }

        self.img_label = tk.Label(self.frame)
        self.img_label.place(relx=0.5, rely=0.45, anchor="center")

        self.text_label = tk.Label(self.frame, text="Пусто", font=("Arial", 10),
                                   wraplength=150, justify="center")
        self.text_label.place(relx=0.5, rely=0.9, anchor="center")

        self.btn = tk.Button(self.frame, text="Посадить", command=self.controller.open_plant_window)
        self.btn.place(relx=0.5, rely=0.95, anchor="center")

    def update_growing(self, sec, plant_name):
        if plant_name.lower() == "пшеница":
            img = self.images["wheat_stage1"] if sec > 2500 else self.images["wheat_stage2"]
        elif plant_name.lower() == "виноград":
            img = self.images["grapes_stage1"] if sec > 2000 else self.images["grapes_stage2"]
        elif plant_name.lower() == "ананас":
            img = self.images["pineapple_stage1"] if sec > 4000 else self.images["pineapple_stage2"]
        else:
            img = self.images["empty"]

        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"Растёт...\n{sec} сек")
        self.btn.config(state="disabled")

    def update_ready(self, plant_name):
        if plant_name.lower() == "пшеница":
            img = self.images["wheat_ready"]
        elif plant_name.lower() == "виноград":
            img = self.images["grapes_ready"]
        elif plant_name.lower() == "ананас":
            img = self.images["pineapple_ready"]
        else:
            img = self.images["empty"]

        self.img_label.config(image=img)
        self.img_label.image = img
        self.text_label.config(text=f"{plant_name}\nСозрело!")
        self.btn.config(state="normal", text="Собрать", command=self.controller.collect_crop)

    def reset(self):
        self.img_label.config(image="")
        self.img_label.image = None
        self.text_label.config(text="Пусто")
        self.btn.config(text="Посадить", command=self.controller.open_plant_window, state="normal")
