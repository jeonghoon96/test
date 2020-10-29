from picamera import PiCamera
# from time import sleep
import time

camera = PiCamera()

camera.start_preview()
time.sleep(5)
camera.capture('/home/pi/image.jpg')
camera.stop_preview()
