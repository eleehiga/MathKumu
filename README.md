# MathKumu
IOS app that will tutor people in math. This is achieved by giving the person problems to work on in a given space on the app and then allowing the person to submit their work to be reviewed automatically. This review will include checking if their solving process, for example in the picture below solving an addition problem, is correct or not and where they went wrong in that process. Finally, this is all possible as a lot of math problems are solved using mechanical steps and therefore the "mechanical" aspect is the reason why these steps are able to be checked by a program. 

Modules in this repository:
- main.py, python file used to run the backend
- MathKumu and MathKumu.IOS folders, contains Xamarin app code
- MathKumu.ipynb, Jupyter Notebook file used to train the neural network that identifies mathematical symbols

What I used to make this app:
- Flask, making the API
- Postman, testing the API
- Tensorflow, Machine learning for optical character recognition
- open-cv, computer vision for parsing individual symbols
- python, programming language
- xamarin, in c# which I used to make my front end

Link to a video of the app running: https://drive.google.com/file/d/1ej_4hOYiHrhyhuLArfXssYiCmUyXj7Vu/view

Picture of app running: 

![Pic_of_Math_Kumu_Running](https://user-images.githubusercontent.com/55113159/147073526-d7b03275-9216-4e42-a433-64a63966dd07.jpg)
