# Создать класс TrafficLight (светофор):
#
#  определить у него один атрибут color (цвет) и метод running (запуск);
#  атрибут реализовать как приватный;

#  в рамках метода реализовать переключение светофора в режимы: красный, жёлтый,
# зелёный;

#  продолжительность первого состояния (красный) составляет 7 секунд, второго
# (жёлтый) — 2 секунды, третьего (зелёный) — на ваше усмотрение;

#  переключение между режимами должно осуществляться только в указанном порядке
# (красный, жёлтый, зелёный);

#  проверить работу примера, создав экземпляр и вызвав описанный метод.
# Задачу можно усложнить, реализовав проверку порядка режимов. При его нарушении
# выводить соответствующее сообщение и завершать скрипт.
import sys
import time
from colorama import Fore # цветная печать в консоли и перемещение курсора
import colorama

class TrafficLight:
    _mode = None   # режим работы
    _color = None  # текущий цвет
    _fps = 0       # частота обновления на экране

    def __init__(self,fps = 2):
        self._mode = 'Red'  # начинаем с красного
        self._color = 'Red'
        self._fps = fps     # 2 кадра в секунду, если что
        print('\n' * 50)

    def NextStep(self):   # логика переключения режимов
        match self._mode:
            case 'Red':
                self._mode = 'YellowRed'
                self._color = 'Yellow'
            case 'YellowRed':
                self._mode = 'Green'
                self._color = 'Green'
            case 'Green':
                self._mode = 'BlinkGreen'
                self._color = 'Green'
            case 'BlinkGreen':
                self._mode = 'YellowGreen'
                self._color = 'Yellow'
            case 'YellowGreen':
                self._mode = 'Red'
                self._color = 'Red'
            case _:
                print("Чтото пошло не так...")
                sys.exit(-1)

    def RedLight(self): # красный глаз светофора
        return True if self._mode in ['Red','YellowRed'] else False

    def YellowLight(self): # желтый глаз светофора
        return True if self._mode in ['YellowRed','YellowGreen'] else False

    def GreenLight(self): # зеленый глаз светофора
        return True if self._mode in ['Green','BlinkGreen'] else False

    def get_color(self): # геттер
        return self._color

    def print_TL(self,GreenLight = True): # вывод на экран светофора

        pos = lambda y, x: colorama.Cursor.POS(x, y)

        print('%s %s' % (pos(1,1), ' ')) # рисуем с этой позиции
        print('+-+')
        print(f'|{Fore.RED + ("*" if self.RedLight() else " ") + Fore.WHITE}|')
        print('+-+')
        print(f'|{Fore.YELLOW + ("*" if self.YellowLight() else " ") + Fore.WHITE}|')
        print('+-+')
        if (self._mode == 'Green') or (self._mode == 'BlinkGreen' and GreenLight == True):
            print('|'+Fore.GREEN+'*'+Fore.WHITE+'|')
        else:
            print('| |')
        print('+-+')

    def running(self): # запуск и главный цикл
        colorama.init()
        for _ in range(10): # 10 циклов пройдем. и хватит
            for i in [7, 2, 5, 2, 2]: # тайминги между переключениями режимов
                j = 0
                blink = False
                while j < i:
                    self.print_TL(blink)
                    time.sleep(1 / self._fps)
                    j += 1 / self._fps
                    blink = not blink
                self.NextStep()

TL = TrafficLight()
TL.running()

