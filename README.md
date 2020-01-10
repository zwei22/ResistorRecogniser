# ResistorRecognizer
The main purpose of this project is to construct an automated resistor recognizer. The resistors are locating with a Haar Cascade Classifier. The classifier is trainned on 1000 positive images and 1500 negative images. Then the color is read through thresholding certain color ranges in HSV color space.

## Hareware setup
* camera: Logitech C920

> If different camera is used, it may be necessary to modify resolution setting for camera capture.

## Software dependency
* numpy=1.16.4
* opencv-python=3.4.3

## Execution
Run the program with the following command:
``` bash
python main.py
```
Note that the index in ```Videocapture(0)``` may need to be change according to different conputer and camera.


## Work division
| Studen ID | Name   | Work                          |
| --------- | ------ | ----------------------------- |
| B04502031 | 施力維 | Find resistor's position, ppt |
| B06901188 | 李宗倫 | Find resistor's position, ppt |
| B05502048 | 鄭婷予 | Read resistor's color, ppt |
| B07502022 | 梁皓瑋 | Read resistor's color, ppt |
