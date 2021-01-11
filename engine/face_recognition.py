####################################################
# Adopted by Abel Onuoha and Dami Oluwole          #
# Modified by Nazmi Asri                           #
# Original code: http://thecodacus.com/            #
# All right reserved to the respective owner       #
####################################################

# Import OpenCV2 for image processing
import cv2

# Import numpy for matrices calculations
import numpy as np
import os 
import engine.generalfunction as fn

def face_recognizer(path):
    #return type = True,id,confidence,count
    #true if face is one, else false
    # Create Local Binary Patterns Histograms for face recognization
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    fn.assure_path_exists("trainer/")
    if(not fn.check_path_exists('trainer/trainer.yml')):
        print('Training Model first!')
    
     # Load the trained mode
    recognizer.read('trainer/trainer.yml')
    # Load prebuilt model for Frontal Face
    cascadePath = "engine/haarcascade_frontalface_default.xml"
    # Create classifier from prebuilt model
    faceCascade = cv2.CascadeClassifier(cascadePath);
    # Set the font style
    font = cv2.FONT_HERSHEY_SIMPLEX
    # Read the image file    
    im = cv2.imread(os.path.abspath(path))
    # Convert the captured frame into grayscale
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)

    # Get all face from the picture
    faces = faceCascade.detectMultiScale(gray, 1.2,5)

    count = len(faces)
    if (count != 1):
        return False,0,0,count

    # For each face in faces
    for(x,y,w,h) in faces:        
        # Recognize the face belongs to which ID
        Id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

    return True,Id,confidence,count
       
    # Close all windows
    cv2.destroyAllWindows()
