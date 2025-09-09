#Task 1

bill = 47.28
tip = 15/100*bill
total = tip+bill
share = total/2

print("Total amount to pay: ", format(total))
print("Each person needs to pay: "+ str(share))

#Task 2

price = int(input("Enter price in Rs per sq. meter: "))
radius = int(input("Radius: "))
height = int(input("Height: "))
area = 2*3.14*radius*height + 3.14*radius**2
cost = area*price
print("Total cost of painting is: ", format(cost))

#Task 3

a= int(input("first number: "))
b= int(input("second number: "))
#temp=a
#a=b
#b=temp
a,b=b,a
print("First number: "+ str(a))
print("Second number: "+ str(b))

#Task 4

name = input("Enter name: ")
date = input("Enter date: ")
print('Letter= "Dear"' + name + ", you are selected, interview date is " + date)