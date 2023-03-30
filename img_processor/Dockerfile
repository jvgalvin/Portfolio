FROM ubuntu
  
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install Cython
RUN pip3 install numpy
RUN pip3 install paho-mqtt
RUN pip3 install boto3
RUN pip3 install botocore
# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY img_processor.py img_processor.py
CMD ["python3","img_processor.py"]
