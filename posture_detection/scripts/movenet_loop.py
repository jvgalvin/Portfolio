#--------------------------------
import numpy as np
import cv2

import tensorflow as tf
import tensorflow_hub as hub

import chime

#--------------------------------
# Load Movenet

module = hub.load("https://tfhub.dev/google/movenet/singlepose/lightning/4")
input_size = 192

def movenet(input_image):
    """Runs detection on an input image.

    Args:
      input_image: A [1, height, width, 3] tensor represents the input image
        pixels. Note that the height/width should already be resized and match the
        expected input resolution of the model before passing into this function.

    Returns:
      A [1, 1, 7, 3] float numpy array representing the predicted keypoint
      coordinates and scores, normalized
    """
    
    model = module.signatures['serving_default']

    # SavedModel format expects tensor type of int32
    input_image = tf.cast(input_image, dtype=tf.int32)
    
    # Run model inference
    outputs = model(input_image)
    
    # Output is a [1, 1, 17, 3] tensor.
    keypoints_with_scores = outputs['output_0'].numpy()
    
    # Keep upper body coordinates [1, 1, 7, 3] tensor
    keypoints_with_scores = keypoints_with_scores[:,:,:7]
    
    # Account for translational variations using shoulder keypoints
    shoulder_avg = keypoints_with_scores[:,:,5:7].mean(axis=2)
    numerator = keypoints_with_scores - shoulder_avg
    
    # Normalize (scale) by farthest keypoint from shoulder_avg
    sqd = (keypoints_with_scores - shoulder_avg)**2
    x = sqd[0][0][:,:1]
    y = sqd[0][0][:,1:2]
    distances = np.sqrt(x+y)
    idx = np.argmax(distances)
    point_max_d = keypoints_with_scores[:,:,idx]
    keypoints_with_scores = numerator / point_max_d
    
    return keypoints_with_scores

#--------------------------------
# Load TFLite Classification Head

interpreter = tf.lite.Interpreter(model_path="../models/movenet_model.tflite")
interpreter.allocate_tensors()

#--------------------------------
# Livestream loop

cap = cv2.VideoCapture(0)
fps = int(cap.get(cv2.CAP_PROP_FPS))
good_frames = 0
bad_frames = 0 
chime.theme("mario")

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    h, w = frame.shape[:2]

    # Send the frame through Movenet
    input_image = tf.expand_dims(frame, axis=0)
    input_image = tf.image.resize_with_pad(input_image, input_size, input_size)
    keypoints_w_scores = movenet(input_image)

    # Send the keypoints through classification head
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    input_shape = input_details[0]['shape']
    input_data = keypoints_w_scores[np.newaxis, :, :, :, ]
    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])

    # Draw rectangular upper border
    frame = cv2.rectangle(frame, (0, 0), (w, h - 1010), color=(0, 0, 0), thickness=-1)

    # Control loop for displaying frames and text

    if np.argmax(output_data) == 0:
      good_frames += 1
      bad_frames = 0
    else:
      good_frames = 0 
      bad_frames += 1
    
    good_time = (1 / fps) * good_frames
    bad_time = (1 / fps) * bad_frames

    if good_time > 0:
      str_to_display = "Good posture time: " + str(round(good_time, 1)) + "s"
      frame = cv2.putText(frame, text=str_to_display, 
                                   org=(50, 50), 
                                   fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                   fontScale=1,
                                   color=(127,255,0),
                                   thickness=2)
    else:
      str_to_display = "Bad posture time: " + str(round(bad_time, 1)) + "s"
      frame = cv2.putText(frame, text=str_to_display, 
                                   org=(50, 50), 
                                   fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                                   fontScale=1,
                                   color=(50,50,255),
                                   thickness=2)

    # Sound alarm if bad posture time exceeds 1 min (60s)
    if bad_time > 60:
      chime.warning()
      bad_frames = 0

    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
