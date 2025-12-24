import unittest
from unittest.mock import MagicMock, patch
from App.Model.mission import Mission
from App.Controller.app_controller import AppController

class TestMissions(unittest.TestCase):

    @patch('App.Controller.app_controller.messagebox.showinfo')
    def test_update_missions(self, mock_msg):
        mission = Mission(1, "Test", "plant", 1, 10)
        app = AppController.__new__(AppController)
        app.missions = [mission]
        app.balance = 0
        app.update_balance = MagicMock()
        app.update_missions = AppController.update_missions.__get__(app)

        app.update_missions("plant", 1)

        self.assertEqual(mission.progress, 1)
        self.assertTrue(mission.completed)
        mock_msg.assert_called()
