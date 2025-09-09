import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

data = pd.read_csv("Heart.csv")
data.dropna()
x = data.iloc[:, :7]
y=data["HeartDisease"]
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
model=RandomForestClassifier()
model.fit(X_train,y_train)
y_predicted=model.predict(X_test)
print(classification_report(y_test, y_predicted))
print(confusion_matrix(y_test, y_predicted))
