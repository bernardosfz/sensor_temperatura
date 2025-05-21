import pika
import time
import json
from config import RABBIT_CONFIG
import serial


serial_port_name = '/dev/ttyACM0'
serial_port = serial.Serial(serial_port_name, 9600)
time.sleep(2)

params = pika.URLParameters(RABBIT_CONFIG)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.exchange_declare(exchange='sens_temp', exchange_type='topic', durable=True)

channel.queue_declare(queue='fila_temp')

def send_temperature():
    print(f"Temperatura: {message}")

    channel.basic_publish(exchange='sens_temp', routing_key='fila_temp', body=message, properties=pika.BasicProperties(delivery_mode=2))

while True:
    message = serial_port.readline().decode()
    send_temperature()
