#Task 1

l = [1,2,3,3,3,3,4,5]
unique_list = []
for num in l:
    if num not in unique_list:
        unique_list.append(num)
print(unique_list)

#Task 2

string = input("Enter string seperated by - : ")
string = string.split("-")
string.sort()
new_string= " ".join(string)
print(new_string)
new_string2= "-".join(string)
print(new_string2)

#Task 3

string= input("Enter a string: ")
list(string)
upper=0
lower=0
for char in string:
    if char.isalpha():
        if char.islower():
            lower+=1
        else:
            upper+=1
print("Upper case",upper)
print("Lower case",lower)

#Task 4

num = int(input("Enter a number: "))
divisor=int(num/2 +1)
sum=0
for i in range(1,divisor):
    if num%i ==0:
        sum+=i
if sum==num:
    print(f"{num} is a perfect number ")
else:
    print(f"{num} is not a perfect number ")

#Task 5

dict1={1:10,2:20}
dict2={3:30,4:40}
dict3={5:50,6:60}
new_dict={}
new_dict=dict(new_dict)
new_dict.update(dict1)
new_dict.update(dict2)
new_dict.update(dict3)
print (new_dict)

#Task 6

list1 = [1, 2, 3, 4]
list2 = [5, 6, 7, 8]
list3 = [9, 10, 11, 12]

result = list(map(lambda x, y, z: x + y + z, list1, list2, list3))

print("Summed List:", result)

#Task 7

list_ = [1,2,3,4,5,6]
result = list(map(lambda x: x**(x-1) , list_))
print(result)

#Task 8

def is_vowel(char):
    return char.lower() in 'aeiou'

text= input("Enter a string: ")
vowels= list(filter(is_vowel,text))
print("Vowels in string are: ", vowels)

#Task 9

#Havent done 2d lists

#Task 10

def get_highly_skilled_employees(employees):
    
    highly_skilled = filter(lambda emp: emp["Grade"] == "Highly skilled", employees)

    full_names = list(map(lambda emp: emp["First name"] + " " + emp["Last name"], highly_skilled))

    return full_names

employees = [
    {"First name": "John", "Last name": "Doe", "Age": 28, "Grade": "Highly skilled"},
    {"First name": "Jane", "Last name": "Smith", "Age": 34, "Grade": "Skilled"},
    {"First name": "Alice", "Last name": "Brown", "Age": 29, "Grade": "Highly skilled"},
    {"First name": "Bob", "Last name": "Davis", "Age": 41, "Grade": "Semi-skilled"},
    {"First name": "Charlie", "Last name": "Miller", "Age": 37, "Grade": "Highly skilled"}
]

print("Highly Skilled Employees:", get_highly_skilled_employees(employees))