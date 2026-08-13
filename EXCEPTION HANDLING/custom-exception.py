class InsufficientBalanceError(Exception):
    pass

balance=300

try:
    if balance<500:
        raise InsufficientBalanceError("Insufficient balance")
except InsufficientBalanceError as e:
    print("Error: ", e)
