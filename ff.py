import cv2
import tensorflow as tf
import numpy as np
import time
import os
import os
import urllib.request
import http
import pandas as pd
import re
from time import sleep
from datetime import datetime
import pickle
filename = 'model.sav'
loaded_model = pickle.load(open(filename, 'rb'))

base = "http://192.168.137.52/"

def transfer(my_url):   #use to send and receive data
    try:
        n = urllib.request.urlopen(base + my_url).read()
        n = n.decode("utf-8")
        return n
    except http.client.HTTPException as e:
        return e

# Specify the absolute path for the Excel file

# Create an empty list to store data
data_list = []

ct = 0


faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

cam = cv2.VideoCapture(0)

sample_frames = 150
# Set the number of frames to capture
frame_counter = 0
image_samples = []

while frame_counter < sample_frames:
    ret, img = cam.read()
    img = cv2.flip(img, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w + 50, y + h + 50), (255, 0, 0), 2)
        im = gray[y:y + h, x:x + w]

    cv2.imshow('image', img)


    if 'im' in locals() and frame_counter < sample_frames:
        cv2.imwrite(r"C:\Users\jithi\Desktop\SKCT-STRESS\STRESS\folder\main"+str(frame_counter)+".jpg",im)
        im_array = cv2.resize(im, (50, 50))
        im_array = cv2.cvtColor(im_array, cv2.COLOR_GRAY2RGB)  # Convert to RGB
        im_array = np.expand_dims(im_array, axis=0)  # Add batch dimension
        image_samples.append(im_array)
        frame_counter += 1
    
    
    cv2.waitKey(1)

cam.release()
cv2.destroyAllWindows()
res = transfer(str(ct))
response = str(res)
print(response)

# Split the received data
values = response.split('-')

if len(values) == 4:
    te, bpm, spo2, ppg = values


# Convert the list of image samples to a numpy array
image_samples = np.concatenate(image_samples, axis=0)

# Load your model
model = tf.keras.models.load_model("CNN.model")

# Make prediction on the entire sample
predictions = model.predict(image_samples)
reports = [[te, bpm, spo2, ppg]]
print(reports)
predicted = loaded_model.predict(reports)
#print(predicted)
ft=predicted[0]
# Calculate the overall stress level
stress_predictions = predictions[:, 0 ]
print("CNN ACCURACY")
print(stress_predictions)
print("KNN ACCURACY")
print(ft)
average_stress_level = np.mean(stress_predictions+ft)
print("Average Stress Level:", average_stress_level)
import os
if average_stress_level <=1.2:
    print("He looked happy and relaxed, showing no signs of stress, ready to keep living his joyful life without any worries.")
else:
    if average_stress_level < 1.6291556:
        print("Feeling a smidge stressed, he finds solace in calming tunes, easing his mind and letting him unwind from worries.")
        document_path = 'stress_reduce.mp3'
        os.system(f'start {document_path}')
    if average_stress_level >=1.6291556:
        print("Burdened by high stress, he finds relief in deep breaths, gentle exercise, and spending time outdoors, while consulting a nearby doctor is vital.")
        print("can go through the document, give a view on it, and read the document for remedies.")
        document_path = 'Stress_Relief_Techniques.docx'
        os.system(f'start {document_path}')
with open("average_stress_level.txt", "w") as file:
    file.write(str(average_stress_level))
