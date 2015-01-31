import serial;
import urllib2;
import time;
import math;

motors = serial.Serial('/dev/ttymxc3', 9600);

TURNRIGHT = "6";
TURNLEFT = "4";
FORWARD = "8";
BACKWARD = "2";
STOP = "5";
FULL_TURN_TIME = 23; # TIME TAKES TO TURN 360, IN SECONDS
TPOS_X = 1433;
TPOS_Y = 408;
DIST_THRESHOLD = 100;
points = [(1472, 380), (1129, 350), (1001, 797)];

def getGPS():
    try:
        data = urllib2.urlopen("http://10.144.7.183/coord.txt").read();
        return int(data.split(",")[0]), int(data.split(",")[1]);
    except:
        print "Could not access coordinates...";

def getUntilDifferent(x, y):
    dx, dy = getGPS();
    while dx == x and dy == y:
        dx, dy = getGPS();
    
def around(x, y, tx, ty):
    return (tx - DIST_THRESHOLD <= x <= tx + DIST_THRESHOLD) and (ty - DIST_THRESHOLD <= y <= ty + DIST_THRESHOLD);

def moveUntilAt(tx, ty):
    dx, dy = getGPS();
    while not around(dx, dy, tx, ty):
        forward(3);
        stop();
        getUntilDifferent(dx, dy);
        dx, dy = getGPS();
    stop();
    
def forward(t):
    motors.write(FORWARD);
    time.sleep(t);

def calcAngle(x, y):
    x = -x;
    print "differences: ", x, y
    angle = math.atan(float(y)/float(x)) * 180.0 / math.pi;
    print "calc angle", angle
    if x == 0:
        if y >= 0:
            return 90;
        else:
            return 270;
    elif x > 0:
        return angle % 360;
    else:
        return (180+angle) % 360;

def angleTime(angle):
    return FULL_TURN_TIME * float(angle) / 360.0;

def turn(direction, angle):
    direction = direction.upper();
    if direction[0] == "L":
        motors.write(TURNLEFT);
        time.sleep(angleTime(angle));
    else:
        motors.write(TURNRIGHT);
        time.sleep(angleTime(angle));
    stop();

def stop():
    motors.write(STOP);


time.sleep(10);
# get current position
curX, curY = getGPS();
print "currentPosition (start)", curX, curY;
# move forwards for 3 seconds
forward(3);
stop();

getUntilDifferent(curX, curY);
# get current position (again)
nextX, nextY = getGPS();
print "nextCoords", nextX, nextY;
difX = nextX - curX;
difY = nextY - curY;
curAngle = calcAngle(difX, difY);
print "currentAngle", curAngle;

for point in points:
    time.sleep(10);
    nextX, nextY = getGPS();
    TPOS_X = point[0];
    TPOS_Y = point[1];
    stop();
    curX, curY = getGPS();
    print "curPos", curX, curY;
    # get target position
    moveX = TPOS_X - nextX;
    moveY = TPOS_Y - nextY;
    # get angle
    targetAngle = calcAngle(moveX, moveY);
    # turn to get correct angle
    moveAngle = (targetAngle - curAngle) % 360;
    print "moveangle", moveAngle;
    turn("LEFT", moveAngle);
    curAngle = targetAngle;

    moveUntilAt(TPOS_X, TPOS_Y);
    stop();
