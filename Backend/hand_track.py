import cv2
import mediapipe as mp
import math
from finger import Finger
from hand import Hand

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

FINGER_JOINTS = {
    "thumb":  (2, 4,  0),
    "index":  (5, 8,  1),
    "middle": (9, 12, 2),
    "ring":   (13, 16, 3),
    "pinky":  (17, 20, 4),
}

def main():
    cap = cv2.VideoCapture(0)
    while True:
        success, image = cap.read()
        if not success:
            break

        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                lm = hand_landmarks.landmark
                wrist = lm[0]
                palm_size = math.hypot(lm[9].x - wrist.x, lm[9].y - wrist.y)

                fingers = []
                for name, (base_idx, tip_idx, channel) in FINGER_JOINTS.items():
                    finger = Finger(
                        tip=lm[tip_idx],
                        base=lm[base_idx],
                        palm_size=palm_size,
                        servo_channel=channel,
                    )
                    fingers.append(finger)

                hand = Hand(fingers=fingers)
                # hand.update_servos(serial_conn)   # <-- once serial.py is wired in

        cv2.imshow("Webcam test", image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

main()