z=3
print(z)
print(type(z))
x=3.5
print(x)
print(type(x))
print(z+x)
a=0o10 # octal representation of 8
a=0x10 # hexadecimal representation of 16
a=0b10000000 # binary representation of 128
# see reverse in next lab
b=4.2e-7 # scientific notation for 0.00000042
c=.4e-2 # scientific notation for 0.004
d=3e7 # scientific notation for 30000000
print(a,b,c,d)
e=2+3j # complex number
print(e)
f=3+3j
print(e+f)
print(type(e))
print('hello')
print("hi")
print('''hello''')
print("""hi""") # triple quotes for multi-line strings
print('a \n b \
c')
print('\a')
print('\u1111')
print('hi')
print(r'hi\b') # raw string, ignores escape sequences
print(R'hi\n') # raw string, ignores escape sequences
print(type(True)) # boolean type
print(type(False)) # boolean type
m=n=o=10
print(m,n,o)
m=5
print(m,n,o)
p=400
q=p
print(p,q)
p=200
print(p,q)
import keyword
print(keyword.kwlist) # list of keywords in Python
print(3*3+5/4-2**3) # operator precedence
print(15/2) # float division
print(15//2) # integer division (floor division)
print(15%2) # modulus operator
print(2**3**2) # exponentiation is right associative
print(a>=b)
print(not True)
print((a>=b) and (b<0))
print((a>=b) or (b>0))
print(m is 5)
print(m is not n)
print(m==n)