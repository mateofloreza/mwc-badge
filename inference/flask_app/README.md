# RTSP server

Install and run simple RTSP: https://github.com/bluenviron/mediamtx/releases/tag/v1.11.3
Unzip it and run it: 

```
./mediamtx
```

In a different terminal:

```
ffmpeg -f v4l2 -i /dev/video2 -vcodec libx264 -preset ultrafast -tune zerolatency -f rtsp rtsp://192.168.178.25:8554/video_feed
```
Then you can run the flask app.
