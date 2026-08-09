# Method Overloading

## Definition
Method overloading allows multiple methods with the same name but different parameters (number, type, or order). In Python, this is simulated using default arguments, *args, **kwargs, or type checking.

## Pros
- **Clean API**: Single method name for related operations
- **Flexibility**: Handle varying input types/counts
- **Backward Compatibility**: Add parameters without breaking calls
- **Readability**: Logical grouping of similar operations

## Cons
- **Not Native**: Python doesn't support true overloading
- **Complexity**: Manual type/argument checking required
- **Maintenance**: Single method grows complex
- **Type Safety**: No compile-time verification

## Use Cases
- Mathematical functions (add 2 or 3 numbers)
- Constructors with optional parameters
- Search functions with varying criteria
- Configuration methods with defaults

## Image
![Method Overloading Diagram](method_overloading.svg)

## Syntax
```python
# Using default arguments
class Math:
    def add(self, a, b, c=0):
        return a + b + c

# Using *args
class Statistics:
    def mean(self, *numbers):
        return sum(numbers) / len(numbers) if numbers else 0

# Using type checking
class Processor:
    def process(self, data):
        if isinstance(data, str):
            return data.upper()
        elif isinstance(data, list):
            return [x * 2 for x in data]
        elif isinstance(data, dict):
            return {k: v*2 for k, v in data.items()}
        return data

math = Math()
math.add(2, 3)      # 5
math.add(2, 3, 4)   # 9

stats = Statistics()
stats.mean(1, 2, 3, 4, 5)  # 3.0

proc = Processor()
proc.process("hello")       # "HELLO"
proc.process([1, 2, 3])     # [2, 4, 6]
proc.process({"a": 1})      # {"a": 2}
```