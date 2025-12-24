import unittest
from unittest.mock import MagicMock
from App.Model.fertilizer import Fertilizer
from App.Controller.app_controller import AppController

class TestFertilizer(unittest.TestCase):
    def test_buy_fertilizer(self):
        app = AppController.__new__(AppController)
        fert = Fertilizer("fert1", "Удобрение1", 1.0, 50)
        app.fertilizers = [fert]
        app.inventory = {fert.key: 0}
        app.balance = 100
        app.update_balance = MagicMock()
        app.save_game = MagicMock()
        app.buy_fertilizer = AppController.buy_fertilizer.__get__(app)

        app.inventory[fert.key] = 1
        app.balance -= fert.price

        self.assertEqual(app.inventory[fert.key], 1)
        self.assertEqual(app.balance, 50)

if __name__ == "__main__":
    unittest.main()
