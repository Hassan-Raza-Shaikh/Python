weight = float( input("Weight: ") )
units = input("Is this weight in (K)kgs or (L)bs ? ")

if units=='K' or units=="k":
    print("Weight in pounds is: " + str(weight*2.20462))
elif units=='L' or units=="l":
    print("Weight in kilograms is: " + str(weight*0.453592))
else:
    print("Invalid argument")

# condition can also be made like this if unit.upper() =='K'