import cv2
import sys
import argparse
from tracking.tracker import Tracker
from tracking.hoop import detect_hoop
import tracking.math

clicked_point = None
h_clicked_point = None


def mouse_callback(event, x, y, flags, param):
    global clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_point = (x, y)
        print(f"[INFO] Clicked at: {clicked_point}")

def h_mouse_callback(event, x, y, flags, param):
    global h_clicked_point
    if event == cv2.EVENT_LBUTTONDOWN:
        h_clicked_point = (x, y)
        print(f"[INFO] Clicked at: {h_clicked_point}")

def main():
    parser = argparse.ArgumentParser(
        description="Basketball auto-tracking with OpenCV 4.12"
    )
    parser.add_argument(
        "--video",
        required=True,
        help="Path to input video file or webcam index (e.g. 0)",
    )
    parser.add_argument(
        "--tracker", default="CSRT", help="Tracker type (CSRT, KCF, MOSSE, etc.)"
    )
    args = parser.parse_args()

    try:
        video_source = int(args.video)
    except ValueError:
        video_source = args.video

    with Tracker(video_source, args.tracker) as tracker:
        frame = tracker.get_frame()
        first_frame = frame.copy()

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


        if clicked_point is None:
            print("[INFO] No point selected. Exiting.")
            sys.exit(0)

        cv2.setMouseCallback("Select basketball (click near center)", h_mouse_callback)

        while True:
            display = frame.copy()
            if clicked_point is not None:
                cv2.circle(display, clicked_point, 5, (0, 255, 255), -1)
            cv2.imshow("Select basketball (click near center)", display)

            key = cv2.waitKey(10) & 0xFF
            if key != 255:
                break


        if clicked_point is None:
            print("[INFO] No point selected. Exiting.")
            sys.exit(0)

        cv2.destroyWindow("Select basketball (click near center)")

        h_bbox = detect_hoop(frame, h_clicked_point)
        bbox, mask = tracker.compute_bbox_from_click(frame, clicked_point)
        if bbox is None:
            print("[WARN] Could not find region similar to clicked color.")
            cv2.imshow("Mask", mask)
            cv2.waitKey(0)
            sys.exit(0)

        x, y, w, h = bbox
        print(f"[INFO] Bounding box: x={x}, y={y}, w={w}, h={h}")

        result = frame.copy()
        cv2.rectangle(result, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.circle(result, clicked_point, 5, (0, 0, 255), -1)
        cv2.imshow("Detected region", result)
        cv2.waitKey(0)

        tracker.init(frame, bbox)

        while True:
            success = False
            try:
                success, frame, box = tracker.update()
            except Exception:
                break
            if success:
                (x, y, w, h) = [int(v) for v in box]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(
                    frame,
                    f"{args.tracker} Tracker",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 255, 0),
                    2,
                )
            else:
                cv2.putText(
                    frame,
                    "Tracking lost - re-detecting...",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.7,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("Basketball Tracking", frame)
            if cv2.waitKey(30) & 0xFF == ord("q"):
                break

        cv2.rectangle(first_frame, (bbox[0], box[1]), (box[0] + box[2], box[1] + box[3]), (0, 255, 0), 2)
        cv2.imshow("First Frame", first_frame)

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
