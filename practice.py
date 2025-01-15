# general decelatrions
age = 20
price = 19.5
name = "Hassan"
name_person = input("Enter your name: ")
is_condition = True
print("hello " + name_person)


# input output
birth = input("Enter your birthyear: ")
age = 2025 - int(birth)
print(age)


# string operations
string = "HellO"
print( string.upper() )
print( string.lower() )
print( string.find('l') )
print( string.replace("ll","LL"))
print( "He" in string )


# arithematic operators
print( 10 + 3) #sum
print( 10 - 3) #difference
print( 10 * 3) #multiply
print( 10 / 3) #divide (floating value)
print( 10 // 3) #divide (integer value)
print( 10 ** 3) #exponent
print( 10 % 3) #remainder


# comparison operators
x = 3>2
print(x)


# logical operators
price = 5
print( price>1 and price<10 )
print( price>5 or price<1 )
print( not price!=5 )


# conditional statements
temperature =30
if temperature>30:
    print("It's a hot day")
elif temperature>20:
    print("It's a nice day")
else:
    print("It's a cold day")


# iterative statements
i=1
while i<=1_0: #can add _ for readability of numbers
    print(i * 'C') #prints that string that specific number of times
    i += 1


# lists
names = ["Hassan","Zara","Hamza","Haris","Rabia"]
print(names)
print(names[0])
print(names[1])
print(names[-1])
names[3]= "Rafay"
print(names)
print(names[0:2])


# list methods
numbers= [1,2,3,4,6,7]
print(numbers)
numbers.append(8)
print(numbers)
numbers.insert(4,5) # first argumnet is index on which number is to be inserted
print(numbers)
print( len(numbers) ) # shows the number of elements in a list
numbers.remove(7)
print(numbers)
print( 7 in numbers)
numbers.clear()
print(numbers)


# for loop vs while loop
numbers = [1,2,3,4,5]

for item in numbers:
    print(item)

i = 0
while i< len(numbers):
    print(numbers[i])
    i += 1


# range function
items = range(5) # if only 1 value given, 0 to less than that value is range, if 2 values given, startng value to less than ending value, and 3rd value is step
print(items)
for number in items:
    print(number)

items = range(5,10) 
print(items)
for number in items:
    print(number)

items = range(5,10,2) 
print(items)
for number in items: # can also be written in a single line as for number in range(5,10) etc, no need to store the result
    print(number)


# tuples
number = (1,2,3,3) # basically it is a constant list so it cannot be appended or re written etc, only found and counted
print( number.count(3) ) # counts how many of that type of number are present
print( number.index(2) ) # returns the first index with occurence of that element