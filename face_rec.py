import face_recognition as fr
import os
import cv2
import face_recognition
import numpy as np
import pandas as pd
import SendMail


def get_encoded_faces():
    encoded = {}

    for dirpath, dnames, fnames in os.walk("./faces"):
        for f in fnames:
            if f.endswith(".jpg") or f.endswith(".png"):
                face = fr.load_image_file("faces/" + f)
                encoding = fr.face_encodings(face)[0]
                encoded[f.split(".")[0]] = encoding

    return encoded


def unknown_image_encoded(img):

    face = fr.load_image_file("faces/" + img)
    encoding = fr.face_encodings(face)[0]

    return encoding


def classify_face(im):

    faces = get_encoded_faces()
    faces_encoded = list(faces.values())
    known_face_names = list(faces.keys())

    img = cv2.imread(im, 1)
 
    face_locations = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, face_locations)

    face_names = []
    for face_encoding in unknown_face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(faces_encoded, face_encoding)
        name = "Unknown"

        # use the known face with the smallest distance to the new face
        face_distances = face_recognition.face_distance(faces_encoded, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            name = known_face_names[best_match_index]

        face_names.append(name)
        df=pd.read_csv('Student List.csv')
        student_name=list(df.loc[df['SRN'] == name].Name)
        branch=list(df.loc[df['SRN'] == name].Branch)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Draw a box around the face
            cv2.rectangle(img, (left-20, top-20), (right+20, bottom+20), (0,0,255), 2)
            start_point = (5, 5)
            end_point = (220, 100)
            color =(181,171,165)
            thickness = -1
            cv2.rectangle(img, start_point, end_point, color, thickness)
            if(name!='Unknown'):
                font=cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(img,student_name[0], (10,30), font, 1, (0,0,0),2,cv2.LINE_AA)
                cv2.putText(img,name, (10,60), font, 1, (0,0,0),2,cv2.LINE_AA)
                cv2.putText(img,'Branch-'+branch[0], (10,90), font, 1, (0,0,0),2,cv2.LINE_AA)


    while True:
        cv2.imshow('Face Recognition', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    return name
        

def recognize():

    SRN_keys=[]
    filenames=[]
    x=set(line.strip() for line in open('No Mask List.txt'))
    x=sorted(x)
    for y in range(0,len(x),20):
        pic=x[y]
        filename=pic+'.jpg'
        SRN=classify_face(filename)
        if SRN!='Unknown':
            SRN_keys.append(SRN)
            filenames.append(filename)

    dict1=pd.DataFrame(filenames,index=SRN_keys)
    dict1.to_csv('Email.csv')

recognize()
SendMail.sendmail()