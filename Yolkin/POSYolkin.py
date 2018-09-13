class Ex_buro: 
    def __init__(self, name, ad):
        self.name = name
        self.ad = ad
        self.ships = []
        self.guides = []
        self.excursions = []

    def __str__(self): # privet
        return f'Бюро параходных экскурсий "{self.name}", наш адрес: "{self.ad}"'

    def add_ship(self, ship):
        self.ships.append(ship)

    def add_guide(self,guide):
        self.guides.append(guide)

    def add_ex(self,ex):
        self.excursions.append(ex)

class Ship:
    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f'Корабль №{self.number} "{self.name}"'

class Route:
    def __init__(self, num,stop1,stop2,stop3):
        self.num = num
        self.stop1 = stop1
        self.stop2 = stop2
        self.stop3 = stop3

    def __str__(self):
        return f'Маршрут №{self.num}, Остановки: {self.stop1,self.stop2,self.stop3}'

class Excursion:
    def __init__(self, num_ex, start_time, end_time, guide, numbers):
        self.num_ex = num_ex
        self.start_time = start_time
        self.end_time = end_time
        self.guide = guide
        self.numbers = numbers

    def __str__(self):
        return f'Номер экскурсии{self.num_ex}, Начало:{self.start_time} , Конец: {self.end_time} Гид: {self.guide}, Кол-во пассажиров {self.numbers}'

buro = Ex_buro("Прогулкин","Невкий проспект, д.34")
