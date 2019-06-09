#基本的监测温度并打印出来
import os
import glob
import time
import subprocess
#使端口运行
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
#找到温度数据
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
#子线程读取温度，通过接口获取消息的前两行
def read_temp_raw():
    catdata = subprocess.Popen(['cat',device_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,err = catdata.communicate()
    out_decode = out.decode('utf-8')
    lines = out_decode.split('\n')
    return lines
#包装了一层并且加入了失败消息检测并且重试直到第一行的末尾有一个YES。这个方法会返回两个值，第一个是摄氏温度，第二个是华氏温度。
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
#循环打印
while True:
    ss = str(read_temp())
    print(ss)
    time.sleep(1)
