# medicalAlarmGen
Generates medical device alarms as .wav files according to FDA standards </br>
When you run the program it asks you if you'd like to run it batch or manual - </br>
                - batch requires you to fill out AlarmSpecifications.txt file with with the pulse duration </br
                  and wait duration for each priority level. It then generates alarms with </br>
                  fundamental frequencies between 300 and 1000 Hz. It will generate two .wav files </br>
                  for each parameter set using two different signals. Each of these generate a signal with </br>
                  4 fundamental frequencies as specified by the FDA for medical alarms.</br>
                - The manual mode will simply prompt you for the parameters to make your alarm, with reminders</br>
                  about the specifications set by the FDA. It will then generate two .wav files using two different</br>
                  functions.</br>
### You can change the path to the specification file and the sample rate by adjusting the global variables.
      
