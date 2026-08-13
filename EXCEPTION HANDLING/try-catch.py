try:
    num=int(input())
    result=10/num
except ValueError:
    print("Invalid Input")
except ZeroDivisionError:
    print("Zero Division Error")
# It can be also written as
# except(ValueError, ZeroDivisionError):
#     print("Invalid Input")
else:
    print("Result: ", result)
finally:
    print("Execution Completed")
