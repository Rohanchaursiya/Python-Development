# Runtime Polymorphism - Operator Polymorphism (Overloading)

import math
from typing import Union


class Vector:
    """2D Vector with operator overloading"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    # Arithmetic operators
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
    
    # Comparison operators
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector):
            return NotImplemented
        return math.isclose(self.x, other.x) and math.isclose(self.y, other.y)
    
    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)
    
    # Container-like operators
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
    
    # Iteration
    def __iter__(self):
        yield self.x
        yield self.y
    
    # String representation
    def __str__(self) -> str:
        return f"({self.x:.2f}, {self.y:.2f})"
    
    def __repr__(self) -> str:
        return f"Vector({self.x}, {self.y})"
    
    # Boolean context
    def __bool__(self) -> bool:
        return not (math.isclose(self.x, 0) and math.isclose(self.y, 0))
    
    # Hash (for use in sets/dicts)
    def __hash__(self) -> int:
        return hash((self.x, self.y))
    
    # Callable
    def __call__(self, scalar: float = 1.0) -> 'Vector':
        return Vector(self.x * scalar, self.y * scalar)
    
    # Math helpers
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
        dot = self.dot(other)
        return math.acos(dot / (self.magnitude() * other.magnitude()))


class Matrix:
    """Simple 2x2 Matrix with operator overloading"""
    
    def __init__(self, a: float, b: float, c: float, d: float):
        self.data = [[a, b], [c, d]]
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        if not isinstance(other, Matrix):
            return NotImplemented
        return Matrix(
            self.data[0][0] + other.data[0][0],
            self.data[0][1] + other.data[0][1],
            self.data[1][0] + other.data[1][0],
            self.data[1][1] + other.data[1][1]
        )
    
    def __mul__(self, other: Union['Matrix', Vector, float]) -> Union['Matrix', Vector]:
        if isinstance(other, Matrix):
            # Matrix multiplication
            a = self.data[0][0] * other.data[0][0] + self.data[0][1] * other.data[1][0]
            b = self.data[0][0] * other.data[0][1] + self.data[0][1] * other.data[1][1]
            c = self.data[1][0] * other.data[0][0] + self.data[1][1] * other.data[1][0]
            d = self.data[1][0] * other.data[0][1] + self.data[1][1] * other.data[1][1]
            return Matrix(a, b, c, d)
        elif isinstance(other, Vector):
            # Matrix-Vector multiplication
            x = self.data[0][0] * other.x + self.data[0][1] * other.y
            y = self.data[1][0] * other.x + self.data[1][1] * other.y
            return Vector(x, y)
        elif isinstance(other, (int, float)):
            # Scalar multiplication
            return Matrix(
                self.data[0][0] * other, self.data[0][1] * other,
                self.data[1][0] * other, self.data[1][1] * other
            )
        return NotImplemented
    
    def __repr__(self) -> str:
        return f"Matrix({self.data[0][0]}, {self.data[0][1]}, {self.data[1][0]}, {self.data[1][1]})"


class Polynomial:
    """Polynomial with operator overloading"""
    
    def __init__(self, *coefficients):
        # coefficients from highest degree to constant
        self.coeffs = list(coefficients) if coefficients else [0]
    
    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        if not isinstance(other, Polynomial):
            return NotImplemented
        max_len = max(len(self.coeffs), len(other.coeffs))
        result = [0] * max_len
        for i, c in enumerate(reversed(self.coeffs)):
            result[-(i+1)] += c
        for i, c in enumerate(reversed(other.coeffs)):
            result[-(i+1)] += c
        return Polynomial(*result)
    
    def __mul__(self, other: 'Polynomial') -> 'Polynomial':
        if not isinstance(other, Polynomial):
            return NotImplemented
        result = [0] * (len(self.coeffs) + len(other.coeffs) - 1)
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
    
    def __repr__(self) -> str:
        terms = []
        for i, c in enumerate(reversed(self.coeffs)):
            if c != 0:
                power = len(self.coeffs) - i - 1
                if power == 0:
                    terms.append(str(c))
                elif power == 1:
                    terms.append(f"{c}x" if c != 1 else "x")
                else:
                    terms.append(f"{c}x^{power}" if c != 1 else f"x^{power}")
        return " + ".join(terms) if terms else "0"


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
    print(f"abs(v1) = {abs(v1):.2f}")
    print(f"v1 == v2: {v1 == v2}")
    print(f"v1 != v2: {v1 != v2}")
    print(f"len(v1) = {len(v1)}")
    print(f"v1[0] = {v1[0]}, v1[1] = {v1[1]}")
    print(f"5 in v1: {5 in v1}")
    print(f"3 in v1: {3 in v1}")
    print(f"bool(v1): {bool(v1)}")
    print(f"bool(Vector(0,0)): {bool(Vector(0,0))}")
    print(f"v1(2) = {v1(2)}")  # Callable
    print(f"v1.dot(v2) = {v1.dot(v2)}")
    print(f"v1.normalize() = {v1.normalize()}")
    print()
    
    print("=== Matrix Operations ===")
    m1 = Matrix(1, 2, 3, 4)
    m2 = Matrix(2, 0, 1, 2)
    v = Vector(1, 1)
    
    print(f"m1 = {m1}")
    print(f"m2 = {m2}")
    print(f"m1 + m2 = {m1 + m2}")
    print(f"m1 * m2 = {m1 * m2}")
    print(f"m1 * v = {m1 * v}")
    print(f"m1 * 2 = {m1 * 2}")
    print()
    
    print("=== Polynomial Operations ===")
    p1 = Polynomial(1, 0, -2)  # x^2 - 2
    p2 = Polynomial(1, 3)       # x + 3
    
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    print(f"p1 + p2 = {p1 + p2}")
    print(f"p1 * p2 = {p1 * p2}")
    print(f"p1(2) = {p1(2)}")
    print(f"p2(-3) = {p2(-3)}")