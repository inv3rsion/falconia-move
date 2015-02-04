import time;
import serial;
import curses;

output = open("/home/ubuntu/falconia/commands.txt", "w");

motors = serial.Serial("/dev/ttymxc3", 9600);
stdscr = curses.initscr();

stdscr.getch();

while True:
    start_time = time.time();
    c = stdscr.getch();
    end_time = time.time();
    if chr(c).upper() == "Q":
        break;
    output.write("%s\t%s\n" % (chr(c).upper(), end_time - start_time));
    motors.write(chr(c).upper());

print "Done."
