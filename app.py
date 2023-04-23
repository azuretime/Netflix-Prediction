from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import os
import numpy as np
import yaml
from PIL import Image
import matplotlib.pyplot as plt

webapp_root = "webapp"
params_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.config['UPLOAD_FOLDER'] = static_dir + '/uploads/'

class  Emptymessage(Exception):
    def __init__(self, message="Receive empty data"):
        self.message = message
        super().__init__(self.message)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

# def predict(data):
#     config = read_params(params_path)
#     label_map = config["raw_data_config"]['label_encoding']
#     model_dir_path = config["model_webapp_dir"]
#     model = joblib.load(model_dir_path)
#     prediction = model.predict(data).tolist()[0]
#     str_prediction = [k for k,v in label_map.items() if v == prediction][0]
#     return str_prediction 

def validate_input(dict_request):
    for _, val in dict_request.items():
        if len(val) == 0:
            raise Emptymessage  
    return True

def form_response(dict_request):
    try:
        if validate_input(dict_request):
            data = dict_request.values()
            print('data=============',data)
            response = 'predict(data 7658765876576)'
            return response
    except Emptymessage as e:
        response =  str(e)
        return response 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            if request.form and ('file' in request.files):
                dict_req = dict(request.form)
                response = form_response(dict_req)

                image = request.files['file']
                if image.filename != '':
                    filename = secure_filename(image.filename)
                    print('upload_image filename: ' + filename)
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                type = request.form['type']
                genre = request.form['genre']
                awards_received = request.form['awards_received']
                awards_nominated = request.form['awards_nominated']
                director = request.form['director']
                writer = request.form['writer']
                rating = request.form['rating']

                return render_template("index.html", response=response, filename= filename)
        except Exception as e:
            print(e)
            error = {"error": "Something went wrong!! Try again later!"}
            error = {"error": e}
            return render_template("404.html", error=error)
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/display/<filename>', methods=["GET"])
def display_image(filename):
    return redirect(url_for('static', filename = '/uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)