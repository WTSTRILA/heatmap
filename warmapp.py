import cv2
import numpy as np

# Load video file
cap = cv2.VideoCapture('output.avi')

# Read pixel coordinate file
data = np.genfromtxt('output.csv', delimiter=',', skip_header=1, usecols=(1, 2))

# Get frame width and height of the video
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Create an empty canvas frame that matches the size of the video frame
canvas = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

# Create a color gradient from blue to red for the heatmap
color_gradient = np.linspace(255, 0, num=len(data)).astype(np.uint8)
heatmap_color = cv2.applyColorMap(color_gradient, cv2.COLORMAP_JET)

# Create a video writer object for the heatmap video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, cap.get(cv2.CAP_PROP_FPS), (frame_width, frame_height))

# Process each frame of the video
while cap.isOpened():
    ret, frame = cap.read()

    if ret:
        # Apply Gaussian blur to reduce noise and increase result accuracy
        blurred = cv2.GaussianBlur(frame, (5, 5), 0)

        # Create a copy of the video frame
        result_frame = blurred.copy()

        # Use the pixel coordinates from the file to create a heatmap on the canvas frame copy
        for i, coord in enumerate(data):
            x, y = coord
            canvas[int(y), int(x)] = heatmap_color[i]

        # Convert color space, such as HSV, to change the colors on the canvas frame copy to match the heatmap
        heatmap_hsv = cv2.cvtColor(canvas, cv2.COLOR_BGR2HSV)
        result_frame[np.where((heatmap_hsv[:, :, 2] != 0))] = heatmap_hsv[:, :, 0:3][np.where((heatmap_hsv[:, :, 2] != 0))]

        # Overlay the canvas frame copy on the video frame
        result = cv2.addWeighted(blurred, 0.5, result_frame, 0.5, 0)

        # Write the heatmap frame to the video file
        out.write(result)

    else:
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
