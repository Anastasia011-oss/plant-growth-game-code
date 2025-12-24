import unittest
from unittest.mock import MagicMock
from App.Model.plant_base import Plant
from App.Controller.app_controller import AppController

class TestBarnAndSell(unittest.TestCase):
    def test_add_to_barn(self):
        app = AppController.__new__(AppController)
        app.plants = [Plant(1, "Пшеница", 1000)]
        app.barn = {}
        app.update_barn_label = MagicMock()
        app.save_game = MagicMock()
        app.update_missions = MagicMock()
        app.add_to_barn = AppController.add_to_barn.__get__(app)

        app.add_to_barn(1)
        self.assertEqual(app.barn[1], 1)
        app.update_missions.assert_called()

    def test_sell_crop(self):
        app = AppController.__new__(AppController)
        app.plants = [Plant(1, "Пшеница", 1000)]
        app.barn = {1: 2}
        app.sell_prices = {1: 10}
        app.balance = 0
        app.update_balance = MagicMock()
        app.update_missions = MagicMock()
        app.update_barn_label = MagicMock()
        app.save_game = MagicMock()
        app.sell_crop = AppController.sell_crop.__get__(app)

        app.sell_crop()
        self.assertEqual(app.balance, 20)
        self.assertEqual(app.barn, {})
        app.update_missions.assert_any_call("sell", 1)
        app.update_missions.assert_any_call("money", 20)

if __name__ == "__main__":
    unittest.main()
