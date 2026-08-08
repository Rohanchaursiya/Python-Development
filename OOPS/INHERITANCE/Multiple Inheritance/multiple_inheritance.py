# Multiple Inheritance Example

class Flyer:
    def __init__(self, max_altitude):
        self.max_altitude = max_altitude
    
    def fly(self):
        return f"Flying up to {self.max_altitude} meters"
    
    def land(self):
        return "Landing safely"


class Swimmer:
    def __init__(self, max_depth):
        self.max_depth = max_depth
    
    def swim(self):
        return f"Swimming down to {self.max_depth} meters"
    
    def surface(self):
        return "Surfacing"


class Duck(Flyer, Swimmer):
    def __init__(self, name, max_altitude, max_depth):
        Flyer.__init__(self, max_altitude)
        Swimmer.__init__(self, max_depth)
        self.name = name
    
    def quack(self):
        return f"{self.name} says Quack!"
    
    def dive(self):
        return f"{self.name} dives underwater"


if __name__ == "__main__":
    duck = Duck("Donald", 100, 10)
    
    print(f"MRO: {[c.__name__ for c in Duck.__mro__]}")
    print()
    print(duck.quack())
    print(duck.fly())
    print(duck.swim())
    print(duck.dive())
    print(duck.land())
    print(duck.surface())