#include <Servo.h>

Servo servox;
Servo servoy;

int xpin = 11;
int ypin = 12;
int lpin = 4;

const byte numChars = 64;
char receivedChars[numChars];
char tempChars[numChars];        // temporary array for use when parsing

int posx = 0;
int posy = 0;
char cmdStr[numChars] = {0};
int posx_new = 0;
int posy_new = 0;

int dt = 50;

void setup() {
  servox.attach(xpin);
  servoy.attach(ypin);
  digitalWrite(lpin,HIGH);
  Serial.begin(9600);
  Serial.setTimeout(50);
}

boolean newData = false;

//============

void loop() {
    recvWithStartEndMarkers();
    if (newData == true) {
        strcpy(tempChars, receivedChars);
            // this temporary copy is necessary to protect the original data
            //   because strtok() used in parseData() replaces the commas with \0
        parseData();
        updatePositions();
        newData = false;
    }
}

//============

void recvWithStartEndMarkers() {
    static boolean recvInProgress = false;
    static byte ndx = 0;
    char startMarker = '<';
    char endMarker = '>';
    char rc;

    while (Serial.available() > 0 && newData == false) {
        rc = Serial.read();

        if (recvInProgress == true) {
            if (rc != endMarker) {
                receivedChars[ndx] = rc;
                ndx++;
                if (ndx >= numChars) {
                    ndx = numChars - 1;
                }
            }
            else {
                receivedChars[ndx] = '\0'; // terminate the string
                recvInProgress = false;
                ndx = 0;
                newData = true;
            }
        }

        else if (rc == startMarker) {
            recvInProgress = true;
        }
    }
}

//============

void parseData() {      // split the data into its parts

    char * strtokIndx; // this is used by strtok() as an index

    strtokIndx = strtok(tempChars,",");      // get the first part - the string
    strcpy(cmdStr, strtokIndx);
    
    strtokIndx = strtok(NULL, ",");
    posx_new = atoi(strtokIndx);     // convert this part to an integer

    strtokIndx = strtok(NULL, ",");
    posy_new = atoi(strtokIndx);     

}

//============

void updatePositions() {
  
    if (String(cmdStr)=="Degree"){ // between 0 and 160
        Serial.println(0);
        posx = posx_new;
        posy = posy_new;
        servox.write(posx);
        servoy.write(posy);
    } else if (String(cmdStr)=="Microsecond") { // between 1000 and 2000
      Serial.println(1);
        posx = posx_new;
        posy = posy_new;
        servox.writeMicroseconds(posx);
        servoy.writeMicroseconds(posy);
    } else if (String(cmdStr)=="Move_Degree") {
      Serial.println(2);
        posx += posx_new;
        posy += posy_new;
        servox.write(posx);
        servoy.write(posy);
    } else if (String(cmdStr)=="Move_Microsecond") {
      Serial.println(3);
        posx += posx_new;
        posy += posy_new;
        servox.writeMicroseconds(posx);
        servoy.writeMicroseconds(posy);
    } else {
        Serial.println(4);
        posx = posx_new;
        posy = posy_new;
        servox.write(posx);
        servoy.write(posy);
    }

    Serial.println(cmdStr);
    Serial.print("posx ");
    Serial.println(posx);
    Serial.print("posy ");
    Serial.println(posy);

}
