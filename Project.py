import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the dataset with caching
@st.cache_data
def load_data():
    data = pd.read_csv('car_crashes.csv')
    return data

data = load_data()

# Preprocess the data
def preprocess_data(data):
    # Convert categorical variables to numeric
    data['Weather_Condition'] = data['Weather_Condition'].astype('category').cat.codes
    data['Road_Condition'] = data['Road_Condition'].astype('category').cat.codes
    return data

data = preprocess_data(data)

# Streamlit UI
st.title("🚗 Car Crash Dashboard")

# Display the dataset
if st.checkbox("Show raw data"):
    st.subheader("Raw Dataset")
    st.write(data)

# Display summary statistics
st.subheader("📊 Summary Statistics")
st.write(data.describe())

# Histogram of Injury Count
st.subheader("📉 Histogram of Injury Count")
fig1, ax1 = plt.subplots()
data['Injury_Count'].hist(ax=ax1, bins=30)
ax1.set_title('Injury Count Distribution')
ax1.set_xlabel('Injury Count')
ax1.set_ylabel('Frequency')
st.pyplot(fig1)

# Pie chart of crash severity
st.subheader("🧩 Pie Chart of Crash Severity")
severity_counts = data['Severity'].value_counts()
fig2, ax2 = plt.subplots()
ax2.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', startangle=90)
ax2.axis('equal')
st.pyplot(fig2)

# Machine Learning Model
st.subheader("🤖 Predicting Crash Severity")

# Define features and label
X = data[['Weather_Condition', 'Road_Condition', 'Injury_Count']]
y = data['Severity']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Evaluate model
accuracy = model.score(X_test, y_test)
st.write(f"**Model Accuracy:** {accuracy:.2f}")
