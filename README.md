## Air Canvas with MediaPipe
This project allows users to draw on a virtual canvas in real-time using only hand gestures, without touching any screen or device. It utilizes OpenCV for computer vision and MediaPipe for hand landmark detection.

Air Canvas is a creative tool that captures hand movements via a webcam and interprets gestures to draw, erase, and clear the canvas. The core idea is to use fingertip positions especially the index finger to track movement and convert it into strokes on a digital whiteboard.

### Technologies Used
Python

OpenCV – for image processing and real-time video capture.

MediaPipe – for hand landmark detection.

NumPy – for image array manipulation.

Collections (Deque) – for managing dynamic stroke paths.

### Features
Draw using the index finger
Raise only the index finger to begin drawing.

Start a new stroke
Raise all five fingers to end the current stroke and start a new one.

Color palette
Choose between BLUE, GREEN, RED, YELLOW, or ERASER by hovering your finger over the color buttons at the top of the screen.

Eraser Tool
Select "ERASER" to erase parts of the drawing with a white stroke.

Clear the canvas
Hover over the "CLEAR" button to erase all strokes.

Save drawing
The final drawing is automatically saved as drawing.png upon exit.

