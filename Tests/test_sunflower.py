import unittest
from App.Model.sunflower import SunflowerModel

class FakeFertilizer:
    mult = 1.0
    price = 50
    key = "fert1"
    name = "Удобрение1"

class TestSunflowerModel(unittest.TestCase):
    def setUp(self):
        self.model = SunflowerModel()

    def test_start_growth(self):
        self.model.start_growth(FakeFertilizer())
        self.assertEqual(self.model.state, "growing")
        self.assertEqual(self.model.remaining, 3000)

    def test_tick_reduces_time(self):
        self.model.start_growth(FakeFertilizer())
        self.model.tick(lambda x: None)
        self.assertEqual(self.model.remaining, 2000)

    def test_tick_finishes(self):
        class TestModel(SunflowerModel):
            def tick(self, callback):
                self.remaining = 0
                self.state = "ready"
                callback("finish")
        model = TestModel()
        finished = []
        model.tick(lambda e: finished.append(e))
        self.assertIn("finish", finished)
        self.assertEqual(model.state, "ready")

if __name__ == "__main__":
    unittest.main()
