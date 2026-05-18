class MyClass:
    def __init__(self):
        self.a = 10
        self.printtext()        

    def printtext(self):
        print(f'the default value is {self.a}')
    
obj = MyClass()


class Parent:
    def __init__(self, firstname, lastname):
        self.firstname = firstname
        self.lastname = lastname
    
    def move(self):
        print('in parent')
    
class Child(Parent):
    def __init__(self, parent, profession):
        super().__init__(parent.firstname, parent.lastname)
        self.profession = profession
    
    def move(self):
        super().move()
        

    def printall(self):
        print(f"first name is {self.firstname}, lastname is {self.lastname} and my profession is {self.profession}")


parObj = Parent('Rajesh','Vemulakonda')
childObj = Child(parObj, 'Software Engineer')

childObj.printall()
parObj.move()
childObj.move()
