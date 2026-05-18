import sys
import random

'''
print(sys.version)
print('Hello World')
'''


print('Hello Rajesh', end=' ! ')
print('how are you doing today ?')
print('I am doing fine and I am', 40,'years old')

fruits = ['apple','orange','mango']
x, y, z = fruits
print(x)
print(y)
print(z)

print('the type of fruits is ', type(fruits))

print('My name is rajesh and my age is', 40)

x = 'great'

def myFunc():
   global x # global variable
   x = 'good'
   print('python is', x)

myFunc()

print('python is', x)

x = 10
print('type of x is ', type(x))
x = 'rajesh'
print('type of x is ', type(x))
 
fruits.append('guava')
fruits.remove('apple')

print(fruits)

simpletuple = (18.5, 26.7)
print(simpletuple)

print(random.randrange(1, 100))

print("This pen is Rajesh's")

print("We are the so-called \"Vikings\" from the north.")

txt1 = "My name is {name} and my age is {age}".format(name = 'Rajesh', age = '40')
txt2 = "My name is {0} and my age is {1}".format('Rajesh','40')
txt3 = "My name is {} and my age is {}".format('Rajesh','40')

print(txt1)
print(txt2)
print(txt3)