#---------------------------------------------DECORATORS---------------------------------------------
#Decorators ---> A decorator is a design pattern in Python that allows you to modify the behavior of a function or method without changing its code.
# It is a higher-order function that takes another function as an argument and extends its behavior.

def auth_required(func):
    def wrapper(self, amount):
        if self.is_logged_in:
            print("User authenticated")
            func(self, amount)
        else:
            print("Please login first")
    return wrapper


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        self.is_logged_in = False

    def login(self):
        self.is_logged_in = True
        print(f"{self.owner} logged in")

    @auth_required
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    @auth_required
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return
        self.balance -= amount
        print(f"Withdrew {amount}. New balance: {self.balance}")

# Example usage
account = BankAccount("Hello", 1000)
account.deposit(500)  
account.login()       
account.deposit(500)  
account.withdraw(200) 



# --------------------------------PROPERTY DECORATOR--------------------------------------
#it is a type of in built decorator 
#it uses method as an variable and we can call it as a variable instead of method. while controlling the access of data 
#it is mainly used for getter and setter and deleter method

def require_password(func):
    def wrapper(self, *args, **kwargs):
        entered = input("Enter password: ")
        if entered == self._password:
            print("Access granted")
            return func(self, *args, **kwargs)
        else:
            print("Wrong password")
    return wrapper
#why the above function is used as a decorator?
#1. it takes function as an input 
#2. it returns new funtion
#3.it adds extra behavior to the methods without modifying their code (it checks for password before executing the method).

class BankAccount:
    def __init__(self, account_number, name, bank):
        self.account_number = account_number
        self.name = name
        self.bank = bank
        self._password = "1234"
        self.balance = 0

    # Getter
    #Getter --> it is used to retrieve the value of an attribute. 
    #It allows you to access the value of a private attribute in a controlled way.
    @property
    def account_info(self):
        return f"{self.name} | {self.bank} | Balance: {self.balance}"

    # Setter (update name safely)
    #Setter --> it is used to set the value of an attribute. 
    #It allows you to update the value of a private attribute in a controlled way.
    @account_info.setter
    def account_info(self, new_name):
        entered = input("Enter password to update name: ")
        if entered == self._password:
            self.name = new_name
            print("Name updated successfully")
        else:
            print(" Wrong password")

    # Deleter (delete account data)
    #Deleter --> it is used to delete an attribute. 
    #It allows you to delete a private attribute in a controlled way.
    @account_info.deleter
    def account_info(self):
        entered = input("Enter password to delete account: ")
        if entered == self._password:
            print(" Deleting account data...")
            del self.name
            del self.bank
            del self.balance
        else:
            print(" Wrong password")

    @require_password
    def deposit(self, amount):
        self.balance += amount
        print(f"Deposited {amount}. New balance: {self.balance}")

    @require_password
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
        else:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")

    @require_password
    def change_password(self, new_password):
        self._password = new_password
        print("Password changed successfully")

# Example usage
account = BankAccount("123456789", "Hello", "Bank of Aditi")
print(account.account_info) 
account.deposit(500)  
account.change_password("987654321") 
account.withdraw(200)

