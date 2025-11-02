# FacialLandmarkDetection_for_MoCap
A project about facial motion capture using Facial Landmark detection to cutdown manual tracking of trackers for facial animation.

# Requirements
This project is created in Python 311. I hope it will run with latest Python version as well.
Creation date: 7-9-2025.
1. Create a virtual environment: python -m venv (name)
2. pip install required packages
3. Open Blender, open the Blender_Plugin.py file and run
4. In the 3D window, press N, then go to Landmark tab, press start server.
5. Run the ipynb file, press r to start streaming to Blender

# Required Packages:
* Open-CV:     pip install opencv-python
* dlib: Lookup in the internet
* numpy
* Blender (3.6) is the preffered version.

# Note
Make sure to place the shape_predictor_68_face_landmarks.dat file in the same directory as ipynb file. or give the complete path in the line landmark_predector variable in ipynb file.<br>
**Link to shape_predictor_68_face_landmarks.dat:** https://www.kaggle.com/datasets/sergiovirahonda/shape-predictor-68-face-landmarksdat

# Requirements
1. Copy/Download the requirements.txt from this GitHub, place it in the project (*venv*) folder.
2. Run the following command on VSCODE terminal or pip terminal in which you have activated your virtual environment (venv). <br>
  **pip install -r requirments.txt**

  *if you're giving the command in JupyterNotebook's code line, add ! at the beginning of the line:* <br>
    **!pip install -r requirements.txt**
3. Make sure to give the right path to the requirements.txt file.
<hr>
date:11-2-2024
# Code found on Kaggle
https://www.kaggle.com/datasets/drgilermo/face-images-with-marked-landmark-points/code

**this one gives error during data preproessing**
Uses Tensorflow for training
Dataset can also be found on the same site
<hr>
