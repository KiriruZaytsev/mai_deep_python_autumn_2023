from unittest import TestCase

from descriptor import Position, PlayerName, Number, FloatStat, BasketballPlayer

class TestDecriptor(TestCase):

    def test_valid_position(self):
        with self.assertRaises(TypeError):
            BasketballPlayer('Luka Doncic', 1, 77, 38.5, 11.2, 9.8)
        with self.assertRaises(ValueError):
            BasketballPlayer('Austin Reaves', 'Shooting Guard', 15, 20.5, 7.8, 7.1)
    
    def test_valid_name(self):
        with self.assertRaises(TypeError):
            BasketballPlayer(0, 0, 0, 0, 0, 0)

    def test_valid_number(self):
        with self.assertRaises(ValueError):
            BasketballPlayer('Kirill Zaytsev', 'PG', 100, 99.9, 99.9, 99.9)
        with self.assertRaises(ValueError):
            BasketballPlayer('Alexey Shar', 'PG', -1, 99.9, 99.9, 99.9)
        with self.assertRaises(TypeError):
            BasketballPlayer('Artyom Morozov', 'SG', 'A', 0.0, 0.0, 0.0)

    def test_valid_float(self):
        with self.assertRaises(TypeError):
            BasketballPlayer('Jimmy Butler', 'SF', 22, 100, 12.5, 10.5)
        with self.assertRaises(ValueError):
            BasketballPlayer('Ivanupolo', 'C', 66, 100.5, -1.2, 5.0)

    def test_get(self):
        player = BasketballPlayer('Jimmy Butler', 'SF', 22, 22.4, 7.8, 8.3)
        player_name = player.name
        player_pos = player.pos
        player_num = player.number
        player_avg = (player.avg_pts, player.avg_assists, player.avg_rebounds)
        self.assertTrue(player_name, 'Jimmy Butler')
        self.assertTrue(player_pos, 'SF')
        self.assertTrue(player_num, 22)
        self.assertTrue(player_avg, (22.4, 7.8, 8.3))

