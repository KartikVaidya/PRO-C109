    # """
    # This is a Python program that uses the Mediapipe library to detect hand landmarks and count fingers
    # to control media playback using keyboard shortcuts.
    
    # :param image: The current frame of the video captured by the webcam
    # :param hand_landmarks: It is a list of detected hand landmarks in the current frame. Each element of
    # the list represents a hand, and contains the landmarks of that hand as a list of 3D coordinates (x,
    # y, z) normalized to the range [0, 1]
    # :param handNo: handNo is a parameter used in the countFingers() function to specify which hand's
    # landmarks to use for finger counting. By default, it is set to 0, which means it will count the
    # fingers of the first hand detected in the image. If there are multiple hands in the image,, defaults
    # to 0 
    
    
import cv2

import mediapipe as mp
from pynput.keyboard import Key, Controller

# `keyboard = Controller()` is creating an instance of the `Controller` class from the
# `pynput.keyboard` module. This instance can be used to simulate keyboard input, such as pressing and
# releasing keys. In this program, it is used to simulate pressing the spacebar key to pause a video
# when the user closes their hand into a fist.
keyboard = Controller()

# `cap = cv2.VideoCapture(0)` is creating an instance of the `VideoCapture` class from the `cv2`
# module. This instance is used to capture video frames from the default camera (index 0) of the
# computer.
cap = cv2.VideoCapture(0)

# `width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))` and `height  =
# int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))` are getting the width and height of the video frame
# captured by the webcam using the `cv2.VideoCapture` instance `cap`. The `cv2.CAP_PROP_FRAME_WIDTH`
# and `cv2.CAP_PROP_FRAME_HEIGHT` are constants that represent the width and height of the video frame
# respectively. The `get()` method of the `VideoCapture` instance is used to get the value of these
# constants for the current video frame. The values are then converted to integers and stored in the
# `width` and `height` variables respectively.
width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) 
height  = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) 

# `mp_hands = mp.solutions.hands` and `mp_drawing = mp.solutions.drawing_utils` are importing the
# `hands` and `drawing_utils` modules from the `mp.solutions` package of the Mediapipe library. These
# modules are used to detect hand landmarks and draw them on the video frame respectively.
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# `hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)` is creating an
# instance of the `Hands` class from the `mp_hands` module of the Mediapipe library. This instance is
# used to detect hand landmarks in the video frames captured by the webcam. The
# `min_detection_confidence` and `min_tracking_confidence` parameters are used to set the minimum
# confidence values required for the hand detection and tracking respectively. If the confidence
# values are below these thresholds, the hand landmarks will not be detected or tracked.
hands = mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5)

# `tipIds` is a list of integers that represent the indices of the finger tip landmarks in the hand
# landmarks list returned by the Mediapipe library. The finger tip landmarks are used to count the
# number of fingers that are open or closed. The indices in the `tipIds` list correspond to the
# following fingers: thumb, index finger, middle finger, ring finger, and little finger.
tipIds = [4, 8, 12, 16, 20]

state = None

