from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import geocoder
import urllib.request
from bs4 import BeautifulSoup
import cv2

from flask import Flask

CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

net = cv2.dnn.readNetFromCaffe("MobileNetSSD_deploy.prototxt.txt", "MobileNetSSD_deploy.caffemodel")

print("[INFO] starting video stream...")
vs = VideoStream(src=0).start()
time.sleep(2.0)
fps = FPS().start()

app = Flask(__name__, static_url_path="")
@app.route("/start", methods)
def start():
	while True:
		# grab the frame from the threaded video stream and resize it
		# to have a maximum width of 400 pixels
		frame = vs.read()
		frame = imutils.resize(frame, width=400)

		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)),
			0.007843, (300, 300), 127.5)

		# pass the blob through the network and obtain the detections and
		# predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in np.arange(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with
			# the prediction	
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is
			# greater than the minimum confidence
			if confidence > 0.2:
				# extract the index of the class label from the
				# `detections`, then compute the (x, y)-coordinates of
				# the bounding box for the object
				idx = int(detections[0, 0, i, 1])
				box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
				(startX, startY, endX, endY) = box.astype("int")

				# draw the prediction on the frame
				#print (CLASSES[idx])
				if CLASSES[idx]=="person":
					

					
					label = "{}: {:.2f}%".format(CLASSES[idx],
						confidence * 100)
					cv2.rectangle(frame, (startX, startY), (endX, endY),
						COLORS[idx], 2)
					y = startY - 15 if startY - 15 > 15 else startY + 15
					cv2.putText(frame, label, (startX, y),
						cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

		# show the output frame
		cv2.imshow("Frame", frame)
		key = cv2.waitKey(1) & 0xFF

		# if the `q` key was pressed, break from the loop
		if key == ord("q"):
			break

		# update the FPS counter
		fps.update()

	# stop the timer and display FPS information
	fps.stop()
	print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
	print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

	# do a bit of cleanup
	cv2.destroyAllWindows()
	vs.stop()	
# @app.route("/")
# def hello():
# 	message = """<html>
# 	<body>

# 	<p>Click the button to get your coordinates.</p>

# 	<button onclick="getLocation()">Try It</button>

# 	<p><strong>Note:</strong> The geolocation property is not supported in IE8 and earlier versions.</p>

# 	<p id="demo"></p>

# 	<script>
# 	var x = document.getElementById("demo");

# 	function getLocation() {
# 	if (navigator.geolocation) {
# 	navigator.geolocation.getCurrentPosition(showPosition);
# 	} else { 
# 	return "Geolocation is not supported by this browser.";
# 	}
# 	}

# 	function showPosition(position) {
# 	console.log( position.coords.latitude + " " +position.coords.longitude);
# 	x.innerHTML=position.coords.latitude + " " +position.coords.longitude;
# 	}
# 	</script>

# 	</body>
# 	</html>
# 	"""
# 	return message
	
if __name__ == "__main__":
    app.run(host="127.0.0.1" ,debug=True)