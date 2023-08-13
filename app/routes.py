from datetime import timedelta
from flask import render_template, request
from google.cloud import storage
import os
from werkzeug.utils import redirect, secure_filename

from app import app, APP_ROOT
from app.process import catdog_predict


# FOR LOCAL TESTING ONLY
# credentials = "catdog-395720-fda24c2997ae.json"
# bucket_name = "catdog-images"
# storage_client = storage.Client.from_service_account_json(credentials, project='catdog-395720')

bucket_name = os.environ.get("BUCKET_NAME")
project_id = os.environ.get("PROJECT_ID")
storage_client = storage.Client(project=project_id)


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
    if request.method == 'POST':
        image = request.files['img']
        filename = secure_filename(image.filename)
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.upload_from_string(image.read(), content_type=image.content_type)
        return redirect('/prediction/{}'.format(filename))


@app.route("/prediction/<filename>", methods=['GET', 'POST'])
def prediction(filename):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(filename)
    image_url = blob.generate_signed_url(
        expiration = timedelta(minutes=5),
        method='GET'
    )
    prediction_probs, prediction_name = catdog_predict(image_url) #imported from process file
    prob_cat = round(prediction_probs[0] * 100, 2)
    prob_dog = round(prediction_probs[1] * 100, 2)
    return render_template('output.html', prob_cat = prob_cat, prob_dog = prob_dog, name = prediction_name, prediction_image = image_url)