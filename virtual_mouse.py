	# """
	# The function uses the Mediapipe library to detect hand landmarks and count fingers, and uses the
	# pynput library to control the mouse based on hand gestures.
	
	# :param image: The current frame captured by the webcam
	# :param hand_landmarks: A list of detected hand landmarks for each hand in the image. Each hand
	# landmark is represented by its x, y, and z coordinates normalized to the range [0, 1]
	# :param handNo: The hand number parameter is used to specify which hand to detect and track. By
	# default, it is set to 0, which means the first hand detected will be used. If there are multiple
	# hands in the frame, you can set it to 1 to track the second hand, and so on, defaults to 0
	# (optional)
	# """
 

# These lines of code are importing the necessary libraries and modules required for the program to
# run. Specifically, `cv2` is the OpenCV library used for image and video processing, `math` is the
# Python math library used for mathematical operations, `mediapipe` is a library for building machine
# learning pipelines to process multimedia content, `pynput` is a library for controlling input
# devices such as the mouse and keyboard, and `pyautogui` is a library for GUI automation and screen
# recording.
import cv2
import math
import mediapipe as mp
from pynput.mouse import Button, Controller
import pyautogui

# `mouse=Controller()` is creating an instance of the `Controller` class from the `pynput.mouse`
# library, which allows the program to control the mouse cursor on the computer. This instance is
# assigned to the variable `mouse`, which is used later in the code to move the mouse cursor and
# simulate mouse clicks.
mouse=Controller()

# `cap = cv2.VideoCapture(0)` is creating an instance of the `VideoCapture` class from the `cv2`
# (OpenCV) library, which allows the program to capture video frames from the default camera (index 0)
# of the computer. This instance is assigned to the variable `cap`, which is used later in the code to
# read frames from the camera and process them.
cap = cv2.VideoCapture(0)

# These lines of code are getting the width and height of the video frame captured by the webcam using
# the `cv2.CAP_PROP_FRAME_WIDTH` and `cv2.CAP_PROP_FRAME_HEIGHT` properties of the `VideoCapture`
# class from the `cv2` (OpenCV) library. The `get()` function is used to retrieve the values of these
# properties, which are then converted to integers using the `int()` function and assigned to the
# `width` and `height` variables, respectively. These variables are used later in the code to scale
# the coordinates of the hand landmarks detected by the Mediapipe library to the size of the video
# frame.
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

# `(screen_width, screen_height) = pyautogui.size()` is using the `size()` function from the
# `pyautogui` library to get the size of the computer screen in pixels. The function returns a tuple
# containing the width and height of the screen, which are then assigned to the variables
# `screen_width` and `screen_height`, respectively. These variables are used later in the code to
# scale the position of the mouse cursor based on the size of the screen.
(screen_width, screen_height) = pyautogui.size()

# These lines of code are importing the `Hands` class from the `mp.solutions.hands` module of the
# Mediapipe library and the `drawing_utils` module from the same library.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# `hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)` is creating an
# instance of the `Hands` class from the `mp.solutions.hands` module of the Mediapipe library. This
# instance is assigned to the variable `hands`, which is used later in the code to detect hand
# landmarks in the video frames captured by the webcam.
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)
tipIds = [4, 8, 12, 16, 20]

