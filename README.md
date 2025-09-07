# FacialLandmarkDetection_for_MoCap
A project about facial motion capture using Facial Landmark detection to cutdown manual tracking of trackers for facial animation.

# Requirements
This project is created in Python 311. I hope it will run with latest Python version as well.
Creation date: 7-9-2025.
1. Create a virtual environment: python -m venv <name>
2. pip install required packages
3. Open Blender, open the Blender_Plugin.py file and run
4. In the 3D window, press N, then go to Landmark tab, press start server.
5. Run the ipynb file, press r to start streaming to Blender

#Required Packages:
*Open-CV:     pip install opencv-python
#dlib: Lookup in the internet
#numpy
#Blender (3.6) is the preffered version.

# Note
Make sure to place the shape_predictor_68_face_landmarks.dat file in the same directory as ipynb file. or give the complete path in the line landmark_predector variable in ipynb file.
