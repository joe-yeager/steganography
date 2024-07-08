# steganography
A python script for embedding messages in photographs.

Takes the ASCII value of a character and converts it to its 8 bit binary representation.  
This is then striped across the 2 least significant bits of the red value for 4 consecutive pixels.  
Inserts a stop sequence of "///" for easy decoding.
