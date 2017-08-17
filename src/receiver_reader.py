#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
import sys
from struct import *
      
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
        data = data.replace('s ', "")
        data = data.replace(' e', "")
        data = data.replace('\r\n', "")
        #data = data.replace('\x', '')
        self.data_list = data.split(' ')

    def parse(self):
        try:
#            del self.data_list[19]
            self.axes = []
            self.buttons = []
            temp1 = self.data_list[:4]
            temp2 = []
            temp3 = []

            for i in range(4, 8):
                temp2.append(self.data_list[i])

            for j in range(8,19):
                temp3.append(self.data_list[j])

            for x in temp1:
                if x is not '':
                    x = unpack('B', x)
                    x = float(x[0])
                    x = (x / 255.0 * 2)-1
                    self.axes.append(x)
                else:
                    self.axes.append(0.00)

            for x in temp2:
                if x is not '':
                    x = unpack('B', x)
                    x = x[0]
                    x = x - 1
                    self.axes.append(x)
                else:
                    self.axes.append(1)

            for x in temp3:
                if x is not '':
                    x = unpack('B', x)
                    x = x[0]
                    self.buttons.append(x)
                else:
                    self.buttons.append(0)

        except:
            print "Caught Exception"

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
        while x[:2] != "s " or x[-4:] != ' e\r\n' or data_length != 19:
            x = ser.readline()
            if x[:2] == "s " and x[-4:] == ' e\r\n':
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
