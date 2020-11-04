#include <DHT11.h>
  
extern volatile unsigned long timer0_millis;

int pin = 10;
int some = 0;
DHT11 dht11(pin);
int start_time;
const int gasPin = A0 ;
float temp_prev;
float humi_prev;
int inputPin = 2;     // 센서 신호핀
int val = 0;          // 센서 신호의 판별을 위한 변수
int speaker = 9;
int sound = 0;
void setup() {
    Serial.begin(9600);

    //dht11.begin();
    pinMode(speaker,OUTPUT);
    pinMode(inputPin, INPUT);    // 센서 Input 설정

}




void loop() {
  delay(600);
  
  int err;
  float temp,humi;
 
  if((err=dht11.read(humi,temp))==0){
      temp_prev = temp;
      humi_prev = humi; 
    
       
  }
  
  
  val = digitalRead(inputPin);         // 센서 신호값을 읽어와서 val에 저장
  
  if (val == HIGH) {  
      start_time = (int)millis();    // 센서 신호값이 HIGH면(인체 감지가 되면)    
      some = 1;    // 시리얼 모니터 출력
     
     
   } 
   else {                             // 센서 신호값이 LOW면(인체감지가 없으면)
       if((int)millis() - start_time > 5000){
       some = 0;
       
       
       
       noTone(speaker);
       //timer0_millis = 0;
       
       }
   }
   
   if(some == 1 && sound == 0){
   
     tone(speaker,1200);
     delay(50);
     noTone(speaker);
     tone(speaker,1300);
     delay(50);
     noTone(speaker);
     tone(speaker,1400);
     delay(50);
     noTone(speaker);
     tone(speaker,1500);
     delay(50);
     noTone(speaker);
     tone(speaker,1509);
     delay(50);
     noTone(speaker);
     
   }
   
   
   
     //Serial.println();
    Serial.println("start");
    Serial.print(temp_prev);
    Serial.print("k");
    Serial.print(humi_prev);
    Serial.print("k"); 
    Serial.print(1000 + analogRead(gasPin));
    Serial.print("k");
    Serial.println(some);
  
 
  delay(600);
  
}
