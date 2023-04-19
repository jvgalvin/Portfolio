# import packages
import mediapipe as mp 
import cv2
import numpy as np
import chime
import os
from tensorflow import keras

mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions

model = keras.models.load_model('../models/mediapipe_model')
    
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
good_frames = 0
bad_frames = 0 
chime.theme("mario")

# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False        
        
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        # Export coordinates
        try:
            # Extract Pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            
            # Extract Face landmarks
            face = results.face_landmarks.landmark
            face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
            
            # Concate rows
            row = pose_row+face_row


            # Make Detections
            
            # X = np.array(pd.DataFrame([row]))
            X = np.array([row])
            
            pose_detection_value = model.predict(X)[0][0]
            comp_pose_detection_value = model.predict(X)[0][1]
        
            if pose_detection_value >= comp_pose_detection_value:
                pose_detection_class = 'Good'
                pose_detection_prob = pose_detection_value
            else:
                pose_detection_class = 'Sit Up Straight'
                pose_detection_prob = comp_pose_detection_value
                    
            if pose_detection_class == 'Good':
                good_frames += 1
                bad_frames = 0
            else:
                good_frames = 0
                bad_frames += 1
                
                
            good_time = (1. / fps) * good_frames
            bad_time = (1. / fps) * bad_frames
            
            
            # To display the text, grab ear coords
            coords = tuple(np.multiply(
                            np.array(
                                (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
                                 results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                        , [480,240]).astype(int))

            
            if pose_detection_class == 'Good':
                cv2.rectangle(image, 
                              (coords[0], coords[1]+5), 
                              (coords[0]+len(pose_detection_class)*20, coords[1]-30), 
                              (0, 128, 0), -1)
            else:
                cv2.rectangle(image, 
                              (coords[0], coords[1]+5), 
                              (coords[0]+len(pose_detection_class)*16, coords[1]-30), 
                              (105,105,105), -1)
            
            
            cv2.putText(image, pose_detection_class, coords, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Get status box
            # cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
            # Get status box
            if pose_detection_class == 'Good':
                cv2.rectangle(image, (0,0), (250, 60), (0, 128, 0), -1)
            else:
                cv2.rectangle(image, (0,0), (250, 60), (105,105,105), -1)
            
            # Display Class
            cv2.putText(image, 'CLASS'
                        , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, pose_detection_class.split(' ')[0]
                        , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Display Probability
            cv2.putText(image, 'PROB'
                        , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            cv2.putText(image, str(round(pose_detection_prob,2))
                        , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
        except:
            pass
        
        if bad_time > 60:
                chime.warning()
                bad_frames = 0
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()