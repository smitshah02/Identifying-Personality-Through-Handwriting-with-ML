import pandas as pd
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle

# Read in the dataset
df = pd.read_csv('lists/final_data.csv', names=["BASE_LINE_ANGLE", "TOP_MARGIN", "LINE_SPACING", "SLANT_ANGLE", "WORD_SPACING", "LETTER_SIZE", "Extroversion","Introversion","Emotional_stability","Neuroticism", "Openness_to_experience","Conscientiousness","Agreeableness", "file_name"])

# Define the target variable names and corresponding features
targets = {"Extroversion": ["LETTER_SIZE", "SLANT_ANGLE", "WORD_SPACING", "TOP_MARGIN", "LINE_SPACING"],
           "Introversion": ["LETTER_SIZE", "SLANT_ANGLE", "WORD_SPACING", "TOP_MARGIN", "LINE_SPACING"],
           "Emotional_stability": ["BASE_LINE_ANGLE", "WORD_SPACING"],
           "Neuroticism": ["BASE_LINE_ANGLE", "SLANT_ANGLE"],
           "Openness_to_experience": ["LETTER_SIZE", "SLANT_ANGLE", "WORD_SPACING", "LINE_SPACING"],
           "Conscientiousness": ["LETTER_SIZE", "WORD_SPACING", "TOP_MARGIN"],
           "Agreeableness": ["LETTER_SIZE", "SLANT_ANGLE", "WORD_SPACING", "LINE_SPACING"]}

# Train and save a separate model for each target variable
for target, features in targets.items():
    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

    # Train the model
    reg = HistGradientBoostingRegressor()
    reg.fit(X_train, y_train)

    # Test the model
    y_pred = reg.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    print(f"Mean Squared Error of {target}: {mse}")

    # Save the model using pickle
    with open(f"new_model/{target}_model.pickle", "wb") as f:
        pickle.dump(reg, f)
