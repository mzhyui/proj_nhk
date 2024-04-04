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
