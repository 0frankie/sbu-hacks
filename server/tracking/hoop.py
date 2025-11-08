from inference_sdk import InferenceHTTPClient
import cv2
import base64

CLIENT = InferenceHTTPClient(
    api_url="https://serverless.roboflow.com",
    api_key="CrneNkMgNmcMGfTFAaD5"
)


def detect_hoop(frame, point, size=200):
    frame = frame[point[1]-size//2:point[1]+size//2, point[0]-size//2:point[0]+size//2]
    _, buffer = cv2.imencode('.jpg', frame)
    img_bytes = base64.b64encode(buffer).decode('utf-8')

    results = CLIENT.infer(img_bytes, model_id="basketball-hoop-images/2")
    bbox = None
    for prediction in results['predictions']:
        if prediction['class'] == 'rim':
            x = int(prediction['x'])
            y = int(prediction['y'])
            w = int(prediction['width'])
            h = int(prediction['height'])
            bbox = (x + point[0] - 3 * size // 4, y + point[1] - 3 * size // 4, w, h)
            break
    return bbox
