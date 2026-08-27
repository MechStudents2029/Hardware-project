import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils

def main():
    cap = cv2.VideoCapture(0)
    frame_count = 0
    while True:
            success, image = cap.read()
            if not success:
                break

            frame_count += 1
    
            print(image.shape, image.dtype)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(rgb)
    
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    wrist = hand_landmarks.landmark[0]
                    index_tip = hand_landmarks.landmark[8]
                    if frame_count % 10 == 0:
                        print(f"Wrist: ({wrist.x:.2f}, {wrist.y:.2f})  Index tip: ({index_tip.x:.2f}, {index_tip.y:.2f})")

            cv2.imshow("Webcam test", image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    cap.release()
    cv2.destroyAllWindows()
    
main()