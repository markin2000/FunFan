import cv2
import time

camera_port = 0
pic_width = 1280
pic_height = 1024
FOV = 75


# Captures a single image from the camera and returns it in PIL format
def get_image(camera):
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im


class PeopleDetector(object):
    def __init__(self):
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        # self.hogParams = {'winStride': (4, 4), 'padding': (32, 32), 'scale': 1.05}
        self.hogParams = {'winStride': (4, 4), 'padding': (8, 8), 'scale': 1.05}

    def get(self, img):
        foundLocations, foundWeights = self.hog.detectMultiScale(img, **self.hogParams)
        r = None
        if len(foundLocations) > 0 and len(foundLocations[0]) > 0:
            r = foundLocations[0]
            # print("Results: " + str(r))
        return r


if __name__ == '__main__':
    PD = PeopleDetector()
    # initialize camera
    camera = cv2.VideoCapture(camera_port)
    pic_width = camera.get(3)
    pic_height = camera.get(4)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)

    servo = GPIO.PWM(pin, 50)  # 50?
    servo.start(NEUTRAL)

    try:
        while True:
            img = get_image(camera)
            if img is None or img.shape is None:
                continue
            time.sleep(0.1)
            res = PD.get(img)
            print res
            if res is not None:
                (x, y, w, h) = res
                xpos = x + w / 2.0
                servo.ChangeDutyCycle(toDutyCycle(deg))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.imshow('image', img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
                # except:
                #     pass
    except KeyboardInterrupt:
        GPIO.cleanup()
        print 'kill!!!!'
