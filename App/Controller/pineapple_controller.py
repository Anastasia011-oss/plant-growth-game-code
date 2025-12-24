from App.Model.pineapple import PineappleModel
from App.Controller.plot_controller_base import PlotControllerBase

class PineappleController(PlotControllerBase):
    def start_growth(self, fert, win):
        self.model = PineappleModel()
        if fert.key != "none":
            self.app_controller.inventory[fert.key] -= 1
        win.destroy()
        self.model.start_growth(fert)
        self.tick()
