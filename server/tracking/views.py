from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from tracking.tracker import Tracker
from tracking.hoop import detect_hoop
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

        with Tracker(path, tracker_type) as tracker:
            frame = tracker.get_frame()
            hoop_bbox = detect_hoop(frame, (hoop_x, hoop_y))
            bbox, _ = tracker.compute_bbox_from_click(frame, (ball_x, ball_y))
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
            return JsonResponse({"ball_bboxes": boxes, "hoop_bbox": hoop_bbox})
    return HttpResponse("Invalid request method", status=405)
