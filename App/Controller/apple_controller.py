from App.Model.apple import AppleModel
from App.Controller.plot_controller_base import PlotControllerBase

class AppleController(PlotControllerBase):
    def start_growth(self, fert, win):
        self.model = AppleModel()
        if fert.key != "none":
            self.app_controller.inventory[fert.key] -= 1
        win.destroy()
        self.model.start_growth(fert)
        self.tick()
