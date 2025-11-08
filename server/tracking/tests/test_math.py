import cv2
import sys
import argparse
from tracking.tracker import Tracker
from tracking.hoop import detect_hoop
import tracking.math
import math

start_frame = 40
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
            if h_clicked_point is not None:
                cv2.circle(display, h_clicked_point, 5, (0, 255, 255), -1)
            cv2.imshow("Select basketball (click near center)", display)

            key = cv2.waitKey(10) & 0xFF
            if key != 255:
                break


        if clicked_point is None:
            print("[INFO] No point selected. Exiting.")
            sys.exit(0)

        cv2.destroyWindow("Select basketball (click near center)")

        h_bbox = detect_hoop(frame, h_clicked_point)
        if h_bbox is None:
            print("[WARN] Could not detect hoop.")
            sys.exit(0)
        bbox, size, mask = tracker.compute_bbox_from_click(frame, clicked_point)
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

        diffs = []
        points = [(x + w // 2, y + h // 2)]

        while True:
            success = False
            try:
                success, frame, box = tracker.update()
            except Exception:
                break
            if success:
                diffs.append(math.sqrt((x-box[0])**2 + (y-box[1])**2))
                (x, y, w, h) = [int(v) for v in box]
                points.append((x + w // 2, y + h // 2))
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

        start_frame = 0
        basketball_size = 0.234
        px_per_meter = size / basketball_size
        actual_angle = tracking.math.calc_actual_angle(points[start_frame:])
        actual_vel = tracking.math.calc_actual_velocity(points[start_frame:], 1/tracker.get_fps(), px_per_meter)
        optimal_vel = tracking.math.calc_optimal_velocity(
            points[start_frame][0],
            points[start_frame][1],
            h_bbox[0] + h_bbox[2] // 2,
            h_bbox[1],
            px_per_meter,
        )
        cv2.rectangle(first_frame, (h_bbox[0], h_bbox[1]), (h_bbox[0] + h_bbox[2], h_bbox[1] + h_bbox[3]), (0, 0, 255), 2)
        cv2.circle(first_frame, (h_bbox[0] + h_bbox[2] // 2, h_bbox[1]), 5, (255, 255, 0), -1)
        for point in points[start_frame:]:
            cv2.circle(first_frame, point, 5, (255, 0, 0), -1)
        t = 0
        x = points[start_frame][0]
        y = points[start_frame][1]
        while y > 0 and x < frame.shape[1] and x > 0 and y < frame.shape[0]:
            c = (0, 0, 255) if t < 0.5 else (0, 0, 0)
            cv2.circle(first_frame, (x, y), 5, c, -1)
            x = int(points[start_frame][0] + actual_vel[0] * t)
            y = int(points[start_frame][1] + actual_vel[1] * t + 0.5 * 9.81 * px_per_meter * t * t)
            t += 0.01
        t = 0
        x = points[start_frame][0]
        y = points[start_frame][1]
        while y > 0 and x < frame.shape[1] and x > 0 and y < frame.shape[0]:
            c = (0, 255, 0) if t < 0.5 else (0, 0, 0)
            cv2.circle(first_frame, (x, y), 5, c, -1)
            x = int(points[start_frame][0] + optimal_vel[0] * t)
            y = int(points[start_frame][1] + optimal_vel[1] * t + 0.5 * 9.81 * px_per_meter * t * t)
            t += 0.01
        cv2.rectangle(first_frame, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), 2)
        cv2.imshow("First Frame", first_frame)
        cv2.waitKey(0)

        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
