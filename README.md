This project involves building a security system that is purely based on transistors. It takes the input from user as a combination of 0s and 1s and if the combination matches then the system will activate the servo motor to rotate 90degrees [opening of the door]

Flow of the system:
  1. User sets the slide switch to vcc[1] or gnd[0] and presses the push button.
  2. The push button is connected to a RC circuit and schmitt trigger circuit for debounce. The push button acts as clock pulse.
  3. The input pattern is validated with moore FSM built using transistors.
  4. Simultaneously on the output side two square wave signals are generated.

     a. A RC relaxation oscillator to generate a square wave with 20ms period.
     
     b. Two monostable multivibrators the take input from the output of the relaxation oscillator and generate pulses of width 500us and 1500us
     
  6. If the input pattern is correct then the system outputs the signal with pulsewidth 1500ms via a 2:1 mux else it outputs the siganl with pulsewidth 500us driving the servo motor appropriately. 


I have also included the program files that i used for this project.
  1. A python program that is used to generate generator functions that will be used to design the pattern detector from the flip flops.
  2. An AI generated cpp arduino function that is used to validate the output signal of the complete system in terms of period and pulsewidth.
