# import the necessary packages
from skimage.measure import compare_ssim
import datetime
import cv2
import imutils
import requests
import json
import math
from urllib.request import urlopen
import urllib3 as urllib2
import RPi.GPIO as GPIO

# Variables
curr_green = 0
curr_red = (curr_green + 1) % 4

time_curr_green = 0
time_curr_red = 0

car_count_1 = 0
car_count_2 = 0
car_count_3 = 0
car_count_4 = 0
red1=2
yel1=3
gre1=4

red2=17
yel2=27
gre2=22

red3=10
yel3=9
gre3=11

red4=5
yel4=6
gre4=13


final_savetime = 0
final_fuelWastage = 0
url = "http://18.191.226.151/"

today11am = datetime.datetime.now().replace(hour=11, minute=0, second=0, microsecond=0)
today12am = datetime.datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)


def beginn():
    global url
    try:

        urlopen("https://www.google.com/")
	

    except urllib2.URLError:
        pass
        # print "...........Network down..............."
        # sys.exit(0)

    else:

        requests.get(url=url + "delete-all")
        sendData(12, 18, 3, 7, 13, 18, 0, 0, 0, 0, 0, 0, 0)


def off_gpio():
    GPIO.output(red1, False)
    GPIO.output(yel1, False)
    GPIO.output(gre1, False)

    GPIO.output(red2, False)
    GPIO.output(yel2, False)
    GPIO.output(gre2, False)

    GPIO.output(red3, False)
    GPIO.output(yel3, False)
    GPIO.output(gre3, False)

    GPIO.output(red4, False)
    GPIO.output(yel4, False)
    GPIO.output(gre4, False)




def sendData(l1_count, l2_count, l3_count, l4_count, l1_timer, l2_timer, l3_timer, l4_timer, a, b, c, d, x):
    payload = {
        "l1": {
            "count": l1_count,
            "timer": l1_timer,
            "running": a
        },
        "l2": {
            "count": l2_count,
            "timer": l2_timer,
            "running": b
        },
        "l3": {
            "count": l3_count,
            "timer": l3_timer,
            "running": c
        },
        "l4": {
            "count": l4_count,
            "timer": l4_timer,
            "running": d
        },
        "green": x
    }
    try:

        urlopen("https://www.google.com/")
    except urllib2.URLError:
        pass
        # print "...........Network down..............."
        # sys.exit(0)

    else:
        headers = {"content-type": "application/json"}
        requests.post(url=url, data=json.dumps(payload), headers=headers)


names = ['9am_lane1.mp4', '9am_lane2.mp4', '9am_lane3.mp4', '9am_lane4.mp4']

print ("..............Clearing previous data...............")
#GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(2, GPIO.OUT, initial = 0)
GPIO.setup(3, GPIO.OUT, initial = 0)
GPIO.setup(4, GPIO.OUT, initial = 0)
GPIO.setup(17, GPIO.OUT, initial = 0)
GPIO.setup(27, GPIO.OUT, initial = 0)
GPIO.setup(22, GPIO.OUT, initial = 0)
GPIO.setup(10, GPIO.OUT, initial = 0)
GPIO.setup(9, GPIO.OUT, initial = 0)
GPIO.setup(11, GPIO.OUT, initial = 0)
GPIO.setup(5, GPIO.OUT, initial = 0)
GPIO.setup(6, GPIO.OUT, initial = 0)
GPIO.setup(13, GPIO.OUT, initial = 0)

print ("gpio done")

beginn()
#
# now = datetime.datetime.now()
# today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
# today1259pm = now.replace(hour=12, minute=59, second=59, microsecond=0)
# today1pm = now.replace(hour=13, minute=0, second=0, microsecond=0)
# today1559pm = now.replace(hour=15, minute=59, second=59, microsecond=0)
# today8am = now.replace(hour=8, minute=0, second=0, microsecond=0)
#

print ("..............Reading video feeds.................")
cap = [cv2.VideoCapture(i) for i in names]

# load 9am base images
image1 = cv2.imread("new_base_lane1_9am.jpg")
image2 = cv2.imread("new_base_lane2_9am.jpg")
image3 = cv2.imread("new_base_lane3_9am.jpg")
image4 = cv2.imread("new_base_lane4_9am.jpg")

imageA1 = image1[156:628, 78:1171]
imageA2 = image2[10:485, 117:1262]

imageA3 = image3[4:521, 137:910]

imageA4 = image4[135:552, 382:1148]

