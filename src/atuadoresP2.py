import machine, time, framebuf, math, mqtt, config, writer, freesans20
from machine import Pin, ADC, I2C
from time import sleep
from math import log
from mqtt import *
from config import *
from writer import Writer
import ssd1306


led1 = Pin(18, Pin.OUT)
led2 = Pin(19, Pin.OUT)
ledLuz = Pin(13, Pin.OUT)
buzzer = Pin(27, Pin.OUT)

#------OLED--------
i2c = I2C(scl=Pin(21), sda=Pin(22))

oled_width=128
oled_height=64

oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

letra20 = Writer(oled, freesans20)

with open('termometro64.pbm', 'rb') as Arq:
    Arq.readline()
    Arq.readline()
    Arq.readline()
    data = bytearray(Arq.read())
    buffer = framebuf.FrameBuffer(data, 29, 64, framebuf.MONO_HLSB)
    Arq.close()
with open('lua64.pbm', 'rb') as Arq:
    Arq.readline()
    Arq.readline()
    Arq.readline()
    data = bytearray(Arq.read())
    buffer2 = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB)
    Arq.close()
with open('sol64.pbm', 'rb') as Arq:
    Arq.readline()
    Arq.readline()
    Arq.readline()
    data = bytearray(Arq.read())
    buffer3 = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB)
    Arq.close()
with open('gotaPNG.pbm', 'rb') as Arq:
    Arq.readline()
    Arq.readline()
    Arq.readline()
    data = bytearray(Arq.read())
    buffer4 = framebuf.FrameBuffer(data, 64, 64, framebuf.MONO_HLSB)
    Arq.close()
#------OLED--------
    
tempoAnterior = time.ticks_ms()

def mostrarInfoOled(temp,umid, lumi, c):
    oled.fill(0)

    if c == 0:
        oled.blit(buffer, 0, 0)

        if temp < 0:
            oled.fill_rect(6 , 35, 15, 10, 0)
            
          
        elif temp > 0 and temp < 10:
            oled.fill_rect(6 , 50, 18, 5, 1)
            oled.fill_rect(10 , 5, 8, 45, 0)

        elif temp > 10 and temp < 20:
            oled.fill_rect(6 , 35, 18, 20, 1)
            #oled.fill_rect(10 , 20, 10, 15, 1)
            oled.fill_rect(10 , 5, 8, 30, 0)

        elif temp > 20 and temp < 30:
            oled.fill_rect(6 , 35, 18, 20, 1)
            oled.fill_rect(10 , 25, 10, 25, 1)
            oled.fill_rect(10 , 10, 8, 15, 0)

        elif temp > 30 and temp < 40:
            oled.fill_rect(6 , 35, 18, 20, 1)
            oled.fill_rect(10 , 15, 10, 25, 1)
            oled.fill_rect(10 , 5, 8, 10, 0)

        elif temp > 40:
            oled.fill_rect(10 , 5, 10, 25, 1)

        #oled.fill_rect(50, 40, 40, 30, 0)
        letra20.set_textpos(oled, 20, 60)
        letra20.printstring(f'{temp} C')

        oled.show()
    elif c == 1:

        if lumi < 300:
            oled.fill_rect(1, 1, 64, 64, 0)
            oled.blit(buffer2, 0, 0)

        elif lumi > 300:
            oled.fill_rect(1, 1, 64, 64, 0)
            oled.blit(buffer3, 0, 0)
        
        oled.text("Lumi:", 70, 10)
        letra20.set_textpos(oled, 20, 70)
        letra20.printstring(f'{lumi}')
    elif c == 2:
        
    
        oled.text("Umidade:", 65, 10)
        letra20.set_textpos(oled, 20, 75)
        letra20.printstring(f'{umid}%')
        
        oled.blit(buffer4, 0, 0)
    elif c == 3:
        tempo = time.gmtime()
        letra20.set_textpos(oled, 0, 15)
        letra20.printstring(f'{tempo[2]} / {tempo[1]} / {tempo[0]}')
        letra20.set_textpos(oled, 30, 30)
        letra20.printstring(f'{tempo[3]} : {tempo[4]}')
    elif c == 5:
        tempo = time.gmtime()
        oled.text(f'{tempo[2]} / {tempo[1]} / {tempo[0]}', 0, 0)
        oled.text(f'{tempo[3]} : {tempo[4]} : {tempo[5]}', 0, 10)
        oled.text(f'Lumi: {lumi}', 0, 20)
        oled.text(f'Temp: {temp} C', 0, 30)
        oled.text(f'Umid: {umid} %', 0, 40)
        
    tempo = time.gmtime()
    if c != 3 and c != 5: oled.text(f'{tempo[3]}:{tempo[4]}', 60, 55)
    oled.show()


    
def alertaOled():
    
    oled.fill(0)
    oled.text("Alerta!", 10, 10)
    oled.text("Enviando",10, 20)
    oled.text("Mensagem!", 10, 30)
    oled.show()
    time.sleep(5)
    
def ledsLogica(msg):
    if msg:
        if msg == b'D1':
            led1.value(not led1.value())
            publicar(TOPICO_D1_LED, str(led1.value()))
            
        if msg == b'D2':
            led2.value(not led2.value())
            publicar(TOPICO_D2_LED, str(led2.value()))
            
        if msg == b'Luz1':
            ledLuz.value(1)
            publicar(TOPICO_LUZ_LED, str(ledLuz.value()))
            buzzer.on()
            time.sleep_ms(100)
            buzzer.off()
            
        elif msg == b'Luz0':
            ledLuz.value(0)
            publicar(TOPICO_LUZ_LED, str(ledLuz.value()))
            


    