# Properties and Descriptors Examples

class Person:
    """Property examples: getter, setter, deleter"""
    
    def __init__(self, name, age, email):
        self._name = name
        self._age = age
        self._email = email
        self._cache = {}
    
    # Basic property with validation
    @property
    def name(self):
        return self._name.title()
    
    @name.setter
    def name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @name.deleter
    def name(self):
        print("Deleting name...")
        self._name = ""
    
    # Read-only property (no setter)
    @property
    def age(self):
        return self._age
    
    @property
    def is_adult(self):
        return self._age >= 18
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value:
            raise ValueError("Invalid email format")
        self._email = value.lower()
    
    # Computed property with caching
    @property
    def profile_summary(self):
        if 'summary' not in self._cache:
            print("Computing profile summary...")
            self._cache['summary'] = f"{self.name}, {self.age} years old, {self.email}"
        return self._cache['summary']
    
    def clear_cache(self):
        self._cache.clear()


class BankAccount:
    """Properties for controlled attribute access"""
    
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self._balance = max(0, initial_balance)
        self._interest_rate = 0.03
        self._transactions = []
    
    @property
    def balance(self):
        return self._balance
    
    @property
    def interest_rate(self):
        return self._interest_rate
    
    @interest_rate.setter
    def interest_rate(self, rate):
        if not 0 <= rate <= 1:
            raise ValueError("Interest rate must be between 0 and 1")
        self._interest_rate = rate
    
    @property
    def transactions(self):
        return tuple(self._transactions)  # Return immutable copy
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transactions.append(("deposit", amount))
    
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        self._balance -= amount
        self._transactions.append(("withdraw", amount))


# Descriptor for reusable validation
class Validated:
    """Descriptor for type and value validation"""
    
    def __init__(self, validator, default=None, doc=""):
        self.validator = validator
        self.default = default
        self.__doc__ = doc
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        obj.__dict__[self.name] = value
    
    def __delete__(self, obj):
        if self.name in obj.__dict__:
            del obj.__dict__[self.name]


class Typed:
    """Descriptor for type enforcement"""
    
    def __init__(self, expected_type, default=None):
        self.expected_type = expected_type
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)
    
    def __set__(self, obj, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(f"{self.name} must be {self.expected_type.__name__}, got {type(value).__name__}")
        obj.__dict__[self.name] = value


class Product:
    """Using descriptors for validation"""
    
    # Reusable descriptors
    name = Typed(str, "")
    price = Validated(lambda v: isinstance(v, (int, float)) and v >= 0, 0.0)
    quantity = Typed(int, 0)
    sku = Typed(str, "")
    
    def __init__(self, name, price, quantity, sku):
        self.name = name
        self.price = price
        self.quantity = quantity
        self.sku = sku
    
    def __repr__(self):
        return f"Product({self.name}, ${self.price}, qty={self.quantity})"


class LazyProperty:
    """Descriptor for lazy evaluation (computed once)"""
    
    def __init__(self, func):
        self.func = func
        self.name = func.__name__
        self.__doc__ = func.__doc__
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        obj.__dict__[self.name] = value  # Cache it
        return value


class DataProcessor:
    """Using LazyProperty for expensive computations"""
    
    def __init__(self, data):
        self.data = data
    
    @LazyProperty
    def sorted_data(self):
        print("Sorting data...")
        return sorted(self.data)
    
    @LazyProperty
    def statistics(self):
        print("Computing statistics...")
        sorted_d = self.sorted_data  # Uses cached!
        return {
            'count': len(sorted_d),
            'sum': sum(sorted_d),
            'mean': sum(sorted_d) / len(sorted_d) if sorted_d else 0,
            'min': min(sorted_d) if sorted_d else None,
            'max': max(sorted_d) if sorted_d else None
        }


# Demonstration
if __name__ == "__main__":
    print("=== Person Properties ===")
    p = Person("alice", 25, "ALICE@EXAMPLE.COM")
    
    print(f"p.name = {p.name}")  # Getter
    print(f"p.age = {p.age}")    # Read-only
    print(f"p.is_adult = {p.is_adult}")
    print(f"p.email = {p.email}")
    
    p.name = "bob smith"       # Setter
    print(f"After setter: {p.name}")
    
    p.email = "BOB@NEW.COM"    # Setter with validation
    print(f"Email normalized: {p.email}")
    
    try:
        p.name = ""            # Validation error
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        p.email = "invalid"    # Validation error
    except ValueError as e:
        print(f"Error: {e}")
    
    print(f"Profile (first): {p.profile_summary}")  # Computes
    print(f"Profile (cached): {p.profile_summary}")  # Cached
    print()
    
    print("=== Bank Account Properties ===")
    acc = BankAccount("Alice", 1000)
    print(f"Balance: ${acc.balance}")
    print(f"Interest rate: {acc.interest_rate}")
    
    acc.interest_rate = 0.05
    print(f"New rate: {acc.interest_rate}")
    
    try:
        acc.interest_rate = 1.5  # Error
    except ValueError as e:
        print(f"Error: {e}")
    
    acc.deposit(500)
    acc.withdraw(200)
    print(f"Transactions: {acc.transactions}")
    print()
    
    print("=== Product with Descriptors ===")
    prod = Product("Laptop", 999.99, 10, "LAP001")
    print(prod)
    
    try:
        prod.price = -100  # Validation error
    except ValueError as e:
        print(f"Error: {e}")
    
    try:
        prod.quantity = "ten"  # Type error
    except TypeError as e:
        print(f"Error: {e}")
    
    try:
        prod.name = 123  # Type error
    except TypeError as e:
        print(f"Error: {e}")
    print()
    
    print("=== LazyProperty ===")
    processor = DataProcessor([5, 2, 8, 1, 9, 3])
    
    print("First access to sorted_data:")
    print(f"  Sorted: {processor.sorted_data}")
    
    print("Second access to sorted_data (cached):")
    print(f"  Sorted: {processor.sorted_data}")
    
    print("Accessing statistics:")
    stats = processor.statistics
    print(f"  Stats: {stats}")
    
    print("Accessing statistics again (cached):")
    stats2 = processor.statistics
    print(f"  Stats: {stats2}")