# Methods: Instance, Class, Static

class Temperature:
    """Temperature converter with all method types"""
    
    def __init__(self, celsius):
        self.celsius = celsius
    
    # Instance method - operates on instance data
    def to_fahrenheit(self):
        return self.celsius * 9/5 + 32
    
    def to_kelvin(self):
        return self.celsius + 273.15
    
    def __str__(self):
        return f"{self.celsius}°C"
    
    def __repr__(self):
        return f"Temperature({self.celsius})"
    
    # Class method - factory/alternative constructors
    @classmethod
    def from_fahrenheit(cls, fahrenheit):
        celsius = (fahrenheit - 32) * 5/9
        return cls(round(celsius, 2))
    
    @classmethod
    def from_kelvin(cls, kelvin):
        celsius = kelvin - 273.15
        return cls(round(celsius, 2))
    
    @classmethod
    def freezing(cls):
        return cls(0)
    
    @classmethod
    def boiling(cls):
        return cls(100)
    
    @classmethod
    def absolute_zero(cls):
        return cls(-273.15)
    
    # Static method - utility functions
    @staticmethod
    def c_to_f(celsius):
        return celsius * 9/5 + 32
    
    @staticmethod
    def f_to_c(fahrenheit):
        return (fahrenheit - 32) * 5/9
    
    @staticmethod
    def c_to_k(celsius):
        return celsius + 273.15
    
    @staticmethod
    def is_freezing(celsius):
        return celsius <= 0
    
    @staticmethod
    def is_boiling(celsius):
        return celsius >= 100
    
    @staticmethod
    def validate_celsius(value):
        return isinstance(value, (int, float)) and value >= -273.15


class Employee:
    """Employee with class-level tracking"""
    
    # Class attributes
    company = "TechCorp"
    employee_count = 0
    _all_employees = []
    
    def __init__(self, name, department, salary):
        if not Temperature.validate_celsius(salary):  # Reuse static method
            raise ValueError("Invalid salary")
        
        self.name = name
        self.department = department
        self.salary = salary
        Employee.employee_count += 1
        Employee._all_employees.append(self)
    
    # Instance method
    def get_info(self):
        return f"{self.name} - {self.department} - ${self.salary:,}"
    
    def give_raise(self, percent):
        self.salary *= (1 + percent/100)
        return self.salary
    
    # Class method
    @classmethod
    def get_total_employees(cls):
        return cls.employee_count
    
    @classmethod
    def get_employees_by_dept(cls, dept):
        return [e for e in cls._all_employees if e.department == dept]
    
    @classmethod
    def from_string(cls, s):
        name, dept, salary = s.split(",")
        return cls(name.strip(), dept.strip(), float(salary))
    
    @classmethod
    def average_salary(cls):
        if not cls._all_employees:
            return 0
        return sum(e.salary for e in cls._all_employees) / len(cls._all_employees)
    
    # Static method
    @staticmethod
    def is_valid_department(dept):
        valid = {"engineering", "sales", "marketing", "hr", "finance"}
        return dept.lower() in valid
    
    @staticmethod
    def format_currency(amount):
        return f"${amount:,.2f}"


class MathUtils:
    """Pure static methods - no class/instance state needed"""
    
    @staticmethod
    def add(*args):
        return sum(args)
    
    @staticmethod
    def multiply(*args):
        result = 1
        for n in args:
            result *= n
        return result
    
    @staticmethod
    def mean(*args):
        return sum(args) / len(args) if args else 0
    
    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True


# Demonstration
if __name__ == "__main__":
    print("=== Temperature - All Method Types ===")
    
    # Instance methods
    temp = Temperature(25)
    print(f"temp = {temp}")
    print(f"to_fahrenheit(): {temp.to_fahrenheit():.1f}°F")
    print(f"to_kelvin(): {temp.to_kelvin():.1f}K")
    print()
    
    # Class methods as factories
    cold = Temperature.from_fahrenheit(32)
    hot = Temperature.from_kelvin(373.15)
    ice = Temperature.freezing()
    steam = Temperature.boiling()
    zero = Temperature.absolute_zero()
    
    print(f"from_fahrenheit(32): {cold}")
    print(f"from_kelvin(373.15): {hot}")
    print(f"freezing(): {ice}")
    print(f"boiling(): {steam}")
    print(f"absolute_zero(): {zero}")
    print()
    
    # Static methods
    print(f"c_to_f(100): {Temperature.c_to_f(100)}°F")
    print(f"f_to_c(212): {Temperature.f_to_c(212)}°C")
    print(f"is_freezing(-5): {Temperature.is_freezing(-5)}")
    print(f"is_boiling(100): {Temperature.is_boiling(100)}")
    print(f"validate_celsius(-300): {Temperature.validate_celsius(-300)}")
    print()
    
    print("=== Employee - Class Methods for Tracking ===")
    emp1 = Employee("Alice", "Engineering", 90000)
    emp2 = Employee("Bob", "Sales", 75000)
    emp3 = Employee("Charlie", "Engineering", 95000)
    emp4 = Employee.from_string("Diana, Marketing, 70000")
    
    print(f"Total employees: {Employee.get_total_employees()}")
    print(f"Average salary: {Employee.format_currency(Employee.average_salary())}")
    print(f"Engineering: {[e.name for e in Employee.get_employees_by_dept('Engineering')]}")
    print(f"Valid dept 'Engineering': {Employee.is_valid_department('Engineering')}")
    print(f"Valid dept 'Legal': {Employee.is_valid_department('Legal')}")
    print()
    
    print("=== MathUtils - Pure Static ===")
    print(f"add(1,2,3,4,5): {MathUtils.add(1,2,3,4,5)}")
    print(f"multiply(2,3,4): {MathUtils.multiply(2,3,4)}")
    print(f"mean(10,20,30): {MathUtils.mean(10,20,30)}")
    print(f"is_prime(17): {MathUtils.is_prime(17)}")
    print(f"is_prime(18): {MathUtils.is_prime(18)}")
    
    # Can call static methods on instances too
    print(f"temp.is_freezing(0): {temp.is_freezing(0)}")
    print(f"emp1.is_valid_department('HR'): {emp1.is_valid_department('HR')}")