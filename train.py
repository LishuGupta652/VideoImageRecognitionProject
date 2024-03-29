import os
from PIL import Image
import numpy as np
import cv2
import pickle

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')
recognizer = cv2.face.LBPHFaceRecognizer_create()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, 'images')

current_id = 0
label_ids = {}
y_label = []
x_train = []

for root , dirs , files in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(" ","-").lower()
            #print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            print(label_ids)
            #y_label.append(label)
            #x_trian.append(path)
            pil_image = Image.open(path).convert("L") #grayScale
            #size = (100,100)
            #pil_image = pil_image.resize(size , Image.ANTIALIAS) 
            image_array=  np.array(pil_image, "uint8")
            #print(image_array)

            faces = face_cascade.detectMultiScale(image_array, scaleFactor = 1.5 , minNeighbors= 5)

            for (x, y ,w, h) in faces:
                roi = image_array[y:y+h , x:x+w]
                x_train.append(roi)
                y_label.append(id_)


#print(y_label)
#print(x_train)


with open('label.pickle', 'wb') as file:
    pickle.dump(label_ids, file)

recognizer.train(x_train , np.array(y_label))
recognizer.save("trainer.yml")



            
