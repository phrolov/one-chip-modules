### ATtiny85 one chip synthesis modules


###### LEGEND

The lines are wired connections.

- `━━━━━━` input
- `══════` output
- `──────` regular connection

Inputs and outputs can be of different types.

- `●` -- sound
- `■` -- trigger or gate
- `▲` -- modulation

The numbers inside the lines are _capacitors_ (e.g. `470nF`) and _resistors_ (e.g. `100K`) of the corresponding nominal value.

All patch points are 0V -- +5V. Ground the inputs when not used.


##### RUNGLER

```
             ┌─────────┐                  
  rst ■━100K━┫○        ├────VCC           
             │         │                  
 rate ▲━━━━━━┫ RUNGLER ┣━━━━━━■ rungler   
             │    &    │    ┌──────────┐  
pulse ■══════╣ VC LFO  ╠═1K═╩═▲ rungler│  
             │         │               │  
      GND──┬┬┤         ╠═1K═╦═▲ tri    │  
           ││└─────────┘    │          │  
           │└──────────470nF┘          │  
           └──────────────────────470nF┘  
                                          
```

Rungler is a stepped voltage generator which is being clocked by the LFO. The output voltage is based on analog combining of 3 bits in a shift register. Witch every clock the shift register shifts the bits and depending on the state of the RUNGLER input inverts (HIGH) or keeps (LOW) the current bit. RATE sets the speed of the triangle wave LFO and on every cycle of the LFO also the RUNGLER is clocked. RUNGLER is invention of Rob Hordijk.


##### VCO

```
              ┌─────────┐                 
 qntzr ■━100K━┫○        ├────VCC          
              │         │                 
 pitch ▲━━━━━━┫         ┣━━━━━━▲ bit shape
              │   VCO   │                 
ws/pwm ▲━━━━━━┫         ╠═1K═══● pulse    
              │         │                 
       GND───┬┤         ╠═1K═╦═● wave     
             │└─────────┘    │            
             └──────────470nF┘            
                                          
```

VCO is voltage controlled oscillator. It produces tones and provides several waveshaping options. The PITCH sets the frequency of the VCO. WS/PWM morphs the WAVEFORM from saw to triangle and to ramp. It also and sets the pulse width at the PULSE output.
The BIT SHAPER alters the binary structure of the WAVEFORM. When grounded the WAVEFORM output is silent and when at +5V the WAVEFORM output is unaffected.
When QUANTIZER is grounded it forces the VCO to produce only semitone pitches.


##### ATTACK DECAY

```
              ┌─────────┐                
  slew ■━100K━┫○        ├────VCC         
              │         │                
attack ▲━━━━━━┫   AD    ┣━━━━━▲■ input   
              │ENVELOPE │    ┌────────┐  
 decay ▲━━━━━━┫  SLEW   ┣━━━━┻━■ cycle│  
              │         │             │  
       GND──┬┬┤         ╠═1K═╦═▲ out  │  
            ││└─────────┘    │        │  
            │└──────────470nF┘        │  
            └─────────────────────100K┘  
                                         
```

Signal going up and down, rise and fall, attack and decay. The most universal synthesis structure principle which has wide range of applications. Can be used as envelope generator, slew limiter, LFO,  waveshaper or audio oscillator. Use the INPUT as gate for the envelope or ground the SLEW to use the INPUT as continuous voltage input where the voltage at the OUTPUT always reaches the voltage at the INPUT with the ATTACK and DECAY slew rate. Ground the CYCLE input to create repeating functions and use the INPUT to reset the cycle.


##### EUCLIDIAN VC DIVIDER

```
               ┌─────────┐           
unequal ■━100K━┫○        ├────VCC    
               │         │           
  steps ▲━━━━━━┫EUCLIDIAN┣━━━━━━■ rst
               │VC DIVIDR│           
  fills ▲━━━━━━┫         ┣━━━━━━■ clk
               │         │           
        GND────┤         ╠═1K═══▲ out
               └─────────┘           
```

Euclidian algorithm equally distributes elements in space or in time. It is easy to equally distribute 4 fills into 8 steps, but how do you distribute 5 of them? This is what the euclidian algorithm decides. This module is trigger generator which creates natural rhythms. At every CLK the algorhithm goes to the next step. Depending on number of STEPS and FILLS it creates equal patterns. Combine several Euclidean sequencers to create natural polyrhythms. When FILLS is grounded it equals 1 and then the STEPS is used as voltage controllable clock divider. Ground the UNEQUAL pin to produce irregular anti-euclidian patterns.


##### SAMPLER

```
                   ┌─────────┐             
      start ▲━100K━┫○        ├────VCC      
                   │         │             
sample rate ▲━━━━━━┫         ┣━━━━━━▲ decay
                   │ SAMPLER │             
     length ▲━━━━━━┫         ┣━━━━━━■ gate 
                   │         │             
            GND───┬┤         ╠═1K═╦═● out  
                  │└─────────┘    │        
                  └──────────470nF┘        
                                           
```

The Sampler has a snippet of pre-recorded sound in the memory which can be played back at different speeds. Signal on GATE input will start the playback of the sample. SAMPLE RATE sets the speed of the playback. DECAY sets how long does the sound fade out after signal at the GATE disappeared. LENGTH will set how much of the sample will be played  before it plays again from the beginning. This can result into very granular sounds. The START sets the point in the sample where the playback starts when the signal appears on the GATE input. When DECAY is at minimum the sample will not repeat. When it is at maximum it will keep repeating endlessly.


