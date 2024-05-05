import datetime
import cv2
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

import numpy as np
from rembg import remove

from PIL import Image

import tensorflow as tf


model = tf.keras.models.load_model("my_model.h5")



def letter_cmp(a, b):
    if a[1] > b[1]:
        return -1
    elif a[1] == b[1]:
        if a[0] > b[0]:
            return 1
        else:
            return -1
    else:
        return 1
    
from functools import cmp_to_key
letter_cmp_key = cmp_to_key(letter_cmp)

class MyApp(View):
    def get(self,request):
        return render (request, 'home.html')
    
    def post(self,request):

        input = Image.open(request.FILES.get("image"))

        output = remove(input)

        name = "output.png"

        output.save(name)

        img = cv2.imread(name)

        resize = tf.image.resize(img,(180,180))

        predicts = model.predict(np.expand_dims(resize/255,0))
        scores = tf.nn.softmax(predicts).numpy().tolist()[0]


        data_cats = ["Mango Good Leaf","Mango Bad Leaf","Sapodilla Good Leaf","Sapodilla Bad Leaf","Lychee Good Leaf","Lychee Bad Leaf"]

        results = []
        for i in range(6):
            results.append((data_cats[i],scores[i]*100))
        
        results.sort(key=letter_cmp_key)
        


        
        return render (request, 'home.html',{"results":results})