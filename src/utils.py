
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import os
import sys
import pickle
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV


def save_object(file_path, obj):
    """This function saves a Python object to a file using pickle."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
    except Exception as e:
        raise CustomException(e, sys)


def evaluate_model(X_train, y_train, X_test, y_test, models, params=None):
    """This function evaluates multiple machine learning models and returns their R2 scores."""
    try:
        report = {}
        for i in range(len(models)):
            model = list(models.values())[i]
            param = params.get(list(models.keys())[i]) if params else None

            if param:
                gs = GridSearchCV(model, param, cv=5, n_jobs=-1, verbose=0)
                gs.fit(X_train, y_train)
                model.set_params(**gs.best_params_)  # Set the best parameters found by GridSearchCV
                model.fit(X_train, y_train)  # Fit the model with the best parameters
            else:
                model.fit(X_train, y_train)

            y_test_pred = model.predict(X_test)  # Predict on test data
            test_model_score = r2_score(y_test, y_test_pred)  # Calculate R2 score
            report[list(models.keys())[i]] = test_model_score  # Store the score in the report
        return report
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path):
    """This function loads a Python object from a file using pickle."""
    try:
        with open(file_path, 'rb') as file_obj:
            return pickle.load(file_obj)
    except Exception as e:
        raise CustomException(e, sys)