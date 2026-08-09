# Concrete Implementation Example

from abc import ABC, abstractmethod
from typing import Protocol
import hashlib
import time
import json


# Abstract interfaces
class StorageBackend(ABC):
    @abstractmethod
    def save(self, key: str, data: bytes) -> bool:
        pass
    
    @abstractmethod
    def load(self, key: str) -> bytes | None:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def list_keys(self, prefix: str = "") -> list[str]:
        pass


class CacheBackend(ABC):
    @abstractmethod
    def get(self, key: str) -> any:
        pass
    
    @abstractmethod
    def set(self, key: str, value: any, ttl: int = 3600) -> bool:
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        pass


class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient: str, message: str) -> bool:
        pass
    
    @property
    @abstractmethod
    def channel_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def max_length(self) -> int:
        pass


# Concrete storage implementations
class LocalFileStorage(StorageBackend):
    def __init__(self, base_path: str = "./storage"):
        import os
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def _get_path(self, key: str) -> str:
        import os
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.base_path, safe_key)
    
    def save(self, key: str, data: bytes) -> bool:
        try:
            with open(self._get_path(key), 'wb') as f:
                f.write(data)
            return True
        except Exception:
            return False
    
    def load(self, key: str) -> bytes | None:
        try:
            with open(self._get_path(key), 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return None
    
    def delete(self, key: str) -> bool:
        try:
            import os
            os.remove(self._get_path(key))
            return True
        except FileNotFoundError:
            return False
    
    def exists(self, key: str) -> bool:
        import os
        return os.path.exists(self._get_path(key))
    
    def list_keys(self, prefix: str = "") -> list[str]:
        import os
        keys = []
        for fname in os.listdir(self.base_path):
            if fname.startswith(prefix):
                keys.append(fname)
        return keys


class S3Storage(StorageBackend):
    """Simulated S3 storage"""
    def __init__(self, bucket: str, region: str = "us-east-1"):
        self.bucket = bucket
        self.region = region
        self._data: dict[str, bytes] = {}
    
    def save(self, key: str, data: bytes) -> bool:
        self._data[key] = data
        return True
    
    def load(self, key: str) -> bytes | None:
        return self._data.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        return key in self._data
    
    def list_keys(self, prefix: str = "") -> list[str]:
        return [k for k in self._data.keys() if k.startswith(prefix)]


class DatabaseStorage(StorageBackend):
    """Simulated database storage"""
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self._data: dict[str, bytes] = {}
    
    def save(self, key: str, data: bytes) -> bool:
        self._data[key] = data
        return True
    
    def load(self, key: str) -> bytes | None:
        return self._data.get(key)
    
    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False
    
    def exists(self, key: str) -> bool:
        return key in self._data
    
    def list_keys(self, prefix: str = "") -> list[str]:
        return [k for k in self._data.keys() if k.startswith(prefix)]


# Concrete cache implementations
class InMemoryCache(CacheBackend):
    def __init__(self):
        self._cache: dict[str, tuple[any, float]] = {}
    
    def get(self, key: str) -> any:
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: any, ttl: int = 3600) -> bool:
        self._cache[key] = (value, time.time() + ttl)
        return True
    
    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> bool:
        self._cache.clear()
        return True


class RedisCache(CacheBackend):
    """Simulated Redis cache"""
    def __init__(self, host: str = "localhost", port: int = 6379):
        self.host = host
        self.port = port
        self._cache: dict[str, tuple[any, float]] = {}
    
    def get(self, key: str) -> any:
        if key in self._cache:
            value, expiry = self._cache[key]
            if time.time() < expiry:
                return value
            else:
                del self._cache[key]
        return None
    
    def set(self, key: str, value: any, ttl: int = 3600) -> bool:
        self._cache[key] = (value, time.time() + ttl)
        return True
    
    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    def clear(self) -> bool:
        self._cache.clear()
        return True


# Concrete notification implementations
class EmailNotification(NotificationChannel):
    def __init__(self, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"📧 Email to {recipient}: {message[:50]}...")
        return True
    
    @property
    def channel_name(self) -> str:
        return "Email"
    
    @property
    def max_length(self) -> int:
        return 10000


class SMSNotification(NotificationChannel):
    def __init__(self, provider: str):
        self.provider = provider
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"📱 SMS via {self.provider} to {recipient}: {message[:50]}...")
        return True
    
    @property
    def channel_name(self) -> str:
        return "SMS"
    
    @property
    def max_length(self) -> int:
        return 160


class PushNotification(NotificationChannel):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"🔔 Push to {recipient}: {message[:50]}...")
        return True
    
    @property
    def channel_name(self) -> str:
        return "Push"
    
    @property
    def max_length(self) -> int:
        return 2000


