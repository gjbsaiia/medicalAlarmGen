# medicalAlarmGen
Generates medical device alarms as .wav files according to FDA standards </br>
When you run the program it asks you if you'd like to run it batch or manual - </br>

    - batch requires you to fill out AlarmSpecifications.txt file with with the pulse duration 
      and wait duration for each priority level. It then generates alarms with 
      fundamental frequencies between 300 and 1000 Hz. It will generate two .wav files 
      for each parameter set using two different signals. Each of these generate a signal with 
      4 fundamental frequencies as specified by the FDA for medical alarms.

    - The manual mode will simply prompt you for the parameters to make your alarm, with reminders
      about the specifications set by the FDA. It will then generate two .wav files using two different
      functions.
                  
### You can change the path to the specification file and the sample rate by adjusting the global variables.
      
