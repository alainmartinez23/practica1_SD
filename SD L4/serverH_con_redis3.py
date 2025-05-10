import pika
import json
import random
import re
import redis
import os
import time

# Conexión a Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

INSULT_LIST = "insult_list_rabbit"
FILTERED_TEXTS = "filtered_texts_rabbit"


def filter_message(text):
    insult_list = r.lrange(INSULT_LIST, 0, -1)
    filtered = text
    for insult in insult_list:
        pattern = re.compile(rf'\b{re.escape(insult)}\b', re.IGNORECASE)
        filtered = pattern.sub("CENSORED", filtered)
    time.sleep(0.2)  # Simula tiempo de procesamiento (para ver el efecto del escalado)
    r.rpush(FILTERED_TEXTS, filtered)
    return filtered

def handle_request(body):
    request = json.loads(body)
    action = request.get("action")
    data = request.get("data", "")

    if action == "add":
        r.rpush(INSULT_LIST, data)
        return "ok"

    elif action == "get":
        insults = r.lrange(INSULT_LIST, 0, -1)
        return random.choice(insults) if insults else None

    elif action == "list":
        return r.lrange(INSULT_LIST, 0, -1)

    elif action == "filter_text":
        return filter_message(data)

    elif action == "get_filtered_texts":
        return r.lrange(FILTERED_TEXTS, 0, -1)

    return None

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='insult_queue')

    def on_request(ch, method, props, body):
        response = handle_request(body)
        ch.basic_publish(
            exchange='',
            routing_key=props.reply_to,
            properties=pika.BasicProperties(correlation_id=props.correlation_id),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print(f"Petición procesada")

    channel.basic_qos(prefetch_count=1)  # Muy importante para reparto justo
    channel.basic_consume(queue='insult_queue', on_message_callback=on_request)
    print(f"Servidor activo y esperando peticiones...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
