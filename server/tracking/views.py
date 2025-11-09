import math
import os
from functools import reduce

import cv2
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

import tracking.math
from tracking.hoop import detect_hoop
from tracking.models import AnalyzedShot
from tracking.tracker import Tracker


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
        start_time = float(request.POST.get("start_time", 0))
        end_time = float(request.POST.get("end_time", 0))

        with Tracker(path, tracker_type) as tracker:
            fps = tracker.get_fps()
            start_frame = int(fps * start_time)
            end_frame = int(fps * end_time)
            tracker.cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame - 1)
            frame = tracker.get_frame()
            _, buffer = cv2.imencode(".jpg", frame)
            thumbnail_name = "thumbnail_" + filename.split(".")[0] + ".jpg"
            fs.save(thumbnail_name, ContentFile(buffer.tobytes()))
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

            boxes = [(0, 0, 0, 0)] * start_frame
            i = 0
            while i < end_frame:
                try:
                    success, frame, box = tracker.update()
                    if not success:
                        break
                    boxes.append(box)
                except Exception:
                    break
                i += 1

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
            made_in_basket = tracking.math.check_is_in_basket(
                points,
                (hoop_bbox[0] + hoop_bbox[2] // 2, hoop_bbox[1] + hoop_bbox[3] // 2),
            )
            is_overshot = tracking.math.check_is_overshot(points, hoop_bbox)
            analyzed_shot = AnalyzedShot(
                video=filename,
                thumbnail=thumbnail_name,
                start_frame=start_frame,
                end_frame=end_frame,
                ball_bboxes=boxes,
                hoop_bbox=hoop_bbox,
                actual_angle=actual_angle,
                actual_velocity=math.sqrt(actual_vel[0] ** 2 + actual_vel[1] ** 2),
                optimal_angle=optimal_angle,
                optimal_velocity=math.sqrt(optimal_vel[0] ** 2 + optimal_vel[1] ** 2),
                px_per_meter=px_per_meter,
                start_pos_x=points[start_frame][0],
                start_pos_y=points[start_frame][1],
                made_in_basket=made_in_basket,
                is_overshot=is_overshot,
            )

            analyzed_shot.save()

            return JsonResponse(model_to_dict(analyzed_shot))

    return HttpResponse("Invalid request method", status=405)


def all(request):
    shots = AnalyzedShot.objects.all()
    shots_list = [model_to_dict(shot) for shot in shots]
    return JsonResponse(shots_list, safe=False)


def get(request, id):
    try:
        shot = AnalyzedShot.objects.get(id=id)
        return JsonResponse(model_to_dict(shot))
    except AnalyzedShot.DoesNotExist:
        return HttpResponse("Shot not found", status=404)


def delete(request, id):
    try:
        shot = AnalyzedShot.objects.get(id=id)
        shot.delete()
        return HttpResponse("Shot deleted", status=200)
    except AnalyzedShot.DoesNotExist:
        return HttpResponse("Shot not found", status=404)


def all_info(request):
    shots = AnalyzedShot.objects.all()
    total_shots = len(shots)
    shots_missed = 0 
    for shot in shots:
        if not shot.made_in_basket:
            shots_missed+=1

    shots_made = len(shots) - shots_missed
    shot_statistics = {
        "shots_made": shots_made,
        "shots_missed": shots_missed,
        "total_shots": total_shots,
    }
    return JsonResponse(shot_statistics, safe=False)
