import unittest
from statistics_service import StatisticsService
from player import Player
from statistics_service import SortBy


class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54),  # 45+54 = 99
            Player("Kurri", "EDM", 37, 53),  # 37+53 = 90
            Player("Yzerman", "DET", 42, 56),  # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89),  # 35+89 = 124
        ]


class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(PlayerReaderStub())

    def test_nonexistent_player(self):
        res = self.stats.search("Selänne")
        self.assertIsNone(res)

    def test_existing_player(self):
        res = self.stats.search("Kurri")
        exp = Player("Kurri", "EDM", 37, 53)
        self.assertEqual(res.name, exp.name)
        self.assertEqual(res.team, exp.team)
        self.assertEqual(res.goals, exp.goals)
        self.assertEqual(res.assists, exp.assists)

    def test_team(self):
        res = self.stats.team("PIT")
        exp = [Player("Lemieux", "PIT", 45, 54)]
        self.assertEqual(exp[0].name, res[0].name)
        self.assertEqual(res[0].team, exp[0].team)
        self.assertEqual(res[0].goals, exp[0].goals)
        self.assertEqual(res[0].assists, exp[0].assists)

    def test_top_default(self):
        res = self.stats.top(1, None)
        exp = [Player("Gretzky", "EDM", 35, 89)]
        self.assertEqual(exp[0].name, res[0].name)
        self.assertEqual(res[0].team, exp[0].team)
        self.assertEqual(res[0].goals, exp[0].goals)
        self.assertEqual(res[0].assists, exp[0].assists)

    def test_top_points(self):
        res = self.stats.top(1, SortBy.POINTS)
        exp = [Player("Gretzky", "EDM", 35, 89)]
        self.assertEqual(exp[0].name, res[0].name)
        self.assertEqual(res[0].team, exp[0].team)
        self.assertEqual(res[0].goals, exp[0].goals)
        self.assertEqual(res[0].assists, exp[0].assists)

    def test_top_assists(self):
        res = self.stats.top(1, SortBy.ASSISTS)
        exp = [Player("Gretzky", "EDM", 35, 89)]
        self.assertEqual(exp[0].name, res[0].name)
        self.assertEqual(res[0].team, exp[0].team)
        self.assertEqual(res[0].goals, exp[0].goals)
        self.assertEqual(res[0].assists, exp[0].assists)

    def test_top_goals(self):
        res = self.stats.top(1, SortBy.GOALS)
        exp = [Player("Lemieux", "PIT", 45, 54)]
        self.assertEqual(exp[0].name, res[0].name)
        self.assertEqual(res[0].team, exp[0].team)
        self.assertEqual(res[0].goals, exp[0].goals)
        self.assertEqual(res[0].assists, exp[0].assists)

    def test_player(self):
        res = Player("Semenko", "EDM", 4, 12).__str__()
        exp = "Semenko EDM 4 + 12 = 16"
        self.assertEqual(exp, res)
