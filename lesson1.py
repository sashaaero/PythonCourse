from my_module import a
from random import randint

class Student:
    def __init__(self, first_name, last_name, age, group, sex): # Конструктор класс
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.group = group
        self.sex = sex
        self.marks = []
        
    def __str__(self):
        # return 'Student <%s %s, age: %d, group: %s, sex: %s>' % (self.first_name, self.last_name, self.age, self.group, self.sex)
        return f'Student <{self.first_name} {self.last_name}, age: {self.age}, group: {self.group}, sex: {self.sex}>'
    
    __repr__ = __str__
    
    def add_mark(self, mark):       
        self.marks.append(mark)
    
    @property
    def avg_mark(self):
        return sum(self.marks) / len(self.marks)
    
        
class Mark:
    def __init__(self, course, value):
        self.course = course
        self.value = value

    def __repr__(self):
        return '%s: %d' % (self.course, self.value)
        

    
s = Student('Alexander', 'Tischenko', 23, '4541', 'male')
for _ in range(25):
    s.add_mark(randint(2, 5))
    
print(s.avg_mark)
