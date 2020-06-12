from flask import Flask
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
first_number = np.random.randint(10, 100)
second_number = np.random.randint(10, 100)

# creates random addition equations with two numbers for now
@app.route("/equation", methods=['GET'])
def create_equation():
    try: 
        return jsonify(str(first_number) + " + " + str(second_number)), 201
    except:
        return "", 500

#@app.route("/check", methods=['POST'])
#def check_number(): 


# analyzes the picture of the person's work
@app.route("/analyzer", methods=['POST'])
def analyze():
    try:
        return "", 201
    except:
        return "", 500
