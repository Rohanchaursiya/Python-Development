# Hybrid Inheritance Example

class LivingBeing:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def breathe(self):
        return f"{self.name} is breathing"
    
    def grow(self):
        self.age += 1
        return f"{self.name} is now {self.age} years old"


class Animal(LivingBeing):
    def __init__(self, name, age, species, habitat):
        super().__init__(name, age)
        self.species = species
        self.habitat = habitat
    
    def move(self):
        return f"{self.name} is moving"
    
    def eat(self):
        return f"{self.name} is eating"


class Plant(LivingBeing):
    def __init__(self, name, age, plant_type, height):
        super().__init__(name, age)
        self.plant_type = plant_type
        self.height = height
    
    def photosynthesize(self):
        return f"{self.name} is photosynthesizing"
    
    def absorb_water(self):
        return f"{self.name} is absorbing water"


class Bird(Animal):
    def __init__(self, name, age, species, habitat, wing_span, can_fly=True):
        super().__init__(name, age, species, habitat)
        self.wing_span = wing_span
        self.can_fly = can_fly
    
    def fly(self):
        if self.can_fly:
            return f"{self.name} is flying with {self.wing_span}m wingspan"
        return f"{self.name} cannot fly"
    
    def lay_eggs(self):
        return f"{self.name} laid eggs"


class Fish(Animal):
    def __init__(self, name, age, species, habitat, max_depth, can_breathe_air=False):
        super().__init__(name, age, species, habitat)
        self.max_depth = max_depth
        self.can_breathe_air = can_breathe_air
    
    def swim(self):
        return f"{self.name} is swimming at depth up to {self.max_depth}m"
    
    def breathe_underwater(self):
        return f"{self.name} is breathing underwater"


class FlyingFish(Fish, Bird):
    def __init__(self, name, age, species, habitat, max_depth, wing_span, glide_distance):
        Fish.__init__(self, name, age, species, habitat, max_depth)
        Bird.__init__(self, name, age, species, habitat, wing_span, can_fly=False)
        self.glide_distance = glide_distance
    
    def glide(self):
        return f"{self.name} glides {self.glide_distance}m above water"
    
    def swim(self):
        return f"{self.name} swims and can glide!"
    
    def fly(self):
        return f"{self.name} doesn't fly but glides for {self.glide_distance}m"


if __name__ == "__main__":
    print("=== Hybrid Inheritance Demo ===\n")
    
    eagle = Bird("Eagle", 5, "Golden Eagle", "Mountains", 2.3)
    salmon = Fish("Salmon", 3, "Atlantic Salmon", "Ocean", 100)
    flying_fish = FlyingFish("Exocet", 2, "Flying Fish", "Tropical Ocean", 50, 0.3, 200)
    
    print("--- Eagle ---")
    print(eagle.breathe())
    print(eagle.move())
    print(eagle.fly())
    print(eagle.lay_eggs())
    print()
    
    print("--- Salmon ---")
    print(salmon.breathe())
    print(salmon.swim())
    print(salmon.breathe_underwater())
    print()
    
    print("--- Flying Fish ---")
    print(flying_fish.breathe())
    print(flying_fish.swim())
    print(flying_fish.glide())
    print(flying_fish.fly())
    print()
    
    print(f"MRO: {[c.__name__ for c in FlyingFish.__mro__]}")