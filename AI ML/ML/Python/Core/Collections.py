fruits = ['apple','guava','orange']

fruits.append('grapes')
fruits.extend('kiwi')

print(f'the fruits are {fruits}')

for i in range(len(fruits)):
    print('for loop:')
    print(i, fruits[i])    

i = 0
while i < len(fruits):   
    print('while loop:')
    print(i, fruits[i])
    i = i + 1
    

thislist = [100, 50, 65, 82, 23]
print(thislist.sort())

# tuple

fruits = ("apple", "mango", "papaya", "pineapple", "pineapple", "cherry")
(green, *tropic, red) = fruits
print(tropic)
print(red)

# dictionary

person = {
    "name" : "Rajesh",
    "age" : 40  
}

print(person)

person["car"] = "baleno"

print(person)

person.update({"name": "Vemulakonda Rajesh"})

print(person)

person.popitem() # pops the last item

print(person)

person.pop("age")

print(person)

iterable = iter(fruits)

print(next(iterable))
print(next(iterable))


class MyNumbers:
   def __iter__(self):
       self.a = 1       
       return self
   
   def __next__(self):
     if self.a <= 5:
       x = self.a
       self.a += 1
       return x
     else:
        StopIteration
   
myObj = MyNumbers()
myiter = iter(myObj)

print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))