# Properties and Descriptors

## Definition
`@property` decorator creates managed attributes with getter/setter/deleter. Descriptors (`__get__`, `__set__`, `__delete__`) provide reusable attribute access logic across classes.

## Pros
- **Properties**: Validation, computed attrs, read-only, backward compat
- **Descriptors**: Reusable logic, DRY, framework building
- **Encapsulation**: Control access without changing API
- **Lazy Evaluation**: Compute on first access

## Cons
- **Performance**: Method call overhead per access
- **Complexity**: Descriptors are advanced
- **Debugging**: Harder to trace attribute access
- **Inheritance**: Descriptor behavior can surprise

## Use Cases
- **Properties**: Validation, computed fields, caching
- **Descriptors**: ORM fields, type checking, lazy loading, caching

## Image
![Properties Diagram](properties.svg)

## Syntax
```python
class Person:
    def __init__(self, name, age):
        self._name = name
        self._age = age
        self._cache = {}
    
    # Property with getter/setter
    @property
    def name(self):
        return self._name.title()
    
    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip()
    
    @name.deleter
    def name(self):
        print("Deleting name")
        self._name = ""
    
    # Read-only computed property
    @property
    def age(self):
        return self._age
    
    @property
    def is_adult(self):
        return self._age >= 18
    
    # Cached property pattern
    @property
    def expensive_computation(self):
        if 'result' not in self._cache:
            print("Computing...")
            self._cache['result'] = sum(i**2 for i in range(10000))
        return self._cache['result']

# Descriptor for reusable validation
class Validated:
    def __init__(self, validator, default=None):
        self.validator = validator
        self.default = default
        self.name = None
    
    def __set_name__(self, owner, name):
        self.name = name
    
    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.name, self.default)
    
    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"Invalid value for {self.name}: {value}")
        obj.__dict__[self.name] = value

class Product:
    # Reusable descriptors
    price = Validated(lambda v: isinstance(v, (int, float)) and v >= 0)
    quantity = Validated(lambda v: isinstance(v, int) and v >= 0)
    name = Validated(lambda v: isinstance(v, str) and len(v) > 0)
    
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

# Usage
p = Person("alice", 25)
print(p.name)       # Alice
p.name = "BOB"      # Bob (validated & title-cased)
print(p.is_adult)   # True
# p.age = 30       # AttributeError: no setter

print(p.expensive_computation)  # Computes first time
print(p.expensive_computation)  # Cached

prod = Product("Widget", 19.99, 100)
# prod.price = -5  # ValueError
# prod.name = ""   # ValueError