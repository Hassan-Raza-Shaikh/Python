#Task 1

l = [4,2,9,4,2,1,8,3,9]
i = 0
while i<len(l):
    j= i+1
    while j<len(l):
        if l[i]==l[j]:
            del(l[j])
        else:
            j+=1
    i+=1
print(l)

l = [4,2,9,4,2,1,8,3,9]
unique_list = []
for num in l:
    if num not in unique_list:
        unique_list.append(num)
print(unique_list)

l = list(dict.fromkeys([4,2,9,4,2,1,8,3,9]))
l.sort()
print(l)

#Task 2

t =(7,2,9,1,5,3)
print(max(t))
print(min(t))
print(sum(t))
t=list(t)
t.sort()
t=tuple(t)
print(t)

#Task 3

sentence = input()
vowels = 0
consonants = 0
for x in sentence:
    if x.isalpha():
        if x.lower() in ('a','e','i','o','u'):
            vowels+=1
        else:
            consonants+=1
print(vowels)
print(consonants)

#Task 4

list_a= [1,2,3,4,5]
list_b= [4,5,6,7,8]
s1= set(list_a)
s2= set(list_b)
common = s1 & s2
print(common)
union= s1 | s2
print(union)
unique_1=s1-s2
unique_2=s2-s1
print(unique_1)
print(unique_2)

#Task 5

for i in range(1,6):
    for j in range(1,6):
        print(i*j, end= '\t')
    print(end= '\n')