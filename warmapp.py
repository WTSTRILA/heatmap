import cv2
import numpy as np


cap = cv2.VideoCapture('output.avi')

data = np.genfromtxt('output.csv', delimiter=',', skip_header=1, usecols=(1, 2))

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

color_gradient = np.linspace(255, 0, num=len(data)).astype(np.uint8)
heatmap_color = cv2.applyColorMap(color_gradient, cv2.COLORMAP_JET)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('heatmap_output.avi', fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height))

while True:
    ret, frame = cap.read()

    if not ret:
        break

    blurred = cv2.GaussianBlur(frame, (5, 5), 0)

    result_frame = blurred.copy()

    for i, coord in enumerate(data):
        x, y = coord.astype(int)
        canvas[y, x] = heatmap_color[i]

    heatmap_hsv = cv2.cvtColor(canvas, cv2.COLOR_BGR2HSV)
    result_frame[np.where((heatmap_hsv[:, :, 2] != 0))] = heatmap_hsv[:, :, 0:3][np.where((heatmap_hsv[:, :, 2] != 0))]

    result = cv2.addWeighted(blurred, 0.5, result_frame, 0.5, 0)

    out.write(result)

cap.release()
out.release()
cv2.destroyAllWindows()
