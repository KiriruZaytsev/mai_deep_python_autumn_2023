class Position:
    #Класс-дескриптор, описывающий позицию игрока
    positions = ('PG', 'SG', 'SF', 'PF', 'C')

    @classmethod
    def _validate_pos(cls, pos):
        if not isinstance(pos, str):
            raise TypeError('Позиция должна быть строкой')
        if not pos in cls.positions:
            raise ValueError('Такой позиции нет')

    def __set_name__(self, obj, name):
        self._protected_pos = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._protected_pos)

    def __set__(self, instance, value):
        self._validate_pos(value)
        setattr(instance, self._protected_pos, value)

class PlayerName:
    #Класс-дескриптор для имени игрока
    @classmethod
    def _validate_name(cls, player_name):
        if not isinstance(player_name, str):
            raise TypeError('Имя должно быть строкой')

    def __set_name__(self, obj, name):
        self._protected_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._protected_name)

    def __set__(self, instance, value):
        self._validate_name(value)
        setattr(instance, self._protected_name, value)

class Number:
    #Класс-дескриптор для номера игрока
    @classmethod
    def _validate_number(cls, num):
        if not isinstance(num, int):
            raise TypeError('Номер должен быть целым числом')
        if num < 0:
            raise ValueError('Номер не может быть отрицательным')
        if num >= 100:
            raise ValueError('Номер должен быть двухзначным числом')

    def __set_name__(self, obj, name):
        self._protected_number = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._protected_number)

    def __set__(self, instance, value):
        self._validate_number(value)
        setattr(instance, self._protected_number, value)

class FloatStat:
    #Класс-дескриптор для вещественных значений
    @classmethod
    def _validate_stat(cls, stat):
        if not isinstance(stat, float):
            raise TypeError('Средняя статистика должна быть вещественным числом')
        if stat < 0.0:
            raise ValueError('Средняя статистика не может быть отрицательной')

    def __set_name__(self, obj, name):
        self._protected_stat = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self._protected_stat)

    def __set__(self, instance, value):
        self._validate_stat(value)
        setattr(instance, self._protected_stat, value)

class BasketballPlayer:
    #Класс, описывающий баскетболиста и его статистику
    name = PlayerName()
    pos = Position()
    number = Number()
    avg_pts = FloatStat()
    avg_assists = FloatStat()
    avg_rebounds = FloatStat()

    def __init__(self, name, pos, number, avg_pts, avg_assists, avg_rebounds):
        self.name = name
        self.pos = pos
        self.number = number
        self.avg_pts = avg_pts
        self.avg_assists = avg_assists
        self.avg_rebounds = avg_rebounds




