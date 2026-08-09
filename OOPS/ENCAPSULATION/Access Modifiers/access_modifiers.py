# Access Modifiers Example

class BankAccount:
    """Demonstrates public, protected, and private access modifiers"""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        # Public attributes - accessible from anywhere
        self.owner = owner
        self.account_type = "checking"
        self.created_at = time.time()
        
        # Protected attributes - internal use, subclass access (convention)
        self._balance = max(0, initial_balance)
        self._transaction_log = []
        self._interest_rate = 0.03
        self._daily_withdrawal_limit = 1000
        self._daily_withdrawn = 0
        
        # Private attributes - name mangled, implementation details
        self.__pin = "0000"
        self.__security_token = self._generate_token()
        self.__failed_attempts = 0
        self.__locked = False
    
    # Public methods - part of the public API
    def deposit(self, amount: float) -> bool:
        """Deposit money into account"""
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self._balance += amount
        self._log_transaction("deposit", amount)
        return True
    
    def withdraw(self, amount: float, pin: str) -> bool:
        """Withdraw money with PIN verification"""
        if not self._verify_pin(pin):
            raise ValueError("Invalid PIN")
        
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        if amount > self._balance:
            raise ValueError("Insufficient funds")
        
        if self._daily_withdrawn + amount > self._daily_withdrawal_limit:
            raise ValueError("Daily withdrawal limit exceeded")
        
        self._balance -= amount
        self._daily_withdrawn += amount
        self._log_transaction("withdraw", amount)
        return True
    
    def get_balance(self, pin: str) -> float:
        """Get current balance (requires PIN)"""
        if not self._verify_pin(pin):
            raise ValueError("Invalid PIN")
        return self._balance
    
    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """Change PIN"""
        if not self._verify_pin(old_pin):
            raise ValueError("Invalid current PIN")
        
        if not (4 <= len(new_pin) <= 8 and new_pin.isdigit()):
            raise ValueError("PIN must be 4-8 digits")
        
        self.__pin = new_pin
        return True
    
    def get_statement(self, pin: str) -> dict:
        """Get account statement"""
        if not self._verify_pin(pin):
            raise ValueError("Invalid PIN")
        
        return {
            "owner": self.owner,
            "balance": self._balance,
            "transactions": tuple(self._transaction_log)
        }
    
    # Protected methods - for internal use and subclasses
    def _log_transaction(self, type: str, amount: float):
        self._transaction_log.append({
            "type": type,
            "amount": amount,
            "balance": self._balance,
            "timestamp": time.time()
        })
    
    def _generate_token(self) -> str:
        import hashlib
        return hashlib.md5(f"{self.owner}{time.time()}".encode()).hexdigest()[:16]
    
    def _verify_pin(self, pin: str) -> bool:
        if self.__locked:
            raise PermissionError("Account locked - too many failed attempts")
        
        if pin == self.__pin:
            self.__failed_attempts = 0
            return True
        else:
            self.__failed_attempts += 1
            if self.__failed_attempts >= 3:
                self.__locked = True
                raise PermissionError("Account locked - too many failed attempts")
            return False
    
    # Private methods - implementation details
    def __reset_failed_attempts(self):
        self.__failed_attempts = 0
    
    def __lock_account(self):
        self.__locked = True
    
    def __unlock_account(self):
        self.__locked = False
        self.__failed_attempts = 0
    
    # Property for controlled read access
    @property
    def balance(self) -> float:
        """Read-only balance (no PIN required for display)"""
        return self._balance
    
    @property
    def is_locked(self) -> bool:
        return self.__locked


class SavingsAccount(BankAccount):
    """Subclass demonstrating protected access"""
    
    def __init__(self, owner: str, initial_balance: float = 0, interest_rate: float = 0.05):
        super().__init__(owner, initial_balance)
        self._interest_rate = interest_rate  # Access protected attribute
        self.account_type = "savings"
    
    def apply_interest(self):
        """Apply interest to balance"""
        interest = self._balance * self._interest_rate  # Access protected
        self._balance += interest
        self._log_transaction("interest", interest)
        return interest
    
    def _log_transaction(self, type: str, amount: float):
        """Override protected method"""
        super()._log_transaction(type, amount)
        # Additional savings-specific logging
        if type == "interest":
            print(f"Interest applied: ${amount:.2f}")


import time

# Demonstration
if __name__ == "__main__":
    print("=== Access Modifiers Demo ===\n")
    
    # Create account
    acc = BankAccount("Alice", 1000)
    print(f"Owner: {acc.owner}")                    # Public: OK
    print(f"Account type: {acc.account_type}")      # Public: OK
    print(f"Balance (property): ${acc.balance}")    # Property: OK
    
    print("\n--- Public Methods ---")
    acc.deposit(500)
    print(f"After deposit: ${acc.balance}")
    
    try:
        acc.withdraw(200, "0000")
        print(f"After withdraw: ${acc.balance}")
    except ValueError as e:
        print(f"Error: {e}")
    
    print("\n--- Protected Access (convention) ---")
    print(f"_balance: {acc._balance}")           # Works but discouraged
    print(f"_transaction_log: {acc._transaction_log}")  # Works but discouraged
    print(f"_interest_rate: {acc._interest_rate}")
    
    print("\n--- Private Access (name mangling) ---")
    # print(acc.__pin)  # AttributeError!
    print(f"_BankAccount__pin: {acc._BankAccount__pin}")  # Works via mangling
    print(f"_BankAccount__security_token: {acc._BankAccount__security_token}")
    print(f"_BankAccount__failed_attempts: {acc._BankAccount__failed_attempts}")
    
    print("\n--- PIN Security ---")
    try:
        acc.get_balance("wrong")
    except ValueError as e:
        print(f"Wrong PIN: {e}")
    
    print(f"Failed attempts: {acc._BankAccount__failed_attempts}")
    
    # Lock account
    for i in range(2):
        try:
            acc.get_balance("wrong")
        except:
            pass
    
    print(f"After 3 failed: locked={acc.is_locked}")
    
    print("\n--- Savings Account (Subclass) ---")
    savings = SavingsAccount("Bob", 5000)
    print(f"Interest rate: {savings._interest_rate}")  # Access protected
    interest = savings.apply_interest()
    print(f"Interest earned: ${interest:.2f}")
    print(f"New balance: ${savings.balance}")
    
    print("\n--- All Attributes ===")
    print("Public:", [a for a in dir(acc) if not a.startswith('_')])
    print("Protected:", [a for a in dir(acc) if a.startswith('_') and not a.startswith('__')])
    print("Private (mangled):", [a for a in dir(acc) if a.startswith('_BankAccount__')])