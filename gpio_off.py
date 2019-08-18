import RPi.GPIO as GPIO


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
off_gpio()
