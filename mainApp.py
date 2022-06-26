from ast import Try
from msilib.schema import Directory
import os
import shutil
import tkinter as tk
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

import pandas as pd
import keras
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Model
from keras.preprocessing import image
from keras.models import load_model
from keras.applications.vgg19 import preprocess_input

def CreateWidgets():
	link_Label = Label(root, text ="Select The Files : ",bg = "#E8D579")
	link_Label.grid(row = 1, column = 0,pady = 150, padx = 150)
	
	root.sourceText = Entry(root, width = 50,textvariable = sourceLocation)
	root.sourceText.grid(row = 1, column = 1,pady = 5, padx = 5,columnspan = 2)
	
	source_browseButton = Button(root, text ="Browse",command = SourceBrowse, width = 15)
	source_browseButton.grid(row = 1, column = 3,pady = 5, padx = 5)
	
	destinationLabel = Label(root, text ="Select The Destination folder : ",bg ="#E8D579")
	destinationLabel.grid(row = 2, column = 0,pady = 5, padx = 5)
	
	root.destinationText = Entry(root, width = 50,textvariable = destinationLocation)
	root.destinationText.grid(row = 2, column = 1,pady = 5, padx = 5,columnspan = 2)
	
	dest_browseButton = Button(root, text ="Browse",command = DestinationBrowse, width = 15)
	dest_browseButton.grid(row = 2, column = 3,pady = 5, padx = 5)
	
	copyButton = Button(root, text ="Copy Files and create folder", command = CopyFile, width = 25)
	copyButton.grid(row = 3, column = 1,pady = 5, padx = 5)
    
	moveButton = Button(root, text ="Move Files and create folder",command = MoveFile, width = 25)
	moveButton.grid(row = 3, column = 2, pady = 100, padx = 5)
    
def SourceBrowse():
    root.sourceText.delete(0, END)
    root.files_list = list(filedialog.askopenfilenames(initialdir ="/"))
    root.sourceText.insert('1', root.files_list)

def DestinationBrowse():
    root.destinationText.delete(0, END)
    destinationdirectory = filedialog.askdirectory(initialdir ="/")
    root.destinationText.insert('1', destinationdirectory)

def CopyFile():
    files_list = root.files_list
    destination_location = destinationLocation.get()
    for f in files_list:
        i_path = f
        imgName= i_path.split('/')[-1]
        model = load_model('./main_Model.h5')
        label = ['animal', 'bird','insects', 'snakes']
        img = image.load_img(i_path, target_size = (224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        thresholded = (features>0.5)*1
        ind = np.argmax(thresholded)
        print('Pridict label : ', label[ind])
        # load_label = Label(root, text ="#################### : ",bg ="#ffffff")
        # load_label.grid(row = 4, column=2, pady = 1, padx=5)
        # load_label = Label(root, text ="==================== : ",bg ="#ffffff")
        try:
            os.makedirs(destination_location+"/"+label[ind])
            shutil.copy(f, destination_location+"/"+label[ind])
            
        except:
            shutil.copy(f, destination_location+"/"+label[ind])
    
    messagebox.showinfo("Success", "Files Copied Successfully")

def MoveFile():
    files_list = root.files_list
    destination_location = destinationLocation.get()
    for f in files_list:
        i_path = f
        imgName= i_path.split('/')[-1]
        model = load_model('./main_Model.h5')
        label = ['animal', 'bird', 'insects','snakes']
        img = image.load_img(i_path, target_size = (224,224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        thresholded = (features>0.5)*1
        ind = np.argmax(thresholded)
        print('Pridict label : ', label[ind])

        try:
            os.makedirs(destination_location+"/"+label[ind])
            shutil.move(f, destination_location+"/"+label[ind])
        except:
            shutil.move(f, destination_location+"/"+label[ind])
    
    messagebox.showinfo("Success", "Files Moved Successfully")


# Creating object of tk class
root = tk.Tk()
	
# Setting the title and background color
# disabling the resizing property
root.geometry("960x700")
root.title("Images Classifier")
root.config(background = "black")

sourceLocation = StringVar()
destinationLocation = StringVar()
	
# Calling the CreateWidgets() function
CreateWidgets()
	
# Defining infinite loop
root.mainloop()
