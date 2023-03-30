int sig = 2;            // Signal pin
int s0 = 32;
int s1 = 33;
int s2 = 25;
int s3 = 26;
int STR = 5;            // Starts game
int PAU = 18;           // Pauses game
int END = 19;           // Ends game
int REDO = 21;          // Recalculates board state
bool play_sound = true; // Global flag // Change to ShouldPlaySpeaker

int i = 0;              // Iterator for testing



// HEADERS
void speakerSelect(int speaker);
void Pause();

void setup(){

// Setup for PWM generation
  pinMode(sig, OUTPUT);

// Setup for speaker selection algorithm
  pinMode(s0, OUTPUT);
  pinMode(s1, OUTPUT);
  pinMode(s2, OUTPUT);
  pinMode(s3, OUTPUT);

// Setup buttons
  pinMode(STR, INPUT_PULLUP);
  pinMode(PAU, INPUT_PULLUP);
  pinMode(REDO, INPUT_PULLUP);

// Button interrupts
  attachInterrupt(digitalPinToInterrupt(STR), Start, FALLING);
  attachInterrupt(digitalPinToInterrupt(PAU), Pause, FALLING);
  attachInterrupt(digitalPinToInterrupt(REDO), changeSpeaker, FALLING);
}


void loop(){

  i = i + 1;
  speakerSelect(i%12);
  int j = 0;

  for(j = 0; j < 15; j++){
      // Audio signal code
    if (play_sound) {
      analogWrite(sig, 127);   // Turn on PWM signal w/ 50% duty cycle
      delay(250);
      analogWrite(sig, 0);     // Turn off PWM signal
      delay(100);
    }
  }
/*

// PWM generation algorithm
for(int i=0; i<255; i++){
    analogWrite(pwmPin, i);
    delay(1);
}
for(int i=255; i>0; i--){
    analogWrite(pwmPin, i);
    delay(1);
}
delay(500);
*/
}

void speakerSelect(int speaker){
  if(speaker==0){
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
  }

  else if(speaker==1){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
  }

  else if(speaker==2){
    digitalWrite(s0, LOW);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
  }

  else if(speaker==3){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, LOW);
    digitalWrite(s3, LOW);
  }   
  
  else if(speaker==4){
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, HIGH);
    digitalWrite(s3, LOW);
  }

  else if(speaker==5){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, LOW);
    digitalWrite(s2, HIGH);
    digitalWrite(s3, LOW);
  }

  else if(speaker==6){
    digitalWrite(s0, LOW);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, HIGH);
    digitalWrite(s3, LOW);
  }

  else if(speaker==7){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, HIGH);
    digitalWrite(s3, LOW);
  }

  else if(speaker==8){
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, HIGH);
  }

  else if(speaker==9){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, LOW);
    digitalWrite(s2, LOW);
    digitalWrite(s3, HIGH);
  }

  else if(speaker==10){
    digitalWrite(s0, LOW);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, LOW);
    digitalWrite(s3, HIGH);
  }

  else if(speaker==11){
    digitalWrite(s0, HIGH);
    digitalWrite(s1, HIGH);
    digitalWrite(s2, LOW);
    digitalWrite(s3, HIGH);
  }

  else{
    digitalWrite(s0, LOW);
    digitalWrite(s1, LOW);
    digitalWrite(s2, HIGH);
    digitalWrite(s3, HIGH);
  }
}

void Pause(){
  play_sound = false;
}

void Start(){
  play_sound = true;
}


// Code for changing during midterm demo
void changeSpeaker(){
  // i+=3;
  // speakerSelect(i%12);
}