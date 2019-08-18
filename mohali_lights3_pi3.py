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
import sys
import time
from time import sleep
import RPi.GPIO as GPIO





# Variables
curr_green = 0
curr_red= (curr_green+1) % 4

time_curr_green = 0
time_curr_red = 0

car_count_1=0
car_count_2=0
car_count_3=0
car_count_4=0

final_savetime = 0
final_fuelWastage = 0
url = "http://18.191.226.151/"

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
        sendData(12,18,3,7,13,18,0,0,0,0,0,0,0)



def sendData(l1_count,l2_count,l3_count,l4_count,l1_timer,l2_timer,l3_timer,l4_timer,a,b,c,d,x):
    payload={
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
        "green":x
        }
    try:

        urlopen("https://www.google.com/")
    except urllib2.URLError:
        pass
        # print "...........Network down..............."
        # sys.exit(0)

    else:
        headers = {"content-type":"application/json"}
        requests.post(url = url,data=json.dumps(payload),headers=headers)


fontSizeTimer =0.8
fontSizeRed =0.8
posx_mode =100
posy_mode =100
posx_lane1=400
posy_lane1=200
posx_lane2=600
posy_lane2=280
posx_lane3=400
posy_lane3=500
posx_lane4=200
posy_lane4=280




names = ['base1_car.mp4', 'base2_car.mp4', 'base3_car.mp4', 'base4_car.mp4']
window_titles = ['LANE1', 'LANE2', 'LANE3', 'LANE4']


print ("..............Clearing previous data...............")
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)

GPIO.setup(7, GPIO.OUT, initial = 1)
#GPIO.setup(20, GPIO.OUT, initial = 0)
GPIO.setup(21, GPIO.OUT, initial = 1)
GPIO.setup(26, GPIO.OUT, initial = 0)
#GPIO.setup(19, GPIO.OUT, initial = 0)
GPIO.setup(13, GPIO.OUT, initial = 1)
GPIO.setup(4, GPIO.OUT, initial = 1)
#GPIO.setup(17, GPIO.OUT, initial = 0)
GPIO.setup(27, GPIO.OUT, initial = 0)
GPIO.setup(23, GPIO.OUT, initial = 1)
#GPIO.setup(24, GPIO.OUT, initial = 0)
GPIO.setup(25, GPIO.OUT, initial = 0)

beginn()




print ("..............Reading video feeds.................")
cap = [cv2.VideoCapture(i) for i in names]

imageA1 = cv2.imread("base1.png")
imageA2 = cv2.imread("base2.jpg")
imageA3 = cv2.imread("base3.jpg")
imageA4 = cv2.imread("base4.png")

grayA1 = cv2.cvtColor(imageA1, cv2.COLOR_BGR2GRAY)
grayA2 = cv2.cvtColor(imageA2, cv2.COLOR_BGR2GRAY)
grayA3 = cv2.cvtColor(imageA3, cv2.COLOR_BGR2GRAY)
grayA4 = cv2.cvtColor(imageA4, cv2.COLOR_BGR2GRAY)


frames = [None] * 4
gray = [None] * 4
gray2 = [None] * 4
ret = [None] * 4


p=0
while(p<5):

    p+=1
    print ("...............ALL RED...................")
    GPIO.output(21,GPIO.HIGH) #G1 OFF
    GPIO.output(7,GPIO.LOW) #R1 ON
    GPIO.output(4,GPIO.LOW) #R2 ON
    GPIO.output(27,GPIO.LOW) #G2 OFF
    GPIO.output(26,GPIO.HIGH) #R3 ON
    GPIO.output(13,GPIO.HIGH) #G3 OFF
    GPIO.output(23,GPIO.LOW) #R4 ON
    GPIO.output(25,GPIO.LOW) #G4 OFF

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
            GPIO.output(21,GPIO.LOW) #G1 ON
            GPIO.output(7,GPIO.HIGH) #R1 OFF
            GPIO.output(4,GPIO.LOW) #R2 ON
            GPIO.output(27,GPIO.LOW) #G2 OFF
            GPIO.output(26,GPIO.HIGH) #R3 ON
            GPIO.output(13,GPIO.HIGH) #G3 OFF
            GPIO.output(23,GPIO.LOW) #R4 ON
            GPIO.output(25,GPIO.LOW) #G4 OFF
            curr_green = 0
            time_curr_green =5
            time_curr_red = time_curr_green + 5
            print ("TIME :", datetime.datetime.now().replace(microsecond=0))
            print ("Current green light is at lane ", (curr_green + 1))
            print ("GReen TIMER: ", time_curr_green)
            print ("Current red light is at lane ", (curr_red + 1))
            print ("RED TIMER: ", time_curr_red)
            print ("---------------------------------------------")
            next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

            # sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
            #          False, False, False, 1)



