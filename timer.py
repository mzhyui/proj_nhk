#!python.exe
from datetime import datetime, timedelta
import threading

# 目标函数，这里仅作为示例
def target_function():
    print("Function is executed at:", datetime.now().strftime("%H:%M:%S"))

# 计算目标时间与当前时间的差值，以秒为单位
def calculate_delay(alt):
    # 当前时间
    now = datetime.now()
    # 目标执行时间，这里设定为今天的19:00:15
    target_datetime = datetime.now() + timedelta(seconds=alt)
    # 如果目标时间已经过去，则设定为明天的该时刻
    if target_datetime < now:
        target_datetime += timedelta(days=1)
    # 计算差值
    delay = (target_datetime - now).total_seconds()
    return delay

# 设置定时器并执行
def set_timer():
    delay = calculate_delay(5)
    timer = threading.Timer(delay, target_function)
    timer.start()
    print(f"Timer set to execute the function in {delay} seconds at {datetime.now() + timedelta(seconds=delay)}")

# 注意：实际调用 set_timer 函数的代码在这里被注释掉了，以防止直接执行。
set_timer()
