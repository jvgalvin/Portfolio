# Posture Detection from a Frontal Camera

Sitting for prolonged periods of time with bad posture can result in serious spinal and health complications. While certain chairs and cushions promote good posture, they are expensive and not easily transported. We present four machine learning models that are capable of detecting good and bad posture from a user-facing webcam. We show that using existing pose estimation models to extract body keypoints from single frames and feeding these latent representations through a fully-connected classification head produces more accurate results than fine-tuning existing image recognition models. We also show that three dimensional feature extraction is more accurate than two dimensional extraction. Two of these models have been quantized, deployed on an NVIDIA Jetson Xavier NX device, and include a user-facing chime to correct sustained (60s) bad posture.

# Demonstrations

## MoveNet (with GPU)

https://user-images.githubusercontent.com/78283671/232340561-b4df0851-a6fc-494c-9dd8-e097578ac818.mov

## MoveNet (Jetson Xavier)

https://user-images.githubusercontent.com/64651726/232379355-c5a2561b-b50b-428d-80d9-0731ccddfff0.mp4


## MediaPipe (with GPU)

https://user-images.githubusercontent.com/88982383/232487198-e524c237-5f98-46d3-8243-00a2e2e12bf0.mov


# Steps to Use MoveNet

1. Clone this repository

    ```
    git clone https://github.com/lindseyBang/W251-Final-Project.git
    ```

2. If you are deploying to a Jetson Xavier NX, build the Docker container for MoveNet. Otherwise, simply navigate to the scripts directory and run the corresponding python file. Step 3 is not needed if you are running locally.

    ```
    ## For deployment on Jetson

    cd movenet_model_file
    docker build -t movenet -f Dockerfile.nvidia .
    ```

    ```
    ## For local use

    cd scripts && python movenet_loop.py
    ```

3. Run the run.sh script (Jetson only)

    ```
    $ sh run.sh
    ```
