import numpy as np
import pandas as pd

# Modelling
import os, sys
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from src.utils import save_object


@dataclass
class data_transformation_config:
    preprocessor_obj_file_path = os.path.join('artifacts', 'preprocessor.pkl')

class DataTransformation:
    def __init__(self):
        self.data_transformation_config = data_transformation_config()

    def get_data_transformer_object(self):
        """This function is responsible for transforming the data. It creates a preprocessing pipeline for numeric and categorical features, which includes imputation, scaling, and encoding. The function returns the preprocessor object that can be used to transform the training and testing datasets."""
        logging.info("Entered the data transformation method")
        try:
            numeric_features = ['math_score', 'reading_score', 'writing_score']
            categorical_features = ['gender', 'race_ethnicity', 'parental_level_of_education', 'lunch', 'test_preparation_course']

            '''creating the pipeline for numeric and categorical features'''
            numeric_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler())
            ])
            categorical_transformer = Pipeline(steps=[
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore')),
                ('scaler', StandardScaler(with_mean=False))
            ])

            logging.info("Numeric and Categorical pipeline created successfully")

            preprocessor = ColumnTransformer(
                [("num_pipeline", numeric_transformer, numeric_features),
                ("cat_pipeline", categorical_transformer, categorical_features)])

            return preprocessor
    
        except Exception as e:
            raise CustomException(e, sys)



    def initiate_data_transformation(self, train_path, test_path):
        """This function is responsible for transforming the data. It creates a preprocessing pipeline for numeric and categorical features, which includes imputation, scaling, and encoding. The function returns the preprocessor object that can be used to transform the training and testing datasets."""
        logging.info("Entered the data transformation method")
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            logging.info("Read train and test data completed")

            preprocessing_obj = self.get_data_transformer_object()

            target_colulmn_name = 'average'
            numeric_features = ['math_score', 'reading_score', 'writing_score']

            input_feature_train_df = train_df.drop(columns=[target_colulmn_name])
            target_feature_train_df = train_df[target_colulmn_name]

            input_feature_test_df = test_df.drop(columns=[target_colulmn_name])
            target_feature_test_df = test_df[target_colulmn_name]

            logging.info("Applying preprocessing object on training and testing datasets.")

            input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessing_obj
            )

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )
        except Exception as e:
            raise CustomException(e, sys)


