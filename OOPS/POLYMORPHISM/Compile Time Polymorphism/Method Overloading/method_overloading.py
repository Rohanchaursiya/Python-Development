# Compile-Time Polymorphism - Method Overloading

class Calculator:
    """Simulates method overloading using default arguments and *args"""
    
    def add(self, a, b, c=0):
        """Add two or three numbers"""
        return a + b + c
    
    def multiply(self, *args):
        """Multiply any number of arguments"""
        if not args:
            return 0
        result = 1
        for num in args:
            result *= num
        return result
    
    def concatenate(self, *items, separator=""):
        """Join items with optional separator"""
        return separator.join(str(item) for item in items)


class Statistics:
    """Statistical operations with flexible arguments"""
    
    def mean(self, *numbers):
        if not numbers:
            return 0
        return sum(numbers) / len(numbers)
    
    def median(self, *numbers):
        if not numbers:
            return 0
        sorted_nums = sorted(numbers)
        n = len(sorted_nums)
        mid = n // 2
        if n % 2 == 0:
            return (sorted_nums[mid-1] + sorted_nums[mid]) / 2
        return sorted_nums[mid]


class DataProcessor:
    """Process different data types with same method name"""
    
    def process(self, data):
        """Process data based on its type"""
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, list):
            return [item * 2 for item in data]
        elif isinstance(data, dict):
            return {k: v * 2 for k, v in data.items()}
        elif isinstance(data, (int, float)):
            return data ** 2
        else:
            return f"Unsupported type: {type(data).__name__}"


if __name__ == "__main__":
    calc = Calculator()
    stats = Statistics()
    processor = DataProcessor()
    
    print("=== Calculator ===")
    print(f"add(2, 3) = {calc.add(2, 3)}")
    print(f"add(2, 3, 4) = {calc.add(2, 3, 4)}")
    print(f"multiply(2, 3) = {calc.multiply(2, 3)}")
    print(f"multiply(2, 3, 4) = {calc.multiply(2, 3, 4)}")
    print(f"concatenate('a', 'b', 'c') = {calc.concatenate('a', 'b', 'c')}")
    print(f"concatenate('a', 'b', 'c', separator='-') = {calc.concatenate('a', 'b', 'c', separator='-')}")
    print()
    
    print("=== Statistics ===")
    print(f"mean(1, 2, 3, 4, 5) = {stats.mean(1, 2, 3, 4, 5)}")
    print(f"median(1, 3, 2, 5, 4) = {stats.median(1, 3, 2, 5, 4)}")
    print(f"median(1, 2, 3, 4) = {stats.median(1, 2, 3, 4)}")
    print()
    
    print("=== Data Processor ===")
    print(f"process('hello') = {processor.process('hello')}")
    print(f"process([1, 2, 3]) = {processor.process([1, 2, 3])}")
    print(f"process({{'a': 1, 'b': 2}}) = {processor.process({'a': 1, 'b': 2})}")
    print(f"process(5) = {processor.process(5)}")