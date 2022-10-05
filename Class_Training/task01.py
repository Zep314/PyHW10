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

class TrafficLight:
    _mode = None
    _color = None
    def __init__(self):
        self._mode = 'Red'
        self._color = 'Red'

    def NextStep(self):
        if self._mode == 'Red':
            self._mode = 'YellowRed'
            self._color = 'Yellow'
        elif self._mode == 'YellowRed':
            self._mode = 'Green'
            self._color = 'Green'
        elif self._mode == 'Green':
            self._mode = 'BlinkGreen'
            self._color = 'Green'
        elif self._mode == 'BlinkGreen':
            self._mode = 'YellowGreen'
            self._color = 'Yellow'
        elif self._mode == 'YellowGreen':
            self._mode = 'Red'
            self._color = 'Red'
        else:
            print("Чтото пошло не так...")
            sys.exit(-1)

    def RedLight(self):
        return True if self._mode in ['Red','YellowRed'] else False

    def YellowLight(self):
        return True if self._mode in ['YellowRed','YellowGreen'] else False

    def GreenLight(self):
        return True if self._mode in ['Green','BlinkGreen'] else False

    def get_color(self):
        return self._color

    def running(self):
        while True:
            for i in [7, 2, 5, 2, 2]:
                print(self._mode)
                time.sleep(i)
                self.NextStep()

TL = TrafficLight()
TL.running()