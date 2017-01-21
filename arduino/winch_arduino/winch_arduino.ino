#include <ros.h>
#include <geometry_msgs/Twist.h>
#include <Servo.h>
#include <Encoder.h>
ros::NodeHandle  nh;

Servo winch;
Encoder winchEncoder(18,19);

//Read value from cmd_vel
//Multiply by 1000 and add to 1000 (stop speed) and write to motor controller
// Conversion (-1.0, 1.0) -> (0, 2000)
void messageCb( const geometry_msgs::Twist& winch_msg){
  float dataVal = winch_msg.linear.x; 
  winch.write((1000*dataVal)+1000);   
}                                     

ros::Subscriber<geometry_msgs::Twist> sub("winch", messageCb );


std_msgs::Float encoder_val;
ros::Publisher encoder("encoder", &encoder_val);

void setup()
{
  pinMode(4, OUTPUT); //PWM motor controller output
  pinMode(A3, INPUT); //Potentiometer input
  pinMode(5, INPUT);  //Hall Effect input
  
  pinMode (18,INPUT);
  pinMode (19,INPUT);
  
  winch.attach(4);
  nh.initNode();
  nh.advertise(encoder);
  nh.subscribe(sub);

  int absPos =0;
  int oldPos =0;
  while(digital.read(5) == LOW)  //Wait until the Hall Effect is tripped before zeroing
  {
    delay(1);
  }
  zero();  //Zero the encoder
}

void loop()
{
   absPos =winchEncoder.read(); //add to the encoders counts
   if(absPos != oldPos)
   {
    encoder_msg.data = float(absPos); 
    chatter.publish( &encoder_val ); //publish the encoder value to ROS
   }
   nh.spinOnce();
   oldPos = absPos;
}


//decide position based on potentiometer voltage
//Note that this function will only be run when the hall effect is tripped
//thus limiting the possible voltages and adding accuracy
int zero()
{
  int potVal = analogRead(A3);
  int temp = 0;
    switch (potVal)     //Might have and if else statement here with tolerances.  Values all need to be determined by testing.
    {
      case 0:
      {
        temp = 0;
        break;
      }
      case 1023:
      {
        temp = 3600;
        break;
      }
      default:
      {
        temp = 0;
      }
    }
     
  winchEncoder.write(temp);  //Write an offset to the encoder, thus making it absolute
}

