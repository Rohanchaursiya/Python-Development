# Private Attributes (Name Mangling) Example

class BaseClass:
    def __init__(self):
        self.public = "public"
        self._protected = "protected"
        self.__private = "base private"
    
    def public_method(self):
        return f"Base: {self.__private_method()}"
    
    def _protected_method(self):
        return "Base protected method"
    
    def __private_method(self):
        return "Base private method"
    
    def show_all(self):
        return {
            "public": self.public,
            "_protected": self._protected,
            "__private (mangled)": self._BaseClass__private,
            "__private_method()": self.__private_method()
        }


class SubClass(BaseClass):
    def __init__(self):
        super().__init__()
        self.__private = "sub private"  # Creates _SubClass__private
        self._protected = "sub protected"  # Overrides parent's
    
    def __private_method(self):
        return "Sub private method"
    
    def access_parent_private(self):
        # Can't access parent's __private directly
        try:
            return self.__private  # This is SubClass's __private
        except:
            return "Error"
    
    def show_all(self):
        parent = super().show_all()
        return {
            **parent,
            "sub __private (mangled)": self._SubClass__private,
            "sub __private_method()": self.__private_method(),
            "parent __private still exists": self._BaseClass__private
        }


# Practical use: preventing accidental override
class Counter:
    def __init__(self):
        self.__count = 0  # Truly internal
    
    def increment(self):
        self.__count += 1
    
    def get_count(self):
        return self.__count


class BadCounter(Counter):
    def __init__(self):
        super().__init__()
        self.__count = 100  # Creates _BadCounter__count, doesn't touch parent!
    
    def get_own_count(self):
        return self.__count  # This is _BadCounter__count


class GoodCounter(Counter):
    def __init__(self):
        super().__init__()
        # Don't define __count - use parent's
    
    def double_increment(self):
        self.increment()
        self.increment()


# Name mangling with methods
class Service:
    def __init__(self):
        self.__api_key = "secret_key_123"
        self.__cache = {}
    
    def __fetch_data(self, key):
        print(f"  Fetching {key} from API...")
        return f"data_for_{key}"
    
    def get_data(self, key):
        if key not in self.__cache:
            self.__cache[key] = self.__fetch_data(key)
        return self.__cache[key]


# Demonstration
if __name__ == "__main__":
    print("=== Base vs Sub Class ===")
    base = BaseClass()
    print("BaseClass:")
    for k, v in base.show_all().items():
        print(f"  {k}: {v}")
    
    print("\nSubClass:")
    sub = SubClass()
    for k, v in sub.show_all().items():
        print(f"  {k}: {v}")
    
    print("\n=== Counter Isolation ===")
    c = Counter()
    c.increment()
    c.increment()
    print(f"Counter: {c.get_count()}")
    
    bc = BadCounter()
    bc.increment()
    print(f"BadCounter parent count: {bc.get_count()}")  # Still 2!
    print(f"BadCounter own count: {bc.get_own_count()}")  # 101
    
    gc = GoodCounter()
    gc.double_increment()
    gc.double_increment()
    print(f"GoodCounter: {gc.get_count()}")  # 4
    
    print("\n=== Service with Private Methods ===")
    svc = Service()
    print(svc.get_data("user:1"))
    print(svc.get_data("user:1"))  # Cached
    print(svc.get_data("user:2"))
    
    # Access via mangling (not recommended)
    print(f"\nDirect access: {svc._Service__api_key}")
    print(f"Cache: {svc._Service__cache}")
    
    print("\n=== All Mangled Names ===")
    print("BaseClass:", [a for a in dir(base) if '__' in a and not a.startswith('__')])
    print("SubClass:", [a for a in dir(sub) if '__' in a and not a.startswith('__')])
    print("Counter:", [a for a in dir(c) if '__' in a and not a.startswith('__')])
    print("BadCounter:", [a for a in dir(bc) if '__' in a and not a.startswith('__')])