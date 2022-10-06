# класс "клетка". Здесь мы задаем и визуальное отображение клеток и их цвет.
# по визуальному отображению мы проверяем какого типа клетка. Уж такая реализация.
# По этой причине нельзя обозначать одним символом два разных типа. Иначе в логике возникнет путаница.
from settings import set_color, Color


class Cell(object):
    empty_cell = set_color(' ', Color.yellow2)
    ship_cell = set_color('■', Color.blue)
    destroyed_ship = set_color('X', Color.yellow)
    damaged_ship = set_color('□', Color.red)
    miss_cell = set_color('•', Color.miss)
