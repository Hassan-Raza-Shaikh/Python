import pandas as pd
import matplotlib.pyplot as plt

#Task 1

data=pd.read_csv('train.csv')
print(data.head(10))
print(data.tail(10))
print(data.isnull().sum())
print(data.duplicated().sum())
print(data.drop_duplicates(inplace=True))
print(data.dropna(inplace=True))
print(data.dtypes)
print(data.nunique())

#Task 2

plt.scatter(data['Age'], data['Fare'], alpha=0.5)
plt.xlabel('Age')
plt.ylabel('Fare')
plt.title('Age vs Fare')
plt.show()

#Task 3


survived_counts = data['Survived'].value_counts()
plt.bar(survived_counts.index, survived_counts.values, color=['red', 'green'])
plt.xticks([0, 1], ['Not Survived', 'Survived'])
plt.title('Survival Count')
plt.ylabel('Count')
plt.show()


#Task 4

male_survived = data[data['Sex'] == 'male']['Survived'].value_counts()

female_survived = data[data['Sex'] == 'female']['Survived'].value_counts()

labels = ['Not Survived', 'Survived']

x = [0, 1]

width = 0.35

plt.bar([i - width/2 for i in x], male_survived.sort_index(), width=width, label='Male', color='blue')
plt.bar([i + width/2 for i in x], female_survived.sort_index(), width=width, label='Female', color='pink')

plt.xticks(x, labels)
plt.ylabel('Count')
plt.title('Survival by Gender')
plt.legend()
plt.show()