##### MASTER CLOCK

```
                 ┌─────────┐                  
 tap mode ■━100K━┫○        ├────VCC           
                 │         │                  
tempo/tap ▲■━━━━━┫ MASTER  ┣━━━━━━■ start/stop
                 │  CLOCK  │                  
    swing ▲━━━━━━┫         ╠══════■ rst       
                 │         │                  
          GND────┤         ╠══════■ clk       
                 └─────────┘                  
```

Master clock module is a convenient way to create clock for the modular system. PLAY/STOP button enables the CLK output while firing the RST to synchronise all devices. TEMPO can be either set with voltage or when grounding the TAP MODE can be set with  few pulses (taps). Every second clock can be delayed to create a swing effect. The amount is set by the SWING input.


##### AUTOMATION / ANALOG SHIFT REGISTER

```
                  ┌─────────┐           
       rst ■━100K━┫○        ├────VCC    
                  │         │           
steps 1-32 ▲━━━━━━┫  AUTOM  ┣━━━━━━■ clk
                  │  ATION  │           
    sample ▲━━━━━━┫         ┣━━━━━━■ rec
                  │         │           
           GND───┬┤         ╠═1K═╦═▲ out
                 │└─────────┘    │      
                 └──────────470nF┘      
                                        
```

This module is a memory array of 32 voltages. CLK advances thru the voltages stored in the memory. NO. OF STEPS sets how many slots are used (1-32) before the memory comes back to the first slot. The module can remember the voltage at the SAMPLE input when there is a gate signal at the REC input and put it to the current memory slot. If the REC is low than the voltages in the memory will keep looping. If the NO. OF STEPS is at minimum the module will act as basic sample and hold module. Trigger at the RST pin will always jump to the first memory slot (step). This module can be used to record knob or CV movements and play them back.


##### RANDOM NOISE

```
                  ┌─────────┐                   
clock mode ■━100K━┫○        ├────VCC            
                  │         │                   
  rate/clk ▲■━━━━━┫ RANDOM  ╠══════■ random gate
                  │  NOISE  │    ┌──────────┐   
      slew ▲━━━━━━┫         ╠═1K═╩═▲ stepped│   
                  │         │               │   
           GND──┬┬┤         ╠═1K═╦═▲ slewed │   
                ││└─────────┘    │          │   
                │└──────────470nF┘          │   
                └──────────────────────470nF┘   
                                                
```

This module generates several random signals at incoming clock which can be either internal or external. When CLOCKED is grounded it expects pulse at the RATE/CLK input to generate new random states. If the internal clock is selected the RATE input sets the speed of the clock which can go up to audiorate to generate audible colored noise. At every clock a new random voltage is generated at the STEPPED output. At every clock the RANDOM GATE will change state based on 50-50 probability. At the SLEWED output there will be new voltage at every clock to gradually fade into. The speed of the fading is set by the SLEW input.


##### LOGIC

```
               ┌─────────┐           
 negate ■━100K━┫○        ├────VCC    
               │         │           
input a ■━━━━━━┫         ╠══════■ or 
               │  LOGIC  │           
input b ■━━━━━━┫         ╠══════■ and
               │         │           
        GND────┤         ╠══════■ xor
               └─────────┘           
```

LOGIC calculates classic logical functions combining INPUT A and B into the 3 outputs OR, AND and XOR. If NEGATE INPUT is grounded the logical conversion is inverted (NOR, NAND, XNOR).


##### LFO

```
                 ┌─────────┐               
sync mode ■━100K━┫○        ├────VCC        
                 │         │               
     rate ▲━━━━━━┫         ┣━━━━━━▲ xor    
                 │   VCO   │               
    shape ▲━━━━━━┫         ┣━━━━━━■ rst/clk
                 │         │               
          GND───┬┤         ╠═1K═╦═▲ out    
                │└─────────┘    │          
                └──────────470nF┘          
                                           
```

LFO (low frequency oscillator) module is a modulation signal source. It creates musical functions that can be used to modulate other modules. The RATE sets the speed of the modulation, SHAPE selects the basic waveform and XOR WS will modify the waveform. The RST input will reset the wave form. When SYNC MODE is grounded the RST/CLK input will act as clock input and the RATE will set divisions / multiplications of that clock. This can be used for modulation that is synchronised with the tempo.


##### SEQ DRIVER DIVIDER

```
               ┌─────────┐                
    rst ■━100K━┫○        ├────VCC         
               │         │                
    clk ■━━━━━━┫   SEQ   ╠══════■ /8 bit 2
               │ DRIVER  │                
address ▲━━━━━━┫ DIVIDER ╠══════■ /4 bit 1
               │         │                
        GND────┤         ╠══════■ /2 bit 0
               └─────────┘                
```

This module can be used as simple clock divider with divisions  2,4, and 8. When clocking the CLK input the internal counter increments and the bit representation appears on the outputs. Pulse at RST input puts the counter to 0. When grounding the CV MODE  the RST pin can be used as voltage to bit address converter -parallel analog to digital converter. The CLK input can still advance the internal counter. When creating analog sequencer with analog multiplexer chip 4051 can be more creative and compact when using this sequence driver.
