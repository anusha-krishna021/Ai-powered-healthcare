import ast
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, MultiLabelBinarizer

# Load and preprocess data
df = pd.read_csv("Final cleaned dataset.csv")
print("Dataset loaded successfully")

# Parse list-type columns
df['Natural Food'] = df['Natural Food'].apply(ast.literal_eval)
df['Yoga'] = df['Yoga'].apply(ast.literal_eval)
df['Symptom'] = df['Symptom'].apply(lambda x: [s.strip() for s in x.split(',')])

# Initialize encoders
mlb_symptom = MultiLabelBinarizer()
mlb_food = MultiLabelBinarizer()
mlb_yoga = MultiLabelBinarizer()

# Encode features
X = pd.concat([
    df[['Age', 'Height_cm', 'Weight_kg', 'BMI']],
    pd.get_dummies(df[['Gender', 'Blood Type', 'Smoking', 'Alcohol Status']], drop_first=True),
    pd.DataFrame(mlb_symptom.fit_transform(df['Symptom']), columns=mlb_symptom.classes_),
    pd.DataFrame(mlb_food.fit_transform(df['Natural Food']), columns=mlb_food.classes_),
    pd.DataFrame(mlb_yoga.fit_transform(df['Yoga']), columns=mlb_yoga.classes_)
], axis=1)

# Encode target
le = LabelEncoder()
y = le.fit_transform(df['Medical Condition'])

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

# Set up Flask app
app = Flask(__name__)
CORS(app)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    input_dict = {
        'Age': data['Age'],
        'Height_cm': data['Height_cm'],
        'Weight_kg': data['Weight_kg'],
        'BMI': data['BMI']
    }

    # Handle categorical variables
    dummy_cols = pd.get_dummies(df[['Gender', 'Blood Type', 'Smoking', 'Alcohol Status']], drop_first=True).columns
    for col in dummy_cols:
        input_dict[col] = 0

    col_key = f"Gender_{data['Gender']}"
    if col_key in dummy_cols: input_dict[col_key] = 1
    col_key = f"Blood Type_{data['Blood Type']}"
    if col_key in dummy_cols: input_dict[col_key] = 1
    col_key = f"Smoking_{data['Smoking']}"
    if col_key in dummy_cols: input_dict[col_key] = 1
    col_key = f"Alcohol Status_{data['Alcohol Status']}"
    if col_key in dummy_cols: input_dict[col_key] = 1

    # Encode symptoms
    for s in mlb_symptom.classes_:
        input_dict[s] = 1 if s in data['Symptom'] else 0

    # Fill food and yoga features with 0 (not user-provided)
    for f in mlb_food.classes_:
        input_dict[f] = 0
    for y_item in mlb_yoga.classes_:
        input_dict[y_item] = 0

    # Create DataFrame
    input_df = pd.DataFrame([input_dict])
    for col in X.columns:
        if col not in input_df.columns:
            input_df[col] = 0
    input_df = input_df[X.columns]

    # Predict
    prediction = model.predict(input_df)[0]
    predicted_condition = le.inverse_transform([prediction])[0]

    # Get recommended food and yoga from the dataset
    match = df[df['Medical Condition'] == predicted_condition].iloc[0]
    suggested_food = match['Natural Food']
    suggested_yoga = match['Yoga']

    return jsonify({
        'prediction': predicted_condition,
        'suggested_food': suggested_food,
        'suggested_yoga': suggested_yoga
    })

# Ensure this is present and not indented
if __name__ == '__main__':
    print("Starting Flask server on port 5001...")
    app.run(debug=True, port=5001)





