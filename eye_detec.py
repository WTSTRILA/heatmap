import cv2
import math
import csv
import time
import record
import parser

class EyeTracker:
    def __init__(self, video_capture, monitor_width, monitor_height):
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.video_capture = video_capture
        self.writer = csv.writer(open('output.csv', 'w', newline=''))
        self.writer.writerow(['Angle', 'X', 'Y', 'Time'])
        self.start_time = time.time()
        self.monitor_width = monitor_width
        self.monitor_height = monitor_height

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            eyes = self.eye_cascade.detectMultiScale(gray, 1.3, 5)

            data = []
            eye_centers = []
            angles = []

            if len(eyes) == 2:
                f = 1400
                W = 6.3
                for (ex, ey, ew, eh) in eyes:
                    eye_center_x = ex + ew//2
                    eye_center_y = ey + eh//2

                    roi_gray = gray[ey:ey + eh, ex:ex + ew]
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(roi_gray)
                    iris_center_x = ex + min_loc[0]
                    iris_center_y = ey + min_loc[1]

                    dx = iris_center_x - eye_center_x
                    dy = iris_center_y - eye_center_y
                    angle = math.atan2(dy, dx) * 180 / math.pi

                    eye_centers.append((eye_center_x, eye_center_y))
                    angles.append(angle)

                    w = abs(iris_center_x - iris_center_y)
                    d = (W * f) / w

                for angle in angles:
                    tan_angle = math.tan(math.radians(angle))
                    x_offset = tan_angle * (d / 10) * self.monitor_width
                    y_offset = tan_angle * (d / 10) * self.monitor_height
                    x = self.monitor_width // 2 + int(x_offset)
                    y = self.monitor_height // 2 - int(y_offset)
                    if x > 0  and x <= self.monitor_width and y >= 0 and y <= self.monitor_height and x != self.monitor_width/2 and y != self.monitor_height/2 :
                        data.append([angle, x, y, int((time.time() - self.start_time) * 1000)])

                for row in data:
                    self.writer.writerow(row)

                cv2.circle(frame, (iris_center_x, iris_center_y), 10, (0, 0, 255), -1)

                print(f'Angle of rotation: {angle} Focal distance {d}')


            cv2.imshow('Video', frame)
            if cv2.waitKey(1) == ord('q'):
                break

        self.video_capture.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    video_capture = cv2.VideoCapture(0)
    eye_tracker = EyeTracker(video_capture, 2560, 1640)
    eye_tracker.run()
    save_video()
    #parser()
