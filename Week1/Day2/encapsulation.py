#---------------------------ENCAPSULATION------------------------
#Wrapping data + methods together
#Restricting direct access to variables

class Bank:
    def __init__(self, account_number, account_holder, balance):
        self.account_number = account_number
        self.account_holder = account_holder 
        self.__balance = balance   # 🔐 private

    def check_balance(self):
        return self.__balance

    def deposit(self, amount):
        self.__balance += amount
        return self.__balance

    def withdrawn(self, amount):
        if amount > self.__balance:
            print("Check Balance!!")
        else:
            self.__balance -= amount
        return self.__balance

    def get_balance(self):
        return self.__balance


canara = Bank(1234567890, "prudhvi", 10000)

print(canara.account_holder)
print(canara.account_number)

print(canara.get_balance())   

canara.deposit(5000)
print(canara.get_balance())

canara.withdrawn(5000)
print(canara.get_balance())