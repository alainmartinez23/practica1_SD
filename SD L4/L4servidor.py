import pika
import json
import random
import re

insult_list = []
filtered_texts = []

def filter_message(text):
    global filtered_texts
    filtered = text
    for insult in insult_list:
        pattern = re.compile(rf'\b{re.escape(insult)}\b', re.IGNORECASE)
        filtered = pattern.sub("CENSORED", filtered)
    filtered_texts.append(filtered)
    return filtered

def handle_request(body):
    request = json.loads(body)
    action = request.get("action")
    data = request.get("data", "")

    if action == "add":
        if data not in insult_list:
            insult_list.append(data)
        return "ok"

    elif action == "get":
        return random.choice(insult_list) if insult_list else None

    elif action == "list":
        return insult_list

    elif action == "filter_text":
        return filter_message(data)

    elif action == "get_filtered_texts":
        return filtered_texts

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

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='insult_queue', on_message_callback=on_request)
    print("InsultServer activo. Esperando peticiones...")
    channel.start_consuming()

if __name__ == "__main__":
    main()
