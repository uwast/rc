#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <Servo.h>

ros::NodeHandle  nh;
Servo rudder;

//Read value from cmd_vel
//Multiply by 60 and add to middle position (90) and write to motor 
//Conversion (-1.0, 1.0) -> (30, 150)
void messageCb( const geometry_msgs::Twist& position_msg){
  float dataVal = position_msg.angular.z; 
  rudder.write(90+(dataVal*60)); 
}

ros::Subscriber<geometry_msgs::Twist> sub("cmd_vel", &messageCb );

void setup()
{ 
  pinMode(3, OUTPUT);
  nh.initNode();
  nh.subscribe(sub);
  rudder.attach(3);
}

void loop()
{  
  nh.spinOnce();
  delay(10); //Check for message every 10 milliseconds
}

