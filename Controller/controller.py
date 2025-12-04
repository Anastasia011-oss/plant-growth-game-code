import tkinter as tk
from tkinter import messagebox
from Model.model import PlotModel
from View.view import PlotView

class PlotController:
    def __init__(self, root, index, app_controller):
        self.app_controller = app_controller
        self.model = PlotModel(index)
        self.view = PlotView(root, index, self)

    def open_plant_window(self):
        win = tk.Toplevel()
        win.title("Посадка")
        win.geometry("260x250")

        tk.Label(win, text="Выберите растение").pack(pady=5)

        plant_var = tk.StringVar(value="1")
        for p in self.app_controller.plants:
            tk.Radiobutton(win, text=p.name, variable=plant_var, value=str(p.id)).pack(anchor="w")

        tk.Label(win, text="Удобрение").pack(pady=5)

        fert_var = tk.StringVar(value="none")
        for f in self.app_controller.fertilizers:
            count = self.app_controller.inventory[f.key]
            if f.key == "none" or count > 0:
                tk.Radiobutton(win, text=f"{f.name} (×{f.mult}) [{count} шт]",
                               variable=fert_var, value=f.key).pack(anchor="w")

        tk.Button(win, text="Посадить",
                  command=lambda: self.start_growth(int(plant_var.get()), fert_var.get(), win)).pack(pady=10)

    def start_growth(self, plant_id, fert_key, win):
        plant = self.app_controller.get_plant(plant_id)
        fert = self.app_controller.get_fertilizer(fert_key)

        if fert.key != "none":
            if self.app_controller.inventory[fert.key] <= 0:
                messagebox.showerror("Ошибка", "Удобрения нет в инвентаре")
                return
            self.app_controller.inventory[fert.key] -= 1

        win.destroy()
        self.model.start_growth(plant, fert)
        self.tick()

    def tick(self):
        if self.model.state != "growing":
            return

        def update(state):
            if state == "finish":
                self.view.update_ready(self.model.plant.name)
            else:
                self.view.update_growing(self.model.remaining // 1000, self.model.plant.name)
                self.model.timer_id = self.view.frame.after(1000, self.tick)

        self.model.tick(update)

    def collect_crop(self):
        self.app_controller.add_to_barn(self.model.plant.id)
        self.view.reset()
        self.model.state = "empty"
        self.model.plant = None
        self.model.remaining = 0

