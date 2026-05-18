#import Collections as nx
from Collections import MyNumbers
import datetime
import json

def myFunction():
    return 'you called myFunction'

print(myFunction())

# keyword arguments

def my_function(animal, name):
    print('the animal is ', animal)
    print('the name is ', name)

my_function(name = 'Rajesh', animal='Tiger')

# positional arguments

my_function('Rajesh','Tiger')

def my_function(*args):
    print('you have sent these', args)

my_function(1,2,3)


def outerFunc():
    x = 100
    def innerFunc():
        x = 10
        print('the value of x inside innner func is :', x)
    innerFunc()
    print('the value of x outside func is :', x)

outerFunc()


def changeCase(func):
    def inner(x):
        return func(x).upper()
    return inner

def greeting(func):
    def inner(x):
        return 'Hello ' + func(x) + ', Have a nice day'
    return inner

@greeting
@changeCase
def myFunction(name):
    return name

@changeCase
def otherFunction(name):
    return name

print(myFunction('rajesh'))
print(otherFunction("srividya"))

print(myFunction.__doc__)
print(myFunction.__name__)

myFunc = lambda a : print('the number multipled by 2 is' , a * 2)
myFunc(10)

def myFunc(n):
    return lambda a : a * n

myDoubler = myFunc(10)
print(myDoubler(20))

myList = [1,2,3,4,5,6,7,8,9,10]

result = 0
 
def sum_list(myList):   
    if not myList:
        return 0
    else:
        return myList[0] + sum_list(myList[1:])
 
print(sum_list(myList))  

def find_max(myList):
    if len(myList) == 1:
        return myList[0]
    else:
        result = find_max(myList[1:])
    return myList[0] if myList[0] > result else result

print(find_max(myList))


def print_numbers(n):
    count = 1
    while count <= n:
        yield count
        count += 1

for i in print_numbers(5):
   # print(i)
   pass

myObj = MyNumbers()

myIter = iter(myObj)

print(next(myIter))
print(next(myIter))
print(next(myIter))
print(next(myIter))

print(datetime.datetime.now())

x = {
  "name": "John",
  "age": 30,
  "city": "New York"
}

# convert to JSON string
y = json.dumps(x, indent = 5)

print('y is a JSON string', y)

# converts JSON string to python dictionary object
y = json.loads(y)
print('y is python JSON object', y)
# x = 1
# if x < 10:
#     raise Exception('some went wrong')

x = input('enter you name :')
print(f'you have entered {x}')

flag = True
while flag == True:
    x = input('enter a number')
    try:
       x = float(x)
       y = False
    except:
        print("you didn't enter a number")
   
print('Thank you')