# Define a function to count fingers
def countFingers(image, hand_landmarks, handNo=0):

    global state

    if hand_landmarks:
        # Get all Landmarks of the FIRST Hand VISIBLE
        landmarks = hand_landmarks[handNo].landmark

        # Count Fingers        
        fingers = []

        # This code block is a for loop that iterates over the `tipIds` list, which contains the indices
        # of the finger tip landmarks in the hand landmarks list returned by the Mediapipe library. For
        # each index in the `tipIds` list, the code gets the y-coordinate of the finger tip landmark and
        # the y-coordinate of the landmark two positions below it (which represents the bottom of the
        # finger). It then checks if the finger is open or closed by comparing the y-coordinates of the
        # finger tip and bottom landmarks. If the finger tip is higher than the bottom, the finger is
        # considered open and a value of 1 is appended to the `fingers` list. If the finger tip is lower
        # than the bottom, the finger is considered closed and a value of 0 is appended to the `fingers`
        # list. The loop continues until all finger tip landmarks have been processed, and the `fingers`
        # list contains a binary representation of which fingers are open (1) or closed (0).
        for lm_index in tipIds:
                # Get Finger Tip and Bottom y Position Value
                finger_tip_y = landmarks[lm_index].y 
                finger_bottom_y = landmarks[lm_index - 2].y

                # Check if ANY FINGER is OPEN or CLOSED
                if lm_index !=4:
                    # This code block is checking if a finger is open or closed by comparing the
                    # y-coordinates of the finger tip landmark and the landmark two positions below it
                    # (which represents the bottom of the finger). If the y-coordinate of the finger
                    # tip is less than the y-coordinate of the bottom landmark, the finger is
                    # considered open and a value of 1 is appended to the `fingers` list. If the
                    # y-coordinate of the finger tip is greater than the y-coordinate of the bottom
                    # landmark, the finger is considered closed and a value of 0 is appended to the
                    # `fingers` list.
                    if finger_tip_y < finger_bottom_y:
                        fingers.append(1)
                        # print("FINGER with id ",lm_index," is Open")

                    if finger_tip_y > finger_bottom_y:
                        fingers.append(0)
                        # print("FINGER with id ",lm_index," is Closed")

        
        totalFingers = fingers.count(1)
        
        # PLAY or PAUSE a Video
        if totalFingers == 4:
            state = "Play"

        if totalFingers == 0 and state == "Play":
            state = "Pause"
            keyboard.press(Key.space)

        # Move Video FORWARD & BACKWARDS    
        finger_tip_x = (landmarks[8].x)*width
 
       # This code block is checking if only one finger is open and if so, it checks the x-coordinate
       # of the index finger tip landmark (landmark with index 8) normalized to the range [0, 1]. If
       # the x-coordinate is less than `width-400`, it simulates pressing the left arrow key on the
       # keyboard to move the video playback backward. If the x-coordinate is greater than `width-50`,
       # it simulates pressing the right arrow key on the keyboard to move the video playback forward.
       # This allows the user to control the video playback by moving their index finger left or
       # right.
        if totalFingers == 1:
            if  finger_tip_x < width-400:
                print("Play Backward")
                keyboard.press(Key.left)

            if finger_tip_x > width-50:
                print("Play Forward")
                keyboard.press(Key.right)
        
        
# Define a function to 
def drawHandLanmarks(image, hand_landmarks):

    # Draw connections between landmark points
    if hand_landmarks:

      for landmarks in hand_landmarks:
               
        mp_drawing.draw_landmarks(image, landmarks, mp_hands.HAND_CONNECTIONS)



while True:
    success, image = cap.read()

   # `image = cv2.flip(image, 1)` is flipping the video frame horizontally. The second argument, `1`,
   # specifies the axis along which the image should be flipped. A value of `1` means that the image
   # should be flipped horizontally, while a value of `0` would flip it vertically. This is done to
   # ensure that the user's hand movements are mirrored correctly on the screen, as the webcam
   # captures the user's movements in reverse.
    image = cv2.flip(image, 1)
    
    # Detect the Hands Landmarks 
    # `results = hands.process(image)` is using the `process()` method of the `Hands` class instance
    # `hands` to detect hand landmarks in the current video frame `image`. The method takes the image
    # as input and returns a `Hands` object that contains the detected hand landmarks. This object can
    # be used to access the hand landmarks and their positions in the image.
    results = hands.process(image)

    # Get landmark position from the processed result
   # `hand_landmarks = results.multi_hand_landmarks` is assigning the list of detected hand landmarks
   # in the current frame to the variable `hand_landmarks`. The `multi_hand_landmarks` attribute of
   # the `results` object returned by the `process()` method of the `Hands` class contains a list of
   # detected hand landmarks, where each element of the list represents a hand and contains the
   # landmarks of that hand as a list of 3D coordinates (x, y, z) normalized to the range [0, 1]. The
   # `hand_landmarks` variable is then passed as an argument to the `countFingers()` and
   # `drawHandLanmarks()` functions to count the number of fingers and draw the landmarks on the video
   # frame respectively.
    hand_landmarks = results.multi_hand_landmarks

    # Draw Landmarks
    drawHandLanmarks(image, hand_landmarks)

    # Get Hand Fingers Position        
    countFingers(image, hand_landmarks)

    cv2.imshow("Media Controller", image)

    # Quit the window on pressing Sapcebar key
    # `key = cv2.waitKey(1)` is waiting for a key event for 1 millisecond and storing the key code in
    # the `key` variable. The `waitKey()` function is a keyboard binding function from the OpenCV
    # library that waits for a specified delay for a keyboard event.
    key = cv2.waitKey(1)
    if key == 27:
        break

# `cv2.destroyAllWindows()` is a function from the OpenCV library that closes all the windows created
# by the program. It is used to clean up the resources used by the program and to close any open
# windows before the program exits.
cv2.destroyAllWindows()
