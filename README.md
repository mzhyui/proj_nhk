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
    - solution: `ffmpeg -framerate 60 -loop 1 -i "./g324.jpg" -i https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/master48k.m3u8 -http_persistent 0 -vf "scale=1920:1080" -c:v libx264 -c:a aac -ar 44100 -ac 1 -f flv rtmp://localhost:1935/live/stream`
        - problem: broken pipe for the video
        - assertion: frame rate set above 30
        - problem: broken video frame
            - solution: use original resolution
    - problem: Failed to update header with correct duration / Failed to update header with correct filesize
        - assertion: .m2u8 files not updated

# progress 4
- target1: nhk <-(ffmpeg/m3u8) jp vps (nginx stream server)-> <-(ffmpeg) local server
    - solution: `ffmpeg -re -i http://45.32.60.242:8088/hls/stream.m3u8 -c:v copy -c:a aac -ar 44100 -ac 1 -maxrate 5000k -bufsize 20000k -f flv`
        - note: re flag to make sure the processing speed is the same as raw input

# progress 5
- target: combine source A (video + audio) with source B (audio) to rtmp (A-video + B-audio)
    - installation: yt-dlp (python >= 3.8)
    - step1: `sudo python3.8 $(which yt-dlp) -f 232 -g https://www.youtube.com/live/Lfl2Nj_QRXU?si=gyGJykghI9zz0oBs` to get m3u8 (use `-F` to get all formats)
    - step1.5: `sudo python3.8 $(which yt-dlp) -f 232 -g https://www.youtube.com/live/Lfl2Nj_QRXU?si=gyGJykghI9zz0oBs > ytb.list.txt`
    - step2: `ffmpeg -re -i $(cat ytb.list.txt) -re -i http://45.32.60.242:8088/hls/stream.m3u8  -map 0:v -map 1:a -c:v copy -c:a aac -f flv <url>`
    - solution2: `ffmpeg -re -i $(cat ytb.list.txt) -re -i https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/master48k.m3u8 -map 0:v -map 1:a -c:v copy -c:a aac -f flv rtmp://localhost:1935/live/stream`
- problems: timeout for the youtube stream

# progress 5
- problem: the hk_server is not stable, may hanging at fetching the .ts file, while the `-reconnect 1` flag is not working
    - solution: use the jp_server to directly push the .ts file to bili
    - patch: use crontab to restart the `ffmpeg` command and fetch the .m3u8 file every 30 minutes to avoid the timeout