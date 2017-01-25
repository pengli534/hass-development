// Sketch for double relay Actuators with buttons with/without DS18B20 temp sensor
// in loop() method, if (value2 != oldValue) {...} can be changed for Rocker switch
// this sketch is coded under mysensor with version 1.5.4
// pengli534@gmail.com

#include <MySensor.h>
#include <SPI.h>
#include <Bounce2.h>

#define RELAY_PIN    3  // Arduino Digital I/O pin number for relay 
#define RELAY_PIN_2  5
#define BUTTON_PIN   4  // Arduino Digital I/O pin number for button 
#define BUTTON_PIN_2 7
#define CHILD_ID_2 12
#define CHILD_ID 11 // Id of the sensor child
#define RELAY_ON 1
#define RELAY_OFF 0

Bounce debouncer = Bounce(); 
int oldValue=0;
bool state;
Bounce debouncer2 = Bounce(); 
int oldValue2=0;
bool state2;

MySensor gw;
MyMessage msg(CHILD_ID,V_LIGHT);
MyMessage msg2(CHILD_ID_2,V_LIGHT);

void incomingMessage(const MyMessage &message) {
  // We only expect one type of message from controller. But we better check anyway.
  if (message.isAck()) {
     Serial.println("This is an ack from gateway");
  }

  if (message.type == V_LIGHT && message.sensor == 11) {
     // Change relay state
     state = message.getBool();
     digitalWrite(RELAY_PIN, state?RELAY_ON:RELAY_OFF);
     // Store state in eeprom
     gw.saveState(CHILD_ID, state);
   }
  else if(message.type == V_LIGHT && message.sensor == 12){  
    
     state2 = message.getBool();
     digitalWrite(RELAY_PIN_2, state2?RELAY_ON:RELAY_OFF);
     // Store state in eeprom
     gw.saveState(CHILD_ID_2, state2);
    
    
     // Write some debug info
     Serial.print("Incoming change for sensor:");
     Serial.print(message.sensor);
     Serial.print(", New status: ");
     Serial.println(message.getBool());
   } 
}


void setup()  
{  
  gw.begin(incomingMessage, AUTO, true);

  // Send the sketch version information to the gateway and Controller
  gw.sendSketchInfo("Double Relay & Button", "0.1");

  // Setup the button
  pinMode(BUTTON_PIN,INPUT);
  // Activate internal pull-up
  digitalWrite(BUTTON_PIN,HIGH);
  
   // Setup the button
  pinMode(BUTTON_PIN_2,INPUT);
  // Activate internal pull-up
  digitalWrite(BUTTON_PIN_2,HIGH);
  
  // After setting up the button, setup debouncer
  debouncer.attach(BUTTON_PIN);
  debouncer.interval(5);
  
  debouncer2.attach(BUTTON_PIN_2);
  debouncer2.interval(5);

  // Register all sensors to gw (they will be created as child devices)
  gw.present(CHILD_ID, S_LIGHT);
  gw.present(CHILD_ID_2, S_LIGHT);

  // Make sure relays are off when starting up
  digitalWrite(RELAY_PIN, RELAY_OFF);
  // Then set relay pins in output mode
  pinMode(RELAY_PIN, OUTPUT);   
  
  digitalWrite(RELAY_PIN_2, RELAY_OFF);
  // Then set relay pins in output mode
  pinMode(RELAY_PIN_2, OUTPUT);   
      
  // Set relay to last known state (using eeprom storage) 
  state = gw.loadState(CHILD_ID);
  digitalWrite(RELAY_PIN, state?RELAY_ON:RELAY_OFF);
  
  state2 = gw.loadState(CHILD_ID_2);
  digitalWrite(RELAY_PIN_2, state2?RELAY_ON:RELAY_OFF);
  
}


/*
*  Example on how to asynchronously check for new messages from gw
*/
void loop() 
{
  gw.process();
  debouncer.update();
  debouncer2.update();
  // Get the update value
  int value = debouncer.read();
  int value2 = debouncer2.read();
  
  //  // if (value2 != oldValue) {...} change for contact switch/Rocker switch
  if (value != oldValue && value == 0) {
      gw.send(msg.set(state?false:true), true); // Send new state and request ack back
  }
  oldValue = value;
  
  // if (value2 != oldValue2) {...}
  if (value2 != oldValue2 && value2 == 0) {
      gw.send(msg2.set(state2?false:true), true); // Send new state and request ack back
  }
  oldValue2 = value2;  
} 
