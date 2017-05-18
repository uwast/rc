#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import sys
      
import time
import serial
if len(sys.argv) == 1:
    print("Must give serial port")
    sys.exit()
ser = serial.Serial(
port=sys.argv[1],
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
counter = 0

class parse_receiver:

    def __init__(self, data):
        data = data.replace('st', "")
        data = data.replace('en', "")
        data = data.replace('\r\n', "")
        self.data_list = data.split('\t')

    def parse(self):
        del self.data_list[19]
        self.axes = []
        self.buttons = []
        temp1 = self.data_list[:8]
        temp2 = []

        for i in range(8,19):
            temp2.append(self.data_list[i])

        for x in temp1:
            if x[0] is "-":
                x = x.replace("-","")
                x = float(x)
                x = -1*x
            else:
                x = float(x)
            self.axes.append(x)

        for x in temp2:
			if x[0] is "-":
				x = x.replace("-","")
				x = int(x)
				x = -1*x
			else:
				x = int(x)
			self.buttons.append(x)

    def length(self):
        return len(self.data_list)

def start():
    global pub
    pub = rospy.Publisher('joy', Joy, queue_size=10)
    rospy.init_node('receiver_to_joy', anonymous=True)
    rate = rospy.Rate(100)
    count = 0
    while not rospy.is_shutdown():
        data_length = 0
        x= ""
        while x[:2] != "st" or x[-5:] != '\ten\r\n' or data_length != 20:
            x = ser.readline()
            if x[:2] == "st" and x[-5:] == '\ten\r\n':
                receiver = parse_receiver(x)
                data_length = receiver.length()
        receiver.parse()
        joy = Joy()
        joy.header.stamp = rospy.get_rostime()
        joy.axes = receiver.axes
        joy.buttons = receiver.buttons
        pub.publish(joy)
        rate.sleep()


if __name__ == '__main__':
    try: 
	    start()
    except rospy.ROSInterruptException:
	    pass
