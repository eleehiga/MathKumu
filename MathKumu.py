import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
from os import listdir
from matplotlib import image
from matplotlib import pyplot
import tensorflow as tf
#from ipywidgets import IntProgress
#from IPython.display import display
import winsound
import cv2
import numpy as np
import os

image = cv2.imread('testequations/testequation6.png')

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Array of initial bounding rects
rects = []

# Bool array indicating which initial bounding rect has
# already been used
rectsUsed = []

# Just initialize bounding rects and set all bools to false
for cnt in cnts:
    rects.append(cv2.boundingRect(cnt))

for rect in rects:
    #img = cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (121, 11, 189), 2)
    img = cv2.rectangle(image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (255,255,255), 2)
plt.imshow(img)
plt.show()
# cropping the image 
img_symbols = list()
for rect in rects:
    crop_img = img[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
    img_symbols.append(crop_img)
value=[255,255,255]
imgs_final = list()
for img_symbol in img_symbols:
    if img_symbol.shape[0] > img_symbol.shape[1]:
        top = 10
        bottom = top
        left = int(((img_symbol.shape[0] + top + bottom) - img_symbol.shape[1]) / 2)
        right = left
    else:
        left = 10
        right = left
        top = int(((img_symbol.shape[1] + left + right) - img_symbol.shape[0]) / 2)
        bottom = top
    img_border = cv2.copyMakeBorder(img_symbol, top, bottom, left, right, cv2.BORDER_CONSTANT,None, value)
    if img_border.ndim == 3:
        imgs_final.append(img_border[:,:,0]) # remove rgb channel
    else:
        imgs_final.append(img_border)

# Predict label of image
class_labels = ['0','1','2','3','4','5','6','7','8','9'] + ['plus','-','times']
model = tf.keras.models.load_model('math_reader_2.model')    # Here loads the model, make sure to turn off when not needed


pred_images = list()

for img_data in imgs_final: 
    img_data = cv2.resize(img_data, dsize=(45,45),interpolation=cv2.INTER_CUBIC)
    #print(img_data.shape)
    pred_images.append(img_data)

pred_images = tf.keras.utils.normalize(pred_images, axis=1)
pred_images = tf.convert_to_tensor(pred_images, dtype=tf.float32)
pred_images = tf.reshape(pred_images, [-1,45,45,1])

probability_labels = model.predict(pred_images)
labels = list()
for i in range(0, len(pred_images)):
    labels.append(class_labels[np.argmax(probability_labels[i])])
    print(labels[i])
    plt.imshow(tf.squeeze(pred_images[i]))
    plt.show()
# put information of character's center coordinates and its label into an array
characters = []
for i in range(len(pred_images)):
    characters.append([0] * 2)

symbols_num = 0
symbols = list()
for i in range(len(pred_images)):
    characters[i].append(labels[i])
    characters[i][0] = int(rects[i][0] + rects[i][2] / 2)
    characters[i][1] = int(rects[i][1] + rects[i][3] / 2)
    if characters[i][2] in ['plus', 'times', '-']:
        symbols_num += 1
        symbols.append(characters[i])
def getYFromChar(item):
    return item[1]
symbols.sort(key = getYFromChar)
print(symbols)
operators = list()
operators.append(symbols[0])
lines  = list()
lines.append(symbols[1])
print(lines)
print(operators)
# with big character list, organize into layers
y_thresh = 20
x_thresh = 30
row = np.zeros(len(characters), dtype=int)
col = np.zeros(len(characters), dtype=int)
def getYFromChar(item):
    return item[1]
characters.sort(reverse = True, key = getYFromChar)
#compare next char to first, layer higher the layer number the more up it is
for i in range(0,len(characters)-1):
    if np.absolute(characters[i + 1][1] - characters[i][1]) < y_thresh:
        row[i + 1] = row[i]
    elif characters[i + 1][1] - characters[i][1] <= y_thresh:
        row[i + 1] = row[i] + 1
def getXFromChar(item):
    return item[0]
characters.sort(reverse = False, key = getXFromChar)
characters.remove(lines[0])
for i in range(len(characters)-1):
    if np.absolute(characters[i + 1][0] - characters[i][0]) < x_thresh:
        col[i + 1] = col[i]
    elif characters[i + 1][0] - characters[i][0] >= x_thresh:
        col[i + 1] = col[i] + 1
characters.append(lines[0])
# do not care about line column values
i = 0
for c in col:
    characters[i].append(c)
    i += 1
i = 0
characters.sort(reverse = True, key = getYFromChar)
for r in row:
    characters[i].insert(3, r)
    if characters[i][0:3] == lines[0]:
        lines[0] = characters[i]
    elif characters[i][2] in ['plus', '-', 'times']:
        operators[0] = characters[i]
    i += 1
def getColFromChar(item):
    return item[4]
def getRowFromChar(item):
    return item[3]
max_row = row[len(characters)-1]
max_col = col[len(characters)-1-len(lines)] # not care about last one because that is the position of the lines
#If addition
if operators[0][2] == 'plus':
    # check if rightmost numbers added up are equalling what they are supposed to
    characters.sort(reverse = True, key = getRowFromChar)
    characters.sort(reverse = True, key = getColFromChar)
    print(characters)
    c_num = max_col
    sum_col = 0
    prev_sum = 0
    have_nums_to_use = False
    for character in characters:
        if character[4] == c_num and not(character[2] in ['plus', '-', 'times']) and character[3] > lines[0][3]:
            sum_col += int(character[2])
            #print(sum_col)
            have_nums_to_use = True
        elif character[4] == c_num and not(character[2] in ['plus', '-', 'times']) and character[3] < lines[0][3]:
            sum_check = int(character[2])
            #print(sum_check)
            if sum_col % 10 != sum_check and have_nums_to_use:
                print('Error when adding in column ' + str(c_num))
            have_nums_to_use = False
            prev_sum = sum_col
            sum_col = 0
        elif not(character[2] in ['plus', '-', 'times']):
            c_num = character[4]
            #print(c_num)
            if character[3] < lines[0][3] and sum_col == 0 and int(prev_sum / 10) != int(character[2]):
                print('Error in leftmost column')
            sum_col += int(character[2])
