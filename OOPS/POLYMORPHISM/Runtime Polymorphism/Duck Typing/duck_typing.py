# Runtime Polymorphism - Duck Typing

class Duck:
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        return f"{self.name} says: Quack! 🦆"
    
    def fly(self):
        return f"{self.name} flies with wings: Flap flap flap!"
    
    def swim(self):
        return f"{self.name} paddles in water"


class Person:
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        return f"{self.name} imitates: QUACK QUACK! 🎭"
    
    def fly(self):
        return f"{self.name} flaps arms: I'm flying! 💪"
    
    def code(self):
        return f"{self.name} writes Python code 🐍"


class Robot:
    def __init__(self, model):
        self.model = model
    
    def quack(self):
        return f"{self.model} synthesizes: QUACK.QUACK.QUACK 🤖"
    
    def calculate(self):
        return f"{self.model} computes: 42 * 42 = 1764"


class RubberDuck:
    def __init__(self, color):
        self.color = color
    
    def quack(self):
        return f"{self.color} rubber duck: Squeak! 🦆"
    
    def float_(self):
        return f"{self.color} rubber duck floats happily"


class Drone:
    def __init__(self, id):
        self.id = id
    
    def fly(self):
        return f"Drone {self.id} hovering with rotors 🚁"
    
    def scan(self):
        return f"Drone {self.id} scanning area..."


def duck_test(creature):
    """Classic duck test - if it quacks like a duck..."""
    print(f"\n--- Testing {creature.__class__.__name__} ---")
    if hasattr(creature, 'quack'):
        print(f"quack(): {creature.quack()}")
    else:
        print("quack(): This creature cannot quack")
    
    # Check for fly method (duck typing with hasattr)
    if hasattr(creature, 'fly'):
        print(f"fly(): {creature.fly()}")
    else:
        print("fly(): This creature cannot fly")
    
    # Check for other methods
    for method in ['swim', 'code', 'calculate', 'float_', 'scan']:
        if hasattr(creature, method):
            print(f"{method}(): {getattr(creature, method)()}")


def make_it_quack(quackable):
    """Function accepting any object with quack() method"""
    if hasattr(quackable, 'quack'):
        print(f"Sound: {quackable.quack()}")
    else:
        print(f"{quackable.__class__.__name__} cannot quack")


def make_it_fly(flyable):
    """Function accepting any object with fly() method"""
    if hasattr(flyable, 'fly'):
        print(f"Flight: {flyable.fly()}")
    else:
        print(f"{flyable.__class__.__name__} cannot fly")


# Protocol for static type checking (Python 3.8+)
from typing import Protocol

class Quackable(Protocol):
    def quack(self) -> str: ...

class Flyable(Protocol):
    def fly(self) -> str: ...

class DuckLike(Quackable, Flyable, Protocol):
    """Combined protocol for duck-like objects"""
    pass


if __name__ == "__main__":
    print("=== Duck Typing Demo ===")
    
    creatures = [
        Duck("Donald"),
        Person("Alice"),
        Robot("R2-D2"),
        RubberDuck("Yellow"),
        Drone("DJI-001")
    ]
    
    for creature in creatures:
        duck_test(creature)
    
    print("\n=== Protocol-Based Functions ===")
    for creature in creatures:
        make_it_quack(creature)
        make_it_fly(creature)
    
    print("\n=== List Processing (Polymorphic) ===")
    # Works with any iterable of quackable objects
    quackers = [Duck("D1"), Person("Bob"), Robot("C3PO")]
    for q in quackers:
        print(q.quack())