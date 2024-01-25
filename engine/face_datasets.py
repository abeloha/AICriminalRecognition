####################################################
# Adopted by Abel Onuoha and Dami Oluwole          #
# Modified by Nazmi Asri                           #
# Original code: http://thecodacus.com/            #
# All right reserved to the respective owner       #
####################################################

# Import OpenCV2 for image processing
import cv2
from PIL import Image

import engine.generalfunction as fn

def execute_face_datasets(face_id, path):

    # Detect object in image using Haarcascade Frontal Face
    face_detector = cv2.CascadeClassifier('engine/haarcascade_frontalface_default.xml')
    # Initialize sample face image
    count = 0
    fn.assure_path_exists("data_images/")
    imagePaths = fn.get_images(path)
    for imagePath in imagePaths:       
            
            print (imagePath)
            
            image_frame = cv2.imread(imagePath)
            # Convert frame to grayscale
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)

            # Detect frames of different sizes, list of faces rectangles
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            
            if(len(faces) == 1):
                # Loops for each faces
                for (x,y,w,h) in faces:
                    # Crop the image frame into rectangle
                    cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)
                    # Increment sample face image
                    count += 1
                    # Save the captured image into the datasets folder
                    cv2.imwrite("data_images/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            if count>100:
                break

    cv2.destroyAllWindows()
    return count;
