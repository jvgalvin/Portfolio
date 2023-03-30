FROM ubuntu
  
ENV DEBIAN_FRONTEND noninteractive
WORKDIR /app
RUN apt-get update
RUN apt install -y python3-dev python3-pip  python3-opencv vim-tiny  libopencv-dev
RUN pip3 install Cython
RUN pip3 install numpy
RUN pip3 install paho-mqtt
RUN export DISPLAY=:0
CMD sudo xhost +
COPY haarcascade_frontalface_default.xml haarcascade_frontalface_default.xml
# example from https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_gui/py_video_display/py_video_display.html
COPY cam.py cam.py

CMD ["python3","cam.py"]
