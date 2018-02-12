#!/usr/bin/python
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import requests
import cv2
import subprocess
from mail import sendmail
import ConfigParser

#file to watch
f = 'auth.log'
filepath = '/var/log/'
keywords = ["unlocked","password", "check failed", "login", "authentication failure", "fail"] # keywords to look into
matchedkw=[]

#reading config
configParser = ConfigParser.RawConfigParser()   
configFilePath = r'config.cfg'
configParser.read(configFilePath)
# Sends email to
EMAIL_TO = configParser.get('config','EMAIL_TO')

class MyHandler(FileSystemEventHandler):
    def mail(self, path, matched):
        cur_time = time.strftime("%d-%b-%Y %I:%M:%S%p")
        bodytext = "Someone possibly accessed the laptop at " + str(cur_time) + "\n" + " Matched keywords: " + str(matched)
        subject = 'Laptop unlocked/accessed at ' + str(cur_time)

        sendmail(toaddr=EMAIL_TO, body=bodytext, subject=subject, file=path) # send file=None if you don't want to send an attachment

    def camcapture(self):
    	camera_port = 0
    	camera = cv2.VideoCapture(camera_port)
    	time.sleep(0.1)  # If you don't wait, the image will be dark
    	return_value, image = camera.read()
        stamp = str(int(time.time()))
        imgpath = "/tmp/image_"+ stamp + ".png"
    	cv2.imwrite(imgpath, image)
    	del(camera)  # so that others can use the camera as soon as possible
        return imgpath
    def readingfromfile(self, file):
        line = None
        try:
            line = subprocess.check_output(['tail', '-1', file])
            line = str(line)
        except Exception as e:
            print "ERROR: Unable to read lines from file"

        return line

    def on_modified(self, event):
        flag = False
        matchedkw=[]
        print "Got it! (someevent): ", event, event.src_path
        if str(event.src_path) == filepath + f:
            print "event occured"
            last_line = self.readingfromfile(str(event.src_path))
            for ele in keywords:
                if ele in last_line:
                    if flag is False:
                        flag = True
                    print "Matched keyword:" + ele 
                    matchedkw.append(ele) 
        if flag is True:
            imgpath=None
            imgpath = self.camcapture()
            if imgpath is not None:
                self.mail(imgpath, matchedkw)



if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=filepath, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
