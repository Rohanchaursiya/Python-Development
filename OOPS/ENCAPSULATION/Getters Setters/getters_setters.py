# Getters and Setters Example

class Person:
    """Traditional getters/setters vs @property"""
    
    def __init__(self, name: str, age: int, email: str):
        # Traditional private attributes
        self._name = ""
        self._age = 0
        self._email = ""
        
        # Use setters for validation
        self.set_name(name)
        self.set_age(age)
        self.set_email(email)
    
    # Traditional getter/setter methods
    def get_name(self) -> str:
        return self._name
    
    def set_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()
    
    def get_age(self) -> int:
        return self._age
    
    def set_age(self, value: int):
        if not isinstance(value, int):
            raise TypeError("Age must be integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be 0-150")
        self._age = value
    
    def get_email(self) -> str:
        return self._email
    
    def set_email(self, value: str):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        self._email = value.lower()
    
    # Computed property (read-only)
    def is_adult(self) -> bool:
        return self._age >= 18
    
    def display_name(self) -> str:
        return f"{self._name} ({self._age})"


class Temperature:
    """@property for multiple temperature scales"""
    
    def __init__(self, celsius: float = 0):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self) -> float:
        return self._celsius + 273.15
    
    @kelvin.setter
    def kelvin(self, value: float):
        if value < 0:
            raise ValueError("Kelvin cannot be negative")
        self.celsius = value - 273.15


class BankAccount:
    """@property with validation and side effects"""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = max(0, initial_balance)
        self._interest_rate = 0.03
        self._transaction_count = 0
    
    @property
    def balance(self) -> float:
        return self._balance
    
    @property
    def interest_rate(self) -> float:
        return self._interest_rate
    
    @interest_rate.setter
    def interest_rate(self, rate: float):
        if not 0 <= rate <= 1:
            raise ValueError("Interest rate must be 0-1")
        self._interest_rate = rate
    
    @property
    def transaction_count(self) -> int:
        return self._transaction_count
    
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._transaction_count += 1
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            return False
        self._balance -= amount
        self._transaction_count += 1
        return True


class UserProfile:
    """@property with caching"""
    
    def __init__(self, first_name: str, last_name: str, email: str):
        self._first_name = first_name.strip().title()
        self._last_name = last_name.strip().title()
        self._email = email.lower()
        self._cache = {}
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        self._first_name = value.strip().title()
        self._invalidate_cache()
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        self._last_name = value.strip().title()
        self._invalidate_cache()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if "@" not in value:
            raise ValueError("Invalid email")
        self._email = value.lower()
    
    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
    
    @property
    def initials(self) -> str:
        return f"{self._first_name[0]}.{self._last_name[0]}."
    
    # Expensive computed property with caching
    @property
    def profile_hash(self) -> str:
        if 'hash' not in self._cache:
            print("  Computing profile hash...")
            import hashlib
            data = f"{self.full_name}{self.email}".encode()
            self._cache['hash'] = hashlib.sha256(data).hexdigest()[:16]
        return self._cache['hash']
    
    def _invalidate_cache(self):
        self._cache.clear()


class Config:
    """@property for backward compatibility"""
    
    def __init__(self):
        self._settings = {"debug": False, "timeout": 30}
    
    @property
    def debug_mode(self) -> bool:
        return self._settings.get("debug", False)
    
    @debug_mode.setter
    def debug_mode(self, value: bool):
        self._settings["debug"] = bool(value)
    
    # Deprecated property
    @property
    def verbose(self) -> bool:
        import warnings
        warnings.warn("verbose is deprecated, use debug_mode", DeprecationWarning, stacklevel=2)
        return self.debug_mode
    
    @verbose.setter
    def verbose(self, value: bool):
        import warnings
        warnings.warn("verbose is deprecated, use debug_mode", DeprecationWarning, stacklevel=2)
        self.debug_mode = value


# Demonstration
if __name__ == "__main__":
    print("=== Traditional Getters/Setters ===")
    p = Person("alice smith", 25, "ALICE@EXAMPLE.COM")
    
    print(f"Name: {p.get_name()}")
    print(f"Age: {p.get_age()}")
    print(f"Email: {p.get_email()}")
    print(f"Adult: {p.is_adult()}")
    print(f"Display: {p.display_name()}")
    
    p.set_name("bob jones")
    p.set_age(30)
    print(f"Updated: {p.get_name()}, {p.get_age()}")
    
    try:
        p.set_age(-5)
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== Temperature with @property ===")
    t = Temperature(25)
    print(f"C: {t.celsius}, F: {t.fahrenheit}, K: {t.kelvin}")
    
    t.fahrenheit = 212
    print(f"After F=212: C={t.celsius}, K={t.kelvin}")
    
    t.kelvin = 300
    print(f"After K=300: C={t.celsius}, F={t.fahrenheit}")
    
    try:
        t.celsius = -300
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== BankAccount with Validation ===")
    acc = BankAccount("Alice", 1000)
    print(f"Balance: ${acc.balance}")
    print(f"Interest rate: {acc.interest_rate}")
    
    acc.interest_rate = 0.05
    print(f"New rate: {acc.interest_rate}")
    
    try:
        acc.interest_rate = 1.5
    except ValueError as e:
        print(f"Error: {e}")
    
    acc.deposit(500)
    acc.withdraw(200)
    print(f"Transactions: {acc.transaction_count}")
    
    print("\n=== UserProfile with Caching ===")
    u = UserProfile("john", "doe", "JOHN@EXAMPLE.COM")
    print(f"Full name: {u.full_name}")
    print(f"Initials: {u.initials}")
    
    print("First hash access:")
    print(f"  {u.profile_hash}")
    
    print("Second hash access (cached):")
    print(f"  {u.profile_hash}")
    
    u.first_name = "jane"
    print(f"After name change: {u.full_name}")
    print("Hash after invalidation:")
    print(f"  {u.profile_hash}")
    
    print("\n=== Config with Deprecation ===")
    c = Config()
    c.debug_mode = True
    print(f"Debug mode: {c.debug_mode}")
    # print(c.verbose)  # Would show DeprecationWarning