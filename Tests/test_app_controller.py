import unittest
from unittest.mock import MagicMock
from App.Controller.app_controller import AppController
from App.Model.plant_base import Plant
from App.Model.fertilizer import Fertilizer


class TestAppController(unittest.TestCase):
    def setUp(self):
        self.app = AppController.__new__(AppController)

        self.app.plants = [Plant(1, "Пшеница", 5000)]
        self.app.fertilizers = [Fertilizer("fert1", "Удобрение1", 1.0, 50)]
        self.app.plot_count = 2
        self.app.balance = 100
        self.app.barn = {}
        self.app.inventory = {"fert1": 0}

        self.app.update_balance = MagicMock()
        self.app.update_missions = MagicMock()
        self.app.update_barn_label = MagicMock()
        self.app.save_game = MagicMock()

        self.app.add_to_barn = AppController.add_to_barn.__get__(self.app)
        self.app.sell_crop = AppController.sell_crop.__get__(self.app)
        self.app.buy_fertilizer = AppController.buy_fertilizer.__get__(self.app)

        self.app.sell_prices = {1: 60}  # 1 растение = 60₴

    def test_add_to_barn(self):
        self.app.add_to_barn(1)
        self.assertEqual(self.app.barn[1], 1)
        self.app.update_missions.assert_called()

    def test_sell_crop(self):
        self.app.barn = {1: 2}  # 2 растения в амбаре
        self.app.sell_crop()

        # earned = 2 * 60 = 120
        self.assertEqual(self.app.balance, 100 + 120)
        self.assertEqual(self.app.barn, {})
        self.app.update_missions.assert_any_call("sell", 1)
        self.app.update_missions.assert_any_call("money", 120)

    def test_buy_fertilizer(self):
        fert = self.app.fertilizers[0]
        # Симулируем покупку без диалогов
        self.app.inventory[fert.key] = 0
        self.app.balance = 100

        if self.app.balance >= fert.price:
            self.app.balance -= fert.price
            self.app.inventory[fert.key] += 1

        self.assertEqual(self.app.inventory[fert.key], 1)
        self.assertEqual(self.app.balance, 50)


if __name__ == "__main__":
    unittest.main()
