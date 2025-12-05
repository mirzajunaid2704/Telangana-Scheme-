import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
df = pd.read_csv("data.csv")

# Encode categorical columns
le_caste = LabelEncoder()
df["caste"] = le_caste.fit_transform(df["caste"])

le_district = LabelEncoder()
df["district"] = le_district.fit_transform(df["district"])

le_scheme = LabelEncoder()
df["scheme"] = le_scheme.fit_transform(df["scheme"])

# Save encoders for later
pickle.dump(le_caste, open("le_caste.pkl", "wb"))
pickle.dump(le_district, open("le_district.pkl", "wb"))
pickle.dump(le_scheme, open("le_scheme.pkl", "wb"))

# Features and target
X = df.drop("scheme", axis=1)
y = df["scheme"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("model.pkl", "wb"))

print("Model trained and saved successfully!")