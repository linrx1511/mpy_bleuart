"""
The MIT License (MIT)
micropython 实现BLE串口1透传功能
"""
import ubluetooth as bt
from machine import Pin, UART, Timer
import machine
import binascii
from ble.ble_uart import BLEUART

BLE_NAME = ""  # 定义蓝牙名称，如果为空则使用UID取名称
  
def main():
    def rx_callback(data):
        print("ble received:")
        print(binascii.hexlify(bytearray(data)))
        uart.write(data)

    def timer_callback(t):
        # LED连接成功常亮，断开的闪烁
        led.value(0 if bleuart.is_connected() else not led.value())    

    ble = bt.BLE()
    if BLE_NAME != "":
        name = BLE_NAME
    else:
        addr = machine.unique_id() # 读出ID后3bytes作为name
        #print(binascii.hexlify(bytearray(addr)))
        name = "VW-%02X%02X%02X" % (addr[3], addr[4], addr[5]) 
    print(name)
    bleuart = BLEUART(ble, rx_callback, name)
    
    uart = UART(1, 9600)
    uart.init(9600, bits=8, parity=None, stop=1, tx=16, rx=17) #串口1配置
    #uart.irq(UART.RX_ANY, priority=1, handler=uart_callback, wake=machine.IDLE)
    
    tim = Timer(-1)
    tim.init(period=300, mode=Timer.PERIODIC,callback=timer_callback) #
    
    led = Pin(14, Pin.OUT, value=0)
    
    while True:
        if uart.any() > 0:
            # 为了兼容性每次只发送20字节，对应BLE的默认MTU
            data = uart.read(min(20, uart.any()))
            print("uart received:")
            print(binascii.hexlify(bytearray(data)))
            bleuart.send(data)

if __name__ == "__main__":
    main()
