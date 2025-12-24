import tkinter as tk
from App.Model.plant_base import PlantModel
from App.View.plot_view import PlotView

class PlotControllerBase:
    def __init__(self, root, index, app_controller):
        self.app_controller = app_controller
        self.model = None
        self.view = PlotView(root, index, self)

    def open_plant_window(self):
        options = [p.name for p in self.app_controller.plants]
        choice = tk.simpledialog.askstring("Посадить", "Выберите растение:\n" + "\n".join(options))
        if not choice:
            return
        plant = next((p for p in self.app_controller.plants if p.name.lower() == choice.lower()), None)
        if not plant:
            tk.messagebox.showerror("Ошибка", "Такого растения нет")
            return
        self.model = PlantModel(plant)
        self.model.start_growth()
        self.tick()

    def tick(self):
        if not self.model or self.model.state != "growing":
            return

        def update(state):
            if state == "finish":
                self.view.update_ready(self.model.plant.name)
            else:
                self.view.update_growing(self.model.remaining // 1000, self.model.plant.name)

        self.model.timer_id = self.view.frame.after(1000, self.tick)
        self.model.tick(update)

    def collect_crop(self):
        if not self.model or not self.model.plant:
            return
        self.app_controller.add_to_barn(self.model.plant.id)
        self.view.reset()
        self.model.state = "empty"
        self.model.plant = None
        self.model.remaining = 0
        self.model = None
