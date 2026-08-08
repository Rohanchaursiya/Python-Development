# Hierarchical Inheritance Example

from abc import ABC, abstractmethod
import math


class Shape(ABC):
    def __init__(self, color):
        self.color = color
    
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    def get_color(self):
        return self.color
    
    def __str__(self):
        return f"{self.__class__.__name__} (Color: {self.color})"


class Circle(Shape):
    def __init__(self, color, radius):
        super().__init__(color)
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius
    
    def get_diameter(self):
        return 2 * self.radius


class Rectangle(Shape):
    def __init__(self, color, width, height):
        super().__init__(color)
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def is_square(self):
        return self.width == self.height


class Triangle(Shape):
    def __init__(self, color, side_a, side_b, side_c):
        super().__init__(color)
        self.side_a = side_a
        self.side_b = side_b
        self.side_c = side_c
    
    def area(self):
        s = (self.side_a + self.side_b + self.side_c) / 2
        return math.sqrt(s * (s - self.side_a) * (s - self.side_b) * (s - self.side_c))
    
    def perimeter(self):
        return self.side_a + self.side_b + self.side_c
    
    def is_equilateral(self):
        return self.side_a == self.side_b == self.side_c


class Square(Rectangle):
    def __init__(self, color, side):
        super().__init__(color, side, side)
        self.side = side
    
    def get_diagonal(self):
        return self.side * math.sqrt(2)


if __name__ == "__main__":
    shapes = [
        Circle("Red", 5),
        Rectangle("Blue", 4, 6),
        Triangle("Green", 3, 4, 5),
        Square("Yellow", 5)
    ]
    
    for shape in shapes:
        print(shape)
        print(f"  Area: {shape.area():.2f}")
        print(f"  Perimeter: {shape.perimeter():.2f}")
        print()
    
    square = Square("Purple", 10)
    print(f"Square diagonal: {square.get_diagonal():.2f}")
    print(f"Is square: {square.is_square()}")