grayA1 = cv2.cvtColor(imageA1, cv2.COLOR_BGR2GRAY)
grayA2 = cv2.cvtColor(imageA2, cv2.COLOR_BGR2GRAY)
grayA3 = cv2.cvtColor(imageA3, cv2.COLOR_BGR2GRAY)
grayA4 = cv2.cvtColor(imageA4, cv2.COLOR_BGR2GRAY)

frames = [None] * 4
gray = [None] * 4
gray2 = [None] * 4
ret = [None] * 4

width_1 = 3.5
width_2 = 4
width_3 = 3.5
widht_4 = 2.5

p = 0
while (p < 5):
    p += 1
    GPIO.output(red1, True)
    GPIO.output(red2, True)
    GPIO.output(red3, True)
    GPIO.output(red4, True)
    print ("...............ALL RED...................")



for i, c in enumerate(cap):

    ret[i], frames[i] = c.read()
    # print "ret is",ret
    if True in ret:
        gray[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
        gray2[i] = imutils.resize(gray[i], width=400, height=400)

print("*********************************************")
print("InteLights turned on @: ", datetime.datetime.now().replace(microsecond=0))
print("*********************************************")

if False in ret:
    print ("-----------------START run in MANUAL MODE ------------------")
    curr_green = 0

    GPIO.output(red1, False)
    GPIO.output(gre1, True)

    time_curr_green = 5
    time_curr_red = time_curr_green + 5
    print ("TIME :", datetime.datetime.now().replace(microsecond=0))
    print ("Current green light is at lane ", (curr_green + 1))
    print ("GReen TIMER: ", time_curr_green)
    print ("Current red light is at lane ", (curr_red + 1))
    print ("RED TIMER: ", time_curr_red)
    print ("---------------------------------------------")
    next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

    sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
             False, False, False, 1)



