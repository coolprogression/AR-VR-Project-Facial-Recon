import cv2
import numpy as np
import sqlite3

import cv2,os
import numpy as np
from PIL import Image


cam = cv2.VideoCapture(0)
detector=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def addData(Id, Name, Age, Gender,):
	conn=sqlite3.connect("FaceBase.db")
	cmd="SELECT * FROM People WHERE ID="+str(Id)
	cursor=conn.execute(cmd)
	isRecordExist=0
	for row in cursor:
		isRecordExist=1
	if(isRecordExist==1):
		cmd="UPDATE People SET Name="+str(name)+","+"Age="+str(age)+","+"Gender="+str(major)+"WHERE ID="+str(Id)
	else:
		cmd="INSERT INTO People(ID, Name, Age , Gender) Values ("+str(Id)+","+str(Name)+","+str(Age)+","+str(major)+")"

	conn.execute(cmd)
	conn.commit()
	conn.close()
	print 'You have added to our database'
	print 'Please rotate head while the camera captures your face'
		
		
		
Id=raw_input('Enter your id: ')
name=raw_input('Please enter your name: ')
age=raw_input('Please enter your age: ')
major=raw_input('Please enter your major: ')
name=("'"+name+"'")
major=("'"+major+"'")
addData(Id, name, age, major)


sampleNum=0
while(True):
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
		
        #incrementing sample number 
        sampleNum=sampleNum+1
        #saving the captured face in the dataset folder
        cv2.imwrite("dataSet/User."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])

        cv2.imshow('frame',img)
    #wait for 100 miliseconds 
    if cv2.waitKey(100) & 0xFF == ord('q'):
        break
    # break if the sample number is morethan 20
    elif sampleNum>20:
        break
cam.release()
cv2.destroyAllWindows()




recognizer = cv2.createLBPHFaceRecognizer()
detector= cv2.CascadeClassifier("haarcascade_frontalface_default.xml");

def getImagesAndLabels(path):
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    faceSamples=[]
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces=detector.detectMultiScale(imageNp)
        #If a face is there then append that in the list as well as Id of it
        for (x,y,w,h) in faces:
            faceSamples.append(imageNp[y:y+h,x:x+w])
            Ids.append(Id)
    return faceSamples,Ids

faces,Ids = getImagesAndLabels('dataSet')
recognizer.train(faces, np.array(Ids))
recognizer.save('trainner/trainner.yml')

print 'You are all set'

question=raw_input('Would you like to add another user? (yes/no): ')
if (question == 'yes'):
	execfile('capture.py')
else:
	execfile('rec.py')