# `pinch=False` is initializing a boolean variable `pinch` to `False`. This variable is used later in
# the code to keep track of whether a pinch gesture has been formed between the thumb and index finger
# of the hand being tracked.
pinch=False

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):

	global pinch

	if hand_landmarks:
		# Get all Landmarks of the FIRST Hand VISIBLE
		landmarks = hand_landmarks[handNo].landmark

		# Count Fingers        
		fingers = []

		for lm_index in tipIds:
			# Get Finger Tip and Bottom y Position Value
			finger_tip_y = landmarks[lm_index].y 
			finger_bottom_y = landmarks[lm_index - 2].y

			# Check if ANY FINGER is OPEN or CLOSED
			if lm_index !=4:
				if finger_tip_y < finger_bottom_y:
					fingers.append(1)


				if finger_tip_y > finger_bottom_y:
					fingers.append(0)

		totalFingers = fingers.count(1)

		# PINCH

		# Draw a LINE between FINGER TIP and THUMB TIP
		# These lines of code are calculating the x and y coordinates of the finger tip and thumb tip
		# landmarks detected by the Mediapipe library, and scaling them based on the width and height of the
		# video frame captured by the webcam. The `landmarks[8]` and `landmarks[4]` refer to the landmarks
		# representing the tip of the index finger and the tip of the thumb, respectively. The `x` and `y`
		# attributes of these landmarks represent their normalized coordinates in the range [0, 1]. By
		# multiplying these normalized coordinates with the width and height of the video frame, we get the
		# actual pixel coordinates of the finger tip and thumb tip in the image. The `int()` function is
		# used to convert these coordinates to integers, as they need to be integers to be used in the
		# `cv2.line()` and `cv2.circle()` functions later in the code.
		finger_tip_x = int((landmarks[8].x)*width)
		finger_tip_y = int((landmarks[8].y)*height)

		thumb_tip_x = int((landmarks[4].x)*width)
		thumb_tip_y = int((landmarks[4].y)*height)

		cv2.line(image, (finger_tip_x, finger_tip_y),(thumb_tip_x, thumb_tip_y),(255,0,0),2)

		# Draw a CIRCLE on CENTER of the LINE between FINGER TIP and THUMB TIP
		# This code block is calculating the center point between the finger tip and thumb tip landmarks
		# detected by the Mediapipe library. It first calculates the average of the x-coordinates and
		# y-coordinates of the two landmarks, and then sets the `center_x` and `center_y` variables to these
		# average values. Finally, it draws a small red circle at the center point on the `image` using the
		# `cv2.circle()` function.
		center_x = int((finger_tip_x + thumb_tip_x )/2)
		center_y = int((finger_tip_y + thumb_tip_y )/2)

		cv2.circle(image, (center_x, center_y), 2, (0,0,255), 2)

		# Calculate DISTANCE between FINGER TIP and THUMB TIP
		# `distance = math.sqrt(((finger_tip_x - thumb_tip_x)**2) + ((finger_tip_y - thumb_tip_y)**2))` is
		# calculating the Euclidean distance between the finger tip and thumb tip landmarks detected by the
		# Mediapipe library. It first calculates the difference between the x-coordinates and y-coordinates
		# of the two landmarks, squares them, adds them together, and then takes the square root of the
		# result to get the distance between the two points. This distance is used later in the code to
		# determine whether a pinch gesture has been formed.
		distance = math.sqrt(((finger_tip_x - thumb_tip_x)**2) + ((finger_tip_y - thumb_tip_y)**2))

		print("Distance: ", distance)
		
		print("Computer Screen Size :",screen_width, screen_height, "Output Window size: ", width, height)
		print("Mouse Position: ", mouse.position, "Tips Line Centre Position: ", center_x, center_y)

		# Set Mouse Position on the Screen Relative to the Output Window Size	
		# This code block is calculating the relative position of the mouse on the screen based on the
		# position of the hand in the video frame. It first calculates the x and y coordinates of the center
		# of the line between the finger tip and thumb tip, and then scales these coordinates based on the
		# size of the output window (specified by the `width` and `height` variables) and the size of the
		# computer screen (specified by the `screen_width` and `screen_height` variables). Finally, it sets
		# the position of the mouse on the screen using the `mouse.position` function from the
		# `pynput.mouse` library.
		relative_mouse_x = (center_x/width)*screen_width
		relative_mouse_y = (center_y/height)*screen_height
		
		mouse.position = (relative_mouse_x, relative_mouse_y)

		# Check PINCH Formation Conditions
		# This code block is checking for the formation of a pinch gesture between the thumb and index
		# finger of the hand being tracked. If the distance between the tips of the thumb and index finger
		# is greater than 40 pixels and the `pinch` variable is `True`, it means that the pinch gesture has
		# been released, so the `pinch` variable is set to `False` and the left mouse button is released
		# using the `mouse.release(Button.left)` function. If the distance between the tips of the thumb and
		# index finger is less than or equal to 40 pixels and the `pinch` variable is `False`, it means that
		# the pinch gesture has been formed, so the `pinch` variable is set to `True` and the left mouse
		# button is pressed using the `mouse.press(Button.left)` function.
		if distance > 40:
			if pinch == True:
				pinch = False			
				mouse.release(Button.left)

		if distance <= 40 :
			if(pinch==False):
				pinch=True
				mouse.press(Button.left)


# Define a function to 
def drawHandLanmarks(image, hand_landmarks):
	"""
	This function draws connections between landmark points on an image of a hand using the MediaPipe
	Hands library in Python.
	
	:param image: The image on which the hand landmarks will be drawn
	:param hand_landmarks: This parameter is a list of dictionaries containing the landmarks of each
	hand detected in the image. Each dictionary contains the landmarks for a single hand, with keys
	representing the landmark type (e.g. "WRIST", "THUMB_TIP") and values representing the coordinates
	of the landmark in the image
	"""

    # Draw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



# This code block is the main loop of the program that captures video frames from the default camera
# (specified by `cap = cv2.VideoCapture(0)`) and processes them to detect hand landmarks and control
# the mouse cursor based on hand gestures.
while True:
	success, image = cap.read()
	
	image = cv2.flip(image, 1)

	# Detect the Hands Landmarks 
	results = hands.process(image)

	# Get landmark position from the processed result
	hand_landmarks = results.multi_hand_landmarks

	# Draw Landmarks
	drawHandLanmarks(image, hand_landmarks)

	# Get Hand Fingers Position        
	countFingers(image, hand_landmarks)

	cv2.imshow("Media Controller", image)

	# Quit the window on pressing Sapcebar key
	key = cv2.waitKey(1)
	if key == 27:
		break

# `cv2.destroyAllWindows()` is a function from the OpenCV library that closes all the windows created
# by the program. It is used at the end of the program to ensure that all windows are closed when the
# program is terminated.
cv2.destroyAllWindows()
