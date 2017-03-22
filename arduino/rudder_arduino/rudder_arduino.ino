#if (ARDUINO >= 100)
 #include <Arduino.h>
#else
 #include <WProgram.h>
#endif

#include <Servo.h> 
#include <ros.h>
#include <std_msgs/Float32.h>

ros::NodeHandle  nh;

Servo servo;

void servo_cb( const std_msgs::Float32& cmd_msg){
  servo.write(cmd_msg.data); 
}


ros::Subscriber<std_msgs::Float32> sub("rudder", servo_cb);

void setup(){
  nh.initNode();
  nh.subscribe(sub);
  
  servo.attach(3); //attach it to pin 3
}

void loop(){
  nh.spinOnce();
  delay(10);
}
