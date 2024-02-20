# Detection-mouvement-with-Open-cv
This project aims to develop a system for motion, color, and object detection using OpenCV with Python. It leverages advanced image processing capabilities to detect and track motion, identify specific colors, and detect moving objects in real-time scenes.

Usage
Run the script using the command:

python detection_mouv.py

To specify a video file as input:
bash
python detection_mouv.py --video videos/example_01.mp4
To stream from a video source (e.g., an IP camera):

perl
python detection_mouv.py --video rtsp2://@ip:/video/

Required Packages
To run this project, you need to have the following Python packages installed:

OpenCV: OpenCV (Open Source Computer Vision Library) is a powerful library for computer vision and image processing tasks. It provides various functions for image manipulation, object detection, and video analysis.

pip install opencv-python
pip install imutils


The script captures video from a webcam or a specified video file or video stream.
It detects motion in the video stream, tracks specific colors, and identifies moving objects.
The detected objects are outlined with rectangles, and their presence is indicated on the frame.
The current state (presence or absence of detected objects) is displayed on the frame.
Date and time information are also displayed on the frame for reference.
Press 'q' to quit the application.
Conclusion
This project demonstrates the capabilities of OpenCV for motion, color, and object detection tasks in Python. By following the instructions provided and installing the required packages, you can use this project to detect and track motion, identify colors, and detect objects in real-time video streams or files.
