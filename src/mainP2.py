import machine, network, time, framebuf, math, atuadoresP2, sensoresP2, config, mqtt
from machine import Pin, ADC, I2C
from time import sleep
from math import log
from mqtt import conectar, publicar
from sensoresP2 import lerDHT, lerLDR
from atuadoresP2 import *
from config import *
cliente = None



c = 0
m = False
try:
    import urequests as requests
except:
    import requests
import esp
esp.osdebug(None)

import gc
gc.collect()



tempoAnterior = time.ticks_ms()
tempoAnterior2 = time.ticks_ms()

def msgWhat(ntelefone, api_key, mensagem):
    url = f"https://api.callmebot.com/whatsapp.php?phone={ntelefone}&text={mensagem}&apikey={api_key}"

    response = requests.get(url)
    if response.status_code == 200:
        print("mensagem enviada")
    else:
        print('Erro:')
        print(response.text)
    
    
# HARDWARE

# WIFI
wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print("Conectando WiFi...")
wifi.connect(SSID, SENHA)

while not wifi.isconnected():
    time.sleep(1)

print("WiFi conectado!")
print(wifi.ifconfig())

cliente = conectar("esp32", BROKER)
botaoMSG = Pin(33, Pin.IN, Pin.PULL_UP)
botaoM = Pin(12, Pin.IN, Pin.PULL_UP)
ledM = Pin(14, Pin.OUT)
intervaloOLED1 = 5000
intervaloOLED2 = 1000

    
def msgNodeRed():
    temperatura, umidade = lerDHT()
    publicar(TOPICO_DHTT, str(temperatura))
    publicar(TOPICO_DHTU, str(umidade))
    publicar(TOPICO_LDR, str(lerLDR()))
    publicar(TOPICO_BTN, str(botaoMSG.value()))

while True:
    tempoAtual = time.ticks_ms()
    cliente.check_msg()
    if time.ticks_diff(tempoAtual, tempoAnterior) > 2000:
        temperatura, umidade = lerDHT()
        msgNodeRed()
        tempoAnterior = tempoAtual
        
    if time.ticks_diff(tempoAtual, tempoAnterior2) > intervaloOLED1 and m == False:
        mostrarInfoOled(temperatura, umidade, lerLDR(), c)
        tempoAnterior2 = tempoAtual
        intervaloOLED1 = 5000
        c += 1
        print (c)
        if c >= 4:
            c = 0
    if time.ticks_diff(tempoAtual, tempoAnterior2) > intervaloOLED2 and m == True:
        mostrarInfoOled(temperatura, umidade, lerLDR(), c)
        tempoAnterior2 = tempoAtual
        intervaloOLED2 = 1000
        

        
        
    if botaoMSG.value() == 0:
        #msgWhat(ntelefone, api_key, mensagem)
        temperatura, umidade = lerDHT()
        alertaOled()
        mensagem = f"Alerta!%20Temperatura:%20{temperatura}%20%20Umidade:%20{umidade}%20%20Luminosidade:%20{lerLDR()}"
        msgWhat(ntelefone, api_key, mensagem)

        
        while botaoMSG.value() == 0:
            time.sleep(0.3)
    if botaoM.value() == 0:
        m = not m
        print('M')
        if m:
            c = 5
            intervaloOLED2 = 0
            ledM.on()
        else:
            c = 0
            intervaloOLED1 = 0
            ledM.off()
        while botaoM.value() == 0:
            time.sleep(0.3)

    
    
