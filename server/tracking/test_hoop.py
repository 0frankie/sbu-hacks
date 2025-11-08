import cv2
import argparse
from tracker import Tracker
from hoop import detect_hoop
import sys

clicked_point = None


def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"[INFO] Clicked at: {clicked_point}")


def main():
    parser = argparse.ArgumentParser(
        description="Basketball auto-tracking with OpenCV 4.12"
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Path to input video file or webcam index (e.g. 0)",
    )
    args = parser.parse_args()

    try:
        video_source = int(args.video)
    except ValueError:
        video_source = args.video

    with Tracker(video_source, "MIL") as tracker:
        frame = tracker.get_frame()

        cv2.namedWindow("Select basketball (click near center)")
        cv2.setMouseCallback("Select basketball (click near center)", mouse_callback)

        print(
            "[INFO] Click on the basketball (or close to its center). Press any key when done."
        )

        while True:
            display = frame.copy()
            if clicked_point is not None:
                cv2.circle(display, clicked_point, 5, (0, 255, 255), -1)
            cv2.imshow("Select basketball (click near center)", display)

            key = cv2.waitKey(10) & 0xFF
            if key != 255:
                break

        cv2.destroyWindow("Select basketball (click near center)")

        if clicked_point is None:
            print("[INFO] No point selected. Exiting.")
            sys.exit(0)

        bbox = detect_hoop(frame, clicked_point)

        if bbox is None:
            print("[INFO] No hoop detected. Exiting.")
            sys.exit(0)

        cv2.rectangle(
            frame,
            (bbox[0] - bbox[2] // 2, bbox[1] - bbox[3] // 2),
            (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2),
            (0, 255, 0),
            2,
        )

        cv2.imshow("Detected Hoop", frame)
        cv2.waitKey(0)

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
