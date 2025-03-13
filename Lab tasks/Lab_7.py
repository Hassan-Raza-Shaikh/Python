import pandas as pd

dat = pd.read_csv("Data.csv") 

null_values = dat.isnull()
print(null_values)

dat.fillna(0, inplace=True)
print(dat)

s = dat.Salary.sum()
print(s)

uni = dat.Country.unique()
print(uni)