// MultiStepper
// -*- mode: C++ -*-
//
// Control both Stepper motors at the same time with different speeds
// and accelerations. 
// Requires the AFMotor library (https://github.com/adafruit/Adafruit-Motor-Shield-library)
// And AccelStepper with AFMotor support (https://github.com/adafruit/AccelStepper)
// Public domain!

#include <AccelStepper.h>
#include <AFMotor.h>


#define TARGET_STEP 210
#define MIN_STEP_CHECK  150
#define POST_STEP   205



int cposition;
int lightFlag=0;
int motorFlag=0;
int frameCount=0;
int nextFlag=0;

// two stepper motors one on each port
AF_Stepper motor1(200, 1);
AF_DCMotor motor2(3,MOTOR12_1KHZ);
//AF_Stepper motor2(200, 2);

// you can change these to DOUBLE or INTERLEAVE or MICROSTEP!
// wrappers for the first motor!
void forwardstep1() {  
  motor1.onestep(FORWARD, SINGLE);
}
void backwardstep1() {  
  motor1.onestep(BACKWARD, SINGLE);
}


// Motor shield has two motor ports, now we'll wrap them in an AccelStepper object
AccelStepper stepper1(forwardstep1, backwardstep1);


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
  motor2.setSpeed(255);
  LightOff();
  stepper1.setMaxSpeed(400.0);
  stepper1.setAcceleration(400.0);
}





void stopMotor()
{
                  stepper1.setCurrentPosition(0);
                  stepper1.moveTo(0);
                  motor1.release();
                  motorFlag=0;
                  cposition=0;
}

void LightOff()
{
  motor2.run(FORWARD);
  lightFlag=0;
}

void LightOn()
{
  motor2.run(BACKWARD);
  lightFlag=1;
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
         motor1.release();
         frameCount++;
       }
     if(cposition>MIN_STEP_CHECK)
        if(new_v ==1)  
        {
          if(cposition <POST_STEP)
           {
             stepper1.setCurrentPosition(POST_STEP);
           } 
        }


         
    stepper1.run();
}
