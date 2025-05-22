import pika 
from config import RABBIT_CONFIG
import serial
import time

serial_port_name = '/dev/ttyACM0'
serial_port = serial.Serial(serial_port_name, 9600)
time.sleep(2)

ultimo_evento = time.time()
TIMEOUT_SEGUNDOS = 60
comando_atual = None

def callback(ch, method, properties, body):
    global ultimo_evento, comando_atual
    temperatura = int(body.decode())
    print(f"Temperatura: {temperatura}")
    ch.basic_ack(delivery_tag=method.delivery_tag)
    
    if temperatura > 26:
        comando = "ON"
    else:
        comando = "OFF"
        
    if comando != comando_atual:
        serial_port.write(f"{comando}\n".encode("utf-8"))
        comando_atual = comando
    
    ultimo_evento = time.time()

try:
    params = pika.URLParameters(RABBIT_CONFIG)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    
    channel.exchange_declare(exchange='sens_temp', exchange_type='topic', durable=True)
    channel.queue_declare(queue='fila_temp')
    channel.queue_bind(exchange='sens_temp', queue='fila_temp', routing_key='fila_temp')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='fila_temp', on_message_callback=callback)

    print("Consumidor está aguardando mensagens...")

    while True:
        channel.connection.process_data_events(time_limit=10)
        agora = time.time()
        if agora - ultimo_evento > TIMEOUT_SEGUNDOS:
            if comando_atual != "OFF":
                print("Timeout atingido. Enviando comando OFF para Arduino.")
                serial_port.write(b"OFF\n")
                comando_atual = "OFF"
            ultimo_evento = agora
except KeyboardInterrupt:
    print("Saiu")
