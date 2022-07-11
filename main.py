"""
The MIT License (MIT)
micropython 实现BLE串口1透传功能
"""
import ubluetooth as bt
from machine import Pin, UART, Timer
import binascii
from ble.ble_uart import BLEUART

# 定义蓝牙名称
BLE_NAME = "VW-Linrx"
  
def main():
    def rx_callback(data):
        #print("ble received: {}".format(data))
        print("ble received:")
        print(binascii.hexlify(bytearray(data)))
        uart.write(data)

    def timer_callback(t):
        # LED连接成功常亮，断开的闪烁
        led.value(0 if bleuart.is_connected() else not led.value())    

    ble = bt.BLE()
    bleuart = BLEUART(ble, rx_callback, BLE_NAME)
    
    uart = UART(1, 9600)
    uart.init(9600, bits=8, parity=None, stop=1, tx=16, rx=17) #串口1配置
#     uart.irq(UART.RX_ANY, priority=1, handler=uart_callback, wake=machine.IDLE)
    
    tim = Timer(-1)
    tim.init(period=300, mode=Timer.PERIODIC,callback=timer_callback) #
    
    led = Pin(14, Pin.OUT, value=0)
    
    while True:
        if uart.any() > 0:
            data = uart.read()
            #print("uart received: {}".format(data))
            print("uart received:")
            print(binascii.hexlify(bytearray(data)))
            bleuart.send(data)

if __name__ == "__main__":
    main()
