from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tracking.tracker import Tracker
from tracking.hoop import detect_hoop
import tracking.math
from django.core.files.storage import FileSystemStorage
import os


def index(request):
    return HttpResponse("YOooo")


@csrf_exempt
def track(request):
    if request.method == "POST":
        video = request.FILES.get("video")
        if not video:
            return HttpResponse("No video uploaded", status=400)
        fs = FileSystemStorage()
        filename = fs.save(video.name, video)
        path = os.path.join(fs.location, filename)
        tracker_type = request.POST.get("tracker_type", "CSRT")
        ball_x = int(request.POST.get("ball_x", 0))
        ball_y = int(request.POST.get("ball_y", 0))
        hoop_x = int(request.POST.get("hoop_x", 0))
        hoop_y = int(request.POST.get("hoop_y", 0))
        start_frame = int(request.POST.get("start_frame", 0))

        with Tracker(path, tracker_type) as tracker:
            frame = tracker.get_frame()
            hoop_bbox = detect_hoop(frame, (hoop_x, hoop_y))
            if hoop_bbox is None:
                return HttpResponse("Could not detect hoop.", status=400)
            bbox, size, _ = tracker.compute_bbox_from_click(frame, (ball_x, ball_y))
            basketball_size = 0.234
            px_per_meter = size / basketball_size

            if bbox is None:
                return HttpResponse(
                    "Could not find region similar to clicked color.", status=400
                )

            tracker.init(frame, bbox)

            boxes = []
            while True:
                try:
                    success, frame, box = tracker.update()
                    if not success:
                        break
                    boxes.append(box)
                except Exception:
                    break

            points = list(map(lambda b: (b[0] + b[2] // 2, b[1] + b[3] // 2), boxes))
            actual_angle = tracking.math.calc_actual_angle(points[start_frame:])
            actual_vel = tracking.math.calc_actual_velocity(
                points[start_frame:], 1 / tracker.get_fps(), px_per_meter
            )
            optimal_angle = tracking.math.calc_optimal_angle(
                points[start_frame][0],
                points[start_frame][1],
                hoop_bbox[0] + hoop_bbox[2] // 2,
                hoop_bbox[1],
            )
            optimal_vel = tracking.math.calc_optimal_velocity(
                points[start_frame][0],
                points[start_frame][1],
                hoop_bbox[0] + hoop_bbox[2] // 2,
                hoop_bbox[1],
                px_per_meter,
            )

            return JsonResponse(
                {
                    "ball_bboxes": boxes,
                    "hoop_bbox": hoop_bbox,
                    "actual_angle": actual_angle,
                    "actual_velocity": actual_vel,
                    "optimal_angle": optimal_angle,
                    "optimal_velocity": optimal_vel,
                    "px_per_meter": px_per_meter,
                    "start_pos_x": points[start_frame][0],
                    "start_pos_y": points[start_frame][1],
                }
            )
    return HttpResponse("Invalid request method", status=405)
