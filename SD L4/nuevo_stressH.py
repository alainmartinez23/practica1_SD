import pika
import json
import time
import uuid
import threading
import random

NUM_REQUESTS = 100
NUM_CLIENTS = 10
TARGET_QUEUE = "insult_queue"

response_times = []
lock = threading.Lock()

INSULTOS_DE_PRUEBA = ["tonto", "payaso", "imbécil", "subnormal", "retrasado"]
TEXTOS_DE_PRUEBA = [
    "Eres un tonto",
    "Eres un imbécil",
    "Payaso anormal",
    "Vaya subnormal estás hecho",
    "Puto retrasado"
]

def send_request(action, data=None, verbose=False):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()

        result = channel.queue_declare(queue='', exclusive=True)
        callback_queue = result.method.queue
        correlation_id = str(uuid.uuid4())

        request = json.dumps({"action": action, "data": data})
        response = {}

        def on_response(ch, method, props, body):
            if props.correlation_id == correlation_id:
                nonlocal response
                response = json.loads(body)
                ch.stop_consuming()

        channel.basic_consume(queue=callback_queue, on_message_callback=on_response, auto_ack=True)

        start = time.time()
        channel.basic_publish(
            exchange='',
            routing_key=TARGET_QUEUE,
            properties=pika.BasicProperties(
                reply_to=callback_queue,
                correlation_id=correlation_id,
            ),
            body=request
        )

        channel.start_consuming()
        end = time.time()

        with lock:
            response_times.append(end - start)

        if verbose:
            print(f"[{action}] → {response}")

        return response

    except Exception as e:
        print(f"Error en la petición {action}: {e}")
    finally:
        try:
            connection.close()
        except:
            pass

def stress_client(client_id):
    for _ in range(NUM_REQUESTS):
        action = random.choice(["filter_text", "list"])

        if action == "filter_text":
            texto = random.choice(TEXTOS_DE_PRUEBA)
            send_request("filter_text", texto)
        elif action == "list":
            send_request("get_filtered_texts")

threads = []
start_time = time.time()
for i in range(NUM_CLIENTS):
    t = threading.Thread(target=stress_client, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
end_time = time.time()

total_requests = NUM_REQUESTS * NUM_CLIENTS
print(f"\nStress test finalizado")
print(f"Total peticiones: {total_requests}")
print(f"Tiempo total: {end_time - start_time:.2f} segundos")
