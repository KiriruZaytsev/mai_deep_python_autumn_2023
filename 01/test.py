import homework as hw
import unittest

class TestGame(unittest.TestCase):

    def test_validate_input(self):
        new_game = hw.TicTacGame()
        self.assertFalse(new_game.validate_input(0, 1), False)
        self.assertTrue(new_game.validate_input(1, 1), True)
        new_game.board[0][0] = 'X'
        self.assertFalse(new_game.validate_input(1, 1), False)
        new_game.board[0][1] = 'O'
        self.assertFalse(new_game.validate_input(1, 2), False)
        self.assertRaises(TypeError, new_game.validate_input, '0', '0')
        self.assertRaises(TypeError, new_game.validate_input, [0], '0')
        self.assertRaises(TypeError, new_game.validate_input, (0, ), '0')

    def test_check_winner(self):
        game = hw.TicTacGame()
        self.assertEqual(game.check_winner(), 0)
        game.board = [['X', '.', '.'], ['X', '.', '.'], ['X', '.', '.']]
        self.assertEqual(game.check_winner(), 1)
        game.board = [['X', '.', '.'], ['.', 'X', '.'], ['.', '.', 'X']]
        self.assertEqual(game.check_winner(), 1)
        game.board = [['X', 'X', 'X'], ['O', 'O', '.'], ['.', '.', 'X']]
        self.assertEqual(game.check_winner(), 1)
        self.assertEqual(game.check_winner(), 1)
        game.board = [['.', 'X', '.'], ['O', 'O', 'O'], ['X', '.', 'X']]
        self.assertEqual(game.check_winner(), 2)
        game.board = [['O', 'O', 'X'], ['X', 'X', 'O'], ['O', 'X', 'X']]
        self.assertEqual(game.check_winner(), 3)

    def test_get_turn(self):
        new_game1 = hw.TicTacGame()
        self.assertRaises(ValueError, new_game1.get_turn, 'X', -1, -1)
        self.assertRaises(ValueError, new_game1.get_turn, 'T', 1, 2)
        new_game1.board[2][2] = 'X'
        self.assertRaises(ValueError, new_game1.get_turn, 'O', 3, 3)


    def test_get_opponent_char(self):
        game = hw.TicTacGame()
        self.assertRaises(ValueError, game.get_opponent_char, '1')
        self.assertEqual(game.get_opponent_char('X'), 'O')
        self.assertEqual(game.get_opponent_char('O'), 'X')

    def test_start_game(self):
        game1 = hw.TicTacGame()
        self.assertRaises(ValueError, game1.start_game, 3)
        
