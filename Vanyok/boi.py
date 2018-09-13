class carService:

    def __init__(self, name, address):
        self.serviceName = name
        self.address = address
        self.manager = None
        self.orders = []
        self.workers = []

    def __str__(self):
        return f'Car service <{self.serviceName}, address: {self.address}> manager: {self.manager}>'

    def addWorker(self, worker):
        self.workers.append(worker)

    def addOrder(self, order):
        self.orders.append(order)


class Worker:

    def __init__(self, surname, name, spec, post, salary):
        self.surname = surname
        self.name = name
        self.specialization = spec
        self.post = post
        self.salary = salary
        self.currentOrders = []

    def __str__(self):
        return f'Worker <{self.surname} {self.name} specialization: {self.specialization}>'


class Order:

    def __init__(self, customer, date1, date2, typeOfWork, descrrr, car):
        self.state = "Принят"
        self.customer = customer
        self.receivingDate = date1
        self.completionDate = date2
        self.typeOfWork = typeOfWork
        self.description = descrrr
        self.worker = None
        self.car = car




class Customer:

    def __init__(self, surname, name, num):
        self.surname = surname
        self.name = name
        self.phoneNumber = num
        self.oldOrders = []
        self.cars = []

    def __str__(self):
        return f'Customer <{self.surname} {self.name}, phone number: {self.phoneNumber}>'


class Car:

    def __init__(self, manufacturer, model, mileage, cType, color, num, owner):
        self.manufacturer = manufacturer
        self.model = model
        self.mileage = mileage
        self.chassisType = cType
        self.color = color
        self.licencePlateNumber = num
        self.owner = owner

    def __str__(self):
        return f'Car <{self.manufacturer} {self.model}, licence plate number: {self.licencePlateNumber}, ' \
               f'owner: {self.owner}>'


serv = carService("У Михалыча", "Москва, ул.Пушкина, д. Колотушкина")
manager = Worker("Иванов", "Иван","Менеджмент", "Управляющий", 50000)
serv.manager = manager

mechanic = Worker("Петров", "Пётр", "Ремонт узлов двигателя", "Моторист", 30000)
washer = Worker("Собакин", "Димон", "Мойка и чистка автомобилей", "Мойщик", 20000)
serv.addWorker(mechanic)
serv.addWorker(washer)


customer = Customer("Кириллов", "Кирилл", "7911185465")
car = Car("VAZ", "2107", "142531", "Седан", "Белый","а251кн78", customer)
order1 = Order(customer,"21.05.2018", "28.05.2018", "Ремонт двигателя", "Заменить ГБЦ", car)
order1.worker = mechanic
serv.addOrder(order1)

customer2 = Customer("Павлов", "Павел", "7964654515")
car2 = Car("Hyuindai", "Solaris", "20354", "Седан", "Зеленый","к789тн61", customer2)
order2 = Order(customer2,"10.06.2018","10.06.2018","Мойка и чистка", "Вымыть машину, пропылесосить салон.", car2)
order2.worker = washer
serv.addOrder(order2)
