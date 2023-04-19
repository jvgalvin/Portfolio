import warnings

warnings.filterwarnings("ignore")

import cv2
import tensorflow as tf
import numpy as np
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import chime

tflite_model_file = "../models//vgg_model.tflite"

interpreter = tf.lite.Interpreter(model_path=tflite_model_file)

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
good_frames = 0
bad_frames = 0
chime.theme("mario")

# Initiate holistic model

while cap.isOpened():
    ret, frame = cap.read()

    # Recolor Feed
    images = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    images.flags.writeable = False

    # Recolor image back to BGR for rendering
    images.flags.writeable = True
    images = cv2.cvtColor(images, cv2.COLOR_RGB2BGR)

    img = cv2.resize(images, (150, 150))
    # img = Image.fromarray(img, 'RGB')
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    img = np.array(img, dtype=np.float32)
    # print(img) - working

    interpreter.resize_tensor_input(input_details[0]['index'], (len(img), 150, 150, 3))
    interpreter.resize_tensor_input(output_details[0]['index'], (len(img), 2))
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    tflite_model_predictions = interpreter.get_tensor(output_details[0]['index'])

    # Make Detections
    # X = np.array(pd.DataFrame([row]))
    pose_detection_value = tflite_model_predictions[0][0]
    comp_pose_detection_value = tflite_model_predictions[0][1]
    # print(pose_detection_value)

    if pose_detection_value >= comp_pose_detection_value:
        pose_detection_class = 'Good'
        pose_detection_prob = pose_detection_value
    else:
        pose_detection_class = 'Sit Up Straight'
        pose_detection_prob = comp_pose_detection_value

    # print(pose_detection_class)
    # print(pose_detection_prob)

    if pose_detection_class == 'Good':
        good_frames += 1
        bad_frames = 0
    else:
        good_frames = 0
        bad_frames += 1

    good_time = (1. / fps) * good_frames
    bad_time = (1. / fps) * bad_frames

    # To display the text, grab ear coords
    coords = (250, 100)  # (288, 127) Good / (348, 105) Bad

    if pose_detection_class == 'Good':
        cv2.rectangle(images,
                      (coords[0], coords[1] + 5),
                      (coords[0] + len(pose_detection_class) * 20, coords[1] - 30),
                      (0, 128, 0), -1)
    else:
        cv2.rectangle(images,
                      (coords[0], coords[1] + 5),
                      (coords[0] + len(pose_detection_class) * 16, coords[1] - 30),
                      (105, 105, 105), -1)

    cv2.putText(images, pose_detection_class, coords,
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Get status box
    if pose_detection_class == 'Good':
        cv2.rectangle(images, (0, 0), (250, 60), (0, 128, 0), -1)
    else:
        cv2.rectangle(images, (0, 0), (250, 60), (105, 105, 105), -1)

    # Display Class
    cv2.putText(images, 'CLASS'
                , (95, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(images, pose_detection_class.split(' ')[0]
                , (90, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Display Probability
    cv2.putText(images, 'PROB'
                , (15, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(images, str(round(pose_detection_prob, 2))
                , (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    if bad_time > 60:
        chime.warning()
        bad_frames = 0

    cv2.imshow('Raw Webcam Feed', images)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
