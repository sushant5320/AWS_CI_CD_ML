from flask import Flask, request, render_template
import pandas as pd
import numpy as np
from src.pipeline.predict_pipeline import CustomData, PredictPipeline
from sklearn.preprocessing import StandardScaler


application = Flask(__name__)
app = application


@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'GET':
        return render_template('home.html')
    else:
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('race_ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            math_score=float(request.form.get('math_score')),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )

        input_df = data.get_data_as_dataframe()

        # Make predictions
        predict_pipeline = PredictPipeline()
        prediction = predict_pipeline.predict(input_df)

        return render_template('home.html', prediction=prediction[0])
   


if __name__ == "__main__":
    app.run(host="0.0.0.0")