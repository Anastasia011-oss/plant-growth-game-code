from App.Model.grapes import GrapesModel
from App.Controller.plot_controller_base import PlotControllerBase

class GrapesController(PlotControllerBase):
    def start_growth(self, fert, win):
        self.model = GrapesModel()
        if fert.key != "none":
            self.app_controller.inventory[fert.key] -= 1
        win.destroy()
        self.model.start_growth(fert)
        self.tick()
