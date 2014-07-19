'''
Created on Jul 19, 2014

@author: shah
'''

import os
import json
from flask import Flask, request, render_template
import predictor

app = Flask(__name__)

@app.route("/predict", methods=['GET'])
def predict():
    sex = request.args["sex"]
    age = request.args["age"]
    beh_id = request.args["beh_id"]
    zip_code = request.args["zip_code"]

    ans = predictor.predict(sex, age, beh_id, zip_code)
    return json.dumps(ans)

@app.route("/")
def input():
    return render_template("input.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)