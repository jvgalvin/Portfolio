#!/bin/bash

export DISPLAY=:0
xhost +
docker run -it --rm --device /dev/video0 --network host -e DISPLAY=$DISPLAY bolnerm/movenet
