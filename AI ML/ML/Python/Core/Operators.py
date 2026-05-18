x = 15
y = 2

print(f' The division of numbers is : {x / y}')
print(f' The floor division of numbers is : {x // y}')

# bitwise operators

x = 5
x &= 3
'''
5 --> 101
3 --> 011
'''
print(f'the bitwise AND is {x}') #  001 --> 1
x = 5
x |= 3
print(f'the bitwise AND is {x}') #  001 --> 7
x = 5
x ^= 3 # x = x ^ 3
print(f'the bitwise XOR is {x}') # 110 --> 6
x = 5
print(f'the bitwise NOT is {~x}') # 110 --> -6
x = 5
print(f'the left most shift is {x << 2}') # 10100 --> 12
print(f'the right most shift is {x >> 2}') # 01 --> 1

# Identity Operators

x = ['apple','banana']
y = ['apple','banana']

print(x == y)
print(x is y)

x = 10

if x < 7:
    print('x is less than 7')
elif x < 8:
     print('x is less than 8')
elif x < 9:
     print('x is less than 9')
else :
     print('x is less than 10')

age = 25
is_student = False
has_discount_code = True

if age < 25 and not is_student or has_discount_code:
   print('condition satisfied')

if age > 25:
   pass  # pass is the statement we use when we want to skip

day = 5

match day:
    case 1:
        print('sunday')        
    case 2:
        print('monday')
    case 3:
        print('tuesday')
    case 4:
        print('wednesday')
    case _:
        print('any given day')
    
