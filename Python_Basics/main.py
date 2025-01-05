# print("hello, World")
# def isPrime(n):
#     if n==0 or n==1:
#         return False
#     for i in range(2,n):
#         if n%i==0:
#             return False
#     return True

# def isPalin(str):
#     return str==str[::-1]



# a=int(input("Enter a Number : "))
# print(isPrime(a))

# # b=input("Enter a String : ")

# print(isPalin(str(a)))


s=input()
s=s.split(",")
print(type(s))
li=[0]*100
li2=[]
for i in s:
    li[int(i)]+=1
for i in range(len(li)):
    if li[i]>=len(s)//3:
        li2.append(i)
print(li2)