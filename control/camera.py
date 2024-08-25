import cv2

def gen_frames():
    cap = cv2.VideoCapture(0)  # 0번 카메라(기본 웹캠) 연결

    if not cap.isOpened():
        print("Cannot open camera")
        return

    while True:
        success, frame = cap.read()
        if not success:
            break

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')