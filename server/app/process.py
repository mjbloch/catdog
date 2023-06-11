import cv2
import tensorflow as tf
import numpy as np
import os

from app import app, APP_ROOT

# Model configuration
model = tf.keras.models.load_model( "catdog.model.h5" )


def catdog_predict(filename):
    tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)

    img_size = 90
    classes = ["Cat","Dog"]
    
    target = os.path.join(app.config['UPLOAD'], filename)

    raw_image = cv2.imread( target, cv2.IMREAD_GRAYSCALE )
    img_resized = cv2.resize( raw_image, (img_size, img_size) )

    x_raw = np.array( img_resized ).reshape( -1, img_size, img_size, 1)

    # normalizing - 255 possible colors values in each pixel 
    X = x_raw / 255.0

    Y = model.predict(X)

    probs = list( Y[0] )
    max_value = max( probs )
    the_index = probs.index( max_value )
    classification = classes[ the_index ]

    return probs, classification