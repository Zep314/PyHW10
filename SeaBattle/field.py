# Поле игры. Состоит из трех частей: карта - где расставлены корабли игрока.
# Радар на котором игрок отмечает свои ходы и результаты
# Поле с весом клеток. Используется для ходов ИИ


from settings import FieldPart
from cell import Cell
from ship import Ship


# игровое поле
class Field(object):

    def __init__(self, size):
        self.size = size
        self.map = [[Cell.empty_cell for _ in range(size)] for _ in range(size)]   # наше поле
        self.radar = [[Cell.empty_cell for _ in range(size)] for _ in range(size)] # поле соперника
        self.weight = [[1 for _ in range(size)] for _ in range(size)]

    def get_field_part(self, element):
        if element == FieldPart.main:
            return self.map
        if element == FieldPart.radar:
            return self.radar
        if element == FieldPart.weight:
            return self.weight

    # Рисуем поле. Здесь отрисовка делится на две части. т.к. отрисовка весов клеток идёт по другому
    def draw_field(self, element):

        field = self.get_field_part(element)
        weights = self.get_max_weight_cells()

        if element == FieldPart.weight:  # нужно было для отладки
            for x in range(self.size):
                for y in range(self.size):
                    if (x, y) in weights:
                        print('\033[1;32m', end='')
                    if field[x][y] < self.size:
                        print(" ", end='')
                    if field[x][y] == 0:
                        print(str("" + ". " + ""), end='')
                    else:
                        print(str("" + str(field[x][y]) + " "), end='')
                    print('\033[0;0m', end='')
                print()

        else:
            # Всё что было выше - рисование веса для отладки, его можно не использовать в конечной игре.
            # Само поле рисуется всего лишь вот так:
            for x in range(-1, self.size):
                for y in range(-1, self.size):
                    if x == -1 and y == -1:
                        print("  ", end="")
                        continue
                    if x == -1 and y >= 0:
                        print(y + 1, end=" ")
                        continue
                    if x >= 0 and y == -1:
                        print(chr(65+x), end='')
                        continue
                    print(" " + str(field[x][y]), end='')
                print("")
        print("")

    # Функция проверяет, помещается ли корабль на конкретную позицию конкретного поля.
    # Будем использовать при расстановке кораблей, а так же при вычислении веса клеток
    # возвращает False если не помещается и True если корабль помещается
    def check_ship_fits(self, ship, element):

        field = self.get_field_part(element)

        if ship.x + ship.height - 1 >= self.size or ship.x < 0 or \
                ship.y + ship.width - 1 >= self.size or ship.y < 0:
            return False

        x = ship.x
        y = ship.y
        width = ship.width
        height = ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                if str(field[p_x][p_y]) == Cell.miss_cell:
                    return False

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                if str(field[p_x][p_y]) in (Cell.ship_cell, Cell.destroyed_ship):
                    return False

        return True

    # Когда корабль уничтожен необходимо пометить все клетки вокруг него сыграными (Cell.miss_cell)
    # а все клетки корабля - уничтоженными (Cell.destroyed_ship). Так и делаем в два подхода.
    def mark_destroyed_ship(self, ship, element):

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x - 1, x + height + 1):
            for p_y in range(y - 1, y + width + 1):
                if p_x < 0 or p_x >= len(field) or p_y < 0 or p_y >= len(field):
                    continue
                field[p_x][p_y] = Cell.miss_cell

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                field[p_x][p_y] = Cell.destroyed_ship

    # добавление корабля: пробегаемся от позиции х у корабля по его высоте и ширине и помечаем на поле эти клетки
    # параметр element - сюда мы передаем к какой части поля мы обращаемся: основная, радар или вес
    def add_ship_to_field(self, ship, element):

        field = self.get_field_part(element)

        x, y = ship.x, ship.y
        width, height = ship.width, ship.height

        for p_x in range(x, x + height):
            for p_y in range(y, y + width):
                # в клетку мы записываем ссылку на корабль.
                # т.е. обращаясь к клетке мы всегда можем получить текущее HP корабля
                field[p_x][p_y] = ship

    # функция возвращает список координат с самым большим коэффициентом шанса попадания
    def get_max_weight_cells(self):
        weights = {}
        max_weight = 0
        # Просто пробегаем по всем клеткам и заносим их в словарь с ключом который является значением в клетке
        # заодно запоминаем максимальное значение. Далее просто берём из словаря список координат с этим
        # максимальным значением weights[max_weight]
        for x in range(self.size):
            for y in range(self.size):
                if self.weight[x][y] > max_weight:
                    max_weight = self.weight[x][y]
                weights.setdefault(self.weight[x][y], []).append((x, y))

        return weights[max_weight]

    # пересчет веса клеток
    def recalculate_weight_map(self, available_ships):
        # Для начала мы выставляем всем клеткам 1.
        # нам необязательно знать какой вес был у клетки в предыдущий раз:
        # эффект веса не накапливается от хода к ходу.
        self.weight = [[1 for _ in range(self.size)] for _ in range(self.size)]

        # Пробегаем по всем полю.
        # Если находим раненый корабль - ставим клеткам выше ниже и по бокам
        # коэффициенты умноженные на 50 т.к. логично что корабль имеет продолжение в одну из сторон.
        # По диагоналям от раненой клетки ничего не может быть - туда вписываем нули
        for x in range(self.size):
            for y in range(self.size):
                if self.radar[x][y] == Cell.damaged_ship:

                    self.weight[x][y] = 0

                    if x - 1 >= 0:
                        if y - 1 >= 0:
                            self.weight[x - 1][y - 1] = 0
                        self.weight[x - 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x - 1][y + 1] = 0

                    if y - 1 >= 0:
                        self.weight[x][y - 1] *= 50
                    if y + 1 < self.size:
                        self.weight[x][y + 1] *= 50

                    if x + 1 < self.size:
                        if y - 1 >= 0:
                            self.weight[x + 1][y - 1] = 0
                        self.weight[x + 1][y] *= 50
                        if y + 1 < self.size:
                            self.weight[x + 1][y + 1] = 0

        # Перебираем все корабли оставшиеся у противника.
        # Это открыто, исходя из правил игры.  Проходим по каждой клетке поля.
        # Если там уничтоженный корабль, поврежденный или клетка с промахом -
        # ставим туда коэффициент 0. Больше делать нечего - переходим следующей клетке.
        # Иначе прикидываем может ли этот корабль с этой клетки начинаться в какую-либо сторону
        # и если он помещается прибавляем клетке 1.

        for ship_size in available_ships:

            ship = Ship(ship_size, 1, 1, 0)
            # вот тут бегаем по всем клеткам поля
            for x in range(self.size):
                for y in range(self.size):
                    if self.radar[x][y] in (Cell.destroyed_ship, Cell.damaged_ship, Cell.miss_cell) \
                            or self.weight[x][y] == 0:
                        self.weight[x][y] = 0
                        continue
                    # вот здесь поворачиваем корабль и проверяем помещается ли он
                    for rotation in range(0, 4):
                        ship.set_position(x, y, rotation)
                        if self.check_ship_fits(ship, FieldPart.radar):
                            self.weight[x][y] += 1
