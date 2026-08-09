# Class Definition Examples

class SimpleClass:
    """Basic class with class and instance attributes"""
    class_attr = "I'm shared"
    
    def __init__(self, value):
        self.instance_attr = value
    
    def show(self):
        return f"Class: {self.class_attr}, Instance: {self.instance_attr}"


class BankAccount:
    """Real-world class with validation"""
    bank_name = "Python National Bank"
    interest_rate = 0.03
    total_accounts = 0
    
    def __init__(self, owner, initial_balance=0):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        
        self.owner = owner
        self.balance = initial_balance
        self.account_number = BankAccount.total_accounts + 1000
        BankAccount.total_accounts += 1
        self._transactions = []
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self.balance += amount
        self._transactions.append(f"Deposited: ${amount}")
        return self.balance
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._transactions.append(f"Withdrew: ${amount}")
        return self.balance
    
    def get_statement(self):
        return f"Account: {self.account_number}\nOwner: {self.owner}\nBalance: ${self.balance:.2f}"


class DataContainer:
    """Class with different method types"""
    
    def __init__(self, data):
        self.data = data
    
    def instance_method(self):
        return f"Instance data: {self.data}"
    
    @classmethod
    def from_string(cls, s):
        return cls(s.split(","))
    
    @classmethod
    def empty(cls):
        return cls([])
    
    @staticmethod
    def validate(data):
        return isinstance(data, list)
    
    def __repr__(self):
        return f"DataContainer({self.data})"


# Demonstration
if __name__ == "__main__":
    print("=== Simple Class ===")
    obj1 = SimpleClass("first")
    obj2 = SimpleClass("second")
    print(obj1.show())
    print(obj2.show())
    print(f"Class attr shared: {obj1.class_attr is obj2.class_attr}")
    print()
    
    print("=== Bank Account ===")
    try:
        acc1 = BankAccount("Alice", 1000)
        acc2 = BankAccount("Bob", 500)
        
        print(acc1.get_statement())
        print()
        
        acc1.deposit(200)
        acc1.withdraw(150)
        print(f"Alice balance: ${acc1.balance}")
        
        print(f"Total accounts: {BankAccount.total_accounts}")
        print(f"Bank: {BankAccount.bank_name}")
    except ValueError as e:
        print(f"Error: {e}")
    print()
    
    print("=== Data Container ===")
    dc1 = DataContainer([1, 2, 3])
    dc2 = DataContainer.from_string("a,b,c")
    dc3 = DataContainer.empty()
    
    print(dc1.instance_method())
    print(dc2.instance_method())
    print(dc3.instance_method())
    print(f"Validate [1,2]: {DataContainer.validate([1,2])}")
    print(f"Validate 'str': {DataContainer.validate('string')}")