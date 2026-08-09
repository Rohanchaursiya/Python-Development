# Magic Methods (Dunder Methods) Examples

import math
from typing import Union


class Vector:
    """2D Vector with comprehensive operator overloading"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    # === Arithmetic Operators ===
    def __add__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector') -> 'Vector':
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: Union[int, float]) -> 'Vector':
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Vector':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[int, float]) -> 'Vector':
        if not isinstance(scalar, (int, float)) or scalar == 0:
            return NotImplemented
        return Vector(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector':
        return Vector(-self.x, -self.y)
    
    def __pos__(self) -> 'Vector':
        return Vector(+self.x, +self.y)
    
    def __abs__(self) -> float:
        return math.hypot(self.x, self.y)
    
    def __pow__(self, power: float) -> 'Vector':
        mag = abs(self) ** power
        if mag == 0:
            return Vector(0, 0)
        angle = math.atan2(self.y, self.x)
        return Vector(mag * math.cos(angle), mag * math.sin(angle))
    
    # === Comparison Operators ===
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    def __lt__(self, other: 'Vector') -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return abs(self) < abs(other)
    
    def __le__(self, other: 'Vector') -> bool:
        return self.__lt__(other) or self.__eq__(other)
    
    def __gt__(self, other: 'Vector') -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return abs(self) > abs(other)
    
    def __ge__(self, other: 'Vector') -> bool:
        return self.__gt__(other) or self.__eq__(other)
    
    # === Container Protocol ===
    def __len__(self) -> int:
        return 2
    
    def __getitem__(self, index: int) -> float:
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError("Vector index out of range (0-1)")
    
    def __setitem__(self, index: int, value: float):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Vector index out of range (0-1)")
    
    def __contains__(self, value: float) -> bool:
        return math.isclose(value, self.x) or math.isclose(value, self.y)
    
    def __iter__(self):
        yield self.x
        yield self.y
    
    def __reversed__(self):
        yield self.y
        yield self.x
    
    # === String Representation ===
    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    def __format__(self, format_spec: str) -> str:
        return f"({self.x:{format_spec}}, {self.y:{format_spec}})"
    
    # === Boolean Context ===
    def __bool__(self) -> bool:
        return not (math.isclose(self.x, 0) and math.isclose(self.y, 0))
    
    # === Hash (for dict/set) ===
    def __hash__(self) -> int:
        return hash((round(self.x, 10), round(self.y, 10)))
    
    # === Callable ===
    def __call__(self, scalar: float = 1.0) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
    
    # === Math Helpers ===
    def magnitude(self) -> float:
        return abs(self)
    
    def normalize(self) -> 'Vector':
        mag = self.magnitude()
        if mag == 0:
            return Vector(0, 0)
        return self / mag
    
    def dot(self, other: 'Vector') -> float:
        return self.x * other.x + self.y * other.y
    
    def angle(self, other: 'Vector') -> float:
        return math.acos(self.dot(other) / (self.magnitude() * other.magnitude()))


class Polynomial:
    """Polynomial with operator overloading"""
    
    def __init__(self, *coefficients):
        # coefficients from highest degree to constant
        # e.g., Polynomial(1, 0, -2) = x² - 2
        self.coeffs = list(coefficients) if coefficients else [0]
        # Remove leading zeros
        while len(self.coeffs) > 1 and self.coeffs[0] == 0:
            self.coeffs.pop(0)
    
    def degree(self) -> int:
        return len(self.coeffs) - 1
    
    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        if not isinstance(other, Polynomial):
            return NotImplemented
        max_deg = max(self.degree(), other.degree())
        result = [0] * (max_deg + 1)
        for i, c in enumerate(reversed(self.coeffs)):
            result[-(i+1)] += c
        for i, c in enumerate(reversed(other.coeffs)):
            result[-(i+1)] += c
        return Polynomial(*result)
    
    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        if not isinstance(other, Polynomial):
            return NotImplemented
        return self + Polynomial(*(-c for c in other.coeffs))
    
    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        if not isinstance(other, Polynomial):
            return NotImplemented
        result = [0] * (self.degree() + other.degree() + 1)
        for i, a in enumerate(reversed(self.coeffs)):
            for j, b in enumerate(reversed(other.coeffs)):
                result[-(i+j+1)] += a * b
        return Polynomial(*result)
    
    def __call__(self, x: float) -> float:
        """Evaluate polynomial at x"""
        result = 0
        for i, c in enumerate(reversed(self.coeffs)):
            result += c * (x ** i)
        return result
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Polynomial):
            return NotImplemented
        return self.coeffs == other.coeffs
    
    def __str__(self) -> str:
        if not self.coeffs:
            return "0"
        terms = []
        for i, c in enumerate(self.coeffs):
            if c == 0:
                continue
            power = self.degree() - i
            if power == 0:
                term = str(c)
            elif power == 1:
                term = f"{c}x" if c != 1 else "x"
            else:
                term = f"{c}x^{power}" if c != 1 else f"x^{power}"
            terms.append(term)
        return " + ".join(terms) if terms else "0"
    
    def __repr__(self) -> str:
        return f"Polynomial({', '.join(map(str, self.coeffs))})"


class SmartList:
    """List-like object with custom behavior"""
    
    def __init__(self, *items):
        self._items = list(items)
        self._access_count = 0
    
    def __len__(self):
        return len(self._items)
    
    def __getitem__(self, index):
        self._access_count += 1
        if isinstance(index, slice):
            return SmartList(*self._items[index])
        return self._items[index]
    
    def __setitem__(self, index, value):
        self._items[index] = value
    
    def __delitem__(self, index):
        del self._items[index]
    
    def __contains__(self, item):
        return item in self._items
    
    def __iter__(self):
        return iter(self._items)
    
    def __reversed__(self):
        return reversed(self._items)
    
    def __add__(self, other):
        if isinstance(other, SmartList):
            return SmartList(*(self._items + other._items))
        return NotImplemented
    
    def __mul__(self, n):
        if isinstance(n, int):
            return SmartList(*(self._items * n))
        return NotImplemented
    
    def __rmul__(self, n):
        return self.__mul__(n)
    
    def __str__(self):
        return f"SmartList({self._items})"
    
    def __repr__(self):
        return f"SmartList({', '.join(repr(x) for x in self._items)})"
    
    def __bool__(self):
        return bool(self._items)
    
    def access_count(self):
        return self._access_count
    
    def append(self, item):
        self._items.append(item)


# Demonstration
if __name__ == "__main__":
    print("=== Vector Operations ===")
    v1 = Vector(3, 4)
    v2 = Vector(1, 2)
    
    print(f"v1 = {v1}")
    print(f"v2 = {v2}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"3 * v1 = {3 * v1}")
    print(f"v1 / 2 = {v1 / 2}")
    print(f"-v1 = {-v1}")
    print(f"+v1 = {+v1}")
    print(f"abs(v1) = {abs(v1):.2f}")
    print(f"v1 ** 2 = {v1 ** 2}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 != v2: {v1 != v2}")
    print(f"v1 < v2: {v1 < v2}")
    print(f"v1 > v2: {v1 > v2}")
    print(f"len(v1) = {len(v1)}")
    print(f"v1[0] = {v1[0]}, v1[1] = {v1[1]}")
    print(f"5 in v1: {5 in v1}")
    print(f"3 in v1: {3 in v1}")
    print(f"list(v1) = {list(v1)}")
    print(f"reversed: {list(reversed(v1))}")
    print(f"format: {v1:.1f}")
    print(f"bool(v1): {bool(v1)}")
    print(f"bool(Vector(0,0)): {bool(Vector(0,0))}")
    print(f"hash(v1): {hash(v1)}")
    
    # Use in set/dict
    vectors = {Vector(1,2), Vector(3,4), Vector(1,2)}
    print(f"Set of vectors: {vectors}")
    
    vec_dict = {Vector(1,0): "x-axis", Vector(0,1): "y-axis"}
    print(f"Vector dict: {vec_dict}")
    
    print(f"v1(2) = {v1(2)}")  # Callable
    print(f"v1.dot(v2) = {v1.dot(v2)}")
    print(f"v1.normalize() = {v1.normalize()}")
    print(f"angle(v1, v2) = {math.degrees(v1.angle(v2)):.1f}°")
    print()
    
    print("=== Polynomial Operations ===")
    p1 = Polynomial(1, 0, -2)   # x² - 2
    p2 = Polynomial(1, 3)       # x + 3
    p3 = Polynomial(2, -1)      # 2x - 1
    
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p3 = {p3}")
    print(f"p1 + p2 = {p1 + p2}")
    print(f"p1 - p2 = {p1 - p2}")
    print(f"p1 * p2 = {p1 * p2}")
    print(f"p2 * p3 = {p2 * p3}")
    print(f"p1(2) = {p1(2)}")
    print(f"p2(-3) = {p2(-3)}")
    print(f"p3(0.5) = {p3(0.5)}")
    print()
    
    print("=== SmartList ===")
    sl = SmartList(1, 2, 3, 4, 5)
    print(f"sl = {sl}")
    print(f"len(sl) = {len(sl)}")
    print(f"sl[1] = {sl[1]}")
    print(f"sl[1:4] = {sl[1:4]}")
    print(f"3 in sl = {3 in sl}")
    print(f"sl + SmartList(6,7) = {sl + SmartList(6,7)}")
    print(f"sl * 2 = {sl * 2}")
    print(f"bool(sl) = {bool(sl)}")
    print(f"Access count: {sl.access_count()}")
    for x in sl:
        print(f"  Iter: {x}")
    print(f"Access count after iteration: {sl.access_count()}")