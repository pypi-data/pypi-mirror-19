import os
import pickle

from Tkinter import *
from PIL import ImageTk, Image
import tkMessageBox
import tkFileDialog 
from ttk import Frame, Button, Label, Style

from random import randint
from PIL import Image

import mosaic

class MainFrame(Frame):
  
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
    
        
    def initUI(self):

        self.pack(fill=BOTH, expand=0)

        Button(self, text = "Select Image Dataset Directory", command = lambda: openDir(self)).grid(row=0, column=0, pady=5)
        self.dirName = StringVar()
        Label(self, textvariable=self.dirName).grid(row=0, column=1, columnspan=2, pady=5, sticky=W)

        Button(self, text = "Select File", command = lambda: openFile(self)).grid(row=1, column=0, pady=5)
        self.fileName = StringVar()
        Label(self, textvariable=self.fileName).grid(row=1, column=1, columnspan=2, pady=5, sticky=W)

        self.iamgelabel = Label(self)
        self.iamgelabel.grid(row=1, column=3)        

        Label(self, text = "Enter Number of Grids: ").grid(row=2, column=0, pady=5)
        
        self.entry = Entry(self, bd=5)
        self.entry.grid(row=2, column=1, pady=5, sticky=W)

        Button(self, text = "CREATE", command = lambda: startMosaic(self.dirName.get(), self.fileName.get(), self.entry.get(), self.parent)).grid(row=3, column=0, pady=5)
 
def openDir(app):
    dirName = tkFileDialog.askdirectory(initialdir='./')
    app.dirName.set(dirName)

def openFile (app):
    dirName = app.dirName.get()
    if not os.path.isdir(dirName):
        dirName = './'
    fileName = tkFileDialog.askopenfilename(initialdir = dirName)
    app.fileName.set(fileName)

    size = 64, 64
    img = Image.open(fileName)
    img.thumbnail(size)
    imgtk = ImageTk.PhotoImage(img)
    app.iamgelabel.configure(image=imgtk)
    app.iamgelabel.image = imgtk

def startMosaic(dirName, fileName, num_grids, frame):
    wind = Toplevel(frame)
    try:
        mosaic.build_mosaic(fileName, num_grids=int(num_grids), root=wind, datasetdir=dirName)
    except ValueError:
        mosaic.build_mosaic(fileName, root=wind, datasetdir=dirName)

def main():
    root = Tk()
    size = 220, 220
    root.title('PYMOS')
    app = MainFrame(root)
    root.geometry("480x360")
    root.mainloop()

  