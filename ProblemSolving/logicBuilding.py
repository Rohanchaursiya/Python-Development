# a=int(input())
# b=int(input())
# print(a+b)

# x,y=map(int,input().split(','))
# print(x+y)

def linearSearch(n,l,k):
    ans=-1
    for i in range(len(l)):
        if l[i]==k:
            return i
    return ans



n=int(input())
list= list(map(int, input().split(',')))
k=int(input())
print(linearSearch(n,list,k))