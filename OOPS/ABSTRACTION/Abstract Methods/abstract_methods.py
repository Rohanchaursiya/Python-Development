# Abstract Methods Example

from abc import ABC, abstractmethod
from typing import Generic, TypeVar
import time

T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Generic repository with abstract methods"""
    
    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass
    
    @abstractmethod
    def get_all(self) -> list[T]:
        pass
    
    @abstractmethod
    def add(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass
    
    # Concrete method using abstract ones
    def exists(self, id: int) -> bool:
        return self.get_by_id(id) is not None
    
    def count(self) -> int:
        return len(self.get_all())


class InMemoryRepository(Repository[dict]):
    def __init__(self):
        self._data: dict[int, dict] = {}
        self._next_id = 1
    
    def get_by_id(self, id: int) -> dict | None:
        return self._data.get(id)
    
    def get_all(self) -> list[dict]:
        return list(self._data.values())
    
    def add(self, entity: dict) -> dict:
        entity = entity.copy()
        entity['id'] = self._next_id
        self._data[self._next_id] = entity
        self._next_id += 1
        return entity
    
    def update(self, entity: dict) -> dict:
        id = entity.get('id')
        if id not in self._data:
            raise ValueError(f"Entity {id} not found")
        self._data[id] = entity
        return entity
    
    def delete(self, id: int) -> bool:
        if id in self._data:
            del self._data[id]
            return True
        return False


# Abstract class with multiple abstract methods
class PaymentGateway(ABC):
    @abstractmethod
    def authorize(self, amount: float, currency: str) -> str:
        """Returns authorization code"""
        pass
    
    @abstractmethod
    def capture(self, auth_code: str) -> bool:
        pass
    
    @abstractmethod
    def void(self, auth_code: str) -> bool:
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: float) -> str:
        """Returns refund ID"""
        pass
    
    @property
    @abstractmethod
    def supported_currencies(self) -> list[str]:
        pass
    
    @property
    @abstractmethod
    def gateway_name(self) -> str:
        pass
    
    # Template method
    def process_payment(self, amount: float, currency: str) -> dict:
        if currency not in self.supported_currencies:
            raise ValueError(f"{self.gateway_name} doesn't support {currency}")
        
        auth_code = self.authorize(amount, currency)
        if not auth_code:
            return {"success": False, "error": "Authorization failed"}
        
        captured = self.capture(auth_code)
        if not captured:
            self.void(auth_code)
            return {"success": False, "error": "Capture failed"}
        
        return {
            "success": True,
            "gateway": self.gateway_name,
            "auth_code": auth_code,
            "amount": amount,
            "currency": currency
        }


class StripeGateway(PaymentGateway):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def authorize(self, amount: float, currency: str) -> str:
        return f"stripe_auth_{int(time.time())}"
    
    def capture(self, auth_code: str) -> bool:
        return True
    
    def void(self, auth_code: str) -> bool:
        return True
    
    def refund(self, transaction_id: str, amount: float) -> str:
        return f"stripe_refund_{int(time.time())}"
    
    @property
    def supported_currencies(self) -> list[str]:
        return ["USD", "EUR", "GBP", "JPY", "CAD", "AUD"]
    
    @property
    def gateway_name(self) -> str:
        return "Stripe"


class PayPalGateway(PaymentGateway):
    def __init__(self, client_id: str, secret: str):
        self.client_id = client_id
        self.secret = secret
    
    def authorize(self, amount: float, currency: str) -> str:
        return f"paypal_auth_{int(time.time())}"
    
    def capture(self, auth_code: str) -> bool:
        return True
    
    def void(self, auth_code: str) -> bool:
        return True
    
    def refund(self, transaction_id: str, amount: float) -> str:
        return f"paypal_refund_{int(time.time())}"
    
    @property
    def supported_currencies(self) -> list[str]:
        return ["USD", "EUR", "GBP", "CAD", "AUD"]
    
    @property
    def gateway_name(self) -> str:
        return "PayPal"


# Abstract property example
class Configurable(ABC):
    @property
    @abstractmethod
    def config_schema(self) -> dict:
        """Returns JSON schema for configuration"""
        pass
    
    @property
    @abstractmethod
    def default_config(self) -> dict:
        pass
    
    def validate_config(self, config: dict) -> bool:
        # Simplified validation
        required = self.config_schema.get("required", [])
        return all(key in config for key in required)


class DatabaseConfig(Configurable):
    @property
    def config_schema(self) -> dict:
        return {
            "type": "object",
            "required": ["host", "port", "database"],
            "properties": {
                "host": {"type": "string"},
                "port": {"type": "integer"},
                "database": {"type": "string"},
                "username": {"type": "string"},
                "password": {"type": "string"}
            }
        }
    
    @property
    def default_config(self) -> dict:
        return {
            "host": "localhost",
            "port": 5432,
            "database": "app",
            "username": "user",
            "password": ""
        }


# Demonstration
if __name__ == "__main__":
    print("=== Repository Pattern ===")
    repo = InMemoryRepository()
    
    user1 = repo.add({"name": "Alice", "email": "alice@example.com"})
    user2 = repo.add({"name": "Bob", "email": "bob@example.com"})
    
    print(f"Added: {user1}")
    print(f"Count: {repo.count()}")
    print(f"Exists ID 1: {repo.exists(1)}")
    print(f"All: {repo.get_all()}")
    
    repo.update({"id": 1, "name": "Alice Smith", "email": "alice@example.com"})
    print(f"Updated: {repo.get_by_id(1)}")
    
    repo.delete(2)
    print(f"After delete: {repo.get_all()}")
    
    print("\n=== Payment Gateway ===")
    gateways = [
        StripeGateway("sk_test_123"),
        PayPalGateway("client_123", "secret_456")
    ]
    
    for gateway in gateways:
        print(f"\n--- {gateway.gateway_name} ---")
        print(f"Currencies: {gateway.supported_currencies}")
        
        result = gateway.process_payment(99.99, "USD")
        print(f"Payment: {result}")
        
        if result["success"]:
            refund_id = gateway.refund(result["auth_code"], 50.00)
            print(f"Partial refund: {refund_id}")
    
    print("\n=== Configurable ===")
    db_config = DatabaseConfig()
    print(f"Schema: {db_config.config_schema}")
    print(f"Defaults: {db_config.default_config}")
    
    test_config = {"host": "db.example.com", "port": 5432, "database": "prod"}
    print(f"Valid config: {db_config.validate_config(test_config)}")
    
    incomplete = {"host": "localhost"}
    print(f"Incomplete config: {db_config.validate_config(incomplete)}")