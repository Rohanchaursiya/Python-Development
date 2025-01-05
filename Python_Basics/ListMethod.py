# -------------List--------------#
'''
    # Lists are used to store multiple items in a single variable.
    # Lists are defined by enclosing items in square brackets [], separated by commas.
    # Lists are mutable, meaning their values can be changed after they are created.
    # Lists support indexing and slicing operations.
    # Lists are ordered.
    # Lists can contain duplicate values.
    # Lists can be nested (list inside another list).
    # Lists are one of 4 built-in data types in Python used to store collections of data,
    # and other 3 are Tuple, Set, and Dictionary, all with different qualities and usage.
'''

#--------------List Method-------#

# append() - Adds an element at the end of the list.
# clear() - Removes all elements from the list.
# copy() - Returns a shallow copy of the list.
# count() - Returns the number of occurrences of an element in the list.
# extend() - Adds elements from another list to the end of the current list.
# index() - Returns the index of the first occurrence of an element in the list.
# insert() - Adds an element at a specified index in the list.
# pop() - Removes the element at the specified index and returns it.
# remove() - Removes the first occurrence of an element from the list.
# reverse() - Reverses the order of the elements in the list.
# sort() - Sorts the elements of the list in ascending order.

list1=["Mai","Hu","List"]
list2=["Rohan","Kumar","Chaursiya"]
print(list1)
print(list2)
#-------Access List Items------#
print(list1[0])
print(list1[2])
print(list1[-1])
print(list1[1:3])

#-------Modify/Change List Items------#

list1[0]="MAI"
print(list1)
list1[1:3]=["Rohan","Kumar"]
print(list1)

#-------Add List Items------#

list1.append("New Item")
print(list1)
list1.extend(list2)
print(list1)
list1.extend(list2)
print(list1)

#-------Remove List Items------#
list1.remove("Kumar")
print(list1)
list2.pop(1)
print(list2)
del list2[1]
print(list2)
print(list1.clear())


#--------------List Comprehension-------#
