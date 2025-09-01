# UAS-Demo
OVERVIEW OF THE PROJECT

This project automates casualty detection, classification, and rescue pad assignment using computer vision and priority-based optimization.It processes input aerial images, detects land, ocean, rescue pads, and casualties, assigns casualties to the nearest pads based on emergency severity & capacity, and calculates a Rescue Ratio (Pr) to measure overall rescue efficiency.

FEATURES

1) Detects land and ocean regions using HSV segmentation
2) Identifies rescue pads by color detection (Blue, Pink, Grey)
3) Calculates distance between casualties and pads
4) Assigns casualties to pads based on:
    1) Emergency priority
    2) Nearest distance
    3) Pad capacity constraints
    4) Computes Rescue Ratio per image
    5) Ranks images based on Pr in descending order

DATASET AND INPUTS

1) Input Aerial images (1.png to 10.png)
2) Each image contains:
3) Land & ocean regions
4) Rescue pads (Blue, Pink, Grey)
5) Casualties of different colors & shapes


REQUIRED LIBRARIES

1) OpenCV → cv2
2) NumPy → numpy
3) Matplotlib → matplotlib

ALGORITHM

1) Land & Ocean Segmentation

Uses HSV color thresholding to classify:
Ocean → Blue mask
Land → Yellow mask
Generates overlay images for visualization.

2) Rescue Pad Detection

Uses Hough Circle Transform to detect circular pads.
Identifies pads based on HSV color ranges:
Blue Pad → Light blue range
Pink Pad → Pink range
Grey Pad → White/light grey range
Stores (x, y, color) for each pad.

3) Casualty Detection

Uses HSV color segmentation + contour detection.
Classifies casualties based on:
Color → Red, Yellow, Green (Severity)
Shape → Triangle, Square, Star
Extracts (x, y, shape, color) for each casualty.

4) Priority Assignment

Each casualty gets a priority score based on:
Emergency severity (Red=3, Yellow=2, Green=1)
Age group (Elders=3, Children=2, Adults=1)
priority_score = emergency_score × shape_score

5) Distance Calculation

Uses Euclidean distance:
distance = sqrt((x_pad - x_casualty)² + (y_pad - y_casualty)²)
Stores distances for all casualties → pads.

6) Casualty Assignment

Sorts casualties by priority, then nearest distance.
Assigns casualties to pads based on:
Remaining capacity of pads
Closest distance
Highest priority first
Pad capacities:
Blue → 4
Pink → 3
Grey → 2

7) Rescue Ratio Calculation

Pr = (Sum of priority scores assigned) / (Total number of casualties)
Higher Pr → better rescue efficiency.

8) Ranking Images

Stores (image_name, Pr) for each image.
Sorts results in descending order of Pr.


HOW TO RUN

python Project.py
