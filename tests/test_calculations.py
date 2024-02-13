import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFund


@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(60)

@pytest.mark.parametrize("num1, num2, result", [
    (3, 2, 5),
    (8, 3, 11),
    (10, 20, 30)
])

def test_add(num1, num2, result):
    print("testing add")
    assert add(num1, num2) == result

def test_subtract():
    assert subtract(8, 5) == 3

def test_multiply():
    assert multiply(5, 5) == 25

def test_divide():
    assert divide(25, 5) == 5

def test_bank_set_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 60

def test_bank_withdraw(bank_account):
    bank_account.withdraw(40)
    assert bank_account.balance == 20

def test_bank_deposit(bank_account):
    bank_account.deposit(40)
    assert bank_account.balance == 100

def test_bank_calculate_interest(bank_account):
    bank_account.calculate_interest()
    assert round(bank_account.balance, 4) == 66

@pytest.mark.parametrize("deposit, withdrew, balance", [
    (150, 100, 50),
    (450, 300, 150),
    (130, 120, 10)
])

def test_bank_transaction(zero_bank_account, deposit, withdrew, balance):
    zero_bank_account.deposit(deposit)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == balance

def test_bank_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFund):
        bank_account.withdraw(250)
        