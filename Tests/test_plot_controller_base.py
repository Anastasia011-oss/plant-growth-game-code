import unittest
from unittest.mock import MagicMock
from App.Controller.plot_controller_base import PlotControllerBase
from App.Model.plant_base import Plant, PlantModel

class FakePlant:
    def __init__(self, pid=1, name="TestPlant", grow_time=5000):
        self.id = pid
        self.name = name
        self.grow_time = grow_time

class FakePlotView:
    def __init__(self, root, index, controller):
        self.frame = MagicMock()
    def update_ready(self, name):
        self.updated_ready = name
    def update_growing(self, remaining, name):
        self.updated_growing = (remaining, name)
    def reset(self):
        self.reset_called = True

class TestPlotControllerBase(unittest.TestCase):
    def setUp(self):
        self.controller = PlotControllerBase.__new__(PlotControllerBase)
        self.controller.app_controller = MagicMock()
        self.controller.app_controller.plants = [FakePlant()]
        self.controller.view = FakePlotView(None, 0, self.controller)
        self.controller.model = None

    def test_tick_without_model(self):
        self.controller.tick()
        self.assertIsNone(self.controller.model)

    def test_collect_crop_without_model(self):
        self.controller.collect_crop()
        self.assertIsNone(self.controller.model)

    def test_collect_crop_with_model(self):
        plant = FakePlant()
        model = PlantModel(plant)
        model.state = "ready"
        self.controller.model = model
        self.controller.app_controller.add_to_barn = MagicMock()
        self.controller.collect_crop()
        self.controller.app_controller.add_to_barn.assert_called_once_with(plant.id)
        self.assertIsNone(self.controller.model)

if __name__ == "__main__":
    unittest.main()
