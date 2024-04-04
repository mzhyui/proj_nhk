#!python.exe
from time import sleep
import requests
import re
from datetime import datetime, timedelta
import threading
import xml.etree.ElementTree as ET

# 指定你要下载的文件的URL
url = 'https://www.nhk.or.jp/radio/player/?ch=r1'

proxy = dict({
        "http": "socks5://127.0.0.1:7890",
        "https": "socks5://127.0.0.1:7890"
    })
headers_mainpage = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9,ja-JP;q=0.8,ja;q=0.7,en-US;q=0.6,en;q=0.5',
    'Cache-Control': 'max-age=0',
    'Dnt': '1',
    # 'If-Modified-Since': 'Tue, 05 Dec 2023 03:00:22 GMT',
    # 'If-None-Match': '"1430-60bba6f749de3"',
    'Sec-Ch-Ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}
headers_m3u8 = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Host': 'radio-stream.nhk.jp',
    'Origin': 'https://www.nhk.or.jp',
    'Referer': 'https://www.nhk.or.jp/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'cross-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Google Chrome";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"'
}
session = requests.Session()

# 使用requests.get来发送HTTP GET请求，下载文件
print("requesting: ", url)
response = session.get(url,
                    headers=headers_mainpage, proxies=proxy)
aac_path = None
# 检查请求是否成功
if response.status_code == 200:
    # save the response
    with open('downloaded_file.html', 'wb') as file:
        file.write(response.content)

    print(session.cookies)

else:
    print('Failed to download the file. Status code:', response.status_code)
    print(response)
    exit(1)

print("requesting: ", 'https://www.nhk.or.jp/radio/config/config_web.xml')
response_config = session.get('https://www.nhk.or.jp/radio/config/config_web.xml',
                    headers=headers_mainpage, proxies=proxy)

if response_config.status_code == 200:
    with open('downloaded_file.xml', 'wb') as file:
        file.write(response_config.content)
    print('response_config downloaded successfully.')
    # print(response_config.content)

    # get value of radiru_config->stream_url->the third data->r1hls
    tree = ET.parse('downloaded_file.xml')
    root = tree.getroot()
    # for child in root:
    #     if child.tag == 'radiru_config':
    #         for grandchild in child:
    #             if grandchild.tag == 'stream_url':
    #                 for greatgrandchild in grandchild:
    #                     if greatgrandchild.tag == 'data':
    #                         print(greatgrandchild)
    #                         break
    #                 break
    #         break
    print(root[1][2][4].text)
    m3u8_url = root[1][2][4].text
    match = re.search(r'/live/(\d+)/', m3u8_url)
    latest_id = match.group(1) if match else None
    print(latest_id)
    print(session.cookies)
else:
    print('Failed to download response_config. Status code:', response_config.status_code)
    print(response_config)
    # exterminate the program
    exit(1)


print("requesting: ", m3u8_url.replace('master', 'master'))
response_m3u8 = session.get(m3u8_url.replace('master', 'master'), 
                            headers=headers_m3u8, proxies=proxy)

if response_m3u8.status_code == 200:
    with open('downloaded_file.m3u8', 'wb') as file:
        file.write(response_m3u8.content)
    print('response_m3u8 downloaded successfully.')
    # print(response_m3u8.content)
    decoded_content = response_m3u8.content.decode('utf-8')
    first_aac_path = re.search(r'(\d+T\d+/master48k/\d+/master48k_\d+.aac)', decoded_content)
    aac_path = first_aac_path.group(0) if first_aac_path else None
    print(aac_path)

else:
    print('Failed to download response_m3u8. Status code:', response_m3u8.status_code)
    print(response_m3u8)
    # exterminate the program
    exit(1)

    

# for idx in range(10):
#     path_parts = re.match(r"(.*/master48k_)(\d+)(\.aac)", aac_path)
#     if path_parts:
#         base, number, extension = path_parts.groups()
#         incremented_number = str(int(number) + 1).zfill(len(number))
#         incremented_path = f"{base}{incremented_number}{extension}"

#     response_aac = requests.get(f'https://radio-stream.nhk.jp/hls/live/{latest_id}/nhkradiruakr1/{incremented_path}',headers=headers)


#     if response_aac.status_code == 200:
#         with open(path_parts.groups()[1]+'.aac', 'wb') as file:
#             file.write(response_aac.content)
#         print('File downloaded successfully.')
#         # print(response_aac.content)
    
#     aac_path = incremented_path
#     sleep(10)

def target_function():
    global aac_path
    path_parts = re.match(r"(.*/master48k_)(\d+)(\.aac)", aac_path)
    if path_parts:
        base, number, extension = path_parts.groups()
        incremented_number = str(int(number) + 1).zfill(len(number))
        incremented_path = f"{base}{incremented_number}{extension}"

    response_aac = session.get(f'https://radio-stream.nhk.jp/hls/live/{latest_id}/nhkradiruakr1/{incremented_path}', 
                                headers=headers_m3u8, proxies=proxy)


    if response_aac.status_code == 200:
        with open(path_parts.groups()[1]+'.aac', 'wb') as file:
            file.write(response_aac.content)
        print('response_aac downloaded successfully.')
        # print(response_aac.content)
    
    else:
        print('Failed to download response_aac. Status code:', response_aac.status_code)
        print(response_aac)
        # exterminate the program
        exit(1)

    aac_path = incremented_path

# 计算目标时间与当前时间的差值，以秒为单位
def calculate_delay(target_datetime):
    # 当前时间
    now = datetime.now()
    # 如果目标时间已经过去，则设定为明天的该时刻
    if target_datetime < now:
        target_datetime += timedelta(days=1)
    # 计算差值
    delay = (target_datetime - now).total_seconds()
    return delay

# 设置定时器并执行
def set_timer(target_datetime):
    delay = calculate_delay(target_datetime)
    timer = threading.Timer(delay, target_function)
    timer.start()
    print(f"Timer set to execute the function in {delay} seconds at {datetime.now() + timedelta(seconds=delay)}")


begin_time = datetime.now()
for idx in range(10):
    begin_time = begin_time + timedelta(seconds=10)
    set_timer(begin_time)
    pass
