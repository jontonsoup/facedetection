import cv2
import urllib2
import urllib
from subprocess import call
import time

def detect(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return [], img
    rects[:, 2:] += rects[:, :2]
    return rects, img

def box(rects, img):
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x2, y2), (127, 255, 0), 2)
    cv2.imwrite('detimage.jpg', img);

def send_request(rects):
    if len(rects) > 0:
        print("Face Detected")
        data = urllib.urlencode({})
        request = urllib2.Request('http://middleserver.herokuapp.com/set/face_detected', data)
        response = urllib2.urlopen(request)
    else:
        print("Face Not Detected")
        data = urllib.urlencode({})
        request = urllib2.Request('http://middleserver.herokuapp.com/set/face_not_detected', data)
        response = urllib2.urlopen(request)
while(True):
    print("Taking Picture")
    call(["raspistill", "-awb", "auto" , "-o", "image.jpg"])
    print("Detecting")
    rects, img = detect("image.jpg")
    #box(rects, img)
    send_request(rects)
    call(["rm", "image.jpg"])
    time.sleep(1)
