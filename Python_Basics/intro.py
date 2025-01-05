# Python is a Popular Interpreted Programming Language created by Guido Van Rossum in 1991.
# It can be used for server-side Web-development, Software Development and System Scripting

# python --version
# python file_name.py(to run the python file)

# ----------Comments -------------#
'''
    # Comments can be used to explain Python code,to make code more readable and to prevent execution while testing

    # Singleline comment
    # Mutliline comments(''' ''' or """ """)
    
'''

# --------------Variables -------------#
# Variables are Containers, which is used to store the data values.
# We can easily create variables because there are no rules in python for variable creation 

# ------------Variables Name ------------#
'''
    # must start with a letter or underscore
    # cannot start with a number
    # only contains alphanumeric characters and underscores(A-Z, a-z and _ )
    # case sensitive(name, Name and NAME all three are different)
    #can not be a python keyword 
    # eg  var, _var, var_name etc.
'''

# -----------Variable Assignment ------------#
# ------------Datatype and Types of DataTypes ------------#

'''
    # Python is a dynamically-typed language, meaning you don't need to specify the data type explicitly.
    # we can simply get the types of any data by using type() function
    # eg   x=10    type(x) will return type of data that holds by variable x

    # Numeric Types:	int, float, complex
    # Sequence Types:	list, tuple, range
    # Mapping Type:	    dict
    # Set Types:	    set, frozenset
    # Boolean Type:	    bool
    # Binary Types:	    bytes, bytearray, memoryview
    # None Type:	    NoneType

    x=20
    print(x)
    print(type(x))

    x=20.20
    print(x)
    print(type(x))

    x=2j
    print(x)
    print(type(x))

    x="Mai hu String"
    print(x)
    print(type(x))

    x=["Mai","Hu","List"]
    print(x)
    print(type(x))

    x=("Mai","Hu","Tuple")
    print(x)
    print(type(x))

    x={"Name":"Dictionary","SureName":"Kumar"}
    print(x)
    print(type(x))

    x={"Name","Name","Set","Surname","Kumar"}
    print(x)
    print(type(x))

    x=({"Name","Name","FrozenSet","Surname","Kumar"})
    print(x)
    print(type(x))

    x=range(3)
    print(x)
    print(type(x))

    x=False
    print(x)
    print(type(x))

    x=b"10"
    print(x)
    print(type(x))

    x=bytearray(3)
    print(x)
    print(type(x))



'''





echo "# Python-Development" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/Rohanchaursiya/Python-Development.git
git push -u origin main