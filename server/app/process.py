import cv2
from google.cloud import storage
import io
import numpy as np
import os
import urllib
import tensorflow as tf

from app import app, APP_ROOT

# Model configuration
model_path = os.path.join(APP_ROOT, 'catdog.model.h5')
# model_path =  os.path.join("app", "catdog.model.h5")
model = tf.keras.models.load_model( model_path )


def catdog_predict(image_url):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    img_size = 90
    classes = ["Cat","Dog"]
    
    resp = urllib.request.urlopen(image_url)
    image_np = np.asarray(bytearray(resp.read()), dtype="uint8")
    image_raw = cv2.imdecode(image_np, cv2.IMREAD_GRAYSCALE)
    imgage_resized = cv2.resize( image_raw, (img_size, img_size) )

    x_raw = np.array( imgage_resized ).reshape( -1, img_size, img_size, 1)

    # normalizing - 255 possible colors values in each pixel 
    X = x_raw / 255.0

    Y = model.predict(X)

    probs = list( Y[0] )
    max_value = max( probs )
    the_index = probs.index( max_value )
    classification = classes[ the_index ]

    return probs, classification