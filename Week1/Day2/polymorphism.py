#---------------------------POLYMORPHISM---------------------------

#One method ,Many Forms(Behaviours)
#same function/method name works differently based on the object that is calling it.
#same method --> different outputs

class Dog:
    def speak(self):
        return "Woof!"
class Cat:
    def speak(self):
        return "Meow!"
dog = Dog()
cat = Cat()
print(dog.speak())
print(cat.speak())



#-----------------------DUCK TYPING-----------------------
#Object type doesn't matters, only the method (behavior) matters.

class Bird:
    def fly(self):
        return "I can fly!"
class Airplane:
    def fly(self):
        return "I can fly too!"
def make_it_fly(thing):
    print(thing.fly())

bird = Bird()
airplane = Airplane() 
make_it_fly(bird)
make_it_fly(airplane)



#----------------------METHOD OVERLOADING----------------------
#Same method name but different parameters (number or type) in the same class.
class Calculator:
    def add(self,a,b):
        return a + b
    def add(self,a,b,c):
        return a + b + c 
calc = Calculator()
print(calc.add(2,3,4)) 
#print(calc.add(2,3))  # This will raise an error because the method with two parameters is overwritten by the method with three parameters.



#--------------------------METHOD OVERRIDING----------------------
#Runtime polymorphism
#Child class changes parent method's behavior.
#parent method replaced by child method.
class Parent:
    def greet(self):
        return "Hello from Parent!" 
class Child(Parent):
    def greet(self):
        return "Hello from Child!"
parent = Parent()
child = Child()
print(parent.greet()) # This will call the greet method of the Parent class, so it will return "Hello from Parent!"
print(child.greet()) # The child class's greet method overrides the parent class's greet method, so when we call child.greet(), it returns "Hello from Child!" instead of "Hello from Parent!"



