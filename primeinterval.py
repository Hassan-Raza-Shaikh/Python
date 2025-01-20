a = int(input("Enter the lower interval: "))
b = int(input("Enter the upper interval: "))

j = a
flag = 0
while j<=b:
    i = 2
    flag = True
    while i < j:
        if j%i == 0:
            flag = False
            break
        i+=1
    if flag :
        print("Number is Prime:" + str(j))
    else:
        print("Number is Composite :" + str(j))
    j+=1

import math

a = int(input("Enter the lower interval: "))
b = int(input("Enter the upper interval: "))

#for j in range(a, b + 1):
#    if j <= 1:  # Handle cases for 0 and 1
#        print(f"{j} is neither prime nor composite.")
#        continue
#    flag = True  # Assume the number is prime
#    for i in range(2, int(math.sqrt(j)) + 1):  # Check up to √j
#        if j % i == 0:
#            flag = False
#            break  # No need to check further divisors
#    if flag:
#        print(f"Number is Prime: {j}")
#    else:
#        print(f"Number is Composite: {j}")
