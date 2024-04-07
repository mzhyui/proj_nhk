# proj_nhk
- save nhk radio from nhk japan and use webserver to play
![image](nhk.png)

# progress 1
- get main page: code 304
- get audio file: code 403
- solution: disable proxy

# progress 2
- target1: combine all audio files into one file
- target2: use main page to get the url of audio files
    - solution: get config.xml
    - problem: error code 403 sometimes
        - cause: cookies expired?
            - answer: no; succeed on macOs
- change route

# progress 3
> https://www.digitalocean.com/community/tutorials/how-to-set-up-a-video-streaming-server-using-nginx-rtmp-on-ubuntu-20-04 \
https://www.bilibili.com/read/cv1083415/

- target1: set up the stream server (for test)
- target2: use ffmpeg to upstream
    - solution: `ffmpeg -re -i https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/master48k.m3u8 -c:v copy -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost/live/stream`
        - problem: `keepalive request failed for 'https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/20230903T220028/master48k/00927/master48k_00449.aac' with error: 'Input/output error' when opening url, retrying with new connection`
    - solution: audio could be successfully pushed to the server, but need to combine with video for bili
    - solution: jpeg + x264
          - steps: `sudo apt-get install libx264-dev`
          - steps: `./configure --enable-gpl --enable-libx264 --enable-openssl --enable-nonfree` (ssl version >= 3.0.0)
    - solution: `ffmpeg -framerate 60 -loop 1 -i https://www.nhk.or.jp/prog/img/324/g324.jpg -i https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/master48k.m3u8 -http_persistent 0 -vf "scale=1920:1080" -c:v libx264 -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost:1935/live/stream`
        - problem: broken pipe for the video
        - solution: frame rate set above 30
            - problem: broken video frame
    - problem: Failed to update header with correct duration / Failed to update header with correct filesize
    - assertion: .m2u8 files not updated
