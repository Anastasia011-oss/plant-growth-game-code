import unittest
from unittest.mock import MagicMock
from App.Model.apple import AppleModel
from App.Controller.apple_controller import AppleController

class FakeFertilizer:
    mult = 1.0
    price = 50
    key = "fert1"
    name = "Удобрение1"

class TestAppleController(unittest.TestCase):
    def test_start_growth_without_gui(self):
        controller = AppleController.__new__(AppleController)
        controller.app_controller = MagicMock()
        controller.app_controller.inventory = {"fert1": 1}

        win = MagicMock()
        fert = FakeFertilizer()

        controller.tick = MagicMock()

        controller.start_growth(fert, win)

        win.destroy.assert_called_once()
        self.assertEqual(controller.app_controller.inventory["fert1"], 0)
        self.assertIsInstance(controller.model, AppleModel)
        self.assertEqual(controller.model.state, "growing")
        controller.tick.assert_called_once()

if __name__ == "__main__":
    unittest.main()
