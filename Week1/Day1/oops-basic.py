# -----------------------CLASS,OBJECT,VARIABLE,METHOD,ATTRIBUTES-----------------------

class Car:  #Class --> it is a blueprint or template for creating objects. It defines the properties and behaviors that the objects created from the class will have.
    def __init__(self,model,year,color):  #Constructor --> it is a special method that is automatically called when an object of the class is created. It is used to initialize the attributes of the object.
        self.model = model
        self.year = year
        self.color = color
    def info(self): #Method --> it is a function that is defined inside a class and is used to perform some action on the objects of the class.
        print(f"Model: {self.model}, Year: {self.year}, Color: {self.color}")

car1 = Car("Toyota",2015,"Black")  #Object --> it is an instance of a class.
car2 = Car("Honda",2018,"White")
car1.info()
car2.info()

car1.model = "Tesla"

car1.info()




class Bank:
    def __init__(self,account_number,account_holder,balance):
       self.account_number = account_number
       self.account_holder = account_holder 
       self.balance = balance

    def check_balance(self):
        return self.balance
    def deposit(self,amount):
        self.balance += amount
        return self.balance
    def withdrawn(self,amount):
        if amount > self.balance:
            print("Check Balance!!")
        else:
            self.balance -= amount
        return self.balance
    
canara = Bank(1234567890,"prudhvi",10000)

print(canara.account_holder)
print(canara.account_number)
print(canara.balance)

canara.deposit(5000)
print(canara.balance)
canara.withdrawn(5000)
print(canara.balance)
