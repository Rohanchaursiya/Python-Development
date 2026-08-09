# Object Creation Examples

class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.created_at = __import__('datetime').datetime.now()
    
    def greet(self):
        return f"Hi, I'm {self.name}, {self.age} years old"
    
    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"


class DatabaseConnection:
    """Simulates expensive resource"""
    _connections = 0
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connected = False
        DatabaseConnection._connections += 1
        self.id = DatabaseConnection._connections
    
    def connect(self):
        if not self.connected:
            print(f"Connecting to {self.host}:{self.port}...")
            self.connected = True
        return self
    
    def query(self, sql):
        if not self.connected:
            raise RuntimeError("Not connected")
        return f"Result for: {sql}"
    
    def close(self):
        if self.connected:
            print(f"Closing connection {self.id}")
            self.connected = False
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, *args):
        self.close()


class ProductFactory:
    """Factory pattern for object creation"""
    
    @staticmethod
    def create_product(product_type, **kwargs):
        if product_type == "book":
            return Book(**kwargs)
        elif product_type == "electronics":
            return Electronics(**kwargs)
        elif product_type == "clothing":
            return Clothing(**kwargs)
        else:
            raise ValueError(f"Unknown product type: {product_type}")


class Product:
    def __init__(self, name, price, sku):
        self.name = name
        self.price = price
        self.sku = sku
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.name}, ${self.price})"


class Book(Product):
    def __init__(self, name, price, sku, author, isbn):
        super().__init__(name, price, sku)
        self.author = author
        self.isbn = isbn


class Electronics(Product):
    def __init__(self, name, price, sku, brand, warranty_months):
        super().__init__(name, price, sku)
        self.brand = brand
        self.warranty_months = warranty_months


class Clothing(Product):
    def __init__(self, name, price, sku, size, color):
        super().__init__(name, price, sku)
        self.size = size
        self.color = color


# Prototype pattern (cloning)
import copy

class Prototype:
    def __init__(self):
        self.objects = {}
    
    def register(self, name, obj):
        self.objects[name] = obj
    
    def unregister(self, name):
        del self.objects[name]
    
    def clone(self, name, **attrs):
        obj = copy.deepcopy(self.objects[name])
        for key, value in attrs.items():
            setattr(obj, key, value)
        return obj


if __name__ == "__main__":
    print("=== Basic Instantiation ===")
    p1 = Person("Alice", 30)
    p2 = Person("Bob", 25)
    print(p1)
    print(p2)
    print(f"Different objects: {p1 is not p2}")
    print(f"Different IDs: {id(p1) != id(p2)}")
    print()
    
    print("=== Dynamic Attributes ===")
    p1.email = "alice@example.com"
    p1.phone = "555-1234"
    print(f"p1 email: {p1.email}")
    print(f"p2 has email: {hasattr(p2, 'email')}")
    print()
    
    print("=== Resource Management ===")
    db = DatabaseConnection("localhost", 5432)
    db.connect()
    print(db.query("SELECT * FROM users"))
    db.close()
    print()
    
    print("=== Context Manager (Preferred) ===")
    with DatabaseConnection("db.server", 3306) as conn:
        print(conn.query("SELECT * FROM products"))
    print("Connection auto-closed")
    print()
    
    print("=== Factory Pattern ===")
    book = ProductFactory.create_product("book", 
        name="Python Guide", price=29.99, sku="B001",
        author="John Doe", isbn="978-1234567890")
    laptop = ProductFactory.create_product("electronics",
        name="Laptop", price=999.99, sku="E001",
        brand="TechBrand", warranty_months=24)
    shirt = ProductFactory.create_product("clothing",
        name="T-Shirt", price=19.99, sku="C001",
        size="L", color="Blue")
    
    print(book)
    print(laptop)
    print(shirt)
    print()
    
    print("=== Prototype Pattern ===")
    proto = Prototype()
    
    # Register prototype
    base_book = Book("Template", 0, "TEMPLATE", "Author", "0000000000")
    proto.register("book", base_book)
    
    # Clone and customize
    book1 = proto.clone("book", name="Python 101", price=25.00, sku="B002", author="Jane Smith", isbn="1111111111")
    book2 = proto.clone("book", name="Advanced Python", price=35.00, sku="B003", author="Bob Wilson", isbn="2222222222")
    
    print(book1)
    print(book2)
    print(f"Same object? {book1 is book2}")