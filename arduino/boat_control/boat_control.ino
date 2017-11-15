#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Float32.h>
#include <std_msgs/Int32.h>
#include <math.h>

#define WindVanePin (A4)       // The pin the wind vane sensor is connected to

ros::NodeHandle  nh;
std_msgs::Int32 winddir;

Servo servo_rudder;
Servo servo_winch;
int VaneValue;       // raw analog value from wind vane
int CalDirection;    // calibrated wind value
int LastValue;
int count=0;

void servo_cb( const std_msgs::Float32& cmd_msg){
    //Write the received data directly to the rudder servo
    servo_rudder.write(cmd_msg.data);  
}

void winch_cb( const std_msgs::Int32& pos_msg){
    //map the rotation (0-2160 degrees) to a motor value between 1000 and 2000
    int position_msg = map(pos_msg.data, 0, 2160, 1000, 2000);
    servo_winch.writeMicroseconds(position_msg);
}

ros::Subscriber<std_msgs::Float32> sub_rudder("rudder", servo_cb);
ros::Subscriber<std_msgs::Int32> sub_winch("winch",winch_cb);
ros::Publisher anemometer("anemometer", &winddir);

void setup(){
    // setup subscribers 
    nh.initNode();
    nh.subscribe(sub_rudder);
    nh.subscribe(sub_winch);
    nh.advertise(anemometer);
  
    servo_rudder.attach(3); // attach rudder to pin 3
    servo_winch.attach(4); // attach winch to pin 4
    LastValue = 0;

    pinMode(WindVanePin, INPUT);
}

void loop(){
     VaneValue = analogRead(WindVanePin);

     // Map 0-1023 ADC value to 0-360
     CalDirection = map(VaneValue, 0, 1023, 0, 360);
   
     if(CalDirection >= 360)
         CalDirection = CalDirection - 360;
     
     if(CalDirection < 0)
         CalDirection = CalDirection + 360;
  

      // Only update the display if change greater than 5 degrees. 
    if(abs(CalDirection - LastValue) > 5)
    { 
         LastValue = CalDirection;
         winddir.data = CalDirection;
         anemometer.publish(&winddir);
       
    }
  
    nh.spinOnce();
}
