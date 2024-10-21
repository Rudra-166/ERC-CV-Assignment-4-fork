# ERC-CV-Assignment-4-Question-1

import mediapipe as mp
import cv2
cap=cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.4, min_tracking_confidence=0.4)
while True:
    ret, frame=cap.read()
    flipped= cv2.flip(frame,1)

    results=hands.process(flipped)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(flipped, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('Hand contour',flipped)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
