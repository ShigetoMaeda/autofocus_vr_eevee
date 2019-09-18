# An experiment for VR
Auto focus for VR on EEVEE for Blender2.8

## USAGE:
Change some setting for your environment, and [RUN] the python code. It could be run on Mac, but windows are better.

## For gyro sensor(in Arduino code):
```
Serial.begin(230400); --> change for your PC.(9600, 115200, 230400...)
```
```
Serial.print(quat.w(), 4);
Serial.print(",");
Serial.print(quat.x(), 4); --> change for your sensor's direction and use
Serial.print(",");
Serial.print(quat.z(), 4); --> change for your sensor's direction and use
Serial.print(",");
Serial.print(-quat.y(), 4); --> change for your sensor's direction and use
Serial.println("");
```
## For Blender(Python code):
for Windows,
```
line 90: self.ser = serial.Serial("COM5", 230400) --> Arduino port, serial speed
```
for Mac,
```
self.ser = serial.Serial("/dev/cu.usbserial-1420", 230400) --> like this
```

In this .blend file, the camera animation was set. So you can [Play] animation, and [Run] script. (very slow!)
