# Реализовать класс Road (дорога).
#  определить атрибуты: length (длина), width (ширина);
#  значения атрибутов должны передаваться при создании экземпляра класса;

#  атрибуты сделать защищёнными;

#  определить метод расчёта массы асфальта, необходимого для покрытия всей дороги;
#  использовать формулу: длина*ширина*масса асфальта для покрытия одного кв. метра
# дороги асфальтом, толщиной в 1 см*число см толщины полотна;

#   проверить работу метода.
# Например: 20 м*5000 м*25 кг*5 см = 12500 т.

class Road:
    _length = None
    _width = None

    def __init__(self,length,width):
        self._width = width
        self._length = length

    def get_length(self):
        return self._length
    def get_width(self):
        return self._width


    def calc_mass(self,mass_sqmeter,thinkness):
        return self._length*self._width*mass_sqmeter*thinkness / 1000

my_road = Road(5000,20)
mass_sq_meter = 25
thinkness = 5
print(f'Масса асфальтового покрытия при ширине дороги {my_road.get_width()} м, длине дороги {my_road.get_length()} м,\n'
      f' массе асфальта {mass_sq_meter} кг/м^2 и толщине покрытия {thinkness} см будет'
      f' {my_road.calc_mass(mass_sq_meter,thinkness)} т'
      )