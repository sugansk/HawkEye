from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import urllib.request
from bs4 import BeautifulSoup
import cv2
import geocoder
from geopy.geocoders import Nominatim
import geopy.geocoders

from flask import Flask,request

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
lat=[]
long=[]
count=0
co_ordinates=""
@app.route("/start")
def start():
	global lat
	global long
	global count
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
				print (CLASSES[idx])
				if CLASSES[idx]=="person":
					
					feed_xml=urllib.request.urlopen('127.0.0.1:5000/CurrLoc.html').read()
					feed=BeautifulSoup(feed_xml.decode('utf8'),"lxml")
					#print('\n=============================================================================================\n',feed,'\n==============================================================\n')
					lat.append(feed.find_all('div',id=re.compile('^lat'))
					long.append(feed.find_all('div',id=re.compile('^long'))
					count+=1	
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
@app.route("/getCause",methods=['POST'])
def getCasualties():
	try:
		global lat
		global long
		global count
		print('=================================================================')
		data=request.data
		data=data.decode('ascii')
		print(data)
		
		
		co_ordinates="<!DOCTYPE html><html><head><title>Casualties</title><style>table {font-family: arial, sans-serif; border-collapse: collapse;width: 100%;} td, th { border: 1px solid #dddddd; text-align: left; padding: 8px;} tr:nth-child(even) { background-color: #dddddd;}</style></head><body><h2>The List Of Casualties</h2><table><tr><th>S No</th><th>Latitude</th><th>Longitude</th></tr>"
		
		for i in range(0,count):
			co_ordinates+="<tr><td>"+str(i)+"</td><td>"+str(lat[i])+"</td><td>"+str(lng[i])+"</td></tr>"
		co_ordinates=co_ordinates+'</table></body></html>'
		print(co_ordinates,'------------------------------')
		return co_ordinates
		
	except Exception as e:
		return str(e)
@app.route("/getPath",methods=['POST'])
def getPath():
	try:
		#global co_ordinates
		print('=================================================================')
		data=request.data
		data=data.decode('ascii')
		print(data)
		co_ordinates='<!DOCTYPE html><html><head><title>Path Image</title><style>table {font-family: arial, sans-serif; border-collapse: collapse;width: 100%;} td, th { border: 1px solid #dddddd; text-align: left; padding: 8px;} tr:nth-child(even) { background-color: #dddddd;}</style></head><body><h1>Optimal Path To Rescue</h1><p><img src = "path.png" alt = "Optimal Path To Rescue" /></p><h2>Co-ordinates Of Casualties</h2><table><tr><th>S No</th><th>Latitude</th><th>Longitude</th></tr>'
		
		for i in range(0,count):
			co_ordinates+="<tr><td>"+str(i)+"</td><td>"+str(lat[i])+"</td><td>"+str(lng[i])+"</td></tr>"
		co_ordinates=co_ordinates+'</table></body></html>'
		return co_ordinates
	except Exception as e:
		return str(e)

 @app.route("/")
 def hello():
	content = get_file('index.html')
    return Response(content, mimetype="text/html")
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
    app.run()