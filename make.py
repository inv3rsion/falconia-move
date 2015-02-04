import math;
import time;
import urllib2;
import serial;

commands = [];
motors = serial.Serial("/dev/ttymxc3", 9600, timeout=0);

TURNRIGHT = "6";
TURNLEFT = "4";
FORWARD = "8";
BACKWARD = "2";
STOP = "5";
FULL_TURN_TIME = 23;
DIST_THRESHOLD = 50;
STARTX = 1472;
ENDX = 380;

def around(tx, ty, cx, cy):
    return (tx - cx) ** 2 + (ty - cy) ** 2 < DIST_THRESHOLD ** 2;

def get_gps():
    try:
        data = urllib2.urlopen("http://10.144.7.183/coord.txt").read();
        return int(data.split(",")[0]), int(data.split(",")[1]);
    except:
        print "Could not access coordinates...";

def forward(amt):
    motors.write(FORWARD);
    time.sleep(amt);

def stop():
    motors.write(STOP);

def wait_until_gps_updates(x, y):
    newx, newy = get_gps();
    while newx == x and newy == y:
        newx, newy = get_gps();

def get_current_angle(dx, dy):
    if dx == 0:
        if dy >= 0:
            return 90;
        return 270;
    elif dx < 0:
        angle = math.atan(dy, dx) * 180 / math.pi;
        angle = (180 + angle) % 360;
        return angle;
    else:
        angle = math.atan(dy, dx) * 180 / math.pi;
        return angle;

def turnleft(angle):
    turn_time = angle / 360.0 * FULL_TURN_TIME;
    motors.write(TURN_LEFT);
    time.sleep(turn_time);

def drive_until_at(tx, ty):
    dx, dy = getGPS();
    while not around(tx, ty, dx, dy):
        forward(3);
        stop();
        wait_until_gps_updates(dx, dy);
        dx, dy = get_gps();
    stop();

def get_to_starting_position():
    time.sleep(13);
    cx, cy = get_gps();
    time.sleep(6);
    forward(3);
    stop();
    wait_until_gps_updates(cx, cy);
    nx, ny = get_gps();
    dx = nx - cx;
    dy = ny - cy;
    cangle = get_current_angle(dx, dy);
    print "current angle:", cangle;
    
    dx = STARTX - nx;
    dy = STARTY - ny;
    tangle = get_current_angle(dx, dy);
    turn_angle = (tangle - cangle) % 360;
    turnleft(turn_angle);
    drive_until_at(STARTX, STARTY);
    turn_angle = (60 - tangle) % 360;
    turnleft(turn_angle);
    time.sleep(3);

def run():
    get_to_starting_position();
    for command in commands:
        motors.write(command[0]);
        time.sleep(command[1]);

def read_commands():
    with open("/home/ubuntu/falconia/commands.txt", "r") as f:
        for line in f.readlines():
            data = line.strip().split("\t");
            commands.append([data[0], float(data[1])]);

def main():
    read_commands();
    run();

if __name__ == '__main__':
    main();
