# End-to-End Containerized Face Detection Application

The repository contains an end-to-end face detection application which can be deployed on any ARM64 edge device and any x86-64 cloud machine. A webcam captures a livestream of video, extracts faces from each frame, and sends them as binary messages to the cloud for processing and storage. The cloud machine converts the binary messages into png files and uses boto3 to send these to S3 for storage. The entire application is containerized within Docker and uses Kubernetes (k3s) for orchestration at the edge. 

The application uses Mosquitto (MQTT) as its messaging fabric. More specifically, it uses a QoS level of 0, where delivery is "best effort." Since the camera is capturing multiple frames per second and the use case is benign (personal enrichment), there is no need to guarantee delivery of every single message. If this were to be deployed within an industrial warehouse or an autonomous vehicle, a higher QoS would be advised given the increased importance of each individual frame.

Additionally, two MQTT topics are used within the application. One topic is specific to the edge device and the other is for transmission from the edge to the cloud. The camera publishes messages to the "cam_bin" topic locally on the device, which is picked up and logged (locally, via a broker) by a logger. A forwarder subscribes to the local MQTT topic and publishes to a remote MQTT topic ("cam_bin_remote"). On the cloud, the image processor subscribes to the remote MQTT topic (also via a broker) so that it can process the binary messages into .png files for storage. These topics are intentionally isolated so that one could use the local topic to perform some type of action at the edge (i.e., move the camera, etc.) and customize when an image should be sent to the cloud for processing and storage.

## Requirements

In order to run this application, you will need the following:
  
  1. An ARM64 edge device (or VM emuluation of an edge device) equipped with access to a video camera. Check that the video camera is mounted to /dev/video0. If it is not, then update the mount path in camera.yaml and cv.VideoCapture(0) in cam.py.
  2. A cloud account with a running VM (x86-64), public IP address, and access credentials. Port 1883 should be opened.
  3. Some type of cloud storage (this uses S3). The S3 bucket in this example is completely public and [can be found here](https://s3.console.aws.amazon.com/s3/buckets/jvgalvin-faces?region=us-west-1&tab=objects).
  4. Kubernetes and Docker should both be installed on the edge device. Docker should be installed on the cloud VM.
  5. The face detection model file (located in this repository). Note that you can substitute this with your own model, but you must update the camera Dockerfile and cam.py accordingly.
  6. The Python scripts located in this repository.

## Instructions

Once the above is confirmed, follow the below steps on the edge device:

  1. Clone this repo:

    git clone https://github.com/jvgalvin/face_detection_app.git   
    
  2. Turn on k3s if it isn't automatically enabled:

    sudo systemctl start k3s
    
  3. Update LOCAL_MQTT_HOST in cam.py with the Cluster IP for the mosquitto-service. You can find this with:

    kubectl get service mosquitto-service
    
  4. Update REMOTE_MQTT_HOST in forwarder.py and img_processor.py with the public IP address of the cloud VM.
    
  5. Build the following Docker images in the corresponding directories. Alternatively, you could pull the Docker images from DockerHub and run the containers:
    
    # To build the images
    
    sudo docker build -t jvgalvin/camera:v2 .
    sudo docker build -t jvgalvin/logger:v1 .
    sudo docker build -t jvgalvin/edge_broker:v1 .
    sudo docker build -t jvgalvin/forwarder:v1 .
    
    # To pull from DockerHub
    
    sudo docker pull jvgalvin/camera:v2
    sudo docker pull jvgalvin/logger:v1
    sudo docker pull jvgalvin/edge_broker:v1
    sudo docker pull jvgalvin/forwarder:v1
    
    sudo docker run jvgalvin/camera:v2
    sudo docker run jvgalvin/logger:v1
    sudo docker run jvgalvin/edge_broker:v1
    sudo docker run jvgalvin/forwarder:v1

  6. Deploy into k3s:
    
    kubectl apply -f mosquitto.yaml
    kubectl apply -f mosquittoService.yaml
    kubectl apply -f logger.yaml
    kubectl apply -f forwarder.yaml
    
  7. Confirm the above pods and service are running:

    kubectl get pods
    kubectl get service mosquitto-service
    
On the cloud VM, follow these steps:
  
  1. Clone this repo:

    git clone https://github.com/jvgalvin/face_detection_app.git 
    
  2. Build the following Docker images. Alternatively, you could pull them from DockerHub:

    sudo docker build -t jvgalvin/cloudbroker:v1 .
    sudo docker build -t jvgalvin/imgprocessor:v1 .
    
  3. Run the broker:

    sudo docker run -it --rm jvgalvin/cloudbroker:v1
    
  4. Run the image processor. Note that you will need to pass in the access credentials as environment variables when running the below container. The below example uses AWS:

    sudo docker run -it --rm -e AWS_ACCESS_KEY_ID=<> -e AWS_SECRET_ACCESS_KEY=<> jvgalvin/imgprocessor:v1
    
Images should now appear in the S3 bucket!



