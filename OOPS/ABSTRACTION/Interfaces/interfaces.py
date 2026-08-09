# Interfaces (Protocols) Example

from typing import Protocol, runtime_checkable
from abc import ABC, abstractmethod
import json


# Protocol-based interfaces (Python 3.8+)
@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> None: ...
    def area(self) -> float: ...


@runtime_checkable
class Serializable(Protocol):
    def to_json(self) -> str: ...
    def from_json(self, data: str) -> None: ...


@runtime_checkable
class Comparable(Protocol):
    def __lt__(self, other: 'Comparable') -> bool: ...
    def __eq__(self, other: object) -> bool: ...


# Implementations - no inheritance required!
class Circle:
    def __init__(self, radius: float):
        self.radius = radius
    
    def draw(self) -> None:
        print(f"  🔵 Drawing circle with radius {self.radius}")
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def to_json(self) -> str:
        return json.dumps({"type": "circle", "radius": self.radius})
    
    def from_json(self, data: str) -> None:
        d = json.loads(data)
        self.radius = d["radius"]
    
    def __lt__(self, other: 'Circle') -> bool:
        return self.area() < other.area()
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Circle) and self.radius == other.radius


class Rectangle:
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    def draw(self) -> None:
        print(f"  🟦 Drawing rectangle {self.width}x{self.height}")
    
    def area(self) -> float:
        return self.width * self.height
    
    def to_json(self) -> str:
        return json.dumps({"type": "rectangle", "width": self.width, "height": self.height})
    
    def from_json(self, data: str) -> None:
        d = json.loads(data)
        self.width = d["width"]
        self.height = d["height"]
    
    def __lt__(self, other: 'Rectangle') -> bool:
        return self.area() < other.area()
    
    def __eq__(self, other: object) -> bool:
        return isinstance(other, Rectangle) and self.width == other.width and self.height == other.height


# Third-party class (can't modify) that accidentally implements Drawable
class LegacyShape:
    def __init__(self, size):
        self.size = size
    
    def draw(self):
        print(f"  Legacy draw: {self.size}")
    
    def area(self):
        return self.size * self.size


# Functions using protocols
def render_shape(shape: Drawable) -> None:
    """Accepts any object with draw() and area()"""
    shape.draw()
    print(f"  Area: {shape.area():.2f}")


def save_shape(shape: Serializable) -> None:
    """Accepts any serializable object"""
    print(f"  Saving: {shape.to_json()}")


def find_largest(shapes: list[Comparable]) -> Comparable:
    """Works with any comparable objects"""
    return max(shapes)


# Protocol composition
class Storage(Protocol):
    def read(self) -> bytes: ...
    def write(self, data: bytes) -> None: ...


class Encrypted(Protocol):
    def encrypt(self, data: bytes) -> bytes: ...
    def decrypt(self, data: bytes) -> bytes: ...


@runtime_checkable
class SecureStorage(Storage, Encrypted, Protocol):
    """Combined protocol - must implement both"""
    pass


class FileStorage:
    def __init__(self, path: str):
        self.path = path
    
    def read(self) -> bytes:
        try:
            with open(self.path, 'rb') as f:
                return f.read()
        except FileNotFoundError:
            return b""
    
    def write(self, data: bytes) -> None:
        with open(self.path, 'wb') as f:
            f.write(data)
    
    def encrypt(self, data: bytes) -> bytes:
        # Simple XOR encryption (for demo)
        key = b"secret"
        return bytes(a ^ b for a, b in zip(data, key * (len(data)//len(key) + 1)))
    
    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)  # XOR is symmetric


def store_data(storage: Storage, data: str) -> None:
    storage.write(data.encode())


def secure_store(storage: Encrypted, data: str) -> None:
    encrypted = storage.encrypt(data.encode())
    print(f"  Stored encrypted: {encrypted.hex()[:32]}...")


# Demonstration
if __name__ == "__main__":
    print("=== Protocol Implementation ===")
    shapes = [Circle(5), Rectangle(4, 6), Circle(3)]
    
    print("\n--- Rendering ---")
    for shape in shapes:
        render_shape(shape)
    
    print("\n--- Serialization ---")
    for shape in shapes:
        save_shape(shape)
    
    print("\n--- Comparison ---")
    largest = find_largest(shapes)
    print(f"Largest: {type(largest).__name__} with area {largest.area():.2f}")
    
    print("\n--- Protocol Checking ---")
    circle = Circle(5)
    rect = Rectangle(4, 6)
    legacy = LegacyShape(10)
    
    print(f"Circle is Drawable: {isinstance(circle, Drawable)}")
    print(f"Rectangle is Drawable: {isinstance(rect, Drawable)}")
    print(f"LegacyShape is Drawable: {isinstance(legacy, Drawable)}")  # True!
    
    print("\n--- Third-party compatibility ---")
    render_shape(legacy)  # Works without inheritance!
    
    print("\n--- Protocol Composition ---")
    fs = FileStorage("test.dat")
    store_data(fs, "Hello World")
    secure_store(fs, "Secret Data")
    
    print("\n--- Runtime checkable ---")
    print(f"FileStorage is SecureStorage: {isinstance(fs, SecureStorage)}")