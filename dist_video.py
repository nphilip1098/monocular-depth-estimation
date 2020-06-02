import numpy as np
import cv2

cap=cv2.VideoCapture(0)

def find_marker(frame):

	gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
	blurred=cv2.GaussianBlur(gray,(3,3),0)
	edged=cv2.Canny(blurred,35,125)

	(cnts,_)=cv2.findContours(edged.copy(),cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	c = max(cnts, key = cv2.contourArea)
	return cv2.minAreaRect(c)

def distance_to_camera(knownWidth, focalLength, perWidth):
	# compute and return the distance from the maker to the camera
	return (knownWidth * focalLength) / perWidth

# initialize the known distance from the camera to the object, which
# in this case is 40 cm
KNOWN_DISTANCE = 45.0

# initialize the known object width, which in this case, the piece of
# paper is 15 cm wide
KNOWN_WIDTH = 15.0

image = cv2.imread('img1.jpg')
marker = find_marker(image)
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH

while True:

	ret,frame=cap.read()
	marker=find_marker(frame)
	cm = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0])

	box=cv2.cv.BoxPoints(marker)
	box = np.int0(box)
	cv2.drawContours(frame, [box], -1, (0, 255, 0), 2)
	cv2.putText(frame, "%.2fcm" % (cm),
		(frame.shape[1] - 300, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,2.0, (0, 255, 0), 3)

	cv2.imshow("Frame",frame)
	if cv2.waitKey(20) & 0xFF ==ord('q'):
		break

cap.release()
cv2.destroyAllWindows()	