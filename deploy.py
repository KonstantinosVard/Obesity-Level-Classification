from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)

model = pickle.load(open("best_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

weight_category_mapping = {
    0: "Insufficient Weight (1/7)",
    1: "Normal Weight (2/7)",
    2: "Overweight I (3/7)",
    3: "Overweight II (4/7)",
    4: "Obese I (5/7)",
    5: "Obese II (6/7)",
    6: "Obese III (7/7)"
}

@app.route("/")
def home():
    result = ""
    return render_template("index.html", **locals())

@app.route("/predict", methods=["POST", "GET"])
def predict():
    result = ""
    if request.method == "POST":
        height = float(request.form['Height'])
        weight = float(request.form['Weight'])

        # Use the same column names as used during model training
        input_data = pd.DataFrame([[height, weight]], columns=["Height", "Weight"])

        # Scale and predict
        scaled_input = scaler.transform(input_data)
        prediction = model.predict(scaled_input)
        
        # Map prediction to category
        result = weight_category_mapping.get(prediction[0], "Unknown Category")

    return render_template("index.html", result=result)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host = '0.0.0.0', port=5000)