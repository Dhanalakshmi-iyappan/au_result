# -*- coding: utf-8 -*-
"""au_result.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lI4j67gw7xPz9eStwWN07GNO7WImo2Ht
"""

# Install required packages if not already installed
!pip install xgboost lightgbm catboost scikit-learn pandas

import pandas as pd
import ast

# Load the dataset
df = pd.read_csv("au_result_data.csv")

# Convert the `res` column from string to dictionary
df["res"] = df["res"].apply(ast.literal_eval)

# Expand the grade dictionary into individual subject columns
grades_df = pd.json_normalize(df["res"])

# Combine expanded grade columns with the original dataframe
df_expanded = pd.concat([df, grades_df], axis=1)

# Drop unnecessary columns
df_expanded.drop(columns=["Unnamed: 0", "res", "studentdetail"], inplace=True)

# 1. Convert grade strings to numeric using safe mapping
grade_map = {
    "O": 10, "A+": 9, "A": 8, "B+": 7, "B": 6,
    "C": 5, "D": 4, "E": 3, "U": 0, "UA": 0, "W": 0,
    "RA": 0, "AB": 0, "": 0, "NA": 0
}
df_numeric = df_expanded.applymap(lambda x: grade_map.get(x, 0))

df_numeric["label"] = df_numeric.apply(lambda row: 1 if (row >= 5).all() else 0, axis=1)

# Optional: Check balance of classes
print(df_numeric["label"].value_counts())

# 3. Train-test split
from sklearn.model_selection import train_test_split

X = df_numeric.drop(columns=["label"])
y = df_numeric["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from sklearn.model_selection import train_test_split

X = df_numeric.drop(columns=["label"])
y = df_numeric["label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

from xgboost import XGBClassifier
from sklearn.ensemble import AdaBoostClassifier
from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

models = {
    "XGBoost": XGBClassifier(use_label_encoder=False, eval_metric='logloss'),
    "AdaBoost": AdaBoostClassifier(),

}

# Train and evaluate all models
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"{name} Accuracy: {acc:.4f}")

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from sklearn.metrics import accuracy_score

# Initialize CatBoost and LightGBM models
additional_models = {
    "CatBoost": CatBoostClassifier(verbose=0),
    "LightGBM": LGBMClassifier()
}

# Train and evaluate the models
for name, model in additional_models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)
    print(f"{name} Accuracy: {acc:.4f}")