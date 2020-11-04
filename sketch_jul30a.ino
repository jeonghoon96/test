#include <DHT11.h>
  
extern volatile unsigned long timer0_millis;

const int pin = 10;      // 온습도센서
DHT11 dht11(pin);        // DHT11(온습도센서) 핀 할당
const int gasPin = A0;   // 가스센서
const int inputPin = 2;  // 인체감지센서
const int speaker = 9;   // 부저스피커

float temp_prev;  // 온도측정값
float humi_prev;  // 습도측정값

int val = 0;      // 인체감지센서 측정값(HIGH/LOW) 
int some = 0;     // 인체감지센서 cool down 변수
int start_time;   // 인체감지 측정 시각

//Time delay for 1 sec
unsigned long previousMillis = 0;
const long interval = 1000;

void setup() {
  Serial.begin(9600);
  pinMode(speaker,OUTPUT);     // Speaker Output 설정
  pinMode(inputPin, INPUT);    // 센서 Input 설정

}

void loop() {  
  unsigned long currentMillis = millis();
  if(currentMillis - previousMillis >= interval){
    previousMillis = currentMillis;      // Timer reset
  
    int err;
    float temp,humi;
 
    if((err=dht11.read(humi,temp))==0){
      temp_prev = temp;
      humi_prev = humi;    
    }
  
    val = digitalRead(inputPin);         // 인체감지센서 신호값을 읽어와서 val에 저장
    if (val == HIGH){                    // 센서 신호값이 HIGH면(인체감지가 된 경우)
      start_time = (int)millis();       
      some = 1;    
    } 
    else {                                    // 센서 신호값이 LOW면(인체감지가 없으면)
      if((int)millis() - start_time > 5000){  // 인체감지가 되지 않는 시간이 5초 이상
      some = 0;
      noTone(speaker);
      }
    }
   
    if(some == 1){                       // 인체감지가 활성화된 동안 부저는 계속 동작
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
    }
     
    Serial.println("start");                 //Serial start
    Serial.print(temp_prev);
    Serial.print("k");
    Serial.print(humi_prev);
    Serial.print("k"); 
    Serial.print(1000 + analogRead(gasPin));
    Serial.print("k");
    Serial.println(some);                    //Serial end  
  }
}
