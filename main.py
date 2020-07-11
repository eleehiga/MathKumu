from flask import Flask
import flask
import cv2
import numpy as np
from matplotlib import pyplot as plt
import tensorflow as tf

app = Flask(__name__)

@app.route('/')
def index():
        #return flask.render_template("index.html")
        return 'Aloha Math Kumu!'

# creates random addition equations with two numbers for now
@app.route("/equation", methods=['GET','POST'])
def create_equation():
    first_number = np.random.randint(10, 100)
    second_number = np.random.randint(10, 100)
    try: 
        type_json = flask.request.get_json()
        if type_json['type'] == "Addition":
            return flask.jsonify(equation = str(first_number) + " + " + str(second_number) + " =",
                                 numbers = [first_number,second_number]), 201
        return "Error", 201
    except:
        return "Error", 500

@app.route("/check", methods=['GET', 'POST'])
def check_number(): 
    try:
        message = "Error"
        check_json = flask.request.get_json() 
        type_equation = check_json['type']
        first_number = check_json['numbers'][0]
        second_number = check_json['numbers'][1]
        answer_number = check_json['answer']
        if type_equation == "Addition":
            if first_number + second_number == int(answer_number):
                message = "Correct"
            else:
                message = "Wrong"
        return str(message), 201
    except:
        return "Error", 500


# analyzes the picture of the person's work
@app.route("/analyzer", methods=['GET','POST'])
def analyze():
    try:
        message = "error" # message to put in json file 

        # works with any image file format
        image_data = flask.request.get_data()
        image_vector = np.frombuffer(image_data, dtype=np.uint8) 
        image = cv2.imdecode(image_vector, cv2.IMREAD_COLOR)
        #plt.imshow(image)
        #plt.show()
        # here is the logic part of the code
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        cnts, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Array of initial bounding rects
        rects = []

        # Finds bounding boxes
        for cnt in cnts:
            rects.append(cv2.boundingRect(cnt)) 
        # cropping the image 
        img_symbols = list()
        for rect in rects:
            crop_img = image[rect[1]:rect[1]+rect[3], rect[0]:rect[0]+rect[2]]
            img_symbols.append(crop_img)
        value=[255,255,255]
        imgs_final = list()
        for img_symbol in img_symbols: #makes the image into a square with adding padding in order to do that
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
            pred_images.append(img_data)

        pred_images = tf.keras.utils.normalize(pred_images, axis=1)
        pred_images = tf.convert_to_tensor(pred_images, dtype=tf.float32)
        pred_images = tf.reshape(pred_images, [-1,45,45,1])

        probability_labels = model.predict(pred_images)
        labels = list()
        for i in range(0, len(pred_images)):
            labels.append(class_labels[np.argmax(probability_labels[i])])
        # put information of character's center coordinates and its label into an array
        characters = []
        for i in range(len(pred_images)):
            characters.append([0] * 4)

        symbols_num = 0
        symbols = list()
        for i in range(len(pred_images)):
            characters[i].append(labels[i])
            characters[i][0] = int(rects[i][0])
            characters[i][1] = int(rects[i][1])
            characters[i][2] = int(rects[i][2])
            characters[i][3] = int(rects[i][3])
            if characters[i][4] in ['plus', 'times', '-']:
                symbols_num += 1
                symbols.append(characters[i])
        def getYFromChar(item):
            return item[1]
        symbols.sort(key = getYFromChar)
        operators = list()
        lines  = list()
        try:
            operators.append(symbols[0])
            lines.append(symbols[1])
        except:
            message = "Mistake: operator and/or line missing"
            work = [["Error", "Error"], ["Error","Error"]]
            response = flask.jsonify({"work": work, "message": message})
            return response, 201
        # see if intervals line up with each other
        row = np.zeros(len(characters), dtype=int)
        col = np.zeros(len(characters), dtype=int)
        def getYFromChar(item):
            return item[1]
        characters.sort(reverse = True, key = getYFromChar)
        interval_x = lambda j : [int(characters[j][0] + characters[j][2] * 0.1), int(characters[j][0] + characters[j][2] * 0.9)]
        interval_y = lambda j : [int(characters[j][1]  + characters[j][3] * 0.1), int(characters[j][1] + characters[j][3] * 0.9)]

        #compare next char to first, layer higher the layer number the more up it is
        for i in range(0,len(characters)-1):
            if not(interval_y(i + 1)[1] < interval_y(i)[0] or interval_y(i + 1)[0] > interval_y(i)[1]):
                row[i + 1] = row[i]
            else:
                row[i + 1] = row[i] + 1
        def getXFromChar(item):
            return item[0]
        characters.sort(reverse = False, key = getXFromChar)
        characters.remove(lines[0])
        for i in range(len(characters)-1):
            if not(interval_x(i + 1)[1] < interval_x(i)[0] or interval_x(i + 1)[0] > interval_x(i)[1]):
                col[i + 1] = col[i]
            else:
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
            characters[i].insert(5, r)
            if characters[i][0:5] == lines[0]:
                lines[0] = characters[i]
            elif characters[i][4] in ['plus', '-', 'times']:
                operators[0] = characters[i]
            i += 1
        def getColFromChar(item):
            return item[6]
        def getRowFromChar(item):
            return item[5]
        max_row = row[len(row)-1]
        max_col = col[len(col)-1-len(lines)] # not care about last one because that is the position of the lines

        # prints out persons work with characters
        work = []
        for i in range(max_row + 1):
            work.append([' '] * (max_col + 1))
        for character in characters:
            work[character[5]][character[6]] = character[4]
            if character[4] == 'plus':
                work[character[5]][character[6]] = '+'
        work = work[::-1] # reverses array
        # checks if you did work correctly
        #If addition
        if operators[0][4] == 'plus':
            # check if rightmost numbers added up are equalling what they are supposed to
            characters.sort(reverse = True, key = getRowFromChar)
            characters.sort(reverse = True, key = getColFromChar)
            c_num = max_col
            sum_col = 0
            prev_sum = 0
            have_nums_to_use = False
            correct = True
            for character in characters:
                if character[6] == c_num and not(character[4] in ['plus', '-', 'times']) and character[5] > lines[0][5]:
                    sum_col += int(character[4])
                    have_nums_to_use = True
                elif character[6] == c_num and not(character[4] in ['plus', '-', 'times']) and character[5] < lines[0][5]:
                    sum_check = int(character[4])
                    if sum_col % 10 != sum_check and have_nums_to_use:
                        message = "Mistake: When adding in column " + str(c_num)
                        correct = False
                    have_nums_to_use = False
                    prev_sum = sum_col
                    sum_col = 0
                elif not(character[4] in ['plus', '-', 'times']):
                    c_num = character[6]
                    if character[5] < lines[0][5] and sum_col == 0 and int(prev_sum / 10) != int(character[4]):
                        message = "Mistake: In leftmost column"
                        correct = False
                    sum_col += int(character[4])
        if correct:
            message = "Your work looks correct to me"
        response = flask.jsonify({"work": work, "message": message})
        return response, 201
    except:
        return "", 500


if __name__ == '__main__':
    #app.run(host="127.0.0.1", post=8080, debug=True)
    app.run()