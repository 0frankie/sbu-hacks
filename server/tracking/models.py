from django.db import models


class AnalyzedShot(models.Model):
    video = models.CharField(max_length=255)
    start_frame = models.IntegerField()
    ball_bboxes = models.JSONField()
    hoop_bbox = models.JSONField()
    actual_angle = models.FloatField()
    actual_velocity = models.FloatField()
    optimal_angle = models.FloatField()
    optimal_velocity = models.FloatField()
    px_per_meter = models.FloatField()
    start_pos_x = models.IntegerField()
    start_pos_y = models.IntegerField()

