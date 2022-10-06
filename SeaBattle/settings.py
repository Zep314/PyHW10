# части карты
class FieldPart(object):
    main = 'map'
    radar = 'radar'
    weight = 'weight'


# просто задаем цвета.
class Color:
    yellow2 = '\033[1;35m'
    reset = '\033[0m'
    blue = '\033[0;34m'
    yellow = '\033[1;93m'
    red = '\033[1;93m'
    miss = '\033[0;37m'


# Функция, которая окрашивает текст в нужный цвет.
def set_color(text, color):
    return color + text + Color.reset