class SlackNotification(NotificationChannel):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(self, recipient: str, message: str) -> bool:
        print(f"💬 Slack to #{recipient}: {message[:50]}...")
        return True
    
    @property
    def channel_name(self) -> str:
        return "Slack"
    
    @property
    def max_length(self) -> int:
        return 40000


# Factory for interchangeability
class StorageFactory:
    @staticmethod
    def create_storage(backend: str, **config) -> StorageBackend:
        backends = {
            "local": LocalFileStorage,
            "s3": S3Storage,
            "database": DatabaseStorage
        }
        if backend not in backends:
            raise ValueError(f"Unknown storage backend: {backend}")
        return backends[backend](**config)


class CacheFactory:
    @staticmethod
    def create_cache(backend: str, **config) -> CacheBackend:
        backends = {
            "memory": InMemoryCache,
            "redis": RedisCache
        }
        if backend not in backends:
            raise ValueError(f"Unknown cache backend: {backend}")
        return backends[backend](**config)


class NotificationFactory:
    @staticmethod
    def create_channel(channel: str, **config) -> NotificationChannel:
        channels = {
            "email": EmailNotification,
            "sms": SMSNotification,
            "push": PushNotification,
            "slack": SlackNotification
        }
        if channel not in channels:
            raise ValueError(f"Unknown notification channel: {channel}")
        return channels[channel](**config)


# Service using abstractions
class FileService:
    def __init__(self, storage: StorageBackend, cache: CacheBackend):
        self.storage = storage
        self.cache = cache
    
    def save_file(self, key: str, content: str) -> bool:
        data = content.encode()
        success = self.storage.save(key, data)
        if success:
            self.cache.set(key, content)
        return success
    
    def get_file(self, key: str) -> str | None:
        # Try cache first
        cached = self.cache.get(key)
        if cached is not None:
            print(f"  Cache hit: {key}")
            return cached
        
        # Load from storage
        data = self.storage.load(key)
        if data is not None:
            content = data.decode()
            self.cache.set(key, content)
            return content
        return None


class NotificationService:
    def __init__(self, channels: list[NotificationChannel]):
        self.channels = channels
    
    def notify_all(self, recipient: str, message: str) -> dict:
        results = {}
        for channel in self.channels:
            if len(message) <= channel.max_length:
                results[channel.channel_name] = channel.send(recipient, message)
            else:
                results[channel.channel_name] = False
                print(f"  {channel.channel_name}: Message too long ({len(message)} > {channel.max_length})")
        return results


# Demonstration
if __name__ == "__main__":
    print("=== Interchangeable Storage ===")
    
    # Create different storage backends
    storages = [
        StorageFactory.create_storage("local", base_path="./demo_storage"),
        StorageFactory.create_storage("s3", bucket="my-bucket"),
        StorageFactory.create_storage("database", connection_string="postgres://localhost")
    ]
    
    for storage in storages:
        print(f"\n--- {type(storage).__name__} ---")
        storage.save("test.txt", b"Hello World!")
        loaded = storage.load("test.txt")
        print(f"  Saved and loaded: {loaded}")
        print(f"  Exists: {storage.exists('test.txt')}")
        print(f"  Keys: {storage.list_keys()}")
    
    print("\n=== Caching Layer ===")
    cache = CacheFactory.create_cache("memory")
    cache.set("user:1", {"name": "Alice", "email": "alice@example.com"}, ttl=60)
    print(f"Cached: {cache.get('user:1')}")
    
    print("\n=== File Service with Cache ===")
    file_service = FileService(
        StorageFactory.create_storage("local", base_path="./demo_files"),
        CacheFactory.create_cache("memory")
    )
    
    file_service.save_file("doc1.txt", "Important document content")
    print(f"First read: {file_service.get_file('doc1.txt')}")
    print(f"Second read: {file_service.get_file('doc1.txt')}")  # Cache hit
    
    print("\n=== Multi-channel Notification ===")
    channels = [
        NotificationFactory.create_channel("email", smtp_server="smtp.gmail.com", port=587),
        NotificationFactory.create_channel("sms", provider="Twilio"),
        NotificationFactory.create_channel("push", api_key="push_key_123"),
        NotificationFactory.create_channel("slack", webhook_url="https://hooks.slack.com/...")
    ]
    
    notifier = NotificationService(channels)
    results = notifier.notify_all("user123", "Your order has been shipped!")
    print(f"Results: {results}")
    
    # Test with long message
    long_msg = "x" * 5000
    results = notifier.notify_all("user123", long_msg)
    print(f"Long message results: {results}")