#include <Wire.h>
#include <LCD_I2C.h>
#include "ESP_Wahaj.h"
#include <SimpleDHT.h>
#include <SoftwareSerial.h>

int pinDHT11 = D0;
SimpleDHT11 dht11(pinDHT11);

int pwm = 0;
float te,bpm,spo2,ph,ppg;
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define REPORTING_PERIOD_MS     1000

// PulseOximeter is the higher level interface to the sensor
// it offers:
//  * beat detection reporting
//  * heart rate calculation
//  * SpO2 (oxidation level) calculation
PulseOximeter pox;

uint32_t tsLastReport = 0;

// Callback (registered below) fired when a pulse is detected
void onBeatDetected()
{
    Serial.println("Beat!");
}

void setup() {
  pinMode(A0,INPUT);
  Serial.begin(115200);

  start("Project","12345678");
 
if (!pox.begin()) {
        Serial.println("FAILED");
        for(;;);
    } else {
        Serial.println("SUCCESS");
    }

    // The default current for the IR LED is 50mA and it could be changed
    //   by uncommenting the following line. Check MAX30100_Registers.h for all the
    //   available options.
    // pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);

    // Register a callback for the beat detection
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
  // Read sensor values from MCP3008
    // Make sure to call update as fast as possible
    pox.update();

    // Asynchronously dump heart rate and oxidation levels to the serial
    // For both, a value of 0 means "invalid"
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        Serial.print("Heart rate:");
        bpm=pox.getHeartRate();
        Serial.print(bpm);
        spo2=pox.getSpO2();
        Serial.print("bpm / SpO2:");
        Serial.print(spo2);
        Serial.println("%");

        tsLastReport = millis();
    }
    if((bpm>50)&&(spo2>90))
    {
   if (CheckNewReq()==1) {
    
      // read without samples.
  byte temperature = 0;
  byte humidity = 0;
  int err = SimpleDHTErrSuccess;
  if ((err = dht11.read(&temperature, &humidity, NULL)) != SimpleDHTErrSuccess) {
    Serial.print("Read DHT11 failed, err="); Serial.println(err);delay(1000);
    return;
  }
  te=temperature;
  Serial.print(te); Serial.print(" *C, "); 
  //Serial.print(hu); Serial.println(" H");
 for(int yu=0;yu<10;yu++)
 {
 int pi=analogRead(A0);
  ppg=ppg+pi;
  delay(200);
  }
 
 
       String myString = String(te)+String("-")+String(bpm)+String("-")+String(spo2)+String("-")+String(ppg);
    returnThisStr(myString);
    delay(1000);
String path = getPath();
      path.remove(0,1);
       pwm = path.toInt();
      ppg=0;
        }
       //  analogWrite(PWM_PIN, pwm);
      
    }
}
  
