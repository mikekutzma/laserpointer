#include <Servo.h>

Servo servox;
Servo servoy;

int xpin = 11;
int ypin = 12;
int lpin = 4;

int posy = 0;
int my = 1;
int dy = 3;
int maxy = 160;


int posx = 0;
int mx = 1;
int dx = 1;
int maxx = 160;

int dt = 50;

void setup() {
  servox.attach(xpin);
  servoy.attach(ypin);
  digitalWrite(lpin,HIGH);
  Serial.begin(9600);
  Serial.setTimeout(50);
  String mystring = "12;65";
  Serial.println(mystring.substring(0,String(mystring).indexOf(';')));
}

void loop() {
/*  
  while(true){
    if(posx<0){
      mx = 1;
      posx=0;
    } else if(posx>maxx){
      mx=-1;
      posx=maxx;
    }
    if(posy<0){
      my = 1;
      posy=0;
    } else if(posy>maxy){
      my=-1;
      posy=maxy;
    }
    servox.write(posx);
    servoy.write(posy);
    posx = posx+(mx*dx);
    posy = posy+(my*dy);
    delay(dt);
  }
  */
  if(Serial.available()){
    String posstring = Serial.readString();
    int delind = posstring.indexOf(';');
    posx = posstring.substring(0,delind).toInt();
    posy = posstring.substring(delind+1).toInt();
  }
  servoy.write(posy);
  servox.write(posx);
  delay(dt);
  
}



