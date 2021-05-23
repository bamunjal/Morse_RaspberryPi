import cv2
import numpy as np
import time


# define a video capture object
vid = cv2.VideoCapture(0)
flashTimer = 0
darkTimer = 0
isStarted = False

alphabet = {
    "-----": "0",
    ".----": "1",
    "..---": "2",
    "...--": "3",
    "....-": "4",
    ".....": "5",
    "-....": "6",
    "--...": "7",
    "---..": "8",
    "----.": "9",
    ".-": "a",
    "-...": "b",
    "-.-.": "c",
    "-..": "d",
    ".": "e",
    "..-.": "f",
    "--.": "g",
    "....": "h",
    "..": "i",
    ".---": "j",
    "-.-": "k",
    ".-..": "l",
    "--": "m",
    "-.": "n",
    "---": "o",
    ".--.": "p",
    "--.-": "q",
    ".-.": "r",
    "...": "s",
    "-": "t",
    "..-": "u",
    "...-": "v",
    ".--": "w",
    "-..-": "x",
    "-.--": "y",
    "--..": "z",
    "/": " ",
    "-·-·--": "!",
    "·-·-·-": ".",
    "--··--": ","
}

detectedWord = ""
showText = "Detected : "

while(True):

    # Capture the video frame
    # by frame
    ret, frame = vid.read()

    # Display the resulting frame
    cv2.imshow('frame', frame)

    # Convert to HSV format
    img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Choose the values based on the color on the point/mark
    lower_red = np.array([0, 120, 210])
    upper_red = np.array([255, 255, 255])
    mask = cv2.inRange(img_hsv, lower_red, upper_red)

    # Bitwise-AND mask and original image
    masked_green = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('frame', frame)
    cv2.imshow('mask', mask)

    counter = cv2.countNonZero(mask)
    # print ("is triggered : "+str(counter))

    flashElapsedTime = 0
    darkElapsedTime = 0
    if(int(counter) > 0 and flashTimer == 0):
        flashTimer = time.time()
        isStarted = True
    if (counter == 0 and flashTimer != 0):
        flashElapsedTime = time.time() - flashTimer
        flashTimer = 0

    if(isStarted):
        if(counter == 0 and darkTimer == 0):
            darkTimer = time.time()
        if (counter != 0 and darkTimer != 0):
            darkElapsedTime = time.time() - darkTimer
            darkTimer = 0
        if(counter == 0 and time.time() - darkTimer > 1):
            darkElapsedTime = time.time() - darkTimer
            darkTimer = 0
            isStarted = False

    if(flashElapsedTime > 0):
        print("flashElapsedTime : "+str(flashElapsedTime))

    if(darkElapsedTime > 0):
        print("darkElapsedTime : "+str(darkElapsedTime))

    if (flashElapsedTime >= 0.5):
        print("Detcted Dash")
        detectedWord += "-"
    elif (flashElapsedTime >= 0.1):
        print("Detcted Dot")
        detectedWord += "."

    if(darkElapsedTime > 0.6):
        print("detected word : "+alphabet[detectedWord])
        showText += alphabet[detectedWord]
        detectedWord = ""

    cv2.putText(masked_green,
                showText,
                (50, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 255, 255),
                2,
                cv2.LINE_4)
    cv2.imshow('res', masked_green)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