else:
    print ("-----------------START run in AI MODE ------------------")
    gray_new_0 = gray[0]  # cropping the second feed (ROI)
    gray_new_0 = gray_new_0[156:628, 78:1171]

    gray_new_1 = gray[1]  # cropping the second feed (ROI)
    gray_new_1 = gray_new_1[10:485, 117:1262]

    gray_new_2 = gray[2]
    gray_new_2 = gray_new_2[4:521, 137:910]

    gray_new_3 = gray[3]
    gray_new_3 = gray_new_3[135:552, 382:1148]

    (score1, diff1) = compare_ssim(grayA1, gray_new_0, full=True)
    (score2, diff2) = compare_ssim(grayA2, gray_new_1, full=True)

    (score3, diff3) = compare_ssim(grayA3, gray_new_2, full=True)
    (score4, diff4) = compare_ssim(grayA4, gray_new_3, full=True)
    high_score = []
    high_score.append(score1)
    high_score.append(score2)
    high_score.append(score3)
    high_score.append(score4)

    curr_green = high_score.index(min(high_score))
    curr_red = (curr_green + 1) % 4

    if (curr_green == 0):
        gray_new_0 = gray[0]  # cropping the second feed (ROI)
        gray_new_0 = gray_new_0[156:628, 78:1171]
        (score1, diff1) = compare_ssim(grayA1, gray_new_0, full=True)
        GPIO.output(gre4, False)
        GPIO.output(red4, True)

        GPIO.output(gre1, True)
        GPIO.output(red1, False)


        if (score1 < 0.41):

            car_count_1 = 38
            time_curr_green = math.ceil(
                (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
        elif (score1 >= 0.41 and score1 < 0.55):

            car_count_1 = 30
            time_curr_green = math.ceil(
                (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
        elif (score1 >= 0.55 and score1 < 0.67):

            car_count_1 = 20
            time_curr_green = math.ceil(
                (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
        elif (score1 >= 0.67 and score1 < 0.75):

            car_count_1 = 12
            time_curr_green = math.ceil(
                (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
        else:

            car_count_1 = 5
            time_curr_green = math.ceil(
                (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))

        time_curr_red = time_curr_green + 5
        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
        print ("Current green light is at lane ", (curr_green + 1))
        print ("GReen TIMER: ", time_curr_green)
        print ("Current red light is at lane ", (curr_red + 1))
        print ("RED TIMER: ", time_curr_red)
        print ("---------------------------------------------")
        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
                 False, False, False, 1)


    elif (curr_green == 1):
        GPIO.output(gre1, False)
        GPIO.output(red1, True)

        GPIO.output(gre2, True)
        GPIO.output(red2, False)

        if (score2 < 0.44):
            car_count_2 = 35
            time_curr_green = math.ceil((3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
        elif (score2 >= 0.44 and score2 < 0.54):
            car_count_2 = 27
            time_curr_green = math.ceil(
                (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
        elif (score2 >= 0.54 and score2 < 0.6):
            car_count_2 = 18
            time_curr_green = math.ceil(
                (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))

        else:

            car_count_2 = 5
            time_curr_green = math.ceil(
                (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
        time_curr_red = time_curr_green + 5
        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
        print ("Current green light is at lane ", (curr_green + 1))
        print ("GReen TIMER: ", time_curr_green)
        print ("Current red light is at lane ", (curr_red + 1))
        print ("RED TIMER: ", time_curr_red)
        print ("---------------------------------------------")
        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0,
                 False,
                 True, False, False, 2)


    elif (curr_green == 2):
        GPIO.output(gre2, False)
        GPIO.output(red2, True)
        GPIO.output(gre3, True)
        GPIO.output(red3, False)

        if (score3 < 0.54 and (today11am < datetime.date.now() and datetime.datetime.now() < today12am)):
            car_count_3 = 30
            time_curr_green = math.ceil((3.651 + (((car_count_3 / width_3) - 1) * (2.543))))

        else:

            if (score3 < 0.54):
                car_count_3 = 15
                time_curr_green = math.ceil((3.651 + (((car_count_3 / width_3) - 1) * (2.543))))
            elif (score3 >= 0.54 and score3 < 0.66):
                car_count_3 = 12
                time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))
            elif (score3 >= 0.66 and score3 < 0.75):
                car_count_3 = 6
                time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))

            else:
                car_count_3 = 4
                time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))

        time_curr_red = time_curr_green + 5

        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
        print ("Current green light is at lane ", (curr_green + 1))
        print ("GReen TIMER: ", time_curr_green)
        print ("Current red light is at lane ", (curr_red + 1))
        print ("RED TIMER: ", time_curr_red)
        print ("---------------------------------------------")
        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red,
                 False,
                 False, True, False, 3)


    elif (curr_green == 3):
        GPIO.output(gre3, False)
        GPIO.output(red3, True)
        GPIO.output(gre4, True)
        GPIO.output(red4, False)

        if (score4 < 0.36):
            car_count_4 = 35
            time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

        elif (score4 >= 0.36 and score4 < 0.57):
            car_count_4 = 32
            time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

        elif (score4 >= 0.57 and score4 < 0.66):
            car_count_4 = 25
            time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

        elif (score4 >= 0.66 and score4 < 0.72):
            car_count_4 = 15
            time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

        else:

            car_count_4 = 5
            time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))
        time_curr_red = time_curr_green + 5

        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
        print ("Current green light is at lane ", (curr_green + 1))
        print ("GReen TIMER: ", time_curr_green)
        print ("Current red light is at lane ", (curr_red + 1))
        print ("RED TIMER: ", time_curr_red)
        print ("---------------------------------------------")

        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green,
                 False,
                 False, False, True, 4)

print ("...............FIRST CYCLE COMPLETE @ ", datetime.datetime.now().replace(microsecond=0))
frames = [None] * 4
gray = [None] * 4
gray2 = [None] * 4
ret = [None] * 4

cap = [cv2.VideoCapture(i) for i in names]

while True:
    for i, c in enumerate(cap):
        ret[i], frames[i] = c.read()

    if ((datetime.datetime.now().replace(microsecond=0) == next_time.replace(microsecond=0))):



        if False in ret:
            print ("---------------After start in MANUAL MODE-----------------")

            curr_green = curr_red
            curr_red = (curr_green + 1) % 4

            time_curr_green = 5
            time_curr_red = time_curr_green + 5

            next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

            if (curr_green == 0):
                GPIO.output(gre4, False)
                GPIO.output(red4, True)

                GPIO.output(gre1, True)
                GPIO.output(red1, False)

                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0,
                         True, False, False, False, 1)


            elif (curr_green == 1):
                GPIO.output(gre1, False)
                GPIO.output(red1, True)

                GPIO.output(gre2, True)
                GPIO.output(red2, False)

                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red,
                         0, False, True, False, False, 2)

            elif (curr_green == 2):
                GPIO.output(gre2, False)
                GPIO.output(red2, True)
                GPIO.output(gre3, True)
                GPIO.output(red3, False)
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green,
                         time_curr_red, False, False, True, False, 3)


            else:
                GPIO.output(gre3, False)
                GPIO.output(red3, True)
                GPIO.output(gre4, True)
                GPIO.output(red4, False)
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0,
                         time_curr_green, False, False, False, True, 4)


        else:
            print ("---------AI MODE ON-----------------------")

            if ret[0] == True and ret[1] == True and ret[2] == True and ret[3] == True:
                for i in [0, 1, 2, 3]:
                    # print "----------feeds accessible------",i+1
                    gray[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
                    gray2[i] = imutils.resize(gray[i], width=400, height=400)

            curr_green = curr_red
            curr_red = (curr_green + 1) % 4

            if (curr_green == 0):

                gray_new_0 = gray[0]  # cropping the second feed (ROI)
                gray_new_0 = gray_new_0[156:628, 78:1171]
                (score1, diff1) = compare_ssim(grayA1, gray_new_0, full=True)

                if (score1 < 0.41):

                    car_count_1 = 38
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
                elif (score1 >= 0.41 and score1 < 0.55):

                    car_count_1 = 30
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
                elif (score1 >= 0.55 and score1 < 0.67):

                    car_count_1 = 20
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
                elif (score1 >= 0.67 and score1 < 0.75):

                    car_count_1 = 12
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))
                else:

                    car_count_1 = 5
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - width_1) * (2.543))))

                GPIO.output(gre4, False)
                GPIO.output(red4, True)

                GPIO.output(gre1, True)
                GPIO.output(red1, False)

                time_curr_red = time_curr_green + 5

                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
                         False, False, False, 1)

            elif (curr_green == 1):
                gray_new_1 = gray[1]
                gray_new_1 = gray_new_1[10:485, 117:1262]

                (score2, diff2) = compare_ssim(grayA2, gray_new_1, full=True)

                if (score2 < 0.44):

                    car_count_2 = 35
                    time_curr_green = math.ceil((3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
                elif (score2 >= 0.44 and score2 < 0.54):

                    car_count_2 = 27
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
                elif (score2 >= 0.54 and score2 < 0.6):

                    car_count_2 = 18
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))
                else:

                    car_count_2 = 5
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / width_2) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                GPIO.output(gre1, False)
                GPIO.output(red1, True)

                GPIO.output(gre2, True)
                GPIO.output(red2, False)
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0,
                         False,
                         True, False, False, 2)



            elif (curr_green == 2):
                gray_new_2 = gray[2]
                gray_new_2 = gray_new_2[4:521, 137:910]

                (score3, diff3) = compare_ssim(grayA3, gray_new_2, full=True)

                if (score3 < 0.54 and (today11am < datetime.datetime.now() and datetime.datetime.now() < today12am)):
                    car_count_3 = 30
                    time_curr_green = math.ceil((3.651 + (((car_count_3 / width_3) - 1) * (2.543))))

                else:

                    if (score3 < 0.54):

                        car_count_3 = 15
                        time_curr_green = math.ceil((3.651 + (((car_count_3 / width_3) - 1) * (2.543))))
                    elif (score3 >= 0.54 and score3 < 0.66):

                        car_count_3 = 12
                        time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))
                    elif (score3 >= 0.66 and score3 < 0.75):

                        car_count_3 = 6
                        time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))

                    else:

                        car_count_3 = 4
                        time_curr_green = math.ceil((3.651 + (((car_count_4 / width_3) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                GPIO.output(gre2, False)
                GPIO.output(red2, True)
                GPIO.output(gre3, True)
                GPIO.output(red3, False)

                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red,
                         False,
                         False, True, False, 3)



            elif (curr_green == 3):

                gray_new_3 = gray[3]
                gray_new_3 = gray_new_3[135:552, 382:1148]

                (score4, diff4) = compare_ssim(grayA4, gray_new_3, full=True)

                if (score4 < 0.36):

                    car_count_4 = 35
                    time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))
                elif (score4 >= 0.36 and score4 < 0.57):

                    car_count_4 = 32
                    time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

                elif (score4 >= 0.57 and score4 < 0.66):

                    car_count_4 = 25
                    time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))
                elif (score4 >= 0.66 and score4 < 0.72):

                    car_count_4 = 15
                    time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

                else:

                    car_count_4 = 5
                    time_curr_green = math.ceil((3.651 + (((car_count_4 / widht_4) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                GPIO.output(gre3, False)
                GPIO.output(red3, True)
                GPIO.output(gre4, True)
                GPIO.output(red4, False)
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green,
                         False,
                         False, False, True, 4)

