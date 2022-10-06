from random import randint

class Game(object):
    _field = None

    def __init__(self):
        self._field = '123456789'

    def PrintField(self):  # функция печати состояния игрового поля
        print('-' * 13)
        for i in range(3):  # печатаем целыми строками
            print(f'| {self._field[i * 3]} | {self._field[i * 3 + 1]} | {self._field[i * 3 + 2]} |')
            print('-' * 13)

    def MyInput(self): # функция ввода нового элемента (с проверками)
        num = int(input('Введите позицию, куда хотите сходить 1..9: ')) # проверку на нецифру делать не стал
        while True:
            if not ((0 < num) and (num < 10)):
                print('Ввели неправильное место на поле')
            elif not(self._field[num-1] in '123456789'): # если поле занято, то вместо цифры там X или O
                print('Это поле уже занято')
            else: return str(num)
            num = int(input('Введите позицию, куда хотите сходить 1..9: '))

    def MyCheckGame(self): # функция проверки окончания игры
        win_patterns = ((0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)) # если в этих позициях
                                                                                     # стоят XXX или OOO,
                                                                                     # то кто-то выйграл
        if len(self._field.replace('X','').replace('O','')) == 0: return 'Победила дружба! Ничья!'
        if 'XXX' in list(filter(lambda x: x,[self._field[win_patterns[i][0]]+\
                                             self._field[win_patterns[i][1]]+\
                                             self._field[win_patterns[i][2]] \
                                        for i in range(len(win_patterns))])):
            return 'XXX Победили крестики XXX'
        if 'OOO' in list(filter(lambda x: x,[self._field[win_patterns[i][0]]+\
                                             self._field[win_patterns[i][1]]+\
                                             self._field[win_patterns[i][2]] \
                                        for i in range(len(win_patterns))])):
            return 'OOO Победили нулики OOO'
        return 'None'

    # щаг бота - в зависимости от алгоритма
    def get_bot_turn(self, my_char, algorithm):
        if algorithm == 2:
            return self.my_random()          # случайный
        elif algorithm == 3:
            return self.mega_brain(my_char)  # самый умный
        else:
            return self.first_free()         # самый тупой

    def first_free(self):  # самый тупой - выбирает первое непустое поле
        return self._field.replace('X', '').replace('O', '')[0]

    def my_random(self):  # случайно выбраем незанятое поле
        self._field = self._field.replace('X', '').replace('O', '')
        return self._field[randint(0, len(self._field) - 1)]

    def win_triple(self,triple: str, my_char):  # triple - строка из 3-х символов (цифры и Х и О)
        s = triple.replace(my_char, '')  # чистим X или O - что на вход дали
        if len(s) == 1 and s.isdigit():
            return s  # если одно место с числом осталось - то это то, что нам нужно
        return ''

    # поверка, можем ли мы победить одним ходом, когда играем за my_char
    def i_can_win(self, my_char):
        win_patterns = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7),
                        (2, 5, 8), (0, 4, 8), (2, 4, 6))  # если в этих позициях
        # стоят XXX или OOO,
        # то кто-то выйграл
        triples = [self._field[win_patterns[i][0]] +
                   self._field[win_patterns[i][1]] +
                   self._field[win_patterns[i][2]]
                   for i in range(len(win_patterns))]  # список заполненных верт, гориз и диагоналей
        k = ''
        for i in range(len(triples)):  # проверка тройки символов на то, что одного из не нехватает
            # для полного заполнения
            k = self.win_triple(triples[i], my_char)
            if k:
                break
        return k

    def mega_brain(self, my_char):
        # проверяем, можем ли победить одним ходом
        ret = self.i_can_win(my_char)
        if ret:
            return ret  # можем!

        alien_char = ('O' if my_char == 'X' else 'X')

        # проверяем, может ли враг победить одним ходом
        ret = self.i_can_win(alien_char)
        if ret:
            return ret  # может! - ходим туда - ему назло!

        best_move = ['5', '1', '3', '7', '9', '2',
                     '4', '6', '8']  # лучшие ходы на поле

        # выбираем из лучших ходов, которые не заняты
        return [i for i in best_move if i in self._field.replace('X', '').replace('O', '')][0]

    def run(self,x_turn, bot_play_X, bot_algorithm):
        game_result = 'None'
        while game_result == 'None':
            self.PrintField()
            if x_turn:
                print('Ходят X')
                if bot_play_X:
                    self._field = self._field.replace(self.get_bot_turn('X', bot_algorithm), 'X')  # бот сходил за X
                else:
                    self._field = self._field.replace(self.MyInput(), 'X')  # чел сходил за X
            else:
                print('Ходят O')
                if not bot_play_X:
                    self._field = self._field.replace(self.get_bot_turn('O', bot_algorithm), 'O')  # бот сходил за O
                else:
                    self._field = self._field.replace(self.MyInput(), 'O')  # чел сходил за O    game_result = MyCheckGame(field)
            game_result = self.MyCheckGame()  # проверяем, чего там с результатом игры
            x_turn = not x_turn
        self.PrintField()
        return game_result