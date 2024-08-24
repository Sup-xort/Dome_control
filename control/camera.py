import cv2

def gen_frames():
    cap = cv2.VideoCapture(0)  # 웹캠 열기 (0은 첫 번째 웹캠을 의미)
    while True:
        success, frame = cap.read()  # 웹캠에서 프레임 읽기
        if not success:
            break
        else:
            # 프레임을 JPEG로 인코딩
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            # 프레임을 바이트 스트림으로 반환
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
