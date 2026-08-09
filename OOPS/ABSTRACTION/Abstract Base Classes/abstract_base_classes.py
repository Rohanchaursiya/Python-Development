# Abstract Base Classes Example

from abc import ABC, abstractmethod
import hashlib


class Shape(ABC):
    """Abstract base class for shapes"""
    
    @abstractmethod
    def area(self) -> float:
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    # Concrete method using abstract ones
    def describe(self) -> str:
        return f"{self.name}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius
    
    @property
    def name(self) -> str:
        return "Circle"
    
    def area(self) -> float:
        return 3.14159 * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * 3.14159 * self.radius


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width = width
        self.height = height
    
    @property
    def name(self) -> str:
        return "Rectangle"
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Triangle(Shape):
    def __init__(self, a: float, b: float, c: float):
        self.a, self.b, self.c = a, b, c
    
    @property
    def name(self) -> str:
        return "Triangle"
    
    def area(self) -> float:
        s = (self.a + self.b + self.c) / 2
        return (s * (s - self.a) * (s - self.b) * (s - self.c)) ** 0.5
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c


# Abstract class with template method
class DataProcessor(ABC):
    def __init__(self, source: str):
        self.source = source
        self.data = None
    
    @abstractmethod
    def load(self) -> None:
        pass
    
    @abstractmethod
    def transform(self) -> None:
        pass
    
    @abstractmethod
    def save(self, destination: str) -> None:
        pass
    
    # Template method - defines algorithm skeleton
    def process(self, destination: str) -> None:
        print(f"Processing {self.source} → {destination}")
        self.load()
        print("  Loaded")
        self.transform()
        print("  Transformed")
        self.save(destination)
        print("  Saved")


class CSVProcessor(DataProcessor):
    def load(self):
        self.data = f"CSV data from {self.source}"
    
    def transform(self):
        self.data = self.data.upper()
    
    def save(self, destination: str):
        print(f"  Saving CSV to {destination}: {self.data}")


class JSONProcessor(DataProcessor):
    def load(self):
        self.data = {"source": self.source, "format": "json"}
    
    def transform(self):
        self.data["processed"] = True
        self.data["format"] = "JSON"
    
    def save(self, destination: str):
        print(f"  Saving JSON to {destination}: {self.data}")


# Plugin system with ABC
class Plugin(ABC):
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def execute(self, data: any) -> any:
        pass
    
    def initialize(self):
        print(f"Initializing {self.name()}")
    
    def cleanup(self):
        print(f"Cleaning up {self.name()}")


class UppercasePlugin(Plugin):
    def name(self) -> str:
        return "Uppercase"
    
    def execute(self, data: str) -> str:
        return data.upper()


class ReversePlugin(Plugin):
    def name(self) -> str:
        return "Reverse"
    
    def execute(self, data: str) -> str:
        return data[::-1]


class HashPlugin(Plugin):
    def name(self) -> str:
        return "Hash"
    
    def execute(self, data: str) -> str:
        return hashlib.md5(data.encode()).hexdigest()


class PluginManager:
    def __init__(self):
        self.plugins: list[Plugin] = []
    
    def register(self, plugin: Plugin):
        plugin.initialize()
        self.plugins.append(plugin)
    
    def process_all(self, data: str) -> dict:
        results = {}
        for plugin in self.plugins:
            results[plugin.name()] = plugin.execute(data)
        return results
    
    def shutdown(self):
        for plugin in self.plugins:
            plugin.cleanup()


# Demonstration
if __name__ == "__main__":
    print("=== Shape Hierarchy ===")
    shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 4, 5)]
    for shape in shapes:
        print(shape.describe())
    
    # shape = Shape()  # TypeError: Can't instantiate abstract class
    
    print("\n=== Template Method Pattern ===")
    csv_proc = CSVProcessor("data.csv")
    csv_proc.process("output.csv")
    
    json_proc = JSONProcessor("data.json")
    json_proc.process("output.json")
    
    print("\n=== Plugin System ===")
    manager = PluginManager()
    manager.register(UppercasePlugin())
    manager.register(ReversePlugin())
    manager.register(HashPlugin())
    
    result = manager.process_all("Hello World")
    for name, value in result.items():
        print(f"  {name}: {value}")
    
    manager.shutdown()