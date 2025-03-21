for i in range(0,10):
    print('*'*i)
l=5
for j in range(1,10,2):
    for k in range(l,0,-1):
        print(' ',end='')
    l-=1
    print('#'*j)