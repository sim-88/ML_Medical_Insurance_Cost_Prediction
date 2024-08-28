import pickle
from flask import Flask, render_template, request, send_from_directory
import pandas as pd

app = Flask(__name__)

# Load the pickled model
with open('medical1.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory(app.root_path + '/static/', filename)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction = None
    if request.method == 'POST':
        try:
            # Get user input from the form
            age = int(request.form['age'])
            sex = int(request.form['sex'])
            bmi = float(request.form['bmi'])
            children = int(request.form['children'])
            smoker = int(request.form['smoker'])
            region = int(request.form['region'])

            # Make prediction
            data = {'age': age, 'sex': sex, 'bmi': bmi, 'children': children, 'smoker': smoker, 'region': region}
            df_data = pd.DataFrame(data, index=[0])
            prediction = model.predict(df_data)[0]
        except Exception as e:
            return render_template('error.html', error=str(e))
    return render_template('index.html', prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)


