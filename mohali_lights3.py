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
        # print( "...........Network down...............")
        # sys.exit(0)
    except e:
        pass
    else:

        requests.get(url=url + "delete-all")
        sendData(12,18,3,7,13,18,0,0,0,0,0,0,0)


def calc_fuel_saving(l1,l2):

    countL1 = int(l1)
    countL2 = int(l2)
    tradTime = 20
    inteTime1 = ((math.sqrt((2 * 12) / 1.8) + (((countL1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
    inteTime2 = ((math.sqrt((2 * 12) / 1.8) + (((countL2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
    if (inteTime1 > tradTime):
        inteTime1 = tradTime
    if (inteTime2 > tradTime):
        inteTime2 = tradTime
    saveTime = tradTime - inteTime1
    idealVechile = 0
    saveTime = math.floor(saveTime)
    if (saveTime > 0):
        idealVechile = countL2
    global final_fuelWastage
    final_fuelWastage+=(idealVechile * saveTime * 0.16)
    global final_savetime
    final_savetime += saveTime
    return final_savetime,final_fuelWastage
    # print("Total fuel Waste in " + str(saveTime) + " sec is " + str(fuelWastage) + " ml.")

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
        # print( "...........Network down...............")
        # sys.exit(0)
    except e:
        pass
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

print( "CODE START")

beginn()

print("*********************************************")
print("InteLights turned on @: ", datetime.datetime.now().replace(microsecond=0))
print("*********************************************")


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
while(p<10):
    base_frame = cv2.imread('frame_base.png')
    base_frame = imutils.resize(base_frame, width=900, height=900)
    cv2.moveWindow("OUTPUT", 425, 110)

    cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
    cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
    cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255),2)
    cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255),2)

    sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, False,
                         False, False, False, 0)

    cv2.imshow("OUTPUT", base_frame)
    p+=1
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


base_frame = cv2.imread('frame_base.jpg')
base_frame = imutils.resize(base_frame, width=900, height=900)
cv2.moveWindow("OUTPUT", 425, 110)

for i, c in enumerate(cap):

        ret[i], frames[i] = c.read()
        # print( "ret is",ret)
        if True in ret:
            gray[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
            gray2[i] = imutils.resize(gray[i], width=400, height=400)

if False in ret:
            print("-----------------START run in MANUAL MODE ------------------")
            curr_green = 0
            time_curr_green =5
            time_curr_red = time_curr_green + 5
            print( "TIME :", datetime.datetime.now().replace(microsecond=0))
            print( "Current green light is at lane ", (curr_green + 1))
            print( "GReen TIMER: ", time_curr_green)
            print( "Current red light is at lane ", (curr_red + 1))
            print( "RED TIMER: ", time_curr_red)
            print( "---------------------------------------------")
            next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
            cv2.putText(base_frame, 'Start in manual mode', (posx_mode, posy_mode),
                        cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)

            cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane1, posy_lane1),
                        cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
            cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane2, posy_lane2),
                        cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
            cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                        (0, 0, 255),
                        2)
            cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                        (0, 0, 255),
                        2)

            sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
                     False, False, False, 1)

            cv2.imshow("OUTPUT", base_frame)

else:
            print( "-----------------START run in AI MODE ------------------")
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
            print( "Initial traffic", high_score)
            curr_green = high_score.index(min(high_score))
            curr_red = (curr_green + 1) % 4
            if (curr_green == 0):
                if (score1 < 0.5):

                    car_count_1 = 20
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score1 >= 0.5 and score1 < 0.55):

                    car_count_1 = 13
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score1 >= 0.55 and score1 < 0.7):

                    car_count_1 = 6
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                else:

                    car_count_1 = 3
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                time_curr_red = time_curr_green + 5
                print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                print( "Current green light is at lane ", (curr_green + 1))
                print( "GReen TIMER: ", time_curr_green)
                print( "Current red light is at lane ", (curr_red + 1))
                print( "RED TIMER: ", time_curr_red)
                print( "---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                cv2.putText(base_frame, 'Start in AI mode', (posx_mode, posy_mode),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane1, posy_lane1),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane2, posy_lane2),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255),
                            2)
                cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255),
                            2)

                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0, True,
                         False, False, False, 1)

                cv2.imshow("OUTPUT", base_frame)
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
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score2 >= 0.5 and score2 < 0.55):

                    car_count_2 = 15
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score2 >= 0.55 and score2 < 0.7):

                    car_count_2 = 9
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                else:

                    car_count_2 = 4
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                time_curr_red = time_curr_green + 5
                print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                print( "Current green light is at lane ", (curr_green + 1))
                print( "GReen TIMER: ", time_curr_green)
                print( "Current red light is at lane ", (curr_red + 1))
                print( "RED TIMER: ", time_curr_red)
                print( "---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                cv2.putText(base_frame, 'Start in AI mode', (posx_mode, posy_mode),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane2, posy_lane2),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane3, posy_lane3),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0,
                         False,
                         True, False, False, 2)

                cv2.imshow("OUTPUT", base_frame)

                # fullname2 = str(datetime.datetime.now()) + '.png'
                # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density2/' + fullname2, gray[1])

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
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_3 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score3 >= 0.18 and score3 < 0.2):

                    car_count_3 = 18
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score3 >= 0.2 and score3 < 0.22):

                    car_count_3 = 13
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score3 >= 0.22 and score3 < 0.25):

                    car_count_3 = 9
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score3 >= 0.25 and score3 < 0.3):

                    car_count_3 = 5
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                else:

                    car_count_3 = 3
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                time_curr_red = time_curr_green + 5
                print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                print( "Current green light is at lane ", (curr_green + 1))
                print( "GReen TIMER: ", time_curr_green)
                print( "Current red light is at lane ", (curr_red + 1))
                print( "RED TIMER: ", time_curr_red)
                print( "---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                cv2.putText(base_frame, 'Start in AI mode', (posx_mode, posy_mode),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane3, posy_lane3),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane4, posy_lane4),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red,
                         False,
                         False, True, False, 3)

                cv2.imshow("OUTPUT", base_frame)
                # fullname3 = str(datetime.datetime.now()) + '.png'
                # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density3/' + fullname3, frames[2])

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
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score4 >= 0.36 and score4 < 0.39):

                    car_count_4 = 40
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score4 >= 0.39 and score4 < 0.42):

                    car_count_4 = 31
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score4 >= 0.43 and score4 < 0.47):

                    car_count_4 = 22
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score4 >= 0.47 and score4 < 0.50):

                    car_count_4 = 13
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                elif (score4 >= 0.50 and score4 < 0.6):

                    car_count_4 = 8
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                else:

                    car_count_4 = 3
                    time_curr_green = math.ceil(
                        (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                time_curr_red = time_curr_green + 5
                print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                print( "Current green light is at lane ", (curr_green + 1))
                print( "GReen TIMER: ", time_curr_green)
                print( "Current red light is at lane ", (curr_red + 1))
                print( "RED TIMER: ", time_curr_red)
                print( "---------------------------------------------")
                next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                cv2.putText(base_frame, 'Start in AI mode', (posx_mode, posy_mode),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane1, posy_lane1),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                            (0, 0, 255), 2)
                cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane4, posy_lane4),
                            cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green,
                         False,
                         False, False, True, 4)

                cv2.imshow("OUTPUT", base_frame)

