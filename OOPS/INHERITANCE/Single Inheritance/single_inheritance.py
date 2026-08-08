# Single Inheritance Example

class Animal:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"{self.name} makes a sound"
    
    def eat(self):
        return f"{self.name} is eating"


class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
    
    def speak(self):
        return f"{self.name} says Woof!"
    
    def fetch(self):
        return f"{self.name} is fetching the ball"


if __name__ == "__main__":
    animal = Animal("Generic Animal")
    dog = Dog("Buddy", "Golden Retriever")
    
    print(animal.speak())
    print(animal.eat())
    print()
    print(dog.speak())
    print(dog.eat())
    print(dog.fetch())
    print(f"Breed: {dog.breed}")