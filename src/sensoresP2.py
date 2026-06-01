from machine import Pin, ADC
from time import sleep
import dht

adcLDR = ADC(Pin(32))
adcLDR.atten(ADC.ATTN_11DB)
sensor = dht.DHT11(Pin(15))
#sensor = dht.DHT22(Pin(15))
def lerDHT():
    try:
        sensor.measure()
        temp = sensor.temperature()
        umid = sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        
        #print('Temperatura: %3.1f C' %temp)
        #print('Temperatura: %3.1f F' %temp_f)
        #print('Umidade: %3.1f %%' %umid)
        
        
        return temp, umid
    except OSError as e:
        print('Erro ao ler o sensor')
       

def lerLDR():
    return adcLDR.read()


