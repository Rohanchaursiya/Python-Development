# String=input()
# print(String)
String="""Mai Hu String"""
print(String)
print(len(String))#it is used to find the length of the string
print("sit" in String)#it is used to check certain pharse or character is present in string
print("sit" not in String)#it is used to check certain pharse or character is not present in string
print(String[0])#Slicing
print(String[2:5])#Slicing
print(String[2:])#Slicing
print(String[:9])#Slicing
print(String[-6:-1])#Negative Slicing
print(String.upper())#it is used to convert string into uppercase string
print(String.lower())#it is used to convert string into lowercase string
print(String.strip())#it is used to remove the whitesapce from start and end
print(String.replace("Hu","Hu New"))#it is used to replace existing value with new assigned value
print(String.split(" "))#it is used to convert the string into list 
print(String.isalpha())#it is used to check the string contains only alphabets
print(String.isalnum())#it is used to check the string contains only alphabets and numbers
print(String.isdigit())#it is used to check the string contains only numbers
print(String.find("Hu"))#it is used to find the index of a character or substring in string
print(String.count("Mai"))#it is used to count the occurrence of a character or substring in string
print(String.startswith("Mai"))#it is used to check the string starts with given substring
print(String.endswith("String"))#it is used to check the string ends with given substring


# -----------String concatenation-------#
#to concatenate or combine two string we can use '+' operator 
a="Rohan"
b="Kumar"
c=a+b
print(c)
c=a+" "+b
print(c)

#------------String Formatting---------#
''' In python we can't combine String and integer normally 
    but by using format() we can easily combine the string and integer 
'''
name='Rohan Kumar Chaursiya'
age=22
print(f"My Name is {name} and I am {age} years old.")
print(f"Price of 1 Mango is 17 then price of 20 Mango is {20*17 :.2f}.")

#------------Escape Sequences---------#

print("Hello\nWorld") # it will print hello on new line and world on the same line
print("Hello\tWorld") # it will print hello and world on the same line with a tab space between them

