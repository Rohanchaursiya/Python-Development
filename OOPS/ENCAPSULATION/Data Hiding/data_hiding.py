# Data Hiding Example

import hashlib
import time
from datetime import datetime


class SecureWallet:
    """Complete data hiding - no direct access to internal state"""
    
    def __init__(self, owner: str, initial_balance: float = 0):
        self._owner = owner
        self.__balance = max(0, initial_balance)
        self.__pin_hash = None
        self.__transaction_history = []
        self.__failed_attempts = 0
        self.__locked = False
        self.__daily_limit = 1000
        self.__daily_withdrawn = 0
        self.__last_reset_date = datetime.now().date()
    
    # Public interface only
    def set_pin(self, pin: str) -> bool:
        """Set PIN (only once)"""
        if self.__pin_hash is not None:
            raise PermissionError("PIN already set - use change_pin()")
        if not (4 <= len(pin) <= 8 and pin.isdigit()):
            raise ValueError("PIN must be 4-8 digits")
        self.__pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        return True
    
    def verify_pin(self, pin: str) -> bool:
        """Verify PIN without exposing it"""
        self.__check_lock()
        self.__reset_daily_if_needed()
        
        pin_hash = hashlib.sha256(pin.encode()).hexdigest()
        if pin_hash == self.__pin_hash:
            self.__failed_attempts = 0
            return True
        else:
            self.__failed_attempts += 1
            if self.__failed_attempts >= 3:
                self.__lock()
                raise PermissionError("Wallet locked - too many failed attempts")
            return False
    
    def deposit(self, amount: float, pin: str) -> float:
        """Deposit funds"""
        if not self.verify_pin(pin):
            raise ValueError("Invalid PIN")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        self.__balance += amount
        self.__record_transaction("deposit", amount)
        return self.__balance
    
    def withdraw(self, amount: float, pin: str) -> float:
        """Withdraw funds"""
        if not self.verify_pin(pin):
            raise ValueError("Invalid PIN")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.__balance:
            raise ValueError("Insufficient funds")
        if self.__daily_withdrawn + amount > self.__daily_limit:
            raise ValueError(f"Daily limit exceeded (${self.__daily_limit})")
        
        self.__balance -= amount
        self.__daily_withdrawn += amount
        self.__record_transaction("withdraw", amount)
        return self.__balance
    
    def get_balance(self, pin: str) -> float:
        """Get current balance"""
        if not self.verify_pin(pin):
            raise ValueError("Invalid PIN")
        return self.__balance
    
    def get_statement(self, pin: str) -> dict:
        """Get account statement"""
        if not self.verify_pin(pin):
            raise ValueError("Invalid PIN")
        
        return {
            "owner": self._owner,
            "balance": self.__balance,
            "daily_limit": self.__daily_limit,
            "daily_used": self.__daily_withdrawn,
            "transactions": tuple(self.__transaction_history),
            "locked": self.__locked
        }
    
    def change_pin(self, old_pin: str, new_pin: str) -> bool:
        """Change PIN"""
        if not self.verify_pin(old_pin):
            raise ValueError("Invalid current PIN")
        if not (4 <= len(new_pin) <= 8 and new_pin.isdigit()):
            raise ValueError("PIN must be 4-8 digits")
        
        self.__pin_hash = hashlib.sha256(new_pin.encode()).hexdigest()
        return True
    
    def unlock_with_recovery(self, recovery_code: str) -> bool:
        """Unlock with recovery code (simplified)"""
        if recovery_code == "RECOVERY123":
            self.__locked = False
            self.__failed_attempts = 0
            return True
        return False
    
    # Read-only properties (no PIN required)
    @property
    def owner(self) -> str:
        return self._owner
    
    @property
    def is_locked(self) -> bool:
        return self.__locked
    
    @property
    def daily_limit(self) -> int:
        return self.__daily_limit
    
    # Internal methods - completely hidden
    def __check_lock(self):
        if self.__locked:
            raise PermissionError("Wallet is locked")
    
    def __lock(self):
        self.__locked = True
    
    def __reset_daily_if_needed(self):
        today = datetime.now().date()
        if today != self.__last_reset_date:
            self.__daily_withdrawn = 0
            self.__last_reset_date = today
    
    def __record_transaction(self, type: str, amount: float):
        self.__transaction_history.append({
            "type": type,
            "amount": amount,
            "balance": self.__balance,
            "timestamp": datetime.now().isoformat()
        })


