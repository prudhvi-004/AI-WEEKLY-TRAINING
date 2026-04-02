# -----------------------INHERITANCE-----------------------
#Inheritance is a fundamental object-oriented programming concept that allows a new class (called a child or subclass) to inherit properties and behaviors (attributes and methods) from an existing class (called a parent or superclass).
class Animal:
    def __init__(self,name):
        self.name = name
    def speak(self):
        pass
class Dog(Animal):
    def speak(self):
        return "Woof!"
class Cat(Animal):
    def speak(self):
        return "Meow!"

dog = Dog("Buddy")
cat = Cat("Balu")
print(dog.name)
print(dog.speak())
print(cat.name)     
print(cat.speak())

#-----------------------Constructor in INHERITANCE-----------------------
# In inheritance, the constructor of the parent class can be called from the child class using the super() function. This allows the child class to initialize the attributes of the parent class before adding its own attributes.
class Vehicle:
    def __init__(self,make,model):
        self.make = make
        self.model = model
class Car(Vehicle):
    def __init__(self,make,model,year):
        super().__init__(make,model)
        self.year = year
car = Car("Toyota","Camry",2020)
print(car.make)
print(car.model)
print(car.year)


#--------------------------------------------SINGLE INHERITANCE ----------------------------------------
#one parent --> one child 
class Father:
    pass
class Son(Father):
    pass

#--------------------------------------------MULTILEVEL INHERITANCE -----------------------------------------
#Chain Inheritance
class GrandFather:
    pass
class Father(GrandFather):
    pass
class Son(Father):
    pass

#----------------------------------------MULTIPLE INHERITANCE -------------------------------------------
#child inherits from multiple parents
class GrandFather:
    pass
class Father:
    pass
class Son(GrandFather,Father):
    pass

#-------------------------------HIERARCHICAL INHERITANCE ------------------------------------
#one parent ---> multiple chidren
class Father:
    pass
class Son(Father):
    pass
class Daughter(Father):
    pass


