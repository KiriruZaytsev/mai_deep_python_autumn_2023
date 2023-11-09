'''В данном модуле осуществлена
реализация LRU cache с помощью
двусвязного списка и хэш-таблицы'''

class Node():
    '''Класс для ноды двусвязного списка'''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.prev = None

class LinkedList():
    '''Класс, в котором реализован двусвязный список'''
    def __init__(self):
        '''Инициализация пустого списка'''
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.size = 0
        self.head.next = self.tail
        self.tail.prev = self.head

    def append(self, key, value):
        '''Вставка в конец списка'''
        node = Node(key, value)
        prev_last = self.tail.prev
        node.next = self.tail
        node.prev = prev_last
        prev_last.next = node
        self.tail.prev = node
        self.size += 1
        return node

    def pop_front(self):
        '''Удаление из начала списка'''
        return self.remove(self.head.next)

    def remove(self, node):
        '''Удаление элемента списка'''
        prev_node = node.prev
        next_node = node.next

        prev_node.next = next_node
        next_node.prev = prev_node

        self.size -= 1

        return node

class LRUCache():
    '''Класс с реализацией LRU cache'''
    def __init__(self, limit = 42):
        '''Инициализация кэша'''
        self.limit = limit
        self.list = LinkedList()
        self.map = {}

    def set(self, key, value):
        '''Функция, вносящая новые данные
        в кэш'''
        if key in self.map:
            self.list.remove(self.map[key])

        node = self.list.append(key, value)
        self.map[key] = node

        if self.list.size > self.limit:
            deleted = self.list.pop_front()
            del self.map[deleted.key]

    def get(self, key):
        '''Функция, которая возвращает по ключу
        данные, хранящиеся в кэше'''
        if key in self.map:
            node = self.map[key]
            self.list.remove(node)
            self.map[key] = self.list.append(key, node.value)
            return node.value
        return None
        