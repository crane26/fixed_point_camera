# -*- coding: utf-8 -*-
import subprocess
import picamera
import os
from time import sleep
import requests


shutter_numb = 0
photo_dir = os.path.expanduser('~/Desktop/tsuruM1/fixed_point_camera/picture')

camera = picamera.PiCamera()
# camera.hflip = True
# camera.vflip = True


def setting():
    camera.resolution = (600,315)
    # camera.brightness = 50
    # camera.flash_mode = 'on'
    # camera.exposure_compensation = 0

def preview(preview_time = 3):
    camera.start_preview()
    sleep(preview_time)
    camera.stop_preview()

def loadFile():
    global shutter_numb

    if os.path.isdir(photo_dir):
        pass
    else:
        print("make photo directory")
        os.mkdir(photo_dir)

    filename = os.path.join(photo_dir, 'camera.set')

    if os.path.isfile(filename):
        pass
    else:
        print("make camera set file")
        with open(filename, mode='w') as fp:
            fp.write('0')

    with open(filename) as fp:
        fp = open(filename)
        tmp_shutter_numb = fp.readlines()
        tmp_shutter_numb = tmp_shutter_numb[0].rstrip()
        shutter_numb = int(tmp_shutter_numb)

def shutter():
    global shutter_numb

    # load shutter number from setting file
    loadFile()

    filename = os.path.join(photo_dir, 'camera.set')

    shutter_numb += 1

    # write shutter number to setting file
    with open(filename, mode='w') as fp:
        fp.write(str(shutter_numb))

    # take photo
    filename = os.path.join(photo_dir, str("{0:06d}".format(shutter_numb)) + '.jpg')
    print(filename)
    with open(filename, mode='wb') as fp:
        camera.capture(fp)

    # send image to LINE
    url = "https://notify-api.line.me/api/notify"
    token = "F2am4nhtK6UOMbLBmKLcEuMpiI8owiE47ytmCWzkg7z"
    headers = {"Authorization": "Bearer " + token}

    message = "ラズパイから写真を送信"
    params = {"message":  message}
    files = {"imageFile": open(filename, "rb")}
    r = requests.post(url, headers=headers, params=params, files=files)
    print(r.text)


if __name__ == '__main__':
    setting()
    preview()
    shutter()
    camera.close()
