# Constructors and Destructors

## Definition
`__init__` initializes a new instance after creation. `__new__` creates the instance itself (rarely overridden). `__del__` is called when object is garbage collected (not guaranteed).

## Pros
- **`__init__`**: Setup instance state, validation
- **`__new__`**: Control instance creation (singletons, immutables)
- **`__del__`**: Cleanup resources (files, connections)

## Cons
- **`__del__`**: Unpredictable timing, reference cycles
- **`__new__`**: Complex, easy to break inheritance
- **Exceptions**: In `__init__` leaves partial object

## Use Cases
- **`__init__`**: Standard initialization
- **`__new__`**: Immutable types, singletons, object pooling
- **`__del__`**: Logging, explicit resource release (with context managers preferred)

## Image
![Constructors Diagram](constructors.svg)

## Syntax
```python
class Resource:
    def __init__(self, name):
        print(f"Initializing {name}")
        self.name = name
        self.handle = open(f"{name}.tmp", "w")
    
    def __del__(self):
        print(f"Cleaning up {self.name}")
        if hasattr(self, 'handle'):
            self.handle.close()

class Singleton:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, value):
        if not hasattr(self, 'initialized'):
            self.value = value
            self.initialized = True

class ImmutablePoint:
    def __new__(cls, x, y):
        instance = super().__new__(cls)
        instance._x = x
        instance._y = y
        return instance
    
    @property
    def x(self): return self._x
    @property
    def y(self): return self._y

# Usage
r = Resource("test")
del r  # Explicit cleanup

s1 = Singleton("first")
s2 = Singleton("second")
print(s1 is s2)  # True
print(s1.value)  # "first" (not overwritten)

p = ImmutablePoint(3, 4)
# p.x = 5  # AttributeError: can't set attribute

# Context manager preferred over __del__
class ManagedResource:
    def __enter__(self):
        self.handle = open("data.txt", "w")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.handle.close()
    
    def write(self, data):
        self.handle.write(data)

with ManagedResource() as mr:
    mr.write("Hello")
# Automatically closed
```