# Property Decorators Example

class Rectangle:
    """Basic @property with validation"""
    
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    @property
    def width(self) -> float:
        return self._width
    
    @width.setter
    def width(self, value: float):
        if value <= 0:
            raise ValueError("Width must be positive")
        self._width = value
    
    @property
    def height(self) -> float:
        return self._height
    
    @height.setter
    def height(self, value: float):
        if value <= 0:
            raise ValueError("Height must be positive")
        self._height = value
    
    # Read-only computed properties
    @property
    def area(self) -> float:
        return self._width * self._height
    
    @property
    def perimeter(self) -> float:
        return 2 * (self._width + self._height)
    
    @property
    def is_square(self) -> bool:
        return self._width == self._height
    
    # Property with deleter
    @property
    def dimensions(self) -> tuple:
        return (self._width, self._height)
    
    @dimensions.setter
    def dimensions(self, value: tuple):
        self.width, self.height = value
    
    @dimensions.deleter
    def dimensions(self):
        self._width = 0
        self._height = 0


class Circle:
    """Property with cached computation"""
    
    def __init__(self, radius: float):
        self.radius = radius
        self._area_cache = None
        self._perimeter_cache = None
    
    @property
    def radius(self) -> float:
        return self._radius
    
    @radius.setter
    def radius(self, value: float):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value
        self._invalidate_cache()
    
    @property
    def area(self) -> float:
        if self._area_cache is None:
            self._area_cache = 3.14159 * self._radius ** 2
        return self._area_cache
    
    @property
    def perimeter(self) -> float:
        if self._perimeter_cache is None:
            self._perimeter_cache = 2 * 3.14159 * self._radius
        return self._perimeter_cache
    
    @property
    def diameter(self) -> float:
        return 2 * self._radius
    
    def _invalidate_cache(self):
        self._area_cache = None
        self._perimeter_cache = None


class UserProfile:
    """Property with validation, normalization, and cache"""
    
    def __init__(self, first_name: str, last_name: str, email: str):
        self._cache = {}
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
    @property
    def first_name(self) -> str:
        return self._first_name
    
    @first_name.setter
    def first_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("First name cannot be empty")
        self._first_name = value.strip().title()
        self._invalidate_cache()
    
    @property
    def last_name(self) -> str:
        return self._last_name
    
    @last_name.setter
    def last_name(self, value: str):
        if not value or not value.strip():
            raise ValueError("Last name cannot be empty")
        self._last_name = value.strip().title()
        self._invalidate_cache()
    
    @property
    def email(self) -> str:
        return self._email
    
    @email.setter
    def email(self, value: str):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        self._email = value.lower()
    
    @property
    def full_name(self) -> str:
        return f"{self._first_name} {self._last_name}"
    
    @property
    def initials(self) -> str:
        return f"{self._first_name[0]}.{self._last_name[0]}."
    
    @property
    def username(self) -> str:
        if 'username' not in self._cache:
            base = f"{self._first_name.lower()}.{self._last_name.lower()}"
            self._cache['username'] = base.replace(" ", "").replace("-", "")
        return self._cache['username']
    
    def _invalidate_cache(self):
        self._cache.clear()


class BankAccount:
    """Property with side effects and validation"""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self.owner = owner
        self._balance = max(0, initial_balance)
        self._interest_rate = 0.03
        self._transaction_log = []
    
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
    def transactions(self) -> tuple:
        return tuple(self._transaction_log)
    
    def deposit(self, amount: float):
        if amount <= 0:
            raise ValueError("Deposit must be positive")
        self._balance += amount
        self._log("deposit", amount)
    
    def withdraw(self, amount: float) -> bool:
        if amount <= 0:
            raise ValueError("Withdrawal must be positive")
        if amount > self._balance:
            return False
        self._balance -= amount
        self._log("withdraw", amount)
        return True
    
    def _log(self, type: str, amount: float):
        self._transaction_log.append({
            "type": type, "amount": amount,
            "balance": self._balance
        })


class Config:
    """Property for backward compatibility and deprecation"""
    
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
        warnings.warn(
            "verbose is deprecated, use debug_mode instead",
            DeprecationWarning,
            stacklevel=2
        )
        return self.debug_mode
    
    @verbose.setter
    def verbose(self, value: bool):
        import warnings
        warnings.warn(
            "verbose is deprecated, use debug_mode instead",
            DeprecationWarning,
            stacklevel=2
        )
        self.debug_mode = value
    
    # Dynamic property creation
    def __getattr__(self, name):
        if name in self._settings:
            return self._settings[name]
        raise AttributeError(f"'{self.__class__.__name__}' has no attribute '{name}'")


# Demonstration
if __name__ == "__main__":
    print("=== Rectangle ===")
    r = Rectangle(10, 5)
    print(f"Width: {r.width}, Height: {r.height}")
    print(f"Area: {r.area}, Perimeter: {r.perimeter}")
    print(f"Is square: {r.is_square}")
    
    r.width = 7
    print(f"After width=7: Area={r.area}")
    
    r.dimensions = (3, 3)
    print(f"After dimensions=(3,3): Is square={r.is_square}")
    
    try:
        r.height = -5
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n=== Circle with Caching ===")
    c = Circle(5)
    print(f"Radius: {c.radius}")
    print(f"Area: {c.area}")  # Computes
    print(f"Area again: {c.area}")  # Cached
    print(f"Perimeter: {c.perimeter}")
    print(f"Diameter: {c.diameter}")
    
    c.radius = 10
    print(f"After radius=10: Area={c.area}")  # Recomputed
    
    print("\n=== UserProfile ===")
    u = UserProfile("john", "doe", "JOHN@EXAMPLE.COM")
    print(f"Full name: {u.full_name}")
    print(f"Initials: {u.initials}")
    print(f"Email: {u.email}")
    print(f"Username: {u.username}")
    
    u.first_name = "jane"
    print(f"After change: {u.full_name}, {u.username}")
    
    print("\n=== BankAccount ===")
    acc = BankAccount("Alice", 1000)
    print(f"Balance: ${acc.balance}")
    acc.deposit(500)
    acc.withdraw(200)
    print(f"Transactions: {acc.transactions}")
    
    print("\n=== Config with Deprecation ===")
    cfg = Config()
    cfg.debug_mode = True
    print(f"Debug mode: {cfg.debug_mode}")
    print(f"Timeout: {cfg.timeout}")
    # cfg.verbose  # Would show DeprecationWarning