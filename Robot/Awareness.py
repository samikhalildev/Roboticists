
import simple_pose_estimation 
import face_recognition as fr
from Constants import *
import cv2, os, time
from scipy.misc import bytescale
import numpy as np

class Awareness:

    def __init__(self, session, imagePath, store):
        self.motion = session.service("ALMotion")
        self.imagePath = imagePath.format('musk')
        self.similarity_threshold = 0.5
        self.store = store
        self.img = None

    '''
        This function will detect if there is a person in the frame.
    '''
    def detectPerson(self, hasName=False):        
        self.img = cv2.imread(self.imagePath)
        xy = self.findPerson()

        if xy is not None:
            print('detected')
            # position of the human face
            person_x, person_y = xy 
            #self.lookAt(person_x, person_y) # make the robot look at the person
            return PERSON_DETECTED
        else:
            print('not detected')
            return UNABLE_TO_DETECT

        time.sleep(0.1)

    def findPerson(self):
        people = simple_pose_estimation.detect(self.img)
        print("Number of people: {0}".format(len(people)))
        print(people)
        for person in people:
            if simple_pose_estimation.NOSE in person or simple_pose_estimation.NECK in person or simple_pose_estimation.RSHOULDER in person:
                x, y = person[simple_pose_estimation.NOSE]
                return x,y


    # this function is called when a person is not already recongised
    # It extracts the features from the face and stores in a json file so that the user can be recognised next time
    def recogniseNewPerson(self, name):
        self.img = cv2.imread(self.imagePath)

        # get the faces in the image
        faces = fr.face_locations(self.img)
        print("Found {0} faces!".format(len(faces)))

        if len(faces) == 1:
            face = faces[0]

            features = fr.face_encodings(self.img, [face])[0].tolist()
            saved = self.store.saveUser(name, features)

            if saved:
                return NEW_PERSON
            else:
                return NOT_RECOGNISED
        else:
            return DETECTED_MULTIPLE_HUMANS
            
        
    # this function will capture the face from the frame and check if features match in the database
    def recognisePerson(self):
        print self.imagePath

        self.img = cv2.imread(self.imagePath)
        
        # get faces in the image
        faces = fr.face_locations(self.img)
        print("Found {0} faces!".format(len(faces)))
        
        for face in faces:
            features = fr.face_encodings(self.img, [face])[0]
            similarity = fr.face_distance(features, self.store.knownUsers.values())
            min_id = np.argmin(similarity)

            if similarity[min_id] < self.similarity_threshold:
                name = self.store.knownUsers.keys()[min_id]
            else:
                name = None

            if name:
                return REGISTERED_PERSON, name
            else:
                return UNABLE_TO_RECOGNISE_PERSON

    def lookAt(self, person_x, person_y):
        pass
    
if __name__ == "__main__":
    pass