frames = [None] * 4
gray = [None] * 4
gray2 = [None] * 4
ret = [None] * 4

cap = [cv2.VideoCapture(i) for i in names]
while True:

    base_frame = cv2.imread('frame_base.jpg')
    base_frame = imutils.resize(base_frame, width=900, height=900)
    cv2.moveWindow("OUTPUT", 425, 110)


    if ((datetime.datetime.now().replace(microsecond=0) == next_time.replace(microsecond=0))):


        for i,c in enumerate(cap):
            ret[i], frames[i] = c.read()
            # print( "ret before normal mode is ",ret)
            if ret[i] ==True:
                # print( "----------feeds accessible------",i+1)
                gray[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
                gray2[i] = imutils.resize(gray[i], width=400, height=400)

        if False in ret:
                    print( "---------------After start in MANUAL MODE-----------------")

                    curr_green = curr_red
                    curr_red = (curr_green + 1) % 4

                    time_curr_green = 5
                    time_curr_red = time_curr_green + 5

                    next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)

                    if(curr_green==0):
                        cv2.putText(base_frame, 'After Start in MANUAL mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane1, posy_lane1),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane2, posy_lane2),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)

                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_green, time_curr_red, 0, 0,
                                 True, False, False, False, 1)

                        cv2.imshow("OUTPUT", base_frame)
                    elif(curr_green ==1):
                        cv2.putText(base_frame, 'After Start in MANUAL mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane2, posy_lane2),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane3, posy_lane3),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red,
                                 0, False,
                                 True, False, False, 2)

                        cv2.imshow("OUTPUT", base_frame)


                    elif(curr_green==2):
                        cv2.putText(base_frame, 'After Start in MANUAL mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane3, posy_lane3),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane4, posy_lane4),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green,
                                 time_curr_red, False,
                                 False, True, False, 3)

                        cv2.imshow("OUTPUT", base_frame)


                    else:
                        cv2.putText(base_frame, 'After Start in MANUAL mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED: ' + str(int(time_curr_red)), (posx_lane1, posy_lane1),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed,
                                    (0, 0, 255), 2)
                        cv2.putText(base_frame, 'GREEN: ' + str(int(time_curr_green)), (posx_lane4, posy_lane4),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0,
                                 time_curr_green, False,
                                 False, False, True, 4)

                        cv2.imshow("OUTPUT", base_frame)


        else:
                    print( "---------AI MODE ON-----------------------")

                    curr_green = curr_red
                    curr_red =(curr_green+1) % 4

                    if(curr_green ==0):
                        gray_new = gray[1] #cropping the second feed (ROI)
                        gray_new = gray_new[150:704, 750:1273]
                        (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)

                        (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        if(score1 <0.5):

                            car_count_1=20
                            time_curr_green = math.ceil(
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score1 >=0.5 and score1 <0.55):

                            car_count_1 = 13
                            time_curr_green = math.ceil(
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score1 >=0.55 and score1 <0.7):

                            car_count_1=6
                            time_curr_green = math.ceil(
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        else:

                            car_count_1 = 3
                            time_curr_green = math.ceil(
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_1 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                        if (score2 < 0.5):

                            car_count_2 = 29
                        elif (score2 >= 0.5 and score2 < 0.55):

                            car_count_2 = 15
                        elif (score2 >= 0.55 and score2 < 0.7):

                            car_count_2 = 9
                        else:

                            car_count_2 = 4

                        if (score3 < 0.18):

                            car_count_3 = 25
                        elif (score3 >= 0.18 and score3 < 0.2):

                            car_count_3 = 18
                        elif (score3 >= 0.2 and score3 < 0.22):

                            car_count_3 = 13
                        elif (score3 >= 0.22 and score3 < 0.25):

                            car_count_3 = 9
                        elif (score3 >= 0.25 and score3 < 0.3):

                            car_count_3 = 5
                        else:

                            car_count_3 = 3

                        if (score4 < 0.36):

                            car_count_4 = 50
                        elif (score4 >= 0.36 and score4 < 0.39):

                            car_count_4 = 40
                        elif (score4 >= 0.39 and score4 < 0.42):

                            car_count_4 = 31
                        elif (score4 >= 0.43 and score4 < 0.47):

                            car_count_4 = 22
                        elif (score4 >= 0.47 and score4 < 0.50):

                            car_count_4 = 13
                        elif (score4 >= 0.50 and score4 < 0.6):

                            car_count_4 = 8
                        else:

                            car_count_4 = 3

                        time_curr_red = time_curr_green + 5
                        print( "TIME :",datetime.datetime.now().replace(microsecond=0))
                        print( "Current green light is at lane " , (curr_green + 1))
                        print( "GReen TIMER: " , time_curr_green)
                        print( "Current red light is at lane " , (curr_red + 1))
                        print( "RED TIMER: " , time_curr_red)
                        print( "---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                        # timee,fuel =calc_fuel_saving(car_count_1,car_count_2)
                        #
                        # cv2.putText(base_frame, 'Time Saved in sec.: ' + str(timee), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        # cv2.putText(base_frame, 'Fuel Saved in ml.: ' + str(fuel), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        cv2.putText(base_frame, 'After Start in AI mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'GREEN: '+str(int(time_curr_green)), (posx_lane1,posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        cv2.putText(base_frame, 'RED: '+str(int(time_curr_red)), (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)

                        sendData(car_count_1,car_count_2,car_count_3,car_count_4,time_curr_green,time_curr_red,0,0,True,False,False,False,1)

                        cv2.imshow("OUTPUT", base_frame)
                        # fullname1 = str(datetime.datetime.now()) + '.png'
                        # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density1/' + fullname1, frames[0])


                    if (curr_green == 1):
                        gray_new = gray[1]
                        gray_new =gray_new[150:704, 750:1273]
                        (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        if (score1 < 0.5):
                            time_curr_green = 40
                            car_count_1 = 20
                        elif (score1 >= 0.5 and score1 < 0.55):
                            time_curr_green = 22
                            car_count_1 = 13
                        elif (score1 >= 0.55 and score1 < 0.7):
                            time_curr_green = 15
                            car_count_1 = 6
                        else:
                            time_curr_green = 10
                            car_count_1 = 3

                        if (score2 < 0.5):

                            car_count_2 = 29
                            time_curr_green =math.ceil (
                            (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score2 >= 0.5 and score2 < 0.55):

                            car_count_2 = 15
                            time_curr_green =math.ceil (
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score2 >= 0.55 and score2 < 0.7):

                            car_count_2 = 9
                            time_curr_green =math.ceil (
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        else:

                            car_count_2 = 4
                            time_curr_green = math.ceil(
                                (math.sqrt((2 * 12) / 1.8) + (((car_count_2 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                        if (score3 < 0.18):

                            car_count_3 = 25

                        elif (score3 >= 0.18 and score3 < 0.2):

                            car_count_3 = 18
                        elif (score3 >= 0.2 and score3 < 0.22):

                            car_count_3 = 13
                        elif (score3 >= 0.22 and score3 < 0.25):

                            car_count_3 = 9
                        elif (score3 >= 0.25 and score3 < 0.3):

                            car_count_3 = 5
                        else:

                            car_count_3 = 3

                        if (score4 < 0.36):

                            car_count_4 = 50
                        elif (score4 >= 0.36 and score4 < 0.39):

                            car_count_4 = 40
                        elif (score4 >= 0.39 and score4 < 0.42):

                            car_count_4 = 31
                        elif (score4 >= 0.43 and score4 < 0.47):

                            car_count_4 = 22
                        elif (score4 >= 0.47 and score4 < 0.50):

                            car_count_4 = 13
                        elif (score4 >= 0.50 and score4 < 0.6):

                            car_count_4 = 8
                        else:

                            car_count_4 = 3

                        time_curr_red = time_curr_green + 5
                        print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                        print( "Current green light is at lane " , (curr_green + 1))
                        print( "GReen TIMER: " , time_curr_green)
                        print( "Current red light is at lane " , (curr_red + 1))
                        print( "RED TIMER: " , time_curr_red)
                        print( "---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                        # timee,fuel = calc_fuel_saving(car_count_2, car_count_3)
                        #
                        # cv2.putText(base_frame, 'Time Saved in sec.: ' + str(timee), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        # cv2.putText(base_frame, 'Fuel Saved in ml.: ' + str(fuel), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        cv2.putText(base_frame, 'After Start in AI mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0,255), 2)
                        cv2.putText(base_frame, 'GREEN: '+str(int(time_curr_green)), (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175,0), 2)
                        cv2.putText(base_frame, 'RED: '+str(int(time_curr_red)), (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX,fontSizeTimer, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, time_curr_green, time_curr_red, 0, False,
                                True, False, False, 2)

                        cv2.imshow("OUTPUT", base_frame)

                        # fullname2 = str(datetime.datetime.now()) + '.png'
                        # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density2/' + fullname2, gray[1])


                    if (curr_green == 2):
                        gray_new = gray[1]
                        gray_new = gray_new[150:704, 750:1273]

                        (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        if (score1 < 0.5):
                            time_curr_green = 40
                            car_count_1 = 20
                        elif (score1 >= 0.5 and score1 < 0.55):
                            time_curr_green = 22
                            car_count_1 = 13
                        elif (score1 >= 0.55 and score1 < 0.7):
                            time_curr_green = 15
                            car_count_1 = 6
                        else:
                            time_curr_green = 10
                            car_count_1 = 3

                        if (score2 < 0.5):

                            car_count_2 = 29
                        elif (score2 >= 0.5 and score2 < 0.55):

                            car_count_2 = 15
                        elif (score2 >= 0.55 and score2 < 0.7):

                            car_count_2 = 9
                        else:

                            car_count_2 = 4

                        if (score3 < 0.18):

                            car_count_3 = 25
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_3 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score3 >= 0.18 and score3 < 0.2):

                            car_count_3 = 18
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score3 >= 0.2 and score3 < 0.22):

                            car_count_3 = 13
                            time_curr_green =math.ceil ((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score3 >= 0.22 and score3 < 0.25):

                            car_count_3 = 9
                            time_curr_green =math.ceil ((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score3 >= 0.25 and score3 < 0.3):

                            car_count_3 = 5
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        else:

                            car_count_3 = 3
                            time_curr_green =math.ceil ((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                        if (score4 < 0.36):

                            car_count_4 = 50
                        elif (score4 >= 0.36 and score4 < 0.39):

                            car_count_4 = 40
                        elif (score4 >= 0.39 and score4 < 0.42):

                            car_count_4 = 31
                        elif (score4 >= 0.43 and score4 < 0.47):

                            car_count_4 = 22
                        elif (score4 >= 0.47 and score4 < 0.50):

                            car_count_4 = 13
                        elif (score4 >= 0.50 and score4 < 0.6):

                            car_count_4 = 8
                        else:

                            car_count_4 = 3

                        time_curr_red = time_curr_green + 5
                        print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                        print( "Current green light is at lane " , (curr_green + 1))
                        print( "GReen TIMER: " , time_curr_green)
                        print( "Current red light is at lane " , (curr_red + 1))
                        print( "RED TIMER: " , time_curr_red)
                        print( "---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)
                        # timee,fuel = calc_fuel_saving(car_count_3, car_count_4)
                        # cv2.putText(base_frame, 'Time Saved in sec.: ' + str(timee), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        # cv2.putText(base_frame, 'Fuel Saved in ml.: ' + str(fuel), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        cv2.putText(base_frame, 'After Start in AI mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0,255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'GREEN: '+str(int(time_curr_green)), (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 175, 0), 2)
                        cv2.putText(base_frame, 'RED: '+str(int(time_curr_red)), (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, 0, 0, time_curr_green, time_curr_red, False,
                                False, True, False, 3)

                        cv2.imshow("OUTPUT", base_frame)
                        # fullname3 = str(datetime.datetime.now()) + '.png'
                        # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density3/' + fullname3, frames[2])



                    if (curr_green == 3):

                        gray_new = gray[1]
                        gray_new = gray_new[150:704, 750:1273]

                        (score1, diff1) = compare_ssim(grayA1, gray[0], full=True)
                        (score2, diff2) = compare_ssim(grayA2, gray_new, full=True)
                        (score3, diff3) = compare_ssim(grayA3, gray[2], full=True)
                        (score4, diff4) = compare_ssim(grayA4, gray[3], full=True)

                        if (score1 < 0.5):
                            time_curr_green = 40
                            car_count_1 = 20
                        elif (score1 >= 0.5 and score1 < 0.55):
                            time_curr_green = 22
                            car_count_1 = 13
                        elif (score1 >= 0.55 and score1 < 0.7):
                            time_curr_green = 15
                            car_count_1 = 6
                        else:
                            time_curr_green = 10
                            car_count_1 = 3

                        if (score2 < 0.5):

                            car_count_2 = 29
                        elif (score2 >= 0.5 and score2 < 0.55):

                            car_count_2 = 15
                        elif (score2 >= 0.55 and score2 < 0.7):

                            car_count_2 = 9
                        else:

                            car_count_2 = 4

                        if (score3 < 0.18):

                            car_count_3 = 25
                        elif (score3 >= 0.18 and score3 < 0.2):

                            car_count_3 = 18
                        elif (score3 >= 0.2 and score3 < 0.22):

                            car_count_3 = 13
                        elif (score3 >= 0.22 and score3 < 0.25):

                            car_count_3 = 9
                        elif (score3 >= 0.25 and score3 < 0.3):

                            car_count_3 = 5
                        else:

                            car_count_3 = 3

                        if (score4 < 0.36):

                            car_count_4 = 50
                            time_curr_green =math.ceil ((math.sqrt((2*12)/1.8)+(((car_count_4/4)-1)*(math.sqrt((5.5*2/1.7))))))
                        elif (score4 >= 0.36 and score4 < 0.39):

                            car_count_4 = 40
                            time_curr_green = math.ceil(
                            (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score4 >= 0.39 and score4 < 0.42):

                            car_count_4 = 31
                            time_curr_green = math.ceil( (math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score4 >= 0.43 and score4 < 0.47):

                            car_count_4 = 22
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score4 >= 0.47 and score4 < 0.50):

                            car_count_4 = 13
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        elif (score4 >= 0.50 and score4 < 0.6):

                            car_count_4 = 8
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))
                        else:

                            car_count_4 = 3
                            time_curr_green = math.ceil((math.sqrt((2 * 12) / 1.8) + (((car_count_4 / 4) - 1) * (math.sqrt((5.5 * 2 / 1.7))))))

                        time_curr_red = time_curr_green + 5
                        print( "TIME :", datetime.datetime.now().replace(microsecond=0))
                        print( "Current green light is at lane " , (curr_green + 1))
                        print( "GReen TIMER: " , time_curr_green)
                        print( "Current red light is at lane " , (curr_red + 1))
                        print( "RED TIMER: " , time_curr_red)
                        print( "---------------------------------------------")
                        next_time = datetime.datetime.now() + datetime.timedelta(seconds=time_curr_red)


                        # timee,fuel = calc_fuel_saving(car_count_4, car_count_1)
                        # cv2.putText(base_frame, 'Time Saved in sec.: ' + str(timee), (40, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        # cv2.putText(base_frame, 'Fuel Saved in ml.: ' + str(fuel), (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        #             (255, 0, 0), 2)
                        cv2.putText(base_frame, 'After Start in AI mode', (posx_mode, posy_mode),
                                    cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (255, 0, 0), 2)
                        cv2.putText(base_frame, 'RED: '+str(int(time_curr_red)), (posx_lane1, posy_lane1), cv2.FONT_HERSHEY_SIMPLEX, fontSizeTimer, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane2, posy_lane2), cv2.FONT_HERSHEY_SIMPLEX,fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'RED', (posx_lane3, posy_lane3), cv2.FONT_HERSHEY_SIMPLEX, fontSizeRed, (0, 0, 255), 2)
                        cv2.putText(base_frame, 'GREEN: '+str(int(time_curr_green)), (posx_lane4, posy_lane4), cv2.FONT_HERSHEY_SIMPLEX,fontSizeTimer, (0, 175, 0), 2)
                        sendData(car_count_1, car_count_2, car_count_3, car_count_4, time_curr_red, 0, 0, time_curr_green, False,
                                False, False, True, 4)

                        cv2.imshow("OUTPUT", base_frame)


            # fullname3 = str(datetime.datetime.now()) + '.png'
            # cv2.imwrite('/home/gaurav/PycharmProjects/itl/density4/' + fullname3, frames[3])
    # pos1=[670,1180,720,150]
    # pos2=[30,310,690,300]w

    # if True == all(ret):
    # for i, f in enumerate(frames):
    #     if ret[i] is True:
    #         cv2.moveWindow(window_titles[i], pos1[i], pos2[i])
    #         cv2.imshow(window_titles[i], gray2[i])



    if cv2.waitKey(1) & 0xFF == ord('q'):
        print( "Exiting")
        requests.get(url=url + "delete-all")

        break

cv2.destroyAllWindows()
