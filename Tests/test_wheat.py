import unittest
from App.Model.wheat import WheatModel

class FakeFertilizer:
    mult = 1.0
    price = 50
    key = "fert1"
    name = "Удобрение1"

class TestWheatModel(unittest.TestCase):
    def setUp(self):
        self.model = WheatModel()

    def test_start_growth(self):
        self.model.start_growth(FakeFertilizer())
        self.assertEqual(self.model.state, "growing")
        self.assertEqual(self.model.remaining, 5000)

    def test_tick_reduces_time(self):
        self.model.start_growth(FakeFertilizer())
        self.model.tick(lambda x: None)
        self.assertEqual(self.model.remaining, 4000)

    def test_tick_finishes(self):
        class TestModel(WheatModel):
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
