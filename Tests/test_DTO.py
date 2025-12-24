import unittest
from App.DTO.plot_dto import PlotDTO

class TestPlotDTO(unittest.TestCase):
    def test_initialization(self):
        plot = PlotDTO(index=0, state="empty", plant_id=None, remaining=0, fertilizer_count=2)
        self.assertEqual(plot.index, 0)
        self.assertEqual(plot.state, "empty")
        self.assertIsNone(plot.plant_id)
        self.assertEqual(plot.remaining, 0)
        self.assertEqual(plot.fertilizer_count, 2)

if __name__ == "__main__":
    unittest.main()
