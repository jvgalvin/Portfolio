# pip install mediapipe opencv-python pandas scikit-learn chime --quiet

# import packages
import mediapipe as mp 
import cv2
import numpy as np
import pandas as pd
import pickle 
import chime


mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions



with open('../models/mediapipe_model/pose_detection_gb_robo.pkl', 'rb') as f:
    model = pickle.load(f)
    
cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
good_frames = 0
bad_frames = 0 
chime.theme("mario")

# initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False        
        
        # make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
                
        # recolor image back to BGR for rendering
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # export coordinates
        try:
            # extract pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            
            # extract face landmarks
            face = results.face_landmarks.landmark
            face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
            
            # concate pose and face row
            row = pose_row+face_row

            # Make Detections
            X = pd.DataFrame([row])
            pose_detection_class = model.predict(X)[0]
            pose_detection_prob = model.predict_proba(X)[0]
            
            if pose_detection_class == 'Good':
                good_frames += 1
                bad_frames = 0
            else:
                good_frames = 0
                bad_frames += 1
                
                
            good_time = (1. / fps) * good_frames
            bad_time = (1. / fps) * bad_frames
            
            # to display the text, grab ear coords
            
            # display near your ear area
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
            cv2.putText(image, str(round(pose_detection_prob[np.argmax(pose_detection_prob)],2))
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