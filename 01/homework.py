"""Импортируем модуль sys, с помощью которого
может быть получено большое число 2**64-1"""
import sys

class TicTacGame:
    """Класс, описывающий игру в крестики-нолики"""

    player_chars = {'X': 1, 'O': 2}

    board = [['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']]

    def show_board(self):
        """Функция вывода игрового поля"""
        board = self.board

        for i in range(3):
            print(board[i])

    def validate_input(self, x_coord, y_coord):
        """Функция проверки корректности хода"""
        if not isinstance(x_coord, int) and not isinstance(y_coord, int):
            raise TypeError('Координаты должны быть целочисленными')
        if (1 <= x_coord <= 3 and 1 <= y_coord <= 3
            and (self.board[x_coord-1][y_coord-1] != 'X'
            and self.board[x_coord-1][y_coord-1] != 'O')):
            return True
        return False

    def check_winner(self):
        """Функция проверки окончания игры. Если результат 0,
        то победитель не выявлен, игра продолжается. Если
        вывод функции 1, то победили X. Если вывод 2, то
        победили 0. Если функция вывела 3, то ничья """
        board = self.board
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != '.':
                return 1 if board[i][0] == 'X' else 2
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != '.':
                return 1 if board[0][i] == 'X' else 2

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '.':
            return 1 if board[0][0] == 'X' else 2
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '.':
            return 1 if board[0][2] == 'X' else 2

        is_draw = True
        for row in board:
            if '.' in row:
                is_draw = False
                break

        if is_draw:
            return 3


        return 0

    def get_turn(self, char, x_coord, y_coord):
        """Функция, которая делает ход на игровом поле, по указанным
        игроком координатам"""
        if char not in ['X', 'O']:
            raise ValueError('Введён некорректный символ')
        print('Введите координаты, куда вы бы хотели сходить')
        x_to_0idx = x_coord-1
        y_to_0idx = y_coord-1
        if self.validate_input(x_coord, y_coord):
            self.board[x_to_0idx][y_to_0idx] = char
        else:
            raise ValueError('Введены недопустимые координаты')

    def get_user_char(self):
        """Функция, которая получает сторону, за которую будет играть
        игрок"""
        print('Введите сторону, за которую вы бы хотели играть')
        user_char = input()
        if user_char not in ['X', 'O']:
            raise ValueError('Введён некорректный символ')
        return user_char

    def get_opponent_char(self, user_char):
        """Функция, вычисляющая сторону, за которую будет играть
        компьютер"""
        if user_char not in ['X', 'O']:
            raise ValueError('Введён недопустимый символ')
        if user_char == 'X':
            return 'O'
        return 'X'

    def minimax(self, field, depth, is_ai_turn, computer_char):
        """Функция, реализующая алгоритм поиска хода для компьютера"""
        player = self.player_chars[computer_char]

        if self.check_winner() == player:
            return 100
        if self.check_winner() == 3-player:
            return -100
        if self.check_winner() == 0:
            return 0

        if is_ai_turn:
            best_score = - sys.maxsize
            for y_coord in range(3):
                for x_coord in range(3):
                    if self.board[y_coord][x_coord] == '.':
                        self.board[y_coord][x_coord] = computer_char
                        score = self.minimax(field, depth + 1, False, computer_char)
                        field[y_coord][x_coord] = '.'
                        best_score = max(best_score, score)
        else:
            best_score = sys.maxsize
            for y_coord in range(3):
                for x_coord in range(3):
                    if self.board[y_coord][x_coord] == '.':
                        self.board[y_coord][x_coord] = self.get_opponent_char(computer_char)
                        score = self.minimax(field, depth + 1, True, computer_char)
                        field[y_coord][x_coord] = '.'
                        best_score = min(best_score, score)
        return best_score

    def get_computer_position(self, computer_char):
        """Функция, возвращающая ход, который сделает компьютер"""
        move = None
        best_score = -sys.maxsize
        field = [self.board[y_coord].copy() for y_coord in range(3)]
        for y_coord in range(3):
            for x_coord in range(3):
                if field[y_coord][x_coord] == '.':
                    field[y_coord][x_coord] = computer_char
                    score = self.minimax(field, 0, False, computer_char)
                    field[y_coord][x_coord] = '.'
                    if score > best_score:
                        best_score = score
                        move = (x_coord, y_coord)

        return move

    def start_singleplayer_game(self):
        """Функция, которая запускают игру против компьютера"""
        user_char = self.get_user_char()
        opponent_char = self.get_opponent_char(user_char)
        result = 0
        self.show_board()
        while result == 0:
            if user_char == 'X':
                x_coord, y_coord = map(int, input().split())
                self.get_turn(user_char, x_coord, y_coord)
                result = self.check_winner()
                print('Ход соперника')
                move = self.get_computer_position(opponent_char)
                x_coord, y_coord = move
                self.board[y_coord][x_coord] = opponent_char
                result = self.check_winner()
                self.show_board()
            elif user_char == 'O':
                print('Ход соперника')
                move = self.get_computer_position(opponent_char)
                x_coord, y_coord = move
                self.board[y_coord][x_coord] = opponent_char
                result = self.check_winner()
                self.show_board()
                x_coord, y_coord = map(int, input().split())
                self.get_turn(user_char, x_coord, y_coord)
                result = self.check_winner()
                self.show_board()

        if result == self.player_chars[user_char]:
            print('Вы выиграли')
        elif result == self.player_chars[opponent_char]:
            print('Вы проиграли')
        else:
            print('Ничья')


    def start_multiplayer_game(self):
        """Функция, которая запускает игру с двумя игроками"""
        player = 0
        result = 0
        while result == 0:
            print(f'Ход игрока {player + 1}')
            if player == 0:
                x_coord, y_coord = map(int, input().split())
                self.get_turn('X', x_coord, y_coord)
                result = self.check_winner()
                self.show_board()
            elif player == 1:
                x_coord, y_coord = map(int, input().split())
                self.get_turn('O', x_coord, y_coord)
                result = self.check_winner()
                self.show_board()
            player = (player+1)%2
        if 0 < result < 3:
            print(f'Победил игрок {result}')
        else:
            print('Ничья')

    def start_game(self, mode):
        """Функция, которая получает режим игры и создаёт соответствующую игру"""
        if not isinstance(mode, int):
            raise TypeError('Режим должен быть числом')
        if mode not in [1, 2]:
            raise ValueError('Режим может быть только singleplayer или multiplayer')
        if mode == 1:
            self.start_singleplayer_game()
        elif mode == 2:
            self.start_multiplayer_game()






if __name__ == "__main__":
    print('Введите режим игры (singleplayer - 1 или multiplayer - 2)')
    game_mode = int(input())
    game = TicTacGame()
    game.start_game(game_mode)
