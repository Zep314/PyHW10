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

class TrafficLight:
    mode = None
    def __init__(self):
        self.mode = 'Red'

    def NextStep(self):
        if self.mode == 'Red': self.mode = 'YellowRed'
        elif self.mode == 'YellowRed': self.mode = 'Green'
        elif self.mode == 'Green': self.mode = 'BlinkGreen'
        elif self.mode == 'BlinkGreen': self.mode = 'YellowGreen'
        elif self.mode == 'YellowGreen': self.mode = 'Red'
        else:
            print("Чтото пошло не так...")
            sys.exit(-1)

    def RedLight(self):
        return True if self.mode in ['Red','YellowRed'] else False

    def YellowLight(self):
        return True if self.mode in ['YellowRed','YellowGreen'] else False

    def GreenLight(self):
        return True if self.mode in ['Green','BlinkGreen'] else False

    def running(self):
        pass