# numpy_youtubelive_demo
This is a demo of exporting a raw numpy array to Youtube Live using a ffmpeg backend.

Also with minimal changes, an opencv input can be used as the input source. This is specifically for cases where you want to edit the video source on the fly and then output it straight to youtube.
If you want straight video-to-youtube, ffmpeg will do that without any of the extra complexities found herein.


This program is a while loop with a hand-off to ffmpeg. However, ffmpeg parameters can be daunting and youtube can be particular. The hope is providing this template will reduce the pain.

Requirements
```
* It will only work on unix based systems (tested working on OSX Catalina)
* Uses Python 3.7 and comes with minimal requirements
* You must have ffmpeg available on path
* opencv is only needed if you want to take in frames from opencv
* Youtube live account key copied into the KEY variable 
```
 
The demo example will init a numpy array and then cycle through some red and green colour mixtures. It dosen't need opencv. 

 
