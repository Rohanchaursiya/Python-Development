#-----------Operators---------#
'''
    # Operators are used to perform operations on variables and values.
'''

#--------Types of Operator----#
'''
    # Arithmetic Operators (+, -, *, /, %, //, **)
    # Assignment Operators (=, +=, -=, *=, /=, %=, //=, &=, |=, ^=, **=, <<=, >>=, :=)
    # Comparison Operators (>, <, ==,!=, >=, <=)
    # Logical Operators (and, or, not)
    # Membership Operators (in, not in)
    # Identity Operators (is, is not)
    # Bitwise Operators (&, |, ^, ~, <<, >>)
'''

#---------Arithmetic Operators---------#

a=10
b=5
print(a+b) # Addition
print(a-b) # Subtraction
print(a*b) # Multiplication
print(a/b) # Division
print(a//b)# Floor Division
print(a%b)# Modulo
print(a**b)# Exponentian

#---------Assignment Operators---------#

a=10
a+=5 # a=a+5
print(a)

a-=5 # a=a-5
print(a)

a*=5 # a=a*5
print(a)

a/=5 # a=a/5
print(a)

a%=5 # a=a%5
print(a)

a//=5 # a=a//5
print(a)

a**=5 # a=a**5
print(a)

print(a:=5) # a=5

#---------Comparison Operators---------#

a=10
b=5
print(a>b) # Greater Than
print(a<b) # Less Than
print(a==b) # Equal To
print(a!=b) # Not Equal To
print(a>=b) # Greater Than Or Equal To
print(a<=b) # Less Than Or Equal To

#---------Logical Operators---------#

a=True
b=False
print(a and b) # Logical AND
print(a or b) # Logical OR
print(not a) # Logical NOT

#---------Membership Operators---------#

a=[1,2,3,4,5]
print(1 in a) # Membership
print(6 in a) # Membership

#---------Identity Operators---------#

a=10
b=10
print(a is b) # Identity
print(a is not b) # Identity

#---------Bitwise Operators---------#

a=10
b=5
print(a&b) # Bitwise AND
print(a|b) # Bitwise OR
print(a^b) # Bitwise XOR
print(~a) # Bitwise NOT
print(a<<2) # Bitwise Left Shift
print(a>>2) # Bitwise Right Shift




