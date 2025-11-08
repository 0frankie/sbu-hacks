import cv2
import argparse
import sys

def create_tracker(tracker_type="CSRT"):
    """
    Create a tracker using OpenCV's legacy module (OpenCV 4.12+).
    """
    tracker_type = tracker_type.upper()
    if tracker_type == "BOOSTING":
        return cv2.legacy.TrackerBoosting.create()
    elif tracker_type == "MIL":
        return cv2.legacy.TrackerMIL.create()
    elif tracker_type == "KCF":
        return cv2.legacy.TrackerKCF.create()
    elif tracker_type == "TLD":
        return cv2.legacy.TrackerTLD.create()
    elif tracker_type == "MEDIANFLOW":
        return cv2.legacy.TrackerMedianFlow.create()
    elif tracker_type == "MOSSE":
        return cv2.legacy.TrackerMOSSE.create()
    elif tracker_type == "CSRT":
        return cv2.legacy.TrackerCSRT.create()
    else:
        raise ValueError(f"Unknown tracker type: {tracker_type}")


def main():
    # --- Parse command line arguments ---
    parser = argparse.ArgumentParser(description="OpenCV 4.12 Object Tracker")
    parser.add_argument(
        "--video", 
        type=str, 
        required=True,
        help="Path to video file or camera index (e.g. 0)"
    )
    parser.add_argument(
        "--tracker",
        type=str,
        default="CSRT",
        help="Tracker type: BOOSTING, MIL, KCF, TLD, MEDIANFLOW, MOSSE, CSRT"
    )
    args = parser.parse_args()

    # --- Video source ---
    try:
        video_source = int(args.video)  # allow webcam index
    except ValueError:
        video_source = args.video

    cap = cv2.VideoCapture(video_source)
    if not cap.isOpened():
        print(f"[ERROR] Cannot open video source: {args.video}")
        sys.exit(1)

    # --- Read first frame ---
    ret, frame = cap.read()
    if not ret:
        print("[ERROR] Cannot read first frame.")
        sys.exit(1)

    # --- Select ROI ---
    roi = cv2.selectROI("Select ROI", frame, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow("Select ROI")

    # --- Create and initialize tracker ---
    tracker = create_tracker(args.tracker)
    tracker.init(frame, roi)
    print(f"[INFO] Using tracker: {args.tracker}")

    # --- Tracking loop ---
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[INFO] End of video or cannot read frame.")
            break

        success, box = tracker.update(frame)

        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{args.tracker} Tracker", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            cv2.putText(frame, "Tracking failure detected", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        cv2.imshow("Tracking", frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
        main()
