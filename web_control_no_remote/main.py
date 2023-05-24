import machine
import utime
from machine import RTC
import time
import json
import re



from machine import Pin , DAC , ADC
from time import sleep


Dim = DAC(Pin(26))
led = Pin(2, Pin.OUT)
led.value(1)
pirx = Pin(19,Pin.IN)

Batt = ADC(Pin(35))
Solar = ADC(Pin(34))
Batt.width( ADC.WIDTH_12BIT ) # 12bit
Batt.atten(ADC.ATTN_11DB)
Solar.width( ADC.WIDTH_12BIT ) # 12bit
Solar.atten(ADC.ATTN_11DB)
BPV = 0.84/1000 #Bit Per Volt

dim = 0
diml = 0
i = 0
n = 0
c1 = ''
c2 = ''
c3 = ''
c4 = ''
c5 = ''
c6 = ''
c7 = ''
c8 = ''
c9 = ''
c10 = ''
c11 = ''
c12 = ''
c13 = ''



start_time = time.time()

try:
  import usocket as socket
except ImportError:
  import socket

import network

import esp
esp.osdebug(None)

import gc
gc.collect()
gc.enable()


ssid = 'CK Solar Lamp'
password = '123456789'
a = ''
b = ''
ap = network.WLAN(network.AP_IF)
ap.active(False)
ap.config(essid=ssid, password=password)
# while ap.active() == False:
#     pass
# 
# print('Connection successful')
# print(ap.ifconfig())
#----------------------------------------------------------------------------------------------
def web_page():
  global a
  global b
  global diml
  global c1
  global c2
  global c3
  global c4
  global c5
  global c6
  global c7
  global c8
  global c9
  global c10
  global c11
  global c12
  
  percent = int(map_range(diml, 0, 70, 0, 100))

  html = """<html><head> <title>Ck Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button7{background-color: #FF0000;}.button8{background-color: #5800FF;}
  .button2{background-color: #4286f4;}.button3{background-color: #41D80C;}
  .button5{background-color: #3DFA16;}.button6{background-color: #AAA4AA;}</style></head><body> <h1>CK Solar Lamp</h1> 
  <p><h2>Brightness : """ + str(diml) + """ dim</h2></p>
  """ + a + """
  """ + b + """
  <p><a href="/?led=on"><button class="button">ON</button></a>
  <a href="/?led=off"><button class="button button2">OFF</button></a></p>
  <p><a href="/?Dim=up"> <button class="button button8">UP</button></a>
  <a href="/?Dim=down"> <button class="button button6">DOWN</button></a></p>
  <p><a href="/?Status"> <button class="button button5">Status</button></a></p>
  <p><a href="/?Reset=reset"> <button class="button button7">REBOOT</button></a></p>
  <p>--------------------------------------------------------------------------------------<p>
  <p><a href="/?auto=auto"> <button class="button button5">AUTO</button></a>
  <a href="/?man=man"> <button class="button button7">MANUAL</button></a></p>
  """ + c1 + """
  """ + c2 + """
  """ + c3 + """
  """ + c4 + """
  """ + c5 + """
  """ + c6 + """
  """ + c7 + """
  """ + c8 + """
  """ + c9 + """
  """ + c10 + """
  """ + c11 + """
  """ + c12 + """

  </body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
#-----------------------------------------------------------------------------------------------
def web():
    global diml
    global ssid
    global password
    global a
    global b
    global c1
    global c2
    global c3
    global c4
    global c5
    global c6
    global c7
    global c8
    global c9
    global c10
    global c11
    global c12
    global items
    
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid=ssid, password=password)
    while ap.active() == False:
        pass
     
    print('Connection successful')
    print(ap.ifconfig())
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    
    led_on = request.find('/?led=on')
    led_off = request.find('/?led=off')
    dim_up = request.find('/?Dim=up')
    dim_down = request.find('/?Dim=down')
    bt_re = request.find('/?Reset=reset')
    Status = request.find('/?Status')
    auto = request.find('/?auto=auto')
    man = request.find('/?man=man')
    
    items = read_data('time.json')
    t1 = int(items[3])
    t2 = int(items[5])
    t3 = int(items[7])
    t4 = int(items[1])
#     percent1 = int(map_range(t1, 0, 70, 0, 100))
#     percent2 = int(map_range(t2, 0, 70, 0, 100))
#     percent3 = int(map_range(t3, 0, 70, 0, 100))
#     percent4 = int(map_range(t4, 0, 70, 0, 100))

    if 'GET' in request and 'input1' in request and 'input2' in request and 'input3' in request and 'input4' in request:
        pattern = r'input1=(\w+)&input2=(\w+)&input3=(\w+)&input4=(\w+)'
        match = re.search(pattern, request)
        if match:
            input1 = match.group(1)
            input2 = match.group(2)
            input3 = match.group(3)
            input4 = match.group(4)
                    
            print('Input 1:', input1)
            print('Input 2:', input2)
            print('Input 3:', input3)
            print('Input 4:', input4)
            data = {'time01': input1, 'time02': input2, 'time03': input3, 'time04': input4}
            write_json_file('time.json', data)
            print('Wrirt Json file Finish')
    
    if led_on == 6:
        print('LED ON')
        diml = 40
               
    if led_off == 6:
        print('LED OFF')
        diml = 0
                 
    if dim_up == 6:
        print('dim up')
        diml += 10

    if dim_down == 6:
        print('dim down')
        diml -= 10             
        if diml <= 0:
            diml = 0
#         dim(diml)
        
    if diml >= 200:
        diml = 200
#         dim(diml)
                    
    if Status == 6:
        print('Status')
        a = '<p><h2>Solar : ' + str(Solar_read) + '</h2></p>'
        b = '<p><h2>Battery : ' + str(Batt_read) + '</h2></p>'

                    
    if bt_re == 6:
        print('Reset now')
        sleep(0.5)
        machine.reset()
        
    if auto == 6:
        print('time start')
        ti3()
        
    if man == 6:
        c1 = '<p>---------------------------------------------<p>'
        c2 = '<form action="/set-input" method="get">'
        c3 = '<label for="input1">change time1:</label>'
        c4 = '<input type="text" id="input1" name="input1"><label> Last : ' + str(t1) +'dim</label><br>'
        c5 = '<label for="input2">change time2:</label>'
        c6 = '<input type="text" id="input2" name="input2"><label> Last : ' + str(t2) +'dim</label><br>'
        c7 = '<label for="input3">change time3:</label>'
        c8 = '<input type="text" id="input3" name="input3"><label> Last : ' + str(t3) +'dim</label><br>'
        c9 = '<label for="input4">change time4:</label>'
        c10 = '<input type="text" id="input4" name="input4"><label> Last : ' + str(t4) +'dim</label><br>'    
        c11 = '<p><input type="submit" value="Save"></p>'
        c12 = '</form>'
        print('c1 = ',c1)
        
        

            
    dim(diml)
    response = web_page()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.send(response)
    conn.close()
     
#-----------------------------------------------------------------------------------------------
def tiStart():
    global elapsed_minutes
    elapsed_minutes = int(time.time() - start_time) 

def tiStop():
    start_time = 0
    elapsed_minutes = int(time.time() - start_time) 
    print('time reset')
#     rtc.stop()

#----------------------------------------------------------------------------------------------------
def map_range(value, in_min, in_max, out_min, out_max):
    # หาระยะของช่วงของค่าต่าง ๆ 
    in_range = in_max - in_min
    out_range = out_max - out_min

    # แปลงค่าจากช่วงของค่าต่าง ๆ เป็นช่วงของ 0 ถึง 100
    mapped_value = (value - in_min) / in_range

    # แปลงค่าที่แปลงแล้วจาก 0 ถึง 100 เป็นช่วงของ out_min ถึง out_max
    return out_min + (mapped_value * out_range)

def percentage_to_integer(percentage):
    # ใช้ฟังก์ชัน map_range เพื่อแปลงค่าร้อยละเป็นจำนวนเต็มระหว่าง 0 ถึง 70
    integer_value = map_range(percentage, 0, 100, 0, 70)
    return integer_value

#--------------------------------------------------------------------
def read():
    global Batt_read
    global Solar_read
    global diml 
    Batt_read = (Batt.read())
    Solar_read = (Solar.read())
 
    SolarCell = (5.1650793650793650793650793650794*Solar_read)+(0.683460317460317) #จากสูตร y = mx + c 
    BATT = (25*Batt_read)+(-34.75) #จากสูตร y = mx + c
    
    print("Solar Cell : " , Solar_read)
    print('Batt : ', Batt_read)
    print('dim = ', diml)
    print('')
#----------------------------------------------
def pir():
    global pirx
    if pirx.value() == 1:
        print('ir D')
        dim(40)
        sleep(10)
    else :
        dim(0)
#----------------------------------------------------------------------------------------
    
def dim(di):
    dix = int(di)
    Dim.write(dix)
        
def ti2():
    global elapsed_minutes
    global diml
    
    tiStart()

    items = read_data('time.json')
    # หาระยะเวลาที่ใช้และแปลงเป็นนาที
#     elapsed_minutes = int(time.time() - start_time)
    print(elapsed_minutes)
    utime.sleep_ms(200)
    
    per1 = int(items[3])
    per2 = int(items[5])
    per3 = int(items[7])
    per4 = int(items[1])

    output01 = percentage_to_integer(per1)
    output02 = percentage_to_integer(per2)
    output03 = percentage_to_integer(per3)
    output04 = percentage_to_integer(per4)
    
    if elapsed_minutes >= 0 and elapsed_minutes < 60:
        print("เปิด 1 ชม 18.00-19.00")
        diml = output01
    elif elapsed_minutes >= 60 and elapsed_minutes < 240:
        print("เปิด 2 ชม 19.00-21.00")
        diml = output02
    elif elapsed_minutes >= 240 and elapsed_minutes < 420:
        print("เปิด 3 ชม 21.00-00.00")
        diml = output03
    elif elapsed_minutes >= 420:
        print("เปิด จนเช้า")
        diml = output04
    print('dim = ',diml)
    dim(diml)#---------------------------------------------------------------------

def ti3():
    global elapsed_minutes
    global diml
    
    tiStart()

    items = read_data('time.json')
    # หาระยะเวลาที่ใช้และแปลงเป็นนาที
#     elapsed_minutes = int(time.time() - start_time)
    print('time : ',elapsed_minutes)
    utime.sleep_ms(2000)
    
    per1 = int(items[3])
    per2 = int(items[5])
    per3 = int(items[7])
    per4 = int(items[1])
    
    if elapsed_minutes >= 0 and elapsed_minutes < 60:
        print("เปิด 1 ชม 18.00-19.00")
        diml = per1
    elif elapsed_minutes >= 60 and elapsed_minutes < 240:
        print("เปิด 2 ชม 19.00-21.00")
        diml = per2
    elif elapsed_minutes >= 240 and elapsed_minutes < 420:
        print("เปิด 3 ชม 21.00-00.00")
        diml = per3
    elif elapsed_minutes >= 420:
        print("เปิด จนเช้า")
        diml = per3
    print('dim = ',diml)
    dim(diml)#----------------------------------------------------
    
def read_data(filename):
    # อ่านไฟล์ JSON ด้วยฟังก์ชัน open และฟังก์ชัน json.load
    with open(filename, 'r') as f:
        data = json.load(f)

    # สร้างตัวแปรสำหรับเก็บข้อมูลที่แยกด้วย ,
    items = []

    # เพื่อนำข้อมูลที่เก็บไว้ใน data มาวนลูป
    for key, value in data.items():
        # ทำการแยกข้อมูลด้วย , และเก็บในตัวแปร items
        items.extend([key, value])
        
    return items
#---------------------------------------------------------------------------------
def write_json_file(filename, data):
    with open(filename, 'w') as file:
        # แปลงข้อมูลในรูปแบบ JSON และบันทึกไฟล์
        json.dump(data, file)
#---------------------------------------------
def mai():
    global Solar_read
    global Batt_read
    global diml
    
    if Solar_read <= 300:
        web()
#         ti3()
        
    elif Batt_read <= 602:
        tiStop()
        ap.active(False)
        
    elif Solar_read >= 300:
        tiStop()
        ap.active(False)
        if diml > 0:
            diml = 0
            dim(diml)
#         dim(diml)
    sleep(0.1)
    
while True:
    read()
    mai()
 
    print('dim = ', diml)
    print('')

