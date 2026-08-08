# Multilevel Inheritance Example

class Vehicle:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year
        self.is_running = False
    
    def start(self):
        self.is_running = True
        return f"{self.brand} ({self.year}) started"
    
    def stop(self):
        self.is_running = False
        return f"{self.brand} stopped"
    
    def get_info(self):
        return f"{self.year} {self.brand}"


class Car(Vehicle):
    def __init__(self, brand, year, model, doors):
        super().__init__(brand, year)
        self.model = model
        self.doors = doors
        self.speed = 0
    
    def accelerate(self, amount):
        self.speed += amount
        return f"Accelerating to {self.speed} km/h"
    
    def brake(self):
        self.speed = 0
        return "Car stopped"
    
    def get_info(self):
        return f"{super().get_info()} {self.model} ({self.doors} doors)"


class SportsCar(Car):
    def __init__(self, brand, year, model, doors, top_speed, horsepower):
        super().__init__(brand, year, model, doors)
        self.top_speed = top_speed
        self.horsepower = horsepower
        self.turbo_mode = False
    
    def activate_turbo(self):
        self.turbo_mode = True
        return f"Turbo activated! Max speed: {self.top_speed} km/h"
    
    def race(self):
        if self.turbo_mode:
            return f"Racing at {self.top_speed} km/h with {self.horsepower} HP!"
        return "Activate turbo first!"
    
    def get_info(self):
        return f"{super().get_info()} - {self.horsepower} HP, Top: {self.top_speed} km/h"


if __name__ == "__main__":
    vehicle = Vehicle("Generic", 2020)
    car = Car("Toyota", 2022, "Camry", 4)
    sports = SportsCar("Ferrari", 2023, "488 GTB", 2, 340, 710)
    
    print("=== Vehicle ===")
    print(vehicle.start())
    print(vehicle.get_info())
    print()
    
    print("=== Car ===")
    print(car.start())
    print(car.accelerate(60))
    print(car.get_info())
    print()
    
    print("=== Sports Car ===")
    print(sports.start())
    print(sports.activate_turbo())
    print(sports.race())
    print(sports.get_info())