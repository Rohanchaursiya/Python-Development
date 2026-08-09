# Constructors and Destructors

class ResourceManager:
    """Demonstrates __init__, __del__, and context manager"""
    
    def __init__(self, name):
        self.name = name
        self.resource = None
        print(f"[{self.name}] __init__ called")
    
    def acquire(self):
        if self.resource is None:
            self.resource = f"Resource for {self.name}"
            print(f"[{self.name}] Acquired: {self.resource}")
        return self.resource
    
    def release(self):
        if self.resource:
            print(f"[{self.name}] Releasing: {self.resource}")
            self.resource = None
    
    def __del__(self):
        print(f"[{self.name}] __del__ called (GC)")
        self.release()
    
    # Context manager protocol
    def __enter__(self):
        print(f"[{self.name}] __enter__")
        return self.acquire()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"[{self.name}] __exit__")
        self.release()
        return False


class Singleton:
    """Singleton pattern using __new__"""
    
    _instance = None
    _initialized = False
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            print("Singleton: Creating new instance via __new__")
            cls._instance = super().__new__(cls)
        else:
            print("Singleton: Returning existing instance")
        return cls._instance
    
    def __init__(self, value="default"):
        if not self._initialized:
            print(f"Singleton: Initializing with {value}")
            self.value = value
            self._initialized = True
        else:
            print(f"Singleton: Ignoring init with {value} (already initialized)")


class ImmutablePoint:
    """Immutable object using __new__"""
    
    def __new__(cls, x, y):
        instance = super().__new__(cls)
        # Set attributes directly to bypass __setattr__
        object.__setattr__(instance, '_x', x)
        object.__setattr__(instance, '_y', y)
        return instance
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y
    
    def __setattr__(self, name, value):
        raise AttributeError(f"'{self.__class__.__name__}' is immutable")
    
    def __repr__(self):
        return f"ImmutablePoint({self._x}, {self._y})"


class DatabaseConnection:
    """Real-world example with proper resource management"""
    
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database
        self.connection = None
        self.cursor = None
        self.connected = False
    
    def connect(self):
        if not self.connected:
            # Simulate connection
            self.connection = f"Connection({self.host}:{self.port}/{self.database})"
            self.cursor = f"Cursor({id(self)})"
            self.connected = True
            print(f"Connected to {self.database}")
        return self
    
    def execute(self, query):
        if not self.connected:
            raise RuntimeError("Not connected")
        print(f"Executing: {query}")
        return f"Result for: {query}"
    
    def close(self):
        if self.connected:
            print(f"Closing connection to {self.database}")
            self.connection = None
            self.cursor = None
            self.connected = False
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        if exc_type:
            print(f"Exception occurred: {exc_val}")
        return False
    
    def __del__(self):
        # Fallback cleanup
        if self.connected:
            print(f"__del__: Cleaning up connection to {self.database}")
            self.close()


class ObjectPool:
    """Object pool using __new__ for reuse"""
    
    _pool = []
    _max_size = 3
    
    def __new__(cls):
        if cls._pool:
            print("ObjectPool: Reusing pooled object")
            return cls._pool.pop()
        print("ObjectPool: Creating new object")
        return super().__new__(cls)
    
    def __init__(self):
        self.data = None
        self.in_use = True
    
    def release(self):
        if self.in_use:
            self.in_use = False
            self.data = None
            if len(ObjectPool._pool) < ObjectPool._max_size:
                ObjectPool._pool.append(self)
                print("ObjectPool: Returned to pool")
            else:
                print("ObjectPool: Pool full, object discarded")


# Demonstration
if __name__ == "__main__":
    print("=== Basic __init__ and __del__ ===")
    rm = ResourceManager("test")
    rm.acquire()
    del rm
    import gc
    gc.collect()
    print()
    
    print("=== Context Manager (Preferred) ===")
    with ResourceManager("ctx_test") as res:
        print(f"Using: {res}")
    print("Automatically cleaned up")
    print()
    
    print("=== Singleton Pattern ===")
    s1 = Singleton("first")
    s2 = Singleton("second")
    s3 = Singleton("third")
    
    print(f"s1 is s2: {s1 is s2}")
    print(f"s1.value: {s1.value}")
    print(f"s2.value: {s2.value}")
    print()
    
    print("=== Immutable Object ===")
    p = ImmutablePoint(3, 4)
    print(p)
    print(f"p.x = {p.x}, p.y = {p.y}")
    try:
        p.x = 10
    except AttributeError as e:
        print(f"Error: {e}")
    print()
    
    print("=== Database Connection ===")
    db = DatabaseConnection("localhost", 5432, "myapp")
    db.connect()
    print(db.execute("SELECT * FROM users"))
    db.close()
    print()
    
    print("=== Context Manager for DB ===")
    with DatabaseConnection("db.server", 3306, "production") as conn:
        print(conn.execute("INSERT INTO logs VALUES ('test')"))
    print()
    
    print("=== Object Pool ===")
    obj1 = ObjectPool()
    obj1.data = "first use"
    print(f"obj1.data: {obj1.data}")
    obj1.release()
    
    obj2 = ObjectPool()  # Should reuse obj1
    print(f"obj2 is obj1: {obj2 is obj1}")
    print(f"obj2.data: {obj2.data}")  # Should be None (reset)
    
    obj2.data = "second use"
    obj2.release()
    
    obj3 = ObjectPool()
    obj4 = ObjectPool()
    obj5 = ObjectPool()
    print(f"Pool size after 5 creates: {len(ObjectPool._pool)}")