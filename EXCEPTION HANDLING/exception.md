# Exceptions in Python

## Overview
An **exception** is an event that disrupts the normal flow of a program's execution. When an error occurs, Python creates an exception object and raises it. If not handled, the program terminates with a traceback.

---

## Exception Hierarchy (Built‑in)

```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 ├── GeneratorExit
 └── Exception
      ├── StopIteration
      ├── StopAsyncIteration
      ├── ArithmeticError
      │    ├── FloatingPointError
      │    ├── OverflowError
      │    └── ZeroDivisionError
      ├── AssertionError
      ├── AttributeError
      ├── BufferError
      ├── EOFError
      ├── ImportError
      │    └── ModuleNotFoundError
      ├── LookupError
      │    ├── IndexError
      │    └── KeyError
      ├── MemoryError
      ├── NameError
      │    └── UnboundLocalError
      ├── OSError
      │    ├── BlockingIOError
      │    ├── ChildProcessError
      │    ├── ConnectionError
      │    │    ├── BrokenPipeError
      │    │    ├── ConnectionAbortedError
      │    │    ├── ConnectionRefusedError
      │    │    └── ConnectionResetError
      │    ├── FileExistsError
      │    ├── FileNotFoundError
      │    ├── InterruptedError
      │    ├── IsADirectoryError
      │    ├── NotADirectoryError
      │    ├── PermissionError
      │    ├── ProcessLookupError
      │    └── TimeoutError
      ├── ReferenceError
      ├── RuntimeError
      │    ├── NotImplementedError
      │    └── RecursionError
      ├── SyntaxError
      │    └── IndentationError
      │         └── TabError
      ├── SystemError
      ├── TypeError
      ├── ValueError
      │    └── UnicodeError
      │         ├── UnicodeDecodeError
      │         ├── UnicodeEncodeError
      │         └── UnicodeTranslateError
      └── Warning
           ├── DeprecationWarning
           ├── PendingDeprecationWarning
           ├── RuntimeWarning
           ├── SyntaxWarning
           ├── UserWarning
           ├── FutureWarning
           ├── ImportWarning
           ├── UnicodeWarning
           └── BytesWarning
```

*Only `Exception` (and its subclasses) should be caught in normal code. `BaseException` subclasses like `SystemExit`, `KeyboardInterrupt`, and `GeneratorExit` are meant for interpreter control.*

---

## Common Exception Types & When They Appear

| Exception | Typical Cause |
|-----------|----------------|
| `ZeroDivisionError` | Division or modulo by zero |
| `IndexError` | Sequence subscript out of range |
| `KeyError` | Dictionary key not found |
| `FileNotFoundError` | Opening a non‑existent file |
| `PermissionError` | Insufficient filesystem permissions |
| `ValueError` | Argument has right type but inappropriate value |
| `TypeError` | Operation applied to an object of inappropriate type |
| `ImportError` / `ModuleNotFoundError` | Failed import |
| `AttributeError` | Attribute reference/assignment fails |
| `RuntimeError` | Errors that don't fall into other categories |
| `NotImplementedError` | Abstract method not overridden |
| `RecursionError` | Maximum recursion depth exceeded |

---

## Handling Exceptions

```python
try:
    # risky code
    result = 10 / 0
except ZeroDivisionError as exc:
    # handle specific error
    print(f"Caught: {exc}")
except (ValueError, TypeError) as exc:
    # handle multiple types
    print(f"Invalid input: {exc}")
else:
    # runs if no exception
    print("Success:", result)
finally:
    # always runs
    print("Cleanup")
```

### Best Practices
1. **Catch specific exceptions** – avoid bare `except:`.
2. **Use `else`** for code that should run only when no exception occurs.
3. **Use `finally`** for resource cleanup (files, sockets, locks).
4. **Raise with context** – `raise NewError("msg") from original` preserves traceback.
5. **Define custom exceptions** for domain‑specific errors:

```python
class ValidationError(Exception):
    """Raised when input validation fails."""
    def __init__(self, field, message):
        self.field = field
        super().__init__(f"{field}: {message}")
```

---

## Pros of Using Exceptions

| Advantage | Explanation |
|-----------|-------------|
| **Separates error handling from business logic** | Cleaner, readable code. |
| **Automatic stack unwinding** | Propagates up until caught, no manual error code checks. |
| **Rich error information** | Exception objects carry message, type, traceback. |
| **Supports `finally` / context managers** | Guarantees cleanup (RAII pattern). |
| **Enables duck‑typed protocols** | EAFP (“Easier to Ask Forgiveness than Permission”) style. |

---

## Cons / Drawbacks

| Disadvantage | Mitigation |
|--------------|------------|
| **Performance overhead** when raised frequently | Use exceptions only for *exceptional* cases, not control flow. |
| **Can hide bugs** if caught too broadly (`except Exception`) | Catch specific types; log unexpected ones. |
| **Complex control flow** – harder to follow for newcomers | Document expected exceptions; keep `try/except` blocks small. |
| **Potential for resource leaks** if `finally` omitted | Always pair acquire/release in `try/finally` or use `with`. |
| **Serialization / cross‑process issues** | Define `__reduce__` for custom exceptions if pickled. |

---

## Quick Reference Cheatsheet

```text
try:
    # code that may raise
except SpecificError as e:
    # handle SpecificError
except (ErrorA, ErrorB) as e:
    # handle multiple
except Exception as e:
    # catch-all for unexpected (log & re-raise)
else:
    # no exception
finally:
    # always executed
```

---

## Further Reading
- **PEP 3151** – Reworking the OS and I/O exception hierarchy.
- **Python Docs** – [Built‑in Exceptions](https://docs.python.org/3/library/exceptions.html)
- **Effective Python** – Item 34: “Prefer `try/except` over `if/else` for error handling.”

---
*Generated for the Python‑Development learning repository.*