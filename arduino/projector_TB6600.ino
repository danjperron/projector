// MultiStepper
// -*- mode: C++ -*-
//
// version for TB6600 stepper controller


#include <AccelStepper.h>

#define dirPin 2
#define stepPin 3
#define ledPin 4
#define motorInterfaceType 1

#define TARGET_STEP 1600
#define MIN_STEP_CHECK  150
#define POST_STEP   790

int cposition;
int lightFlag=0;
int motorFlag=0;
int frameCount=0;
int nextFlag=0;

AccelStepper stepper1 = AccelStepper(motorInterfaceType, stepPin, dirPin);

//  status return from serial communication
//  Light  tab  motor  tab  Frame_count  tab Stepper_position  return
void sendStatus()
{
  Serial.print(lightFlag,DEC);
  Serial.print("\t");
  Serial.print(motorFlag,DEC);
  Serial.print("\t");
  Serial.print(frameCount,DEC);
  Serial.print("\t");
  Serial.println(cposition,DEC);
  Serial.flush();
}



unsigned long Counter;
void setup()
{  
  Serial.begin(9600);
  Serial.flush();
  pinMode(A2,INPUT);
  pinMode(ledPin,OUTPUT);
  LightOff();
  stepper1.setMaxSpeed(30000.0);
  stepper1.setAcceleration(30000.0);
}

void stopMotor()
{
                  stepper1.setCurrentPosition(0);
                  stepper1.moveTo(0);
                  motorFlag=0;
                  cposition=0;
}

void LightOff()
{
  digitalWrite(ledPin,0);
}

void LightOn()
{
  digitalWrite(ledPin,1);
} 


// this is the command received throught the serial port
//
//  0 -> light OFF
//  1 -> light ON
//  C -> stop and reset position
//  I -> request status
//  N -> Next picture frame
//  S -> stop
// system doesnt care about cariage return or line feed

void loop()
{

  byte new_v;
  
 
  
  if(Serial.available()>0) {
    int inByte = Serial.read();
    
    switch (toupper(inByte)) {
      
      case '0': LightOff();
                sendStatus();
                break;
                 
      case '1': LightOn();
                sendStatus();
                break;

      case 'C': stopMotor();
                frameCount=0;
                sendStatus();
                break;

      case 'I': sendStatus();
                break;
      
      case 'N': nextFlag=1;
                stepper1.setCurrentPosition(0);
                motorFlag=1;
                stepper1.moveTo(TARGET_STEP);
                sendStatus();
                break;
                 
      case 'S': stopMotor();
                sendStatus();
                break;
    }
  }
  
    new_v= digitalRead(A2);
    cposition= stepper1.currentPosition();
     if(cposition==TARGET_STEP)
       if(nextFlag)
       {
         nextFlag=0;
         motorFlag=0;
         frameCount++;
       }

     // temporary disable the opto switch here
     /*
       
     if(cposition>MIN_STEP_CHECK)

        if(new_v ==0)  
        {
             stepper1.setCurrentPosition(POST_STEP);

        }
       */
         
    stepper1.run();
}
