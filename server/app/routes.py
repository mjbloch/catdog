from flask import render_template, request
import os
from werkzeug.utils import redirect, secure_filename

from app import app, APP_ROOT
from app.process import catdog_predict


upload_folder = os.path.join(APP_ROOT, 'static', 'uploads')
app.config['UPLOAD'] = upload_folder


@app.route('/')
def home():
    return render_template('index.html', title='Home')


@app.route('/predict')
def predict():
    return render_template('predict.html', title='Predict')


@app.route('/about')
def about():
    return render_template('about.html',title='About')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    # Get the uploaded file from the request
    # print(APP_ROOT)
    # target = os.path.join(APP_ROOT, 'static\\uploads\\')
    # print(target)
    if request.method == 'POST':
        file = request.files['img']
        filename = secure_filename(file.filename)
        # file.save("".join([target, filename]))
        file.save(os.path.join(app.config['UPLOAD'], filename))
        # img = os.path.join(app.config['UPLOAD'], filename)
        # print("image: ", img)
        return redirect('/prediction/{}'.format(filename))


@app.route("/prediction/<filename>", methods=['GET', 'POST'])
def prediction(filename):
    prediction_probs, prediction_name = catdog_predict(filename) #imported from process file
    prob_cat = round(prediction_probs[0] * 100, 2)
    prob_dog = round(prediction_probs[1] * 100, 2)
    image_path = 'uploads' + '/' + filename
    return render_template('output.html', prob_cat = prob_cat, prob_dog = prob_dog, name = prediction_name, prediction_image = image_path)