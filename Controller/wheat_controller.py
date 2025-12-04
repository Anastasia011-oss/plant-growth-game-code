from Model.wheat import WheatModel
from Controller.plot_controller_base import PlotControllerBase

class WheatController(PlotControllerBase):
    def start_growth(self, fert, win):
        self.model = WheatModel()
        if fert.key != "none":
            self.app_controller.inventory[fert.key] -= 1
        win.destroy()
        self.model.start_growth(fert)
        self.tick()
