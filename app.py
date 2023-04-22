from flask import Response, Response, Response, Response, Flask, render_template, request, jsonify, send_from_directory, url_for
from flask_uploads import UploadSet,IMAGES, configure_uploads
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileField, FileAllowed
from wtforms import SubmitField
import os
import numpy as np
import yaml
import joblib 

webapp_root = "webapp"
params_path = "params.yaml"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.config['SECRET_KEY'] = 'keyfjdchtfjyu'
app.config['UPLOADED_PHOTOS_DEST'] = 'uploads'

photos = UploadSet('photos',IMAGES)
configure_uploads(app, photos)

global response
response = 'response'
global file_url
file_url = 'file_url'

class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos, 'Only images are allowed'),
            FileRequired('File field should not be empty')
        ]
    )
    submit = SubmitField('Upload')


class  Emptymessage(Exception):
    def __init__(self, message="Receive empty data"):
        self.message = message
        super().__init__(self.message)

def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def predict(data):
    config = read_params(params_path)
    label_map = config["raw_data_config"]['label_encoding']
    model_dir_path = config["model_webapp_dir"]
    model = joblib.load(model_dir_path)
    prediction = model.predict(data).tolist()[0]
    str_prediction = [k for k,v in label_map.items() if v == prediction][0]
    return str_prediction 

def validate_input(dict_request):
    for _, val in dict_request.items():
        if len(val) == 0:
            raise Emptymessage  
    return True

def form_response(dict_request):
    try:
        if validate_input(dict_request):
            data = dict_request.values()
            response = 'predict(data)'
            return response
    except Emptymessage as e:
        response =  str(e)
        return response 

# @app.route("/", methods=["GET", "POST"])
# def index():
#     if request.method == "POST":
#         try:
#             if request.form:
#                 dict_req = dict(request.form)
#                 response = form_response(dict_req)
#                 return render_template("index.html", response=response)
#         except Exception as e:
#             print(e)
#             error = {"error": "Something went wrong!! Try again later!"}
#             error = {"error": e}
#             return render_template("404.html", error=error)
#     else:
#         return render_template("index.html")

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(app.config['UPLOADED_PHOTOS_DEST'], filename)

@app.route("/", methods=["GET", "POST"])
def upload_image():
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        file_url = url_for('get_image', filename = filename)
    else:
        file_url = None 

    # if request.form:
    #     dict_req = dict(request.form)
    #     global response
    #     response = form_response(dict_req)

    return render_template("index.html", form=form, file_url = file_url)
    # if request.method == "POST":
    #     try:
    #         form = UploadForm()
    #         if form.validate_on_submit():
    #             filename = photos.save(form.photo.data)
    #             file_url = url_for('get_image', filename = filename)
    #         else:
    #             file_url = None 

    #         if request.form:
    #             dict_req = dict(request.form)
    #             response = form_response(dict_req)
    #             return render_template("index.html", response=response)
    #         return render_template("index.html", form=form, file_url = file_url)
    #     except Exception as e:
    #         print(e)
    #         error = {"error": "Something went wrong!! Try again later!"}
    #         error = {"error": e}
    #         return render_template("404.html", error=error)
    # else:
    #     return render_template("index.html")    

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)