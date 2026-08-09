# Runtime Polymorphism - Method Overriding

class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year
        self.is_running = False
    
    def start(self):
        self.is_running = True
        return f"{self.brand} ({self.year}) vehicle starting..."
    
    def stop(self):
        self.is_running = False
        return f"{self.brand} vehicle stopped"
    
    def get_info(self):
        return f"{self.year} {self.brand}"


class Car(Vehicle):
    def __init__(self, brand, year, model, doors):
        super().__init__(brand, year)
        self.model = model
        self.doors = doors
        self.speed = 0
    
    def start(self):
        self.is_running = True
        return f"{self.brand} {self.model} engine starting with key 🔑"
    
    def stop(self):
        self.speed = 0
        self.is_running = False
        return f"{self.brand} {self.model} stopped, parking brake engaged"
    
    def accelerate(self, amount):
        if not self.is_running:
            return "Start the car first!"
        self.speed += amount
        return f"Accelerating to {self.speed} km/h"
    
    def get_info(self):
        return f"{super().get_info()} {self.model} ({self.doors} doors)"


class ElectricCar(Car):
    def __init__(self, brand, year, model, doors, battery_capacity, range_km):
        super().__init__(brand, year, model, doors)
        self.battery_capacity = battery_capacity
        self.range_km = range_km
        self.battery_level = 100
    
    def start(self):
        self.is_running = True
        return f"{self.brand} {self.model} electric motor initializing silently ⚡"
    
    def stop(self):
        self.speed = 0
        self.is_running = False
        return f"{self.brand} {self.model} powered down, regenerative braking active"
    
    def charge(self, percent):
        self.battery_level = min(100, self.battery_level + percent)
        return f"Charging... Battery at {self.battery_level}%"
    
    def get_info(self):
        return f"{super().get_info()} - {self.battery_capacity}kWh, {self.range_km}km range"


class Motorcycle(Vehicle):
    def __init__(self, brand, year, model, engine_cc):
        super().__init__(brand, year)
        self.model = model
        self.engine_cc = engine_cc
        self.gear = 0
    
    def start(self):
        self.is_running = True
        return f"{self.brand} {self.model} ({self.engine_cc}cc) roaring to life! 🏍️"
    
    def shift_gear(self, gear):
        if not self.is_running:
            return "Start the engine first!"
        self.gear = gear
        return f"Shifted to gear {gear}"
    
    def get_info(self):
        return f"{super().get_info()} {self.model} ({self.engine_cc}cc)"


def demonstrate_polymorphism(vehicles):
    """Polymorphic function - works with any Vehicle subclass"""
    print("=== Polymorphic Behavior ===")
    for vehicle in vehicles:
        print(f"\n{vehicle.get_info()}")
        print(f"  Start: {vehicle.start()}")
        print(f"  Stop:  {vehicle.stop()}")


if __name__ == "__main__":
    vehicles = [
        Vehicle("Generic", 2020),
        Car("Toyota", 2022, "Camry", 4),
        ElectricCar("Tesla", 2023, "Model 3", 4, 75, 500),
        Motorcycle("Yamaha", 2021, "R1", 998)
    ]
    
    demonstrate_polymorphism(vehicles)
    
    print("\n=== Specific Features ===")
    car = Car("Honda", 2023, "Civic", 4)
    print(car.accelerate(50))
    print(car.accelerate(30))
    
    ev = ElectricCar("Nissan", 2023, "Leaf", 4, 40, 270)
    print(ev.charge(20))
    print(ev.charge(50))
    
    bike = Motorcycle("Ducati", 2022, "Panigale", 1103)
    print(bike.shift_gear(1))
    print(bike.shift_gear(3))