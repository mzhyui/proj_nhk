while :
do
   ffmpeg -re -i $(cat ytb.list.txt) -re -i https://radio-stream.nhk.jp/hls/live/2023229/nhkradiruakr1/master48k.m3u8 -map 0:v -map 1:a -c:v copy -c:a aac -f flv <url>
   sleep 2 # 稍微等待，然后重新连接
done