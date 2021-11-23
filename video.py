import cv2


def detect_mouth(frame, face_neighboors=10, mouth_neighboors=50):
    face_detector=cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    mouth_detector = cv2.CascadeClassifier('models/haarcascade_smile.xml')
    faces=face_detector.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=face_neighboors)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    for (fx, fy, fw, fh) in faces:
        cv2.rectangle(frame, (fx, fy), (fx+fw, fy+fh), (255, 0, 0), 2)
        roi_gray = gray[fy:fy+fh, fx:fx+fw]
        roi_color = frame[fy:fy+fh, fx:fx+fw]
        mouth = mouth_detector.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=mouth_neighboors)
        for (mx, my, mw, mh) in mouth:
            cv2.rectangle(roi_color,(mx,my),(mx+mw,my+mh),(0,255,0),2)


def gen_frames(save=False): 

    # инициализация камеры
    camera = cv2.VideoCapture(0)

    if save:
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi', fourcc, 30.0, (640,  480))
     
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            print("Can't receive frame")
            break
        else:
            detect_mouth(frame)
            if save:
                out.write(frame)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


if __name__ == '__main__':
    gen_frames()
            