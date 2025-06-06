Purpose
The purpose of this project is to detect human facial emotions such as happiness, sadness, anger, etc., from a video or live camera feed.
Using this, we can analyze facial emotions either in real-time or from a recorded video file using computer vision.

Tools and Libraries Used
Python – Programming language

Flask – Python-based web framework to build the web app

FER – Facial Expression Recognition library that detects emotions from face images

OpenCV – For video and camera capture

Werkzeug – For secure file upload handling

How it Works?
Video Upload or Camera Capture:

The user can upload a video file or capture live video from the webcam.

Uploaded videos are saved in a folder named uploads/.

Reading Video Frames:

The video is read frame by frame using OpenCV.

Each frame is sent to the FER emotion detector.

Emotion Detection:

FER library uses MTCNN face detector to locate faces in each frame.

For each detected face, it predicts probability scores for 7 emotions:

Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral

Aggregate Scores:

The emotion scores from all frames are collected.

Then average percentage scores for each emotion are calculated.

Result Display:

Emotion scores with corresponding emojis are displayed on the webpage.

The top detected emotion is highlighted.

User Interface
A simple HTML page with:

Video upload button

Camera capture button

Display area for emotion scores and emojis

Why is this Project Useful?
Understanding human emotions is important in many fields such as:

Psychology research

Customer experience analysis

Human-computer interaction

Security and surveillance

This project demonstrates practical use of Deep Learning for real-world emotion detection.

Challenges Faced
Efficient processing of video frames

Handling different lighting conditions and face angles

Achieving real-time performance with webcam input

Future Improvements
Add real-time live emotion streaming without saving video files

Support detection and tracking of multiple faces at once

Improve UI with graphs and charts to visualize emotions

Deploy the app on cloud servers for wider access

Summary
This project uses Python and Deep Learning to detect human facial emotions from video or webcam input. It runs as a web application using Flask, displaying the results in the browser.
This is a practical AI project example that is useful for learning and showcasing in a portfolio.
