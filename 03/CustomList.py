class CustomList(list):
    def __eq__(self, other):
        return sum(self) == sum(other)
    
    def __ge__(self, other):
        return sum(self) >= sum(other)
    
    def __le__(self, other):
        return sum(self) <= sum(other)
    
    def __gt__(self, other):
        return sum(self) > sum(other)
    
    def __lt__(self, other):
        return sum(self) < sum(other)
    
    def __str__(self):
        return f"{super().__str__()}, Sum = {sum(self)}"
    
    def __add__(self, other):
        added_length = abs(len(other) - len(self))
        return CustomList(map(sum, zip([*self, *[0] * added_length], [*other, *[0] * added_length])))
    
    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        added_length = abs(len(other) - len(self))
        return CustomList(map(lambda pair: pair[0] - pair[1], zip([*self, *[0] * added_length], [*other, *[0] * added_length])))
    
    def __rsub__(self, other):
        return self.__sub__(other)

