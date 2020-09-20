import subprocess
import time

# import cv2
import numpy as np

YOUTUBE = "rtmp://a.rtmp.youtube.com/live2/"
KEY = ""
dimension = '%sx%s' % (1280, 720)
# https://stackoverflow.com/questions/43991594/piping-pis-opencv-video-to-ffmpeg-for-youtube-streaming

stream_cmd = ['ffmpeg',
              # '-loglevel', 'trace',           # Enable for debugging or to get a feel for what formats etc are being used
              # INPUT
              '-r', '30',  # FPS
              '-f', 'rawvideo',                 # Input is raw video
              '-pix_fmt', 'bgr24',              # Raw video format
              '-s', dimension,                  # size of one frame
              '-i', '-',                        # The input comes from a pipe
              # Audio
              '-ar', '44100',                   # Youtube requires audio channels otherwise it won't play
              '-ac', '2',
              '-acodec', 'pcm_s16le',
              '-f', 's16le',
              '-ac', '2',
              '-i', '/dev/zero',                 # Pipe a stream of zeros, (ensure the user running the command has permissions to the source)
              '-acodec', 'aac',
              '-ab', '128k',
              # OUTPUT
              '-c:v', 'libx264',                # h264 codec
              '-g', '20',
              '-b:v', '2500k',                  # Sets a maximum bit rate (just scrolling through some colours will fall below this due to the compression and youtube will complain but ignore it.
              '-bufsize', '512k',
              '-pix_fmt', 'yuv420p',
              '-f', 'flv',                      # Specify the output format as we don't have a output filename to hint it
              "%s%s" % (YOUTUBE, KEY)]          # FFMPEG will take any unknown arg as an output URI

stream_pipe = subprocess.Popen(stream_cmd,  stdin=subprocess.PIPE)
frame_count = 0

# Uncomment the videcap lines and comment the raw numpy lines if you want
# vidcap = cv2.VideoCapture()
# vidcap.open("test_video.mp4")
try:
    now = time.strftime("%Y-%m-%d-%H:%M:%S")
    img_data = np.zeros((720, 1280, 3), np.uint8)

    while True:
        # Case 1: Opencv read in from a raw video
        # _, frame = vidcap.read()
        ### Alter frame here ###
        # str_img = frame.tostring()

        # Case 2: Raw numpy array output
        img_data[:, :, 2] += 1  # Funk with the colours
        img_data[:, :, 1] += 3  # Mismo

        str_img = img_data.tobytes() # Using pipes requires it be output in a stringable format
        stream_pipe.stdin.write(str_img)

        frame_count += 1
        print(frame_count)
        time.sleep(0.02)    # This will approximate 30fps, a little more is ok, a little less youtube will complain about buffering
except KeyboardInterrupt:
    print("Closing %s" % frame_count)
finally:
    stream_pipe.stdin.close()
    stream_pipe.wait()
    print("Stream shut down")
    # vidcap.release()
    # print("Video source released")
