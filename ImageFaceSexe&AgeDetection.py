#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 2020

@author: Walid Khelifa
"""
#importing the required libraries
import cv2
import face_recognition

#loading the image to detect
image_detection = cv2.imread('images/walid1.JPG')

#detect all faces in the image
#arguments are image,no_of_times_to_upsample, model
all_face_locations = face_recognition.face_locations(image_detection,model='hog')

#print the number of faces detected
print('Le nombre de visages detectes est : {}'.format(len(all_face_locations)))

#looping through the face locations
for index,current_face_location in enumerate(all_face_locations):
    #splitting the tuple to get the four position values of current face
    top_pos,right_pos,bottom_pos,left_pos = current_face_location
    #printing the location of current face
    print('Le visage {} est en position : {}h {}d {}b {}g '.format(index+1,top_pos,right_pos,bottom_pos,left_pos))
    #slicing the current face from main image
    current_face_image = image_detection[top_pos:bottom_pos,left_pos:right_pos]
    
    #The ‘AGE_GENDER_MODEL_MEAN_VALUES’ calculated by using the numpy. mean()        
    AGE_GENDER_MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
    #create blob of current face slice
    #params image, scale, (size), (mean),RBSwap)
    current_face_image_blob = cv2.dnn.blobFromImage(current_face_image, 1, (227, 227), AGE_GENDER_MODEL_MEAN_VALUES, swapRB=False)
    
    # Predicting Gender
    #declaring the labels
    gender_label_list = ['Homme', 'Femme']
    #declaring the file paths
    gender_protext = "dataset/gender_deploy.prototxt"
    gender_caffemodel = "dataset/gender_net.caffemodel"
    #creating the model
    gender_cov_net = cv2.dnn.readNet(gender_caffemodel, gender_protext)
    #giving input to the model
    gender_cov_net.setInput(current_face_image_blob)
    #get the predictions from the model
    gender_predictions = gender_cov_net.forward()
    #find the max value of predictions index
    #pass index to label array and get the label text
    gender = gender_label_list[gender_predictions[0].argmax()]
    
    # Predicting Age
    #declaring the labels
    age_label_list = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(24-30)', '(35-43)', '(48-53)', '(60-80)']
    #declaring the file paths
    age_protext = "dataset/age_deploy.prototxt"
    age_caffemodel = "dataset/age_net.caffemodel"
    #creating the model
    age_cov_net = cv2.dnn.readNet(age_caffemodel, age_protext)
    #giving input to the model
    age_cov_net.setInput(current_face_image_blob)
    #get the predictions from the model
    age_predictions = age_cov_net.forward()
    #find the max value of predictions index
    #pass index to label array and get the label text
    age = age_label_list[age_predictions[0].argmax()]
          
    #draw rectangle around the face detected
    cv2.rectangle(image_detection,(left_pos,top_pos),(right_pos,bottom_pos),(0,0,255),2)
        
    #display the name as text in the image
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(image_detection, gender+" "+age+" ans", (left_pos+105,bottom_pos+30), font, 1, (255,255,255),2)

cv2.imshow("Age and Gender",image_detection)






