import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import scipy
from scipy import misc
import Tkinter as tk
from PIL import Image, ImageTk, ImageDraw
from os import listdir
from os.path import isfile, join
from os import getcwd
import ttk

class App:
    def __init__(self, master):
        self.right_eye_coords = None
        self.left_eye_coords = None
        self.right_mouth_coords = None
        self.left_mouth_coords = None
        self.nose_coords = None
        self.mid_mouth_coords = None

        self.landmarks = {'right_eye': self.right_eye_coords,
                          'left_eye': self.left_eye_coords,
                          'right_mouth': self.right_mouth_coords,
                          'left_mouth': self.left_mouth_coords,
                          'nose': self.nose_coords,
                          'mid_mouth': self.mid_mouth_coords}

        self.colors = {'right_eye': (178,34,34),
                       'left_eye': (34,139,34),
                       'right_mouth': (255,215,25),
                       'left_mouth': (230,69,25),
                       'nose': (70,130,180),
                       'mid_mouth': (199,21,133)}

        self.coords_to_control = None

        self.cv = tk.Canvas(master, width=800, height=600)
        self.cv.grid(row=0,column=0)

        frame = tk.Frame(master)
        frame.grid(row=0, column=1)

        self.faces_dir = 'Faces'
        #self.faces = [ f for f in listdir(faces_dir) if (isfile(join(faces_dir,f)) and '.png' in f)]
        self.face_name = 'face1.png'
        self.im = Image.open(self.faces_dir+'/'+self.face_name)
        self.id = ImageDraw.Draw(self.im)
        self.im.save(self.faces_dir+'/landmarks.png','PNG')
        self.lm_im = Image.open(self.faces_dir+'/landmarks.png')
        self.lm_image = ImageTk.PhotoImage(self.lm_im)
        self.cv.create_image(0,0,image=self.lm_image, anchor='nw')
        self.cv.bind('<Button 1>', self.print_coords)

        self.b_right_eye = tk.Button(frame, 
                                     text='Right Eye',
                                     command=self.mark_right_eye,
                                     highlightbackground='#%02x%02x%02x'%self.colors['right_eye'])
        self.b_right_eye.grid(row=0, column=0)

        self.b_left_eye = tk.Button(frame,
                                    text='Left Eye',
                                    command=self.mark_left_eye,
                                    highlightbackground='#%02x%02x%02x'%self.colors['left_eye'])
        self.b_left_eye.grid(row=0, column=2)

        self.b_nose = tk.Button(frame,
                                text='Nose',
                                command=self.mark_nose,
                                highlightbackground='#%02x%02x%02x'%self.colors['nose'])
        self.b_nose.grid(row=1, column=1)

        self.b_right_mouth = tk.Button(frame,
                                       text='Right Mouth',
                                       command=self.mark_right_mouth,
                                       highlightbackground='#%02x%02x%02x'%self.colors['right_mouth'])
        self.b_right_mouth.grid(row=2, column=0)

        self.b_mid_mouth = tk.Button(frame,
                                     text='Mid Mouth',
                                     command=self.mark_mid_mouth,
                                     highlightbackground='#%02x%02x%02x'%self.colors['mid_mouth'])
        self.b_mid_mouth.grid(row=2, column=1)

        self.b_left_mouth = tk.Button(frame,
                                      text='Left Mouth',
                                      command=self.mark_left_mouth,
                                      highlightbackground='#%02x%02x%02x'%self.colors['left_mouth'])
        self.b_left_mouth.grid(row=2, column=2)

        self.b_save = tk.Button(frame,
                                text='Save',
                                command=self.save_labels)
        self.b_save.grid(row=3, column=1)
        
    def mark_right_eye(self):
        self.coords_to_control = 'right_eye'
        print 'marked right eye!'
    
    def mark_left_eye(self):
        self.coords_to_control = 'left_eye'
        print 'marked left eye!'

    def mark_right_mouth(self):
        self.coords_to_control = 'right_mouth'
        print 'marked right mouth!'
            
    def mark_left_mouth(self):
        self.coords_to_control = 'left_mouth'
        print 'marked left mouth!'

    def mark_mid_mouth(self):
        self.coords_to_control = 'mid_mouth'
        print 'marked mid mouth!'

    def mark_nose(self):
        self.coords_to_control = 'nose'
        print 'marked nose!'

    def save_labels(self):
        lines = [line.strip() for line in open('face_labels.txt')]
        f = open('face_labels.txt', 'w')
        for line in lines:
            if not self.face_name in line:
                f.write(line+'\n')
        new_line = self.face_name+'= '
        new_line += str(self.landmarks)
        f.write(new_line)
        f.close()

    def print_coords(self, event):
        temp_coords = (event.x, event.y)
        if self.coords_to_control == None:
            print 'no landmark chosen, cannot save!'
        else:
            self.landmarks[self.coords_to_control] = temp_coords

        self.im = Image.open(self.faces_dir+'/'+self.face_name)
        self.id = ImageDraw.Draw(self.im)

        
        for key in self.landmarks.keys():
            if not self.landmarks[key] == None:
                key_coords = self.landmarks[key]
                key_colors = self.colors[key]
                self.id.ellipse((key_coords[0] - 10, key_coords[1] - 10,key_coords[0] + 10, key_coords[1] + 10),
                                fill=(key_colors[0], key_colors[1], key_colors[2], 25))

        self.im.save(self.faces_dir+'/landmarks.png','PNG')
        self.lm_im = Image.open(self.faces_dir+'/landmarks.png')
        self.lm_image = ImageTk.PhotoImage(self.lm_im)
        self.cv.create_image(0,0,image=self.lm_image, anchor='nw')
        self.cv.bind('<Button 1>', self.print_coords)

        print self.landmarks

root = tk.Tk()
app = App(root)
root.mainloop()
