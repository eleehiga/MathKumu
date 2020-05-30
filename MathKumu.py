from PIL import Image
from os import listdir
from matplotlib import image
from matplotlib import pyplot
import tensorflow as tf
from ipywidgets import IntProgress
from IPython.display import display
from sklearn.model_selection import train_test_split

loaded_images = list() # will append values to list
image_labels = list()
for i in range(0,9):
    f = IntProgress(min=0, max=len(listdir('handwrittenmathsymbols/'+str(i)))) # Progress bar
    display(f)
    display(str(i))
    for filename in listdir('handwrittenmathsymbols/'+str(i)):
        f.value +=1
        img_data = image.imread('handwrittenmathsymbols/'+str(i)+'/' + filename)
        loaded_images.append(img_data)
        image_labels.append(str(i))
        #print(i)
        #pyplot.imshow(img_data)
        #pyplot.show()
math_symbols =  ['+','-','=','times']
for symbol in math_symbols:
    f = IntProgress(min=0, max=len(listdir('handwrittenmathsymbols/'+symbol)))
    display(f)
    display(symbol)
    for filename in listdir('handwrittenmathsymbols/'+symbol):
        f.value +=1
        img_data = image.imread('handwrittenmathsymbols/'+symbol+'/' + filename)
        loaded_images.append(img_data)
        image_labels.append(symbol)
X_train, X_test, y_train, y_test = train_test_split(loaded_images, image_labels, test_size=0.2)
X_train = tf.keras.utils.normalize(X_train, axis=1)
X_test = tf.keras.utils.normalize(X_test, axis=1)
X_train = tf.convert_to_tensor(X_train, dtype=tf.float32)
X_test = tf.convert_to_tensor(X_test, dtype=tf.float32)
y_train = tf.convert_to_tensor(y_train, dtype=tf.string)
y_test = tf.convert_to_tensor(y_test, dtype=tf.string)

model = tf.keras.Sequential([
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(128, activation=tf.nn.relu),
    tf.keras.layers.Dense(10 + len(math_symbols), activation=tf.nn.softmax)
])

model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])


model.fit(X_train, y_train, epochs=3)