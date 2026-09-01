import math
from pathlib import Path

import cv2
import mediapipe as mp
import serial


MODEL_PATH = str(Path(__file__).with_name("hand_landmarker.task"))

# Tune after watching printed "ratio" values: tucked thumb -> 0 deg, extended -> 180 deg
DIST_MIN = 0.3
DIST_MAX = 1.0


def draw_landmarks(image, landmarks):
    h, w = image.shape[:2]
    pts = [(int(lm.x * w), int(lm.y * h)) for lm in landmarks]
    for conn in mp.tasks.vision.HandLandmarksConnections.HAND_CONNECTIONS:
        cv2.line(image, pts[conn.start], pts[conn.end], (0, 255, 0), 2)
    for pt in pts:
        cv2.circle(image, pt, 4, (0, 0, 255), -1)


def main():
    options = mp.tasks.vision.HandLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=mp.tasks.vision.RunningMode.VIDEO,
        num_hands=1,
    )
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Could not open webcam")

    ser = serial.Serial('COM4', 9600)
    try:
        with mp.tasks.vision.HandLandmarker.create_from_options(options) as landmarker:
            frame_count = 0
            while True:
                success, image = cap.read()
                if not success:
                    break

                frame_count += 1
                rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)
                results = landmarker.detect_for_video(mp_image, int(cap.get(cv2.CAP_PROP_POS_MSEC)))

                if results.hand_landmarks:
                    lm = results.hand_landmarks[0]
                    draw_landmarks(image, lm)

                    thumb_tip   = lm[4]
                    index_tip   = lm[8]
                    index_base  = lm[5]
                    wrist       = lm[0]
                    middle_base = lm[9]

                    thumb_dist = math.hypot(thumb_tip.x - index_base.x, thumb_tip.y - index_base.y)
                    index_dist = math.hypot(index_tip.x - index_base.x, index_tip.y - index_base.y)
                    palm_size  = math.hypot(middle_base.x - wrist.x, middle_base.y - wrist.y)

                    ratio = max(DIST_MIN, min(DIST_MAX, thumb_dist / palm_size))
                    index_ratio = max(DIST_MIN, min(DIST_MAX, index_dist / palm_size))

                    angle = int((ratio - DIST_MIN) / (DIST_MAX - DIST_MIN) * 180)
                    index_angle = int((index_ratio - DIST_MIN) / (DIST_MAX - DIST_MIN) * 180)

                    ser.write(f"{angle},{index_angle}\n".encode())

                    if frame_count % 10 == 0:
                        print(f"ratio: {ratio:.3f} angle: {angle}  |  index_ratio: {index_ratio:.3f} index_angle: {index_angle}")

                cv2.imshow("Hand tracking", image)
                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        ser.close()


main()