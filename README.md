# Medianajones
Compare Mediainfo details for videos; find similarities in an array of videos. What do video A, B, C and D have in common?

Handy as a debugging tool in case you're wondering why some videos are acting strange in some other context. 

### prerequisites:
    1. sudo apt-get install mediainfo
    2. pip install pymediainfo


### how to:
    1. add your videos to the ALL_FILES array
    2. consider whether you want to include "not in common" details or not (can be handy for context; can be annoying if you don't care)
    3. run it damn it

If they're green, they're in common for all the videos. If they're red, they're not.

### Example output
![image](https://user-images.githubusercontent.com/120788835/215189129-83e4b95c-212c-4b9f-a181-20b2899b8aff.png)
