import os
import sys
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR 
from sklearn.neighbors import KNeighborsRegressor
from catboost import CatBoostRegressor
from xgboost import XGBRegressor
from src.utils import save_object, evaluate_model
from sklearn.metrics import r2_score


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join('artifacts', 'model.pkl')

class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1]
            )

            models = {
                "Linear Regression": LinearRegression(),
                "Ridge Regression": Ridge(),
                "Lasso Regression": Lasso(),
                "Decision Tree": DecisionTreeRegressor(),
                "Random Forest": RandomForestRegressor(),
                "AdaBoost": AdaBoostRegressor(),
                "Support Vector Regressor": SVR(),
                "K-Nearest Neighbors": KNeighborsRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "XGBoost Regressor": XGBRegressor()
            }

            params = {
                "Linear Regression": {"fit_intercept": [True, False]},
                "Ridge Regression": {"alpha": [0.01, 0.1, 1, 10, 100]},
                "Lasso Regression": {"alpha": [0.01, 0.1, 1, 10, 100]},
                "Decision Tree": {"max_depth": [None, 5, 10,    15], "min_samples_split": [2, 5, 10]}, 
                "Random Forest": {"n_estimators": [100, 200, 300], "max_depth": [None, 5, 10]},
                "AdaBoost": {"n_estimators": [50, 100, 200], "learning_rate": [0.1, 0.5, 1.0]},
                "Support Vector Regressor": {"C": [0.1, 1, 10], "gamma": ["scale", "auto"]},
                "K-Nearest Neighbors": {"n_neighbors": [3, 5, 7], "weights": ["uniform", "distance"]},
                "CatBoost Regressor": {"iterations": [100, 200, 300], "learning_rate": [0.1, 0.2, 0.3]},
                "XGBoost Regressor": {"n_estimators": [100, 200, 300], "learning_rate": [0.1, 0.2, 0.3]}
            }
            model_report:dict = evaluate_model(X_train, y_train, X_test, y_test, models, params=params)

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]
            best_model = models[best_model_name]

            logging.info(f"Best model found: {best_model_name} with R2 score: {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)

            r2_square = r2_score(y_test, predicted)
            return r2_square

        
        except Exception as e:
            raise CustomException(e, sys)