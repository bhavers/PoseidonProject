#include <Wire.h>
#include "MMA7660.h"
#include "DS1307.h"
#include "DHT.h"
MMA7660 acc;
DS1307 clock;
DHT dht;

#define SLAVE_ADDRESS 0x04
int number = 0;
int state = 0;

int cmd[5];
int index=0;
int flag=0;
int i;
byte val=0,b[9],float_array[4];
int aRead=0;
byte accFlag=0,clkFlag=0;
int8_t accv[3];

unsigned long duration=0;
unsigned long starttime=0;
unsigned long now=0;
unsigned long diff = 0;
unsigned long sampletime_ms = 30000UL;//sampe 30s ;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;

void setup() 
{
    Serial.begin(9600);         // start serial for output
    Wire.begin(SLAVE_ADDRESS);

    Wire.onReceive(receiveData);
    Wire.onRequest(sendData);

    Serial.println("Ready!");

#if 0    
    pinMode(8,INPUT);
    starttime = millis();//get the current time;
#endif
    
}
int pin=0;
int j;
int busy=0;
void loop()
{
   
#if 0  
  
  duration = pulseIn(8, LOW);
  lowpulseoccupancy = lowpulseoccupancy+duration;

  if ((millis()-starttime) > sampletime_ms)//if the sampel time == 30s
  {
    ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
    concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
 
    byte *b1=(byte*)&concentration;            
    for(j=0;j<4;j++)
      b[j+1]=b1[j];    
    
    concentration = 0.0;
    lowpulseoccupancy = 0;
    starttime = millis();
  }  
  
#endif
  

  long dur,RangeCm;
  if(index==4 && flag==0)
  {
    flag=1;
    //Digital Read
    if(cmd[0]==1)
      val=digitalRead(cmd[1]);
      
    //Digital Write
    if(cmd[0]==2)
      digitalWrite(cmd[1],cmd[2]);
      
    //Analog Read
     if(cmd[0]==3)
     {
      aRead=analogRead(cmd[1]);
      b[1]=aRead/256;
      b[2]=aRead%256;
     }
      
    //Set up Analog Write
    if(cmd[0]==4)
      analogWrite(cmd[1],cmd[2]);
        
    //Set up pinMode
    if(cmd[0]==5)
      pinMode(cmd[1],cmd[2]);
    
    //Ultrasonic Read
    if(cmd[0]==7)
    {
      pin=cmd[1];
      pinMode(pin, OUTPUT);
      digitalWrite(pin, LOW);
      delayMicroseconds(2);
      digitalWrite(pin, HIGH);
      delayMicroseconds(5);
      digitalWrite(pin,LOW);
      pinMode(pin,INPUT);
      dur = pulseIn(pin,HIGH);
      RangeCm = dur/29/2;
      b[1]=RangeCm/256;
      b[2]=RangeCm%256;
      //Serial.println(b[1]);
      //Serial.println(b[2]);
    }
    
    // Dust Read
    if(cmd[0]==8)
    { 
      pin=cmd[1];
      pinMode(pin,INPUT);
      lowpulseoccupancy = 0;
      starttime = millis(); 
      
#if 0      
      do {           
        now = millis();
        duration = pulseIn(pin, LOW);
        lowpulseoccupancy = lowpulseoccupancy+duration;
        diff = now - starttime;
      } while ((unsigned long)diff < (unsigned long)30000);            
      
      byte *b1=(byte*)&lowpulseoccupancy;            
      for(j=0;j<4;j++)
            b[j+1]=b1[j];   
      diff = 0;
#endif      
      
      while ((millis()-starttime) < sampletime_ms) {
      
        duration = pulseIn(pin, LOW);
        lowpulseoccupancy = lowpulseoccupancy+duration;
      }
      ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
      concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve

      byte *b1=(byte*)&concentration;
      for(j=0;j<4;j++)
        b[j+1]=b1[j];
        
      concentration = 0.0;
      starttime = 0;  
   
    }
    
    //Accelerometer x,y,z, read
    if(cmd[0]==20)
    {
      if(accFlag==0)
      {
        acc.init();
        accFlag=1;
      }
      acc.getXYZ(&accv[0],&accv[1],&accv[2]);
      b[1]=accv[0];
      b[2]=accv[1];
      b[3]=accv[2];
    }
    //RTC tine read
    if(cmd[0]==30)
    {
      if(clkFlag==0)
      {
        clock.begin();
        //Set time the first time
        //clock.fillByYMD(2013,1,19);
        //clock.fillByHMS(15,28,30);//15:28 30"
	//clock.fillDayOfWeek(SAT);//Saturday
	//clock.setTime();//write time to the RTC chip
        clkFlag=1;
      }
      clock.getTime();
      b[1]=clock.hour;
      b[2]=clock.minute;
      b[3]=clock.second;
      b[4]=clock.month;
      b[5]=clock.dayOfMonth;
      b[6]=clock.year;
      b[7]=clock.dayOfMonth;
      b[8]=clock.dayOfWeek;  
    }
    //Grove temp and humidity sensor pro
    //40- Temperature
    if(cmd[0]==40)
    {
      if(cmd[2]==0)
        dht.begin(cmd[1],DHT11);
      else if(cmd[2]==1)
        dht.begin(cmd[1],DHT22);
      else if(cmd[2]==2)
        dht.begin(cmd[1],DHT21);
      else if(cmd[2]==3)
        dht.begin(cmd[1],AM2301);
      float t= dht.readTemperature();
      float h= dht.readHumidity();
      //Serial.print(t);
      //Serial.print("#");
      byte *b1=(byte*)&t;
      byte *b2=(byte*)&h;
      for(j=0;j<4;j++)
        b[j+1]=b1[j];
      for(j=4;j<8;j++)
        b[j+1]=b2[j-4];
    }
  }

  
}

void receiveData(int byteCount)
{
    while(Wire.available()) 
    {
      if(Wire.available()==4)
      { 
        flag=0;
        index=0;
      }
        cmd[index++] = Wire.read();
    }
}

// callback for sending data
void sendData()
{
  if(cmd[0]==1)
    Wire.write(val);
  if(cmd[0]==3 ||cmd[0]==7)
    Wire.write(b, 3);
  if(cmd[0]==8)
    Wire.write(b, 9);  
  if(cmd[0]==20)
    Wire.write(b, 4);
  if(cmd[0]==30||cmd[0]==40)
    Wire.write(b, 9);
}

