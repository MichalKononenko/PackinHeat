#define BUFFER_LENGTH 17
#define OFFSET 3
#define L 17 // Length of array recieved from Python

const int input_pins[]={1, 2, 3, 4, 5, 6, 7, 8}; // sensor with amp
const int ouput_pins[]={30, 32 ,34 ,36 ,38 ,40 , 42, 44}; // output pins

/**
 * Creates a buffer of size L and returns a pointer to it
 */
int *create_serial_buffer(){
  int *p;
  p = new int[L];
  return p;
}


int offset= 3; // Biases Amplifier

int power = 10;         // turning sensor on and off
                       // outside leads to ground and +5V
int shift=0;

int input[]={0, 700, 700, 700, 700, 700, 700, 700, 700, 2, 2, 2, 2, 2, 2, 2, 2, 2}; //variable to store the inputs to turn on heaters
float temp[]={28 ,30 ,32 ,34 ,36 ,38 ,40 , 42};

int lastlong=0; // variable to store last long loop time
int lastshort=0; // variable to store last short inerval
int tim=0; // variable to store time
int shortinterval=1000; // variable for short interval
int longinterval=30000; //variable forto store long interval
 int counter=8; // number of heaters that are supposed to be turned off
int lengthin=8;
int lengthout=8;

float v=0;
float R=0;

void setup()
{



  pinMode(power, OUTPUT);

  Serial.begin(9600);          //  setup serial
  for (int c=0; c<(lengthout); c++){
          pinMode(l[c], OUTPUT);    // read the input pin
          pinMode(offset, OUTPUT);
          analogWrite(offset,150);
      }


}



void loop()
{

tim=millis(); //updating the value of time




// short loop
if ((tim-lastshort > shortinterval) && (counter = 8) ) {

lastshort=millis();
      for (int f=0; f<8; f++){
 digitalWrite(l[f], HIGH);
  counter=0;
      }
}

      for (int h=0; h<8; h++){
        tim=millis();
        if ((tim-lastshort > (input[h+1]))  && digitalRead(l[h]) ) {
          digitalWrite(l[h],LOW);
          counter=counter+1;

        }
        }





// long loop

if ((tim-lastlong) > longinterval  ) { //&&  lastlong=millis();
  lastlong=millis();
  if (Serial.available() > 0){


    for (int k=0; k<L; k++){
      input[k]=Serial.parseInt();
      if (input[k]==11111){
       shift=k;

      }
    }

   for (int w=shift; w<L; w++){
      input[w-shift]=input[w];

    }
  }


      digitalWrite(power, HIGH);      // turning sensor on
      delay(10);
      for (int a=0; a<(lengthout); a++){
          temp[a] = analogRead(s[a]);    // read the input pin


      }
      digitalWrite(power, LOW);      // turning sensor off
      delay(100);

      for (int e=0; e<(lengthin); e++){


         Serial.print(temp[e]);             // debug value
          if (e!=7){
         Serial.print(",");
           }
      }
  Serial.println(" ");
}
}
