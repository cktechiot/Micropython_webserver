from machine import Pin , DAC , ADC
from time import sleep
from ir_rx import NEC_16

Dim = DAC(Pin(26))
led = Pin(2, Pin.OUT)
led.value(1)

ir_data = 0
def callback(data, addr, ctrl):
    global ir_data
    ir_data = data
    if data > 0:  # NEC protocol sends repeat codes.
        #print('Data {:02x} Addr {:04x}'.format(data, addr))
         print(ir_key[data])
        
        
ir = NEC_16(Pin(21, Pin.IN), callback)
ir_key = {
    0x45: '1',
    0x46: '2',
    0x47: '3',
    0x44: '4',
    0x40: '5',
    0x43: '6',
    0x07: '7',
    0x15: '8',
    0x09: '9',
    0x16: '*',
    0x19: '0',
    0x0D: '#',
    0x18: 'UP',
    0x08: 'LEFT',
    0x1C: 'OK',
    0x5A: 'RIGHT',
    0x52: 'DOWN'
    }

global dim
global i
dim = 50
i = 1

while True:
    if ir_data > 0:
        if ir_key[ir_data] == '5' :
            print('Ir : power')
            i += 1
            print('i : ', i)
            sleep(0.1)
            if i % 2 == 0 :
                dim = 0
            else :
                dim = 50        
        elif ir_key[ir_data] == '0' :
            print('Ir : +')
            sleep(0.1)
            dim += 10

        elif ir_key[ir_data] == 'UP':
            print('Ir : -')
            dim -= 10
            sleep(0.1)
            
    print('dim = ', dim)
    print('')
    ir_data = 0
    if dim >= 60 :
        dim = 55
    elif dim < 0 :
        dim = 0
    else:
        Dim.write(dim)
    sleep(0.1)
