# Purpose
The purpose of this personal project was to practice fine tuning a neural network for image classification.

# Date
This project was completed in June 2022.

# Context
Training a neural network for image classification from the ground up requires loads of images. Often it is quicker and easier to freeze the backbone of a pretrained neural network and train a custom classification head. Note that this only works if the existing neural network was trained on data sufficiently similar to the classes that will be predicted for the new task.

Everybody who knows me or who has looked at my website knows that I love French Bulldogs. So, I decided that in lieu of doing the standard MNIST digit or fashion image classification tasks that pervade the internet, that I would use transfer learning to train a neural network capable of discriminating between images of random Frenchies and my own, Lucy.

# Data
I have tons of images of Lucy, naturally. To gather images for the negative class, I tried using Beautiful Soup to comb the web and download pictures of random French Bulldogs (various colors, sizes, orientations, lighting conditions, etc. are represented in the training set for both the positive and negative classes). I noticed, however, that these images were "too perfect" and too different from my own for the task to be challenging enough for the network. So, I sourced images from https://images.cv/dataset/french-bulldog-image-classification-dataset for the negative class which are more similar to my own.

The training set consists of 137 images of Lucy and 136 images of random Frenchies. The validation set consists of 31 images of Lucy and 25 images of random Frenchies. The test set contains 12 images of Lucy and 12 images of random Frenchies.

# Network
I chose ResNet50, which is a CNN that was trained on over one million images from the ImageNet database.

# Top Line Summary
My classifier reaches a peak validation accuracy of 0.95 after 15 epochs. It reaches a test accuracy of 0.96.

# Writeup
Medium post can be found here: https://johnvgalvin.medium.com/transfer-learning-with-resnet50-lucy-french-bulldog-classifier-146029c8f112