class ImmutableConfig:
    """Truly immutable configuration after initialization"""
    
    def __init__(self, **settings):
        self.__settings = dict(settings)
        self.__frozen = True
    
    def __setattr__(self, name, value):
        if name.startswith('_ImmutableConfig__'):
            super().__setattr__(name, value)
        elif getattr(self, '_ImmutableConfig__frozen', False):
            raise AttributeError(f"Cannot modify frozen config: {name}")
        else:
            super().__setattr__(name, value)
    
    def __getattr__(self, name):
        if name in self.__settings:
            return self.__settings[name]
        raise AttributeError(f"No setting: {name}")
    
    def __delattr__(self, name):
        raise AttributeError("Cannot delete config attributes")
    
    def get(self, key, default=None):
        return self.__settings.get(key, default)
    
    def as_dict(self):
        return self.__settings.copy()
    
    def __repr__(self):
        return f"ImmutableConfig({self.__settings})"


class DataVault:
    """Encrypted data storage with hidden encryption"""
    
    def __init__(self, master_key: str):
        self.__master_key = master_key
        self.__vault = {}
        self.__access_log = []
    
    def _derive_key(self, context: str) -> bytes:
        """Derive encryption key from master key + context"""
        return hashlib.pbkdf2_hmac(
            'sha256',
            self.__master_key.encode(),
            context.encode(),
            100000
        )[:32]
    
    def _encrypt(self, data: str, context: str) -> str:
        """Simple XOR encryption (demo only)"""
        key = self._derive_key(context)
        data_bytes = data.encode()
        encrypted = bytes(a ^ b for a, b in zip(data_bytes, key * (len(data_bytes)//len(key) + 1)))
        return encrypted.hex()
    
    def _decrypt(self, encrypted_hex: str, context: str) -> str:
        key = self._derive_key(context)
        encrypted_bytes = bytes.fromhex(encrypted_hex)
        decrypted = bytes(a ^ b for a, b in zip(encrypted_bytes, key * (len(encrypted_bytes)//len(key) + 1)))
        return decrypted.decode()
    
    # Public interface
    def store(self, key: str, value: str) -> bool:
        self.__vault[key] = self._encrypt(value, key)
        self.__access_log.append(("store", key, time.time()))
        return True
    
    def retrieve(self, key: str) -> str | None:
        if key not in self.__vault:
            return None
        self.__access_log.append(("retrieve", key, time.time()))
        return self._decrypt(self.__vault[key], key)
    
    def delete(self, key: str) -> bool:
        if key in self.__vault:
            del self.__vault[key]
            self.__access_log.append(("delete", key, time.time()))
            return True
        return False
    
    def list_keys(self) -> list[str]:
        return list(self.__vault.keys())
    
    def get_access_log(self) -> list[tuple]:
        return self.__access_log.copy()


# Demonstration
if __name__ == "__main__":
    print("=== SecureWallet ===")
    wallet = SecureWallet("Alice", 1000)
    wallet.set_pin("1234")
    
    print(f"Owner: {wallet.owner}")
    print(f"Balance: ${wallet.get_balance('1234')}")
    print(f"Daily limit: ${wallet.daily_limit}")
    
    wallet.deposit(500, '1234')
    print(f"After deposit: ${wallet.get_balance('1234')}")
    
    wallet.withdraw(200, '1234')
    print(f"After withdraw: ${wallet.get_balance('1234')}")
    
    stmt = wallet.get_statement('1234')
    print(f"Transactions: {len(stmt['transactions'])}")
    for tx in stmt['transactions']:
        print(f"  {tx['type']}: ${tx['amount']} (balance: ${tx['balance']})")
    
    print("\n--- Failed attempts ---")
    for i in range(3):
        try:
            wallet.get_balance("wrong")
        except Exception as e:
            print(f"  Attempt {i+1}: {e}")
    
    print(f"Locked: {wallet.is_locked}")
    wallet.unlock_with_recovery("RECOVERY123")
    print(f"After recovery: {wallet.is_locked}")
    
    print("\n=== ImmutableConfig ===")
    config = ImmutableConfig(
        api_key="secret123",
        max_retries=3,
        timeout=30,
        debug=False
    )
    
    print(f"API Key: {config.api_key}")
    print(f"Timeout: {config.timeout}")
    print(f"All settings: {config.as_dict()}")
    
    try:
        config.timeout = 60
    except AttributeError as e:
        print(f"Error: {e}")
    
    try:
        config.new_setting = "value"
    except AttributeError as e:
        print(f"Error: {e}")
    
    print("\n=== DataVault (Encrypted Storage) ===")
    vault = DataVault("master_key_123")
    
    vault.store("api_key", "sk_live_abcdef123456")
    vault.store("database_url", "postgres://user:pass@localhost/db")
    vault.store("jwt_secret", "super_secret_jwt_key")
    
    print(f"Keys: {vault.list_keys()}")
    print(f"API Key: {vault.retrieve('api_key')}")
    print(f"DB URL: {vault.retrieve('database_url')}")
    print(f"Missing: {vault.retrieve('missing')}")
    
    vault.delete("jwt_secret")
    print(f"After delete: {vault.list_keys()}")
    
    print("\nAccess log:")
    for action, key, timestamp in vault.get_access_log():
        print(f"  {action}: {key} at {timestamp}")