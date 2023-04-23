from flask import Flask, redirect, render_template, request, url_for
from werkzeug.utils import secure_filename
import os
from predict import predict_votes, predict_score, getImgFeatures
webapp_root = "webapp"

static_dir = os.path.join(webapp_root, "static")
template_dir = os.path.join(webapp_root, "templates")

app = Flask(__name__, static_folder=static_dir, template_folder=template_dir)
app.config['UPLOAD_FOLDER'] = static_dir + '/uploads/'

class  Emptymessage(Exception):
    def __init__(self, message="Receive empty data"):
        self.message = message
        super().__init__(self.message)

def validate_input(dict_request):
    for _, val in dict_request.items():
        if len(val) == 0:
            raise Emptymessage  
    return True

def form_response(dict_request):
    try:
        if validate_input(dict_request) and ('file' in request.files):
            data = list(dict_request.values())
            print('data=============',data)

            image = request.files['file']
            file_path = ''
            if image.filename != '':
                filename = secure_filename(image.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                image.save(file_path)
            
            features_popularity, features_quality = getImgFeatures(file_path)
            popularity = predict_votes(data, features_popularity)
            quality = 'High'
            response = 'Popularity: ' + popularity +'\n' + 'Quality: ' + quality
            return response, filename
    except Emptymessage as e:
        response =  str(e)
        return response 

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # try:
            if request.form and ('file' in request.files):
                dict_req = dict(request.form)
                response, filename = form_response(dict_req)

                return render_template("index.html", response=response, filename= filename)
        # except Exception as e:
        #     print(e)
        #     error = {"error": "Something went wrong!! Try again later!"}
        #     error = {"error": e}
        #     return render_template("404.html", error=error)
    else:
        return render_template("index.html")
    return render_template("index.html")

@app.route('/display/<filename>', methods=["GET"])
def display_image(filename):
    return redirect(url_for('static', filename = '/uploads/' + filename), code=301)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)