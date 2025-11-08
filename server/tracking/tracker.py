import cv2
import numpy as np


class Tracker:
    def __init__(self, source, tracker_type):
        self.source = source
        self.tracker_type = tracker_type

    def __enter__(self):
        self.cap = cv2.VideoCapture(self.source)
        self.bbox = None
        if not self.cap.isOpened():
            raise IOError(f"Cannot open video source: {self.source}")

        self.tracker = Tracker.create_tracker(self.tracker_type)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.cap.isOpened():
            self.cap.release()

    def init(self, frame, bbox):
        self.bbox = bbox
        self.tracker.init(frame, bbox)

    def update(self):
        frame = self.get_frame()
        success, box = self.tracker.update(frame)
        if success:
            self.bbox = box
        return success, frame, box

    @staticmethod
    def create_tracker(tracker_type):
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

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            raise IOError("Cannot read frame from video source")
        return frame

    def compute_bbox_from_click(
        self, frame, point, hsv_tolerance=(15, 50, 50), added_padding=5
    ):
        """
        Segment region around clicked pixel using HSV with hue wrapping.
        hsv_tolerance = (H, S, V)
        """
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.int16)
        h, s, v = hsv[point[1], point[0]]

        h_tol, s_tol, v_tol = hsv_tolerance

        # Saturation and value clamping
        lower_s = max(0, s - s_tol)
        upper_s = min(255, s + s_tol)
        lower_v = max(0, v - v_tol)
        upper_v = min(255, v + v_tol)

        # Handle hue wrapping
        lower_h = (h - h_tol) % 180
        upper_h = (h + h_tol) % 180

        # If lower_h > upper_h, we wrap around and need two masks
        if lower_h <= upper_h:
            lower = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
            upper = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)
            mask = cv2.inRange(hsv, lower, upper)
        else:
            # wrap-around case
            lower1 = np.array([0, lower_s, lower_v], dtype=np.uint8)
            upper1 = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)
            lower2 = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
            upper2 = np.array([179, upper_s, upper_v], dtype=np.uint8)
            mask1 = cv2.inRange(hsv, lower1, upper1)
            mask2 = cv2.inRange(hsv, lower2, upper2)
            mask = cv2.bitwise_or(mask1, mask2)

        # Ensure clicked pixel is included
        if mask[point[1], point[0]] == 0:
            mask[point[1], point[0]] = 255

        # Clean up mask
        mask = cv2.medianBlur(mask, 7)
        mask = cv2.erode(mask, None, iterations=1)
        mask = cv2.dilate(mask, None, iterations=2)

        # Find contours
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # just for shape reference
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            return None, mask

        # Choose contour containing clicked point or nearest
        chosen = None
        min_dist = float("inf")
        for cnt in contours:
            if cv2.pointPolygonTest(cnt, point, False) >= 0:
                chosen = cnt
                break
            else:
                M = cv2.moments(cnt)
                if M["m00"] > 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    dist = np.hypot(cx - point[0], cy - point[1])
                    if dist < min_dist:
                        min_dist = dist
                        chosen = cnt

        if chosen is None:
            return None, mask

        x, y, w, h = cv2.boundingRect(chosen)
        return (
            x - added_padding,
            y - added_padding,
            w + 2 * added_padding,
            h + 2 * added_padding,
        ), mask
