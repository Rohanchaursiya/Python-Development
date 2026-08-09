# Magic Methods (Dunder Methods)

## Definition
Special methods with double underscores (`__method__`) that Python calls automatically for built-in operations. Enable operator overloading, container behavior, iteration, and more.

## Pros
- **Pythonic**: Natural syntax (`+`, `len()`, `[]`, `with`)
- **Integration**: Works with built-in functions
- **Polymorphism**: Consistent interface across types
- **Flexibility**: Customize almost any behavior

## Cons
- **Complexity**: Many methods to remember
- **Performance**: Method call overhead
- **Misuse**: Can create confusing APIs
- **Inheritance**: Must implement correctly

## Use Cases
- **Arithmetic**: `+`, `-`, `*`, `/` for math objects
- **Comparison**: `==`, `<`, `>` for sorting
- **Container**: `len()`, `[]`, `in` for collections
- **String**: `str()`, `repr()` for display
- **Context**: `with` statement support
- **Callable**: Objects that act like functions

## Image
![Magic Methods Diagram](magic_methods.svg)

## Syntax
```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y
    
    # Arithmetic
    def __add__(self, other): return Vector(self.x+other.x, self.y+other.y)
    def __sub__(self, other): return Vector(self.x-other.x, self.y-other.y)
    def __mul__(self, scalar): return Vector(self.x*scalar, self.y*scalar)
    def __rmul__(self, scalar): return self.__mul__(scalar)
    def __neg__(self): return Vector(-self.x, -self.y)
    
    # Comparison
    def __eq__(self, other): return self.x==other.x and self.y==other.y
    def __lt__(self, other): return (self.x**2+self.y**2) < (other.x**2+other.y**2)
    
    # Container
    def __len__(self): return 2
    def __getitem__(self, i): return (self.x, self.y)[i]
    def __iter__(self): yield self.x; yield self.y
    
    # String
    def __str__(self): return f"({self.x}, {self.y})"
    def __repr__(self): return f"Vector({self.x}, {self.y})"
    
    # Boolean
    def __bool__(self): return self.x != 0 or self.y != 0
    
    # Hash (for dict/set)
    def __hash__(self): return hash((self.x, self.y))
    
    # Callable
    def __call__(self, scale): return Vector(self.x*scale, self.y*scale)
    
    # Context Manager
    def __enter__(self): print("Entering vector context"); return self
    def __exit__(self, *args): print("Exiting vector context")

# Usage
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(v1 + v2)        # (4, 6)
print(v1 * 3)         # (9, 12)
print(-v1)            # (-3, -4)
print(v1 == v2)       # False
print(v1 < v2)        # False
print(len(v1))        # 2
print(v1[0], v1[1])   # 3 4
print(list(v1))       # [3, 4]
print(str(v1))        # (3, 4)
print(repr(v1))       # Vector(3, 4)
print(bool(v1))       # True

# Hashable - can use in set/dict
points = {Vector(1,2), Vector(3,4)}

# Callable
v3 = v1(2)  # Vector(6, 8)

# Context manager
with v1:
    pass