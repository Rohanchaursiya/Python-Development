# Attributes: Instance vs Class

class Account:
    """Demonstrates instance vs class attributes"""
    
    # Class attributes (shared)
    bank_name = "Global Bank"
    interest_rate = 0.05
    total_accounts = 0
    _all_accounts = []  # Private class attribute
    
    def __init__(self, owner, balance=0):
        # Instance attributes (unique)
        self.owner = owner
        self.balance = balance
        self.account_number = Account.total_accounts + 1000
        self._transactions = []
        
        Account.total_accounts += 1
        Account._all_accounts.append(self)
    
    def deposit(self, amount):
        self.balance += amount
        self._transactions.append(("deposit", amount))
    
    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._transactions.append(("withdraw", amount))
    
    @classmethod
    def get_total_accounts(cls):
        return cls.total_accounts
    
    @classmethod
    def get_all_accounts(cls):
        return cls._all_accounts
    
    def __repr__(self):
        return f"Account({self.account_number}, {self.owner}, ${self.balance})"


class Configuration:
    """Shows mutable class attribute trap"""
    
    # DANGEROUS: mutable class attribute
    settings = {}
    tags = []
    
    def __init__(self, name):
        self.name = name
    
    def add_setting(self, key, value):
        self.settings[key] = value
    
    def add_tag(self, tag):
        self.tags.append(tag)


class SafeConfiguration:
    """Safe version with instance attributes"""
    
    # Class attributes - only immutable
    default_timeout = 30
    max_retries = 3
    
    def __init__(self, name):
        self.name = name
        # Mutable attributes in __init__
        self.settings = {}
        self.tags = []
    
    def add_setting(self, key, value):
        self.settings[key] = value
    
    def add_tag(self, tag):
        self.tags.append(tag)


class Counter:
    """Class attribute for counting instances"""
    
    count = 0
    instances = []
    
    def __init__(self, name):
        self.name = name
        Counter.count += 1
        Counter.instances.append(self)
    
    def __del__(self):
        Counter.count -= 1
        if self in Counter.instances:
            Counter.instances.remove(self)
    
    @classmethod
    def get_count(cls):
        return cls.count


# Demonstration
if __name__ == "__main__":
    print("=== Instance vs Class Attributes ===")
    
    acc1 = Account("Alice", 1000)
    acc2 = Account("Bob", 500)
    acc3 = Account("Charlie", 2000)
    
    print(f"acc1.owner: {acc1.owner}")           # Instance
    print(f"acc1.balance: {acc1.balance}")       # Instance
    print(f"acc1.bank_name: {acc1.bank_name}")   # Class (via instance)
    print(f"Account.bank_name: {Account.bank_name}")  # Class (via class)
    print(f"Total accounts: {Account.total_accounts}")
    print()
    
    print("=== Modifying Class Attribute ===")
    print(f"Before: acc1.interest_rate = {acc1.interest_rate}")
    Account.interest_rate = 0.06
    print(f"After Account.interest_rate = 0.06:")
    print(f"  acc1.interest_rate = {acc1.interest_rate}")
    print(f"  acc2.interest_rate = {acc2.interest_rate}")
    print(f"  Account.interest_rate = {Account.interest_rate}")
    print()
    
    print("=== Shadowing Class Attribute ===")
    print(f"Before shadowing: acc1.bank_name = {acc1.bank_name}")
    acc1.bank_name = "My Personal Bank"  # Creates instance attribute!
    print(f"After acc1.bank_name = 'My Personal Bank':")
    print(f"  acc1.bank_name = {acc1.bank_name}")  # Instance
    print(f"  acc2.bank_name = {acc2.bank_name}")  # Still class
    print(f"  Account.bank_name = {Account.bank_name}")  # Class unchanged
    print()
    
    print("=== Mutable Class Attribute Trap ===")
    cfg1 = Configuration("config1")
    cfg2 = Configuration("config2")
    
    cfg1.add_setting("theme", "dark")
    cfg1.add_tag("production")
    
    print(f"cfg1.settings: {cfg1.settings}")
    print(f"cfg2.settings: {cfg2.settings}")  # SHARED!
    print(f"cfg1.tags: {cfg1.tags}")
    print(f"cfg2.tags: {cfg2.tags}")  # SHARED!
    print()
    
    print("=== Safe Configuration ===")
    safe1 = SafeConfiguration("safe1")
    safe2 = SafeConfiguration("safe2")
    
    safe1.add_setting("theme", "dark")
    safe1.add_tag("production")
    
    print(f"safe1.settings: {safe1.settings}")
    print(f"safe2.settings: {safe2.settings}")  # Independent!
    print(f"safe1.tags: {safe1.tags}")
    print(f"safe2.tags: {safe2.tags}")  # Independent!
    print()
    
    print("=== Counter Pattern ===")
    c1 = Counter("first")
    c2 = Counter("second")
    c3 = Counter("third")
    
    print(f"Counter.count: {Counter.count}")
    print(f"Instances: {[c.name for c in Counter.instances]}")
    
    del c2
    import gc
    gc.collect()
    
    print(f"After deleting c2:")
    print(f"Counter.count: {Counter.count}")
    print(f"Instances: {[c.name for c in Counter.instances]}")