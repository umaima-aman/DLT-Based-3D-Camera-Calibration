# Camera Calibration and 3D Camera Position Estimation Using Direct Linear Transform (DLT)

This project focuses on **Camera Calibration and 3D Camera Position Estimation using the Direct Linear Transform (DLT) method** as part of a Computer Vision assignment.
The objective was to estimate camera parameters using a real-world scene, specifically a corner of a room consisting of two walls and a floor.

## Problem Description

The experiment involved the following steps:

1. **Marker Placement:** Select a corner of a room and place at least six removable markers or draw identifiable patterns distributed across all three planes (two walls and the floor). Ideally, place two markers on each plane.

2. **3D World Coordinate Measurement:** Physically measure the distances of all six markers from the room corner. Use these measurements to determine the 3D world coordinates \((X,Y,Z)\) of each marker.

3. **Image Acquisition:** Capture a photograph of the room corner using a webcam or mobile camera from a distance of a few meters, ensuring that all six markers are visible.

4. **2D Pixel Coordinate Extraction:** Identify the pixel coordinates \((u,v)\) of each marker in the captured image, measured from the top-left corner of the image.

5. **Camera Parameter Estimation:** Apply the Direct Linear Transform (DLT) algorithm using the corresponding 3D world coordinates and 2D image pixel coordinates to estimate the camera projection matrix and camera parameters.

6. **Physical Camera Position Measurement:** Physically measure the camera position in the world coordinate frame, represented by \((C_x,C_y,C_z)\).

7. **Comparison and Evaluation:** Compare the physically measured camera position with the estimated camera position to evaluate the accuracy of the DLT-based estimation.

## Experimental Implementation

The experiment was implemented in Python. OpenCV was used to load and display the captured image and interactively select the six marker locations. NumPy was used for coordinate representation, matrix construction, and Singular Value Decomposition (SVD) to estimate the projection matrix. SciPy's RQ decomposition was used to extract the intrinsic and rotation matrices.

The camera translation vector and 3D camera centre were subsequently calculated from the estimated projection matrix.

## Objective

The primary objective is to understand the relationship between 3D world coordinates and 2D image coordinates, estimate camera parameters using DLT, and evaluate the estimated camera position against physical measurements.
