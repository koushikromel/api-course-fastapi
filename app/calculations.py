def add(num1: int, num2: int):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2

def divide(num1: int, num2: int):
    return num1 / num2


class InsufficientFund(Exception):
    pass

class BankAccount():
    def __init__(self, initial_balance=0):
        self.balance = initial_balance
    
    def deposit(self, amount):
        self.balance += amount
    
    def withdraw(self, amount):
        if amount > self.balance:
            # raise Exception("Insufficient funds")
            raise InsufficientFund("Insufficient funds")
            # raise ZeroDivisionError()

        self.balance -= amount
    
    def calculate_interest(self):
        self.balance *= 1.1
