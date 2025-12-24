import unittest
from unittest.mock import MagicMock
from App.Model.wheat import WheatModel
from App.Controller.wheat_controller import WheatController

class FakeFertilizer:
    key = "fert1"
    name = "Удобрение1"
    mult = 1.0
    price = 50

class TestWheatController(unittest.TestCase):
    def setUp(self):
        self.controller = WheatController.__new__(WheatController)
        self.controller.app_controller = MagicMock()
        self.controller.tick = MagicMock()
        self.controller.model = None
        self.controller.app_controller.inventory = {"fert1": 5}
        self.win = MagicMock()
        self.win.destroy = MagicMock()

    def test_start_growth_with_fertilizer(self):
        fert = FakeFertilizer()
        self.controller.start_growth(fert, self.win)
        self.assertIsInstance(self.controller.model, WheatModel)
        self.assertEqual(self.controller.model.state, "growing")
        self.assertEqual(self.controller.app_controller.inventory[fert.key], 4)
        self.controller.tick.assert_called_once()
        self.win.destroy.assert_called_once()

    def test_start_growth_without_fertilizer(self):
        class NoFert(FakeFertilizer):
            key = "none"

        fert = NoFert()
        self.controller.start_growth(fert, self.win)
        self.assertIsInstance(self.controller.model, WheatModel)
        self.controller.tick.assert_called()
        self.win.destroy.assert_called()

if __name__ == "__main__":
    unittest.main()
