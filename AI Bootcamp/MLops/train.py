import pandas as pd
from sklearn.tree import DecisionTreeClassifier

# 1. Create dataset directly in the file
data = {
    'Hours_Studied': [1, 2, 3, 4, 5, 6, 7, 8],
    'Passed':        [0, 0, 0, 0, 1, 1, 1, 1]
}

df = pd.DataFrame(data)

# 2. Separate features (X) and target (y)
X = df[['Hours_Studied']]
y = df['Passed']

# 3. Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# 4. Predict
test_data = pd.DataFrame({'Hours_Studied': [6.5]})
prediction = model.predict(test_data)

print("Prediction for 6.5 hours studied (1 = Pass, 0 = Fail):", prediction[0])
