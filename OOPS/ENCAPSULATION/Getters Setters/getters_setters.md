# Getters and Setters

## Definition
Getters and setters are methods that control access to private attributes. In Python, they're implemented as methods (`get_x()`, `set_x()`) or more pythonically with `@property` decorator.

## Pros
- **Validation**: Check values before setting
- **Computed Values**: Derive on-the-fly
- **Side Effects**: Trigger updates, logging, notifications
- **Backward Compatibility**: Change internal without breaking API
- **Read/Write Control**: Read-only, write-only, or both

## Cons
- **Verbosity**: More code than direct access
- **Performance**: Method call overhead
- **Boilerplate**: Repetitive for simple attributes
- **Overuse**: Not needed for simple public attributes

## Use Cases
- **Validation**: Email format, positive numbers, ranges
- **Conversion**: Automatic type conversion
- **Events**: Notify observers on change
- **Lazy Loading**: Initialize on first access
- **Caching**: Store computed results

## Image
![Getters Setters Diagram](getters_setters.svg)

## Syntax
```python
class Person:
    def __init__(self, name, age, email):
        self._name = ""
        self._age = 0
        self._email = ""
        # Use setters for validation
        self.name = name
        self.age = age
        self.email = email
    
    # Traditional getter/setter
    def get_name(self):
        return self._name
    
    def set_name(self, value):
        if not value or not value.strip():
            raise ValueError("Name cannot be empty")
        self._name = value.strip().title()
    
    # Property-based (Pythonic)
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise TypeError("Age must be integer")
        if value < 0 or value > 150:
            raise ValueError("Age must be 0-150")
        self._age = value
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email format")
        self._email = value.lower()
    
    @email.deleter
    def email(self):
        self._email = ""
    
    # Read-only property (no setter)
    @property
    def is_adult(self):
        return self._age >= 18
    
    # Computed property
    @property
    def display_name(self):
        return f"{self._name} ({self._age})"

class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius
    
    @property
    def celsius(self):
        return self._celsius
    
    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero!")
        self._celsius = value
    
    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32
    
    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9
    
    @property
    def kelvin(self):
        return self._celsius + 273.15

# Usage
p = Person("alice smith", 25, "ALICE@EXAMPLE.COM")
print(f"Name: {p.name}")          # Alice Smith (validated)
print(f"Email: {p.email}")        # alice@example.com (normalized)
print(f"Adult: {p.is_adult}")     # True (read-only)
print(f"Display: {p.display_name}")  # Alice Smith (25)

# Validation
try:
    p.age = -5
except ValueError as e:
    print(f"Error: {e}")

try:
    p.email = "invalid"
except ValueError as e:
    print(f"Error: {e}")

# Temperature with multiple scales
t = Temperature(25)
print(f"C: {t.celsius}, F: {t.fahrenheit}, K: {t.kelvin}")
t.fahrenheit = 212
print(f"After F=212: C={t.celsius}, K={t.kelvin}")
```