import pika 
from config import RABBIT_CONFIG
import serial
import time

serial_port_name = '/dev/ttyACM0'
serial_port = serial.Serial(serial_port_name, 9600)
time.sleep(2)

def callback (ch, method, proprieties, body):
	temperatura = int(body.decode())
	print (f"Temperatura: {temperatura}")
	ch.basic_ack (delivery_tag=method.delivery_tag)
	
	if temperatura > 28:
		comando = "ON"
	else:
		comando = "OFF"
		
	comando_env = serial_port.write(f"{comando}\n".encode("utf-8"))
	
try:
	params = pika.URLParameters(RABBIT_CONFIG)
	connection = pika.BlockingConnection(params)
	channel = connection.channel()
	
	channel.exchange_declare(exchange = 'sens_temp', exchange_type = 'topic', durable = True)
	
	channel.queue_declare(queue = 'fila_temp')
	
	channel.queue_bind (exchange = 'sens_temp', queue = 'fila_temp', routing_key = 'fila_temp')
	
	channel.basic_qos (prefetch_count=1)
	
	channel.basic_consume (queue = 'fila_temp', on_message_callback=callback)
	
	print ("Consumidor esta aguardando mensagens...")
	
	channel.start_consuming()
except KeyboardInterrupt:
	print ("Saiu")