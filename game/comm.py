import serial
from subprocess import Popen, PIPE

ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

def press_key(key):
	p = Popen(['xte'], stdin=PIPE)
	p.communicate(input=key)


while True:
    rcv = ser.readline()
    cmd = rcv.decode('utf-8').rstrip()

    print (cmd)

    if cmd == "L":
    	press_key('''key j\n''')

    elif cmd == "R":
    	press_key('''key l\n''')

    elif cmd == "U":
    	press_key('''key i\n''')

    elif cmd == "D":
    	press_key('''key k\n''')	

    elif cmd == "TW":
    	press_key('''key a\n''')

    elif cmd == "TS":
    	press_key('''key d\n''')	
		    

