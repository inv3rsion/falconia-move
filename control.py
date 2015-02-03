import serial;
import curses;

motors = serial.Serial("/dev/ttymxc3", 9600);
stdscr = curses.initscr();
while True:
    c = stdscr.getch();
    motors.write(chr(c).upper());

print "Done."