else:
            print ("-----------------START run in AI MODE ------------------")
            gray_new = gray[1]  # cropping the second feed (ROI)
            gray_new = gray_new[150:704, 750:1273]
            (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
            (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)

            (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
            (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)
            high_score = []
            high_score.append(score1)
            high_score.append(score2)
            high_score.append(score3)
            high_score.append(score4)

            curr_green = high_score.index(min(high_score))
            curr_red = (curr_green + 1) % 4
            if (curr_green == 0):
                if (score1 < 0.5):

                    car_count_1 = 20
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                elif (score1 >= 0.5 and score1 < 0.55):

                    car_count_1 = 13
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                elif (score1 >= 0.55 and score1 < 0.7):

                    car_count_1 = 6
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                else:

                    car_count_1 = 3
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                time_curr_red = time_curr_green + 5
                GPIO.output(21,GPIO.LOW) #G1 ON
                GPIO.output(7,GPIO.HIGH) #R1 OFF
                GPIO.output(4,GPIO.LOW) #R2 ON
                GPIO.output(27,GPIO.LOW) #G2 OFF
                GPIO.output(26,GPIO.HIGH) #R3 ON
                GPIO.output(13,GPIO.HIGH) #G3 OFF
                GPIO.output(23,GPIO.LOW) #R4 ON
                GPIO.output(25,GPIO.LOW) #G4 OFF

                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)


                # sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
                #          False, False, False, 1)
                #

            if (curr_green == 1):
                gray_new = gray[1]
                gray_new = gray_new[150:704, 750:1273]
                (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                if (score2 < 0.5):

                    car_count_2 = 29
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                elif (score2 >= 0.5 and score2 < 0.55):

                    car_count_2 = 15
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                elif (score2 >= 0.55 and score2 < 0.7):

                    car_count_2 = 9
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                else:

                    car_count_2 = 4
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_2 / 4) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                GPIO.output(21,GPIO.HIGH) #G1 OFF
                GPIO.output(7,GPIO.LOW) #R1 ON
                GPIO.output(4,GPIO.HIGH) #R2 OFF
                GPIO.output(27,GPIO.HIGH) #G2 ON
                GPIO.output(26,GPIO.HIGH) #R3 ON
                GPIO.output(13,GPIO.HIGH) #G3 OFF
                GPIO.output(23,GPIO.LOW) #R4 ON
                GPIO.output(25,GPIO.LOW) #G4 OFF
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                # sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0,
                #          False,
                #          True, False, False, 2)


            if (curr_green == 2):
                gray_new = gray[1]
                gray_new = gray_new[150:704, 750:1273]

                (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                if (score3 < 0.18):

                    car_count_3 = 25
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_3 / 4) - 1) * (2.543))))
                elif (score3 >= 0.18 and score3 < 0.2):

                    car_count_3 = 18
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score3 >= 0.2 and score3 < 0.22):

                    car_count_3 = 13
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score3 >= 0.22 and score3 < 0.25):

                    car_count_3 = 9
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score3 >= 0.25 and score3 < 0.3):

                    car_count_3 = 5
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                else:

                    car_count_3 = 3
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                # sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red,
                #          False,
                #          False, True, False, 3)

            if (curr_green == 3):
                gray_new = gray[1]
                gray_new = gray_new[150:704, 750:1273]

                (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                if (score4 < 0.36):

                    car_count_4 = 50
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score4 >= 0.36 and score4 < 0.39):

                    car_count_4 = 40
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score4 >= 0.39 and score4 < 0.42):

                    car_count_4 = 31
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score4 >= 0.43 and score4 < 0.47):

                    car_count_4 = 22
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score4 >= 0.47 and score4 < 0.50):

                    car_count_4 = 13
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                elif (score4 >= 0.50 and score4 < 0.6):

                    car_count_4 = 8
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                else:

                    car_count_4 = 3
                    time_curr_green = math.ceil(
                        (3.651 + (((car_count_4 / 4) - 1) * (2.543))))

                time_curr_red = time_curr_green + 5
                print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                print ("Current green light is at lane ", (curr_green + 1))
                print ("GReen TIMER: ", time_curr_green)
                print ("Current red light is at lane ", (curr_red + 1))
                print ("RED TIMER: ", time_curr_red)
                print ("---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                # sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green,
                #          False, False, False, True, 4)


print ("...............FIRST CYCLE COMPLETE @ ",datetime.datetime.now().replace(microsecond=0))
frames = [None] * 4
gray = [None] * 4
gray2 = [None] * 4
ret = [None] * 4

cap = [cv2.VideoCapture(i) for i in names]
while True:


    if ((datetime.datetime.now().replace(microsecond=0) == next_time.replace(microsecond=0))):


        for i,c in enumerate(cap):
            ret[i], frames[i] = c.read()
            # print "ret before normal mode is ",ret
            if ret[i] ==True:
                # print "----------feeds accessible------",i+1
                gray[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
                gray2[i] = imutils.resize(gray[i], width=400, height=400)

        if False in ret:
                    print ("---------------After start in MANUAL MODE-----------------")

                    curr_green = curr_red
                    curr_red = (curr_green + 1) % 4

                    time_curr_green = 5
                    time_curr_red = time_curr_green + 5

                    next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                    if(curr_green==0):

                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane ", (curr_green + 1))
                        print ("GReen TIMER: ", time_curr_green)
                        print ("Current red light is at lane ", (curr_red + 1))
                        print ("RED TIMER: ", time_curr_red)
                        print ("---------------------------------------------")
                        # sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0,
                        #          True, False, False, False, 1)


                    elif(curr_green ==1):
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane ", (curr_green + 1))
                        print ("GReen TIMER: ", time_curr_green)
                        print ("Current red light is at lane ", (curr_red + 1))
                        print ("RED TIMER: ", time_curr_red)
                        print ("---------------------------------------------")

                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red,
                                 0, False,True, False, False, 2)

                    elif(curr_green==2):
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane ", (curr_green + 1))
                        print ("GReen TIMER: ", time_curr_green)
                        print ("Current red light is at lane ", (curr_red + 1))
                        print ("RED TIMER: ", time_curr_red)
                        print ("---------------------------------------------")

                        # sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green,
                        #          time_curr_red, False, False, True, False, 3)


                    else:
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane ", (curr_green + 1))
                        print ("GReen TIMER: ", time_curr_green)
                        print ("Current red light is at lane ", (curr_red + 1))
                        print ("RED TIMER: ", time_curr_red)
                        print ("---------------------------------------------")

                        # sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0,
                        #          time_curr_green, False,False, False, True, 4)


        else:
                    print ("---------AI MODE ON-----------------------")

                    curr_green = curr_red
                    curr_red =(curr_green+1) % 4

                    if(curr_green ==0):
                        gray_new = gray[1] #cropping the second feed (ROI)
                        gray_new = gray_new[150:704, 750:1273]
                        #(score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        score1 = 0.6
                        # (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        #
                        # (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        # (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        if(score1 <0.5):

                            car_count_1=20
                            time_curr_green = math.ceil(
                                (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                        elif (score1 >=0.5 and score1 <0.55):

                            car_count_1 = 13
                            time_curr_green = math.ceil(
                                (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                        elif (score1 >=0.55 and score1 <0.7):

                            car_count_1=6
                            time_curr_green = math.ceil(
                                (3.651 + (((car_count_1 / 4) - 1) * (2.543))))
                        else:

                            car_count_1 = 3
                            time_curr_green = math.ceil(
                                (3.651 + (((car_count_1 / 4) - 1) * (2.543))))

                        # if (score2 < 0.5):
                        #
                        #     car_count_2 = 29
                        # elif (score2 >= 0.5 and score2 < 0.55):
                        #
                        #     car_count_2 = 15
                        # elif (score2 >= 0.55 and score2 < 0.7):
                        #
                        #     car_count_2 = 9
                        # else:
                        #
                        #     car_count_2 = 4
                        #
                        # if (score3 < 0.18):
                        #
                        #     car_count_3 = 25
                        # elif (score3 >= 0.18 and score3 < 0.2):
                        #
                        #     car_count_3 = 18
                        # elif (score3 >= 0.2 and score3 < 0.22):
                        #
                        #     car_count_3 = 13
                        # elif (score3 >= 0.22 and score3 < 0.25):
                        #
                        #     car_count_3 = 9
                        # elif (score3 >= 0.25 and score3 < 0.3):
                        #
                        #     car_count_3 = 5
                        # else:
                        #
                        #     car_count_3 = 3
                        #
                        # if (score4 < 0.36):
                        #
                        #     car_count_4 = 50
                        # elif (score4 >= 0.36 and score4 < 0.39):
                        #
                        #     car_count_4 = 40
                        # elif (score4 >= 0.39 and score4 < 0.42):
                        #
                        #     car_count_4 = 31
                        # elif (score4 >= 0.43 and score4 < 0.47):
                        #
                        #     car_count_4 = 22
                        # elif (score4 >= 0.47 and score4 < 0.50):
                        #
                        #     car_count_4 = 13
                        # elif (score4 >= 0.50 and score4 < 0.6):
                        #
                        #     car_count_4 = 8
                        # else:
                        #
                        #     car_count_4 = 3

                        time_curr_red = time_curr_green + 5
                        GPIO.output(21,GPIO.LOW) #G1 ON
                        GPIO.output(7,GPIO.HIGH) #R1 OFF
                        GPIO.output(4,GPIO.LOW) #R2 ON
                        GPIO.output(27,GPIO.LOW) #G2 OFF
                        GPIO.output(26,GPIO.HIGH) #R3 ON
                        GPIO.output(13,GPIO.HIGH) #G3 OFF
                        GPIO.output(23,GPIO.LOW) #R4 ON
                        GPIO.output(25,GPIO.LOW) #G4 OFF
                        
                        print ("TIME :",datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane " , (curr_green + 1))
                        print ("GReen TIMER: " , time_curr_green)
                        print ("Current red light is at lane " , (curr_red + 1))
                        print ("RED TIMER: " , time_curr_red)
                        print ("---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                        sendData(car_count_1,car_count_2,car_count_3,car_count_4,time_curr_green,time_curr_red,0,0,True,False,False,False,1)


                    elif (curr_green == 1):
                        gray_new = gray[1]
                        gray_new =gray_new[150:704, 750:1273]
                        # (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        #(score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        score2 = 0.6
                        # (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        # (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        # if (score1 < 0.5):
                        #     # time_curr_green = 40
                        #     car_count_1 = 20
                        # elif (score1 >= 0.5 and score1 < 0.55):
                        #     # time_curr_green = 22
                        #     car_count_1 = 13
                        # elif (score1 >= 0.55 and score1 < 0.7):
                        #     # time_curr_green = 15
                        #     car_count_1 = 6
                        # else:
                        #     # time_curr_green = 10
                        #     car_count_1 = 3

                        if (score2 < 0.5):

                            car_count_2 = 29
                            time_curr_green =math.ceil (
                            (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                        elif (score2 >= 0.5 and score2 < 0.55):

                            car_count_2 = 15
                            time_curr_green =math.ceil (
                                (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                        elif (score2 >= 0.55 and score2 < 0.7):

                            car_count_2 = 9
                            time_curr_green =math.ceil (
                                (3.651 + (((car_count_2 / 4) - 1) * (2.543))))
                        else:

                            car_count_2 = 4
                            time_curr_green = math.ceil(
                                (3.651 + (((car_count_2 / 4) - 1) * (2.543))))


                        time_curr_red = time_curr_green + 5
                        GPIO.output(21,GPIO.HIGH) #G1 OFF
                        GPIO.output(7,GPIO.LOW) #R1 ON
                        GPIO.output(4,GPIO.HIGH) #R2 OFF
                        GPIO.output(27,GPIO.HIGH) #G2 ON
                        GPIO.output(26,GPIO.HIGH) #R3 ON
                        GPIO.output(13,GPIO.HIGH) #G3 OFF
                        GPIO.output(23,GPIO.LOW) #R4 ON
                        GPIO.output(25,GPIO.LOW) #G4 OFF
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane " , (curr_green + 1))
                        print ("GReen TIMER: " , time_curr_green)
                        print ("Current red light is at lane " , (curr_red + 1))
                        print ("RED TIMER: " , time_curr_red)
                        print ("---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0, False,
                                 True, False, False, 2)


                    elif (curr_green == 2):
                        gray_new = gray[1]
                        gray_new = gray_new[150:704, 750:1273]

                        # (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        # (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        #(score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        score3 = 0.1
                        # (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        # if (score1 < 0.5):
                        #     time_curr_green = 40
                        #     car_count_1 = 20
                        # elif (score1 >= 0.5 and score1 < 0.55):
                        #     time_curr_green = 22
                        #     car_count_1 = 13
                        # elif (score1 >= 0.55 and score1 < 0.7):
                        #     time_curr_green = 15
                        #     car_count_1 = 6
                        # else:
                        #     time_curr_green = 10
                        #     car_count_1 = 3
                        #
                        # if (score2 < 0.5):
                        #
                        #     car_count_2 = 29
                        # elif (score2 >= 0.5 and score2 < 0.55):
                        #
                        #     car_count_2 = 15
                        # elif (score2 >= 0.55 and score2 < 0.7):
                        #
                        #     car_count_2 = 9
                        # else:
                        #
                        #     car_count_2 = 4

                        if (score3 < 0.18):

                            car_count_3 = 25
                            time_curr_green = math.ceil((3.651 + (((car_count_3 / 4) - 1) * (2.543))))
                        
                        elif (score3 >= 0.18 and score3 < 0.25):

                            car_count_3 = 9
                            time_curr_green =math.ceil ((3.651 + (((car_count_3 / 4) - 1) * (2.543))))
                        elif (score3 >= 0.25 and score3 < 0.3):

                            car_count_3 = 5
                            time_curr_green = math.ceil((3.651 + (((car_count_3 / 4) - 1) * (2.543))))
                        else:

                            car_count_3 = 3
                            time_curr_green =math.ceil ((3.651 + (((car_count_3 / 4) - 1) * (2.543))))

                        # if (score4 < 0.36):
                        #
                        #     car_count_4 = 50
                        # elif (score4 >= 0.36 and score4 < 0.39):
                        #
                        #     car_count_4 = 40
                        # elif (score4 >= 0.39 and score4 < 0.42):
                        #
                        #     car_count_4 = 31
                        # elif (score4 >= 0.43 and score4 < 0.47):
                        #
                        #     car_count_4 = 22
                        # elif (score4 >= 0.47 and score4 < 0.50):
                        #
                        #     car_count_4 = 13
                        # elif (score4 >= 0.50 and score4 < 0.6):
                        #
                        #     car_count_4 = 8
                        # else:
                        #
                        #     car_count_4 = 3

                        time_curr_red = time_curr_green + 5
                        GPIO.output(21,GPIO.HIGH) #G1 OFF
                        GPIO.output(7,GPIO.LOW) #R1 ON
                        GPIO.output(4,GPIO.LOW) #R2 ON
                        GPIO.output(27,GPIO.LOW) #G2 OFF
                        GPIO.output(26,GPIO.LOW) #R3 OFF
                        GPIO.output(13,GPIO.LOW) #G3 ON
                        GPIO.output(23,GPIO.LOW) #R4 ON
                        GPIO.output(25,GPIO.LOW) #G4 OFF
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane " , (curr_green + 1))
                        print ("GReen TIMER: " , time_curr_green)
                        print ("Current red light is at lane " , (curr_red + 1))
                        print ("RED TIMER: " , time_curr_red)
                        print ("---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red, False,
                                 False, True, False, 3)


                    elif (curr_green == 3):

                        gray_new = gray[1]
                        gray_new = gray_new[150:704, 750:1273]

                        # (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        # (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        # (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        # (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)
                        score4 = 0.3
                        # if (score1 < 0.5):
                        #     time_curr_green = 40
                        #     car_count_1 = 20
                        # elif (score1 >= 0.5 and score1 < 0.55):
                        #     time_curr_green = 22
                        #     car_count_1 = 13
                        # elif (score1 >= 0.55 and score1 < 0.7):
                        #     time_curr_green = 15
                        #     car_count_1 = 6
                        # else:
                        #     time_curr_green = 10
                        #     car_count_1 = 3
                        #
                        # if (score2 < 0.5):
                        #
                        #     car_count_2 = 29
                        # elif (score2 >= 0.5 and score2 < 0.55):
                        #
                        #     car_count_2 = 15
                        # elif (score2 >= 0.55 and score2 < 0.7):
                        #
                        #     car_count_2 = 9
                        # else:
                        #
                        #     car_count_2 = 4
                        #
                        # if (score3 < 0.18):
                        #
                        #     car_count_3 = 25
                        # elif (score3 >= 0.18 and score3 < 0.2):
                        #
                        #     car_count_3 = 18
                        # elif (score3 >= 0.2 and score3 < 0.22):
                        #
                        #     car_count_3 = 13
                        # elif (score3 >= 0.22 and score3 < 0.25):
                        #
                        #     car_count_3 = 9
                        # elif (score3 >= 0.25 and score3 < 0.3):
                        #
                        #     car_count_3 = 5
                        # else:
                        #
                        #     car_count_3 = 3

                        if (score4 < 0.36):

                            car_count_4 = 50
                            time_curr_green =math.ceil ((math.sqrt((2*12)/1.8)+(((car_count_4/4)-1)*(math.sqrt((5.5*2/1.7))))))
                        
                        
                        elif (score4 >= 0.36 and score4 < 0.50):

                            car_count_4 = 13
                            time_curr_green = math.ceil((3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                        elif (score4 >= 0.50 and score4 < 0.6):

                            car_count_4 = 8
                            time_curr_green = math.ceil((3.651 + (((car_count_4 / 4) - 1) * (2.543))))
                        else:

                            car_count_4 = 3
                            time_curr_green = math.ceil((3.651 + (((car_count_4 / 4) - 1) * (2.543))))

                        time_curr_red = time_curr_green + 5
                        GPIO.output(21,GPIO.HIGH) #G1 OFF
                        GPIO.output(7,GPIO.LOW) #R1 ON
                        GPIO.output(4,GPIO.LOW) #R2 ON
                        GPIO.output(27,GPIO.LOW) #G2 OFF
                        GPIO.output(26,GPIO.HIGH) #R3 ON
                        GPIO.output(13,GPIO.HIGH) #G3 OFF
                        GPIO.output(23,GPIO.HIGH) #R4 OFF
                        GPIO.output(25,GPIO.HIGH) #G4 ON
                        print ("TIME :", datetime.datetime.now().replace(microsecond=0))
                        print ("Current green light is at lane " , (curr_green + 1))
                        print ("GReen TIMER: " , time_curr_green)
                        print ("Current red light is at lane " , (curr_red + 1))
                        print ("RED TIMER: " , time_curr_red)
                        print ("---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)


                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green, False,
                                 False, False, True, 4)
