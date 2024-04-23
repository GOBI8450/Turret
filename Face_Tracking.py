import cv2
import serial
import time
import keyboard

#Arduino serial connection
ArduinoSerial = serial.Serial('COM3', 9600, timeout=0.1)
time.sleep(1)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

shooting_counter = 1  # Counter for generating unique filenames

shooting_flag = False  # Flag to indicate shooting signal sent
start_time = None  # Variable to store the start time when spacebar is pressed

while cap.isOpened():
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)  # mirror the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 6)  # detect the face

    for x, y, w, h in faces:
        # sending coordinates to Arduino
        string = 'X{0:d}Y{1:d}'.format(x + w // 2, y + h // 2)
        ArduinoSerial.write(string.encode('utf-8'))

        # plot the center of the face
        cv2.circle(frame, (x + w // 2, y + h // 2), 2, (0, 255, 0), 2)

        # plot the region of interest
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

        # check if spacebar is pressed and shooting signal is not sent
        if keyboard.is_pressed('space') and not shooting_flag:
            print("Shooting signal sent!")
            ArduinoSerial.write(b'S')  # Trigger shooting in Arduino
            shooting_flag = True  # Set the shooting flag

            # record the start time when spacebar is pressed
            start_time = time.time()

        # check if 1 second has passed since spacebar was pressed and take a screenshot
        if shooting_flag and time.time() - start_time >= 1:
            print("Taking screenshot!")
            screenshot_filename = f'screenshot{shooting_counter}.png'
            cv2.imwrite(screenshot_filename, frame)
            print(f"Screenshot saved as '{screenshot_filename}'")
            shooting_counter += 1  # Increment the counter for the next screenshot

            # reset the shooting flag after taking the screenshot
            shooting_flag = False

    # plot the squared region in the center of the screen
    cv2.rectangle(frame, (640 // 2 - 30, 480 // 2 - 30),
                  (640 // 2 + 30, 480 // 2 + 30),
                  (255, 255, 255), 3)

    # display the frame in an OpenCV window
    cv2.imshow('img', frame)

    # press 'h' to Quit
    if cv2.waitKey(10) & 0xFF == ord('h'):
        break

# release the video capture and close OpenCV windows
cap.release()
cv2.destroyAllWindows()
