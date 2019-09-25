import tkinter as tk
from PIL import ImageTk, Image
import cv2
from ProductDetails import *

class ProductFinder(tk.Frame):
    
    def __init__(self, master=None):
        super().__init__(master)
        self.x = cv2.VideoCapture(0)
        self.master = master
        self.pack()
        self.widgets()
        self.camera_stream()

    #Declaring all the widgets that are required for the application's GUI
    def widgets(self):
        
        #Declaring 2 frames (Camera Frame and Product Details Frame)
        #1. Live camera feed frame and label for the camera feed
        self.videoFrame = tk.Frame(self)
        self.videoFrame.pack(side="left",padx=10,pady=10) 
        self.videoLabel = tk.Label(self.videoFrame)
        self.videoLabel.pack()
        
        #2. Frame for product details text
        self.productDetailsFrame = tk.Frame(self,bg="#EAE9E9",height=500,width=650)
        self.productDetailsFrame.pack(side="left",padx=10,pady=10)
        
        #3. Declaring buttons
            #Button to take a photo and this button also calls other functions which passes the image to the
            #the inference model and updates the labels of the product details frame
        self.photoButton = tk.Button(self.videoFrame,text="Take Photo",command=self.takePhoto,height=3,width=80)
        self.photoButton.pack(side="left",padx=12,pady=5)

        #4. Product Details Labels
            #ProductName
        self.productName = tk.Label(self.productDetailsFrame,text=ProductDetails.chocolate['productName'])
        self.productName.pack(padx=20,pady=15)
            #ProductPrice
        self.productPrice = tk.Label(self.productDetailsFrame,text=ProductDetails.chocolate['productPrice'])
        self.productPrice.pack(padx=20,pady=15)
            #Aisle Number
        self.aisleNumber = tk.Label(self.productDetailsFrame,text=ProductDetails.chocolate['aisleNumber'])
        self.aisleNumber.pack(padx=20,pady=15)
            #Quantity
        self.productQuantity = tk.Label(self.productDetailsFrame,text=ProductDetails.chocolate['productStock'])
        self.productQuantity.pack(padx=20,pady=15)

    #A method that displays the live camera stream and updates the label of videoFrame widget
    def camera_stream(self):

        #Get the live video, convert it to RGBA color space and resize the output of the image
        _, self.frame = self.x.read()
        cv2image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        img = img.resize((700, 500), Image.ANTIALIAS)

        #Update the label of the videoFrame widget
        imgtk = ImageTk.PhotoImage(image=img)
        self.videoLabel.imgtk = imgtk
        self.videoLabel.configure(image=imgtk)
        self.videoLabel.after(1, self.camera_stream)

    #This function captures a single frame saves it and overrides the existing file when clicked
    def takePhoto(self):
        img_name = "captured_photo.png"
        self.capturedImage = cv2.imwrite(img_name, self.frame)
        '''self.capturedImage = cv2.imencode('.png',self.frame)'''
    
root = tk.Tk()
root.geometry("1000x600")
app = ProductFinder(master=root)
app.mainloop()