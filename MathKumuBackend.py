from flask import Flask
import flask
import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from os import listdir
from matplotlib import image
from matplotlib import pyplot
import tensorflow as tf
import winsound
import cv2
import numpy as np
import os

app = Flask(__name__)

# variables
first_number = 0
second_number = 0

# creates random addition equations with two numbers for now
@app.route("/equation", methods=['GET'])
def create_equation():
    first_number = np.random.randint(10, 100)
    second_number = np.random.randint(10, 100)
    try: 
        return flask.jsonify(str(first_number) + " + " + str(second_number) + " ="), 201
    except:
        return "", 500

#@app.route("/check", methods=['POST'])
#def check_number(): 


# analyzes the picture of the person's work
@app.route("/analyzer", methods=['POST'])
def analyze():
    try:
        image_data = flask.request.get_data()
        image_vector = np.frombuffer(image_data, dtype=np.uint8) 
        image = cv2.imdecode(image_vector, cv2.IMREAD_COLOR)
        plt.imshow(image)
        plt.show()
        return str(image.shape), 201
    except:
        return "", 500

if __name__ == '__main__':
    app.run()
