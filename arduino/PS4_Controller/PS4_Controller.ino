#include <PS4USB.h>

#ifdef dobogusinclude
#include <spi4teensy3.h>
#include <SPI.h>
#endif


int buttons[11];
float axes[8];
USB Usb;
PS4USB PS4(&Usb);

void setup() {
  Serial.begin(9600);
#if !defined(__MIPSEL__)
  while (!Serial); // Wait for serial port to connect - used on Leonardo, Teensy and other boards with built-in USB CDC serial connection
#endif
  if (Usb.Init() == -1) {
    Serial.print(F("\r\nOSC did not start"));
    while (1); // Halt
  }
}
void loop() {
    Usb.Task();
    if (PS4.connected()) {
        if (PS4.getAnalogHat(LeftHatX) > 137 || PS4.getAnalogHat(LeftHatX) < 117) {
            if(PS4.getAnalogHat(LeftHatX)>137)     
                PS4.setRumbleOn(PS4.getAnalogHat(LeftHatX)-128, PS4.getAnalogHat(LeftHatX)-128);
            else
                PS4.setRumbleOn(128-PS4.getAnalogHat(LeftHatX), 128-PS4.getAnalogHat(LeftHatX));
            axes[0] = float(PS4.getAnalogHat(LeftHatX));}
        else{
            axes[0] = 128;
            PS4.setRumbleOn(0, 0);
        }
        if (PS4.getAnalogHat(LeftHatY) > 137 || PS4.getAnalogHat(LeftHatY) < 117)
            axes[1] = float(PS4.getAnalogHat(LeftHatY));
        else
            axes[1] = 128;
        if (PS4.getAnalogHat(RightHatX) > 137 || PS4.getAnalogHat(RightHatX) < 117)
           axes[3] = float(PS4.getAnalogHat(RightHatX));
        else
            axes[3] = 128;
        if (PS4.getAnalogHat(RightHatY) > 137 || PS4.getAnalogHat(RightHatY) < 117)
            axes[4] = float(PS4.getAnalogHat(RightHatY));
        else
            axes[4] = 128;
      
        axes[2] = float(PS4.getAnalogButton(L2));
        axes[5] = float(PS4.getAnalogButton(R2));
        
      
        if (PS4.getButtonClick(UP)) {
            PS4.setLed(Blue);
            axes[7] =1.00;
        }
        else if (PS4.getButtonClick(DOWN)) {
            PS4.setLed(Red);
            axes[7] =-1.00;
        }
        else
            axes[7] =0;
          
        if (PS4.getButtonClick(LEFT)) {
            PS4.setLed(Yellow);
            axes[6] = 1.00;
        }
        else if (PS4.getButtonClick(RIGHT)) {
            PS4.setLed(Green);
            axes[6] = -1.00;
        }
        else 
            axes[6] = 0;
          
        if (PS4.getButtonClick(OPTIONS)) {
            buttons[7] = 1;
        }
        else 
            buttons[7] = 0;
        if (PS4.getButtonClick(SHARE)) {
            buttons[6] = 1;
        }
        else 
            buttons[6] = 0;
          
        buttons[0] = PS4.getButtonClick(CROSS);
        buttons[1] = PS4.getButtonClick(SQUARE);
        buttons[2] = PS4.getButtonClick(CIRCLE);
        buttons[3] = PS4.getButtonClick(TRIANGLE);      
        buttons[9] = PS4.getButtonClick(L3);
        buttons[10] = PS4.getButtonClick(R3);
        buttons[4] = PS4.getButtonClick(L1);  
        buttons[5] = PS4.getButtonClick(R1);
        
        if (PS4.getButtonClick(PS)) {
            PS4.setLedFlash(10,10);
            buttons[8] = 1;
        }
        else {
            buttons[8] = 0;
            PS4.setLedFlash(0,0);
        }
      
    
        axes[0] = (axes[0]/255.0*2)-1;
        axes[1] = 255 - axes[1];
        axes[1] = (axes[1]/255.0*2)-1;
        axes[3] = (axes[3]/255.0*2)-1;
        axes[4] = 255 - axes[4];
        axes[4] = (axes[4]/255.0*2)-1;
    
        axes[2] = 255 - axes[2];
        axes[2] = (axes[2]/255.0*2)-1;
    
        axes[5] = 255 - axes[5];
        axes[5] = (axes[5]/255.0*2)-1;

        Serial.print("st");
        for (int i = 0; i<8; i++){
            Serial.print(axes[i]);
            Serial.print("\t");
        }
        
        for (int i = 0; i<11; i++){
            Serial.print(buttons[i]);
            Serial.print("\t");
        }
        Serial.print("en");
          
        Serial.println();
    }
    delay(10);
}
