from umqtt.simple import MQTTClient
import atuadoresP2, config
from config import *
from atuadoresP2 import *
msg = ""
cliente = None



def publicar(topico, mensagem):
    global cliente

    cliente.publish(topico, mensagem)


def conectar(cliente_id, broker):
    global cliente
    cliente = MQTTClient(cliente_id, broker)
    cliente.set_callback(sub_callback)
    cliente.connect()
    cliente.subscribe(TOPICO_D1)
    cliente.subscribe(TOPICO_D2)
    cliente.subscribe(TOPICO_LUZ, qos = 0)
    print("MQTT conectado!")

    return cliente
def sub_callback(topic, msg):
    #Mostra o tópico e a mensagem recebida
    #topic = topic.decode('utf-8')
    if topic == b'esp32/d1' or topic == b'esp32/d2' or topic == b'esp32/luz':
        atuadoresP2.ledsLogica(msg)
    elif topic == b'esp32/whatR':
        msgWhatR(msg)


def msgWhatR(msg):
    if msg == '200':
        print("mensagem enviada")
    else:
        print('Erro ao enviar mensagem')

