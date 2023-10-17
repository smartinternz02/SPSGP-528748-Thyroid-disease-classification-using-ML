from flask import Flask,render_template,request
import numpy as np
import pickle
import pandas as pd
import uuid
model=pickle.load(open(r"C:\Users\lenovo\Intenship Project\flask\thyroid1_model.pkl",'rb'))
le=pickle.load(open(r"C:\Users\lenovo\Intenship Project\flask\label_encoder.pkl",'rb'))
lef=pickle.load(open(r"C:\Users\lenovo\Intenship Project\flask\label_encoder_y.pkl",'rb'))
app=Flask(__name__)
@app.route("/")
def about():
    return render_template('home.html')

@app.route('/home', methods=['POST','GET'])
def home():
    return render_template('home.html')

@app.route('/predict', methods=['POST','GET'])
def predict():
    return render_template('predict.html')

@app.route('/submit', methods=['POST','GET'])
def submit():
    if request.method == 'POST':
        data = []

        Goitre = request.form['Goitre']
        Tumor = request.form['Tumor']
        Hypopituitary = request.form['Hypopituitary']
        Psych = request.form['Psych']

        data.extend([1 if val == 't' else 0 for val in [Goitre, Tumor, Hypopituitary, Psych]])

        num = ['TSH_VAL', 'T3_VAL', 'TT4_VAL', 'T4U_VAL', 'FTI_VAL', 'TBG_VAL']
        for i in num:
            data.append(float(request.form[i]))

        col = ['goitre', 'tumor', 'hypopituitary', 'psych', 'TSH', 'T3', 'TT4', 'T4U', 'FTI', 'TBG']
        x = pd.DataFrame([data], columns=col)
        pred = model.predict(x)
        diagnoses = {
            0: "antithyroid treatment",
            1: "binding protein",
            2: "general health",
            3: "hyperthyroid",
            4: "hypothyroid",
            5: "miscellaneous",
            6: "replacement therapy"
        }
        prediction_text = diagnoses.get(pred[0], "unknown")

        return render_template('submit.html', prediction_text=prediction_text)


if __name__ == "__main__":
    app.run(debug=True